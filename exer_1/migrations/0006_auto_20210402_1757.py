# Generated by Django 3.1.7 on 2021-04-02 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exer_1', '0005_auto_20210402_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperature',
            name='temp',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]