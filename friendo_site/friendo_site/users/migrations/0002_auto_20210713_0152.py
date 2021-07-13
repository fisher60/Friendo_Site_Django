# Generated by Django 3.2.5 on 2021-07-13 01:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WatchList",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("owners", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name="currency",
            name="amount",
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name="WatchListTitle",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=40)),
                (
                    "watch_list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.watchlist",
                    ),
                ),
            ],
        ),
    ]