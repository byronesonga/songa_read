from rest_framework import serializers
from .models import BorrowRecord
from books.models import Book
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

class BorrowRecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BorrowRecord
        fields = ("id", "user", "book", "borrowed_at", "due_date", "returned_at", "fine_amount")
        read_only_fields = ("borrowed_at", "returned_at", "fine_amount")

    def validate(self, attrs):
        book = attrs.get("book")
        if not book:
            raise serializers.ValidationError("Book is required.")
        if book.available_copies < 1:
            raise serializers.ValidationError("No available copies for this book.")
        return attrs

    def create(self, validated_data):
        # create borrow record & decrease available_copies atomically
        book = validated_data["book"]
        # default due_date to 14 days if not provided
        if not validated_data.get("due_date"):
            validated_data["due_date"] = timezone.localdate() + timedelta(days=14)

        from django.db import transaction
        with transaction.atomic():
            # lock the book row to prevent race conditions (depending on DB)
            book = Book.objects.select_for_update().get(pk=book.pk)
            if book.available_copies < 1:
                raise serializers.ValidationError("No available copies left.")
            book.available_copies -= 1
            book.save()
            borrow = BorrowRecord.objects.create(**validated_data)
        return borrow
