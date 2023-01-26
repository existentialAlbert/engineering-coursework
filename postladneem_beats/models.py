import operator

from django.contrib.auth.models import User
from django.db import models

# class User(AbstractUser):
#     LISTENER = 1
#     UPLOADER = 2
#     AUTHOR = 3
#
#     ROLE_CHOICES = (
#         (LISTENER, 'Listener'),
#         (UPLOADER, 'Uploader'),
#         (AUTHOR, 'Author'),
#     )
#     role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)


class Key(models.Model):
    tonica = models.TextField()
    is_minor = models.BooleanField()

    def __str__(self):
        return f"{self.tonica}{'m' if self.is_minor else ''}"


class Genre(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class Beat(models.Model):
    name = models.TextField(max_length=100, unique=True)
    key = models.ForeignKey(Key, on_delete=models.CASCADE)
    bpm = models.PositiveSmallIntegerField()

    description = models.TextField(max_length=500)

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    authors = models.ManyToManyField(User, related_name="authors")
    file = models.FileField(upload_to="")

    def __str__(self):
        return f"{', '.join(map(operator.attrgetter('username'), self.authors.all()))} - {self.name}"
