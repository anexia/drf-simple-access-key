from rest_framework import viewsets

from drf_simple_access_key import SimpleAccessKey
from drf_simple_access_key.authentication import SimpleAccessKeyAuthentication

from .models import Book, PrivateBook
from .serializers import BookSerializer, PrivateBookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class PrivateBookViewSet(viewsets.ModelViewSet):
    queryset = PrivateBook.objects.all()
    serializer_class = PrivateBookSerializer
    authentication_classes = [SimpleAccessKeyAuthentication]
    permission_classes = [SimpleAccessKey]
