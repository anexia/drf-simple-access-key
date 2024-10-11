from django.db import models


class Book(models.Model):
    title = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )


class PrivateBook(models.Model):
    title = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )
