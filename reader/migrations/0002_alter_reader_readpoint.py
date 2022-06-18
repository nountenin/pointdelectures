# Generated by Django 4.0.3 on 2022-04-10 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
        ('reader', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reader',
            name='readpoint',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='book.readpoint'),
            preserve_default=False,
        ),
    ]