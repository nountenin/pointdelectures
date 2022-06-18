# Generated by Django 4.0.3 on 2022-04-10 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name_author', models.CharField(max_length=50)),
                ('last_name_author', models.CharField(max_length=50)),
                ('biography_author', models.CharField(blank=True, max_length=255, null=True)),
                ('nationality_author', models.CharField(blank=True, max_length=50, null=True)),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn_book', models.CharField(max_length=30)),
                ('title_book', models.CharField(max_length=30)),
                ('number_copy_book', models.IntegerField()),
                ('publication_date_book', models.DateField()),
                ('file_book', models.FileField(blank=True, null=True, upload_to='book_electroniques')),
                ('img1_book', models.ImageField(upload_to='couverture')),
                ('img2_book', models.ImageField(upload_to='couverture')),
                ('resume_book', models.TextField(blank=True, null=True)),
                ('edition_house', models.CharField(max_length=30)),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.author')),
            ],
        ),
        migrations.CreateModel(
            name='ReadPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_readpoint', models.CharField(max_length=50)),
                ('commune_readpoint', models.CharField(max_length=50)),
                ('quartier_readpoint', models.CharField(max_length=50)),
                ('address_readpoint', models.CharField(max_length=50)),
                ('contact1_readpoint', models.CharField(max_length=50)),
                ('contact2_readpoint', models.CharField(max_length=50)),
                ('email_readpoint', models.EmailField(max_length=50)),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Rayon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_rayon', models.CharField(max_length=50)),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
                ('readpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.readpoint')),
            ],
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motif', models.TextField()),
                ('type', models.SmallIntegerField(choices=[('', 'Sélectionnez un type de mouvement'), (1, 'Stock Initial'), (2, 'Approvisionnement'), (3, 'Emprunt'), (4, 'Retour'), (5, 'Transfert')])),
                ('quantite', models.IntegerField()),
                ('date_movement', models.DateField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_category', models.CharField(max_length=30)),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
                ('rayon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.rayon')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.category'),
        ),
    ]
