# Generated by Django 4.0.5 on 2022-06-14 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0011_alter_frequentation_semaine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frequentation',
            name='mois',
            field=models.IntegerField(default=6),
        ),
        migrations.AlterField(
            model_name='frequentation',
            name='semaine',
            field=models.IntegerField(default=24),
        ),
    ]
