# Generated by Django 4.0.3 on 2024-07-09 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarysystem', '0004_student_delete_studentextra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='condition',
            field=models.CharField(choices=[('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')], default='good', max_length=30),
        ),
    ]