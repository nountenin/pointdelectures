# Generated by Django 4.0.3 on 2022-04-15 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0005_alter_reader_readpoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reader',
            name='type_Reader',
            field=models.CharField(blank=True, choices=[('1', 'User'), ('2', 'Reader')], max_length=1, null=True),
        ),
    ]