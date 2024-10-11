from rest_framework import serializers

from .models import Book, PrivateBook


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "pk",
            "title",
        ]


class PrivateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateBook
        fields = [
            "pk",
            "title",
        ]
