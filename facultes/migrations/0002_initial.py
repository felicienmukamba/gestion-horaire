# Generated by Django 4.2.13 on 2024-06-15 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("facultes", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="facultaire",
            name="enseignant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.enseignant"
            ),
        ),
        migrations.AddField(
            model_name="facultaire",
            name="faculte",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="facultes.faculte"
            ),
        ),
        migrations.AddField(
            model_name="departement",
            name="faculte",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="facultes.faculte"
            ),
        ),
    ]
