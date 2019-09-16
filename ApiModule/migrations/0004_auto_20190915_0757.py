# Generated by Django 2.2.5 on 2019-09-15 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiModule', '0003_auto_20190915_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='last_modified',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='emp_id',
            field=models.UUIDField(default='615245ffc9564253b0205dff6487dc5a', unique=True),
        ),
    ]