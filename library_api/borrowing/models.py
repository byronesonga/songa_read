from django.db import models
from django.conf import settings
from books.models import Book
from django.utils import timezone

class BorrowRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrows")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_records")
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateTimeField(blank=True, null=True)
    # optional fine value
    fine_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    class Meta:
        ordering = ("-borrowed_at",)

    def is_overdue(self):
        if self.returned_at:
            return False
        return self.due_date < timezone.localdate()

    def mark_returned(self, return_time=None):
        from django.utils import timezone
        if not return_time:
            return_time = timezone.now()
        self.returned_at = return_time
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

