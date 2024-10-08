# Generated by Django 4.2.16 on 2024-09-05 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app2", "0002_capturedphoto_latitude_capturedphoto_longitude_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SaveImage",
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
                ("name", models.CharField(max_length=50)),
                ("image", models.ImageField(upload_to="images/")),
            ],
        ),
        migrations.AlterField(
            model_name="capturedphoto",
            name="photo",
            field=models.ImageField(upload_to="images/"),
        ),
    ]
