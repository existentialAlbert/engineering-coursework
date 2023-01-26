# Generated by Django 4.1.5 on 2023-01-24 18:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Key",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tonica", models.TextField()),
                ("is_minor", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Mood",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Beat",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.TextField(max_length=100)),
                ("bpm", models.PositiveSmallIntegerField()),
                ("description", models.TextField(max_length=500)),
                ("duration", models.TimeField()),
                ("path", models.FileField(upload_to="data/")),
                ("streams", models.PositiveIntegerField(default=0)),
                ("authors", models.ManyToManyField(related_name="authors", to=settings.AUTH_USER_MODEL)),
                ("genre", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="postladneem_beats.genre")),
                ("key", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="postladneem_beats.key")),
                ("moods", models.ManyToManyField(to="postladneem_beats.mood")),
                (
                    "uploader",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="uploader",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
