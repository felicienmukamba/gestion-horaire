# Generated by Django 4.2.13 on 2024-06-15 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("anneeAcademiques", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attribuer",
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
                ("nbreHeure", models.IntegerField()),
            ],
            options={
                "ordering": ("-id",),
            },
        ),
        migrations.CreateModel(
            name="Cours",
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
            ],
            options={
                "ordering": ("designation",),
            },
        ),
        migrations.CreateModel(
            name="Dispenser",
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
                (
                    "vaccation",
                    models.CharField(
                        choices=[("Jour", "Jour"), ("Soir", "Soir")], max_length=50
                    ),
                ),
                ("prester", models.BooleanField(default=False)),
                ("date", models.DateField()),
                (
                    "anneeAcademique",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="anneeAcademiques.anneeacademique",
                    ),
                ),
                (
                    "cours",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cours.cours"
                    ),
                ),
            ],
            options={
                "ordering": ("-date",),
            },
        ),
    ]
