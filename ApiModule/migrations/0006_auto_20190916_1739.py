# Generated by Django 2.2.5 on 2019-09-16 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiModule', '0005_auto_20190916_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='emp_id',
            field=models.UUIDField(default='56ebb7f1e3f54197b5f9d24b14795b5d', unique=True),
        ),
    ]
