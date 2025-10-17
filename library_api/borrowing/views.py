from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BorrowRecord
from .serializers import BorrowRecordSerializer
from rest_framework.permissions import IsAuthenticated
from books.models import Book
from django.utils import timezone
from django.db import transaction

class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.select_related("user", "book").all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # members see only their own; librarians/admins see all
        if user.is_librarian() or user.is_admin():
            return super().get_queryset()
        return super().get_queryset().filter(user=user)

    @action(methods=["POST"], detail=True, url_path="return", url_name="return")
    def return_book(self, request, pk=None):
        record = self.get_object()
        if record.returned_at:
            return Response({"detail": "Already returned."}, status=status.HTTP_400_BAD_REQUEST)

        # compute fine (simple example: 1 currency unit per overdue day)
        from datetime import datetime, date
        now = timezone.now()
        overdue_days = (now.date() - record.due_date).days
        fine = 0
        if overdue_days > 0:
            fine = overdue_days * 1  # adjust fine calculation as needed

        with transaction.atomic():
            # mark returned
            record.returned_at = now
            record.fine_amount = fine
            record.save()
            # increase book copies
            book = Book.objects.select_for_update().get(pk=record.book.pk)
            book.available_copies = models.F('available_copies') + 1
            book.save()
            # refresh book from db to have updated integer
            book.refresh_from_db()

        serializer = self.get_serializer(record)
        return Response(serializer.data)

