# Generated by Django 5.0.1 on 2024-01-11 16:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admissions", "0002_user_is_admin"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="majorapplication",
            name="student_data",
        ),
        migrations.RemoveField(
            model_name="student",
            name="enrolled_major",
        ),
        migrations.RemoveField(
            model_name="studentdata",
            name="student",
        ),
        migrations.AddField(
            model_name="user",
            name="enrolled_major",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="admissions.major",
            ),
        ),
        migrations.CreateModel(
            name="Application",
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
                ("birthdate", models.DateField()),
                ("birthplace", models.CharField(max_length=50)),
                ("previous_school", models.CharField(max_length=50)),
                ("previous_school_diploma", models.FileField(upload_to="")),
                ("gpa", models.FloatField()),
                ("final_exams_grade", models.FloatField()),
                (
                    "major",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="admissions.major",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Approval",
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
                ("explanation", models.CharField(max_length=2000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "admin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="admin",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="AppliedMajor",
        ),
        migrations.DeleteModel(
            name="MajorApplication",
        ),
        migrations.DeleteModel(
            name="Student",
        ),
        migrations.DeleteModel(
            name="StudentData",
        ),
    ]