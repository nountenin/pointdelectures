# Generated by Django 4.0.3 on 2022-04-12 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_events', models.CharField(max_length=30)),
                ('descriptions', models.CharField(max_length=500)),
                ('image_events', models.ImageField(blank=True, null=True, upload_to='events/images')),
                ('type', models.CharField(choices=[('events', 'Events'), ('ecocitoyenne', 'Ecocitoyenne')], max_length=15)),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
    ]