# Generated by Django 2.2.5 on 2019-09-16 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiModule', '0004_auto_20190915_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='emp_id',
            field=models.UUIDField(default='63f67bc461e54610b3da1a0e865edbed', unique=True),
        ),
    ]
