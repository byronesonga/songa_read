from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Book
from .serializers import BookSerializer
from users.models import CustomUser

class IsLibrarianOrAdmin:
    # we'll use custom permission class later; for brevity check in viewset actions
    pass

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "author", "isbn", "category"]
    ordering_fields = ["title", "author", "published_date"]

