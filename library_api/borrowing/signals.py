from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BorrowRecord
from books.models import Book
from django.db import transaction

@receiver(post_save, sender=BorrowRecord)
def adjust_copies_on_borrow_or_return(sender, instance, created, **kwargs):
    # if created -> copies already decreased in serializer.create
    # but if someone marks returned via admin or direct change, we ensure available_copies increments
    if instance.returned_at:
        # increment available copies
        with transaction.atomic():
            b = Book.objects.select_for_update().get(pk=instance.book.pk)
            b.available_copies = b.available_copies + 1
            b.save()
