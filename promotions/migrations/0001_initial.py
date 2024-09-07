# Generated by Django 4.2.13 on 2024-06-15 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Promotion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("restored_at", models.DateTimeField(blank=True, null=True)),
                ("designation", models.CharField(max_length=50)),
                ("actif", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ("designation",),
            },
        ),
    ]
