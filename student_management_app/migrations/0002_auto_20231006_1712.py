# Generated by Django 3.0.6 on 2023-10-06 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='customuser',
            table='tbl_user',
        ),
        migrations.AlterModelTable(
            name='sessionyearmodel',
            table='tbl_session_year',
        ),
    ]
