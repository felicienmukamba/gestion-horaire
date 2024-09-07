# Generated by Django 4.2.13 on 2024-06-15 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("facultes", "0001_initial"),
        ("anneeAcademiques", "0001_initial"),
        ("promotions", "0001_initial"),
        ("cours", "0001_initial"),
        ("salles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dispenser",
            name="departement",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="facultes.departement"
            ),
        ),
        migrations.AddField(
            model_name="dispenser",
            name="promotion",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="promotions.promotion"
            ),
        ),
        migrations.AddField(
            model_name="dispenser",
            name="salle",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="salles.salle"
            ),
        ),
        migrations.AddField(
            model_name="attribuer",
            name="anneeAcademique",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="anneeAcademiques.anneeacademique",
            ),
        ),
        migrations.AddField(
            model_name="attribuer",
            name="cours",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="cours.cours"
            ),
        ),
        migrations.AddField(
            model_name="attribuer",
            name="departement",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="facultes.departement"
            ),
        ),
    ]
