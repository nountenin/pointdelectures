# Generated by Django 4.0.3 on 2022-04-11 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_complet', models.CharField(max_length=20)),
                ('mail_contact', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]