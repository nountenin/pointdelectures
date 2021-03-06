# Generated by Django 4.0.3 on 2022-04-15 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0003_alter_book_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achat',
            fields=[
                ('book_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.book')),
                ('fournisseur', models.CharField(max_length=50)),
                ('prix_achat', models.IntegerField()),
            ],
            bases=('book.book',),
        ),
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solde_compte', models.IntegerField()),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Depense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle_depense', models.CharField(choices=[('Achat de fourniture', 'Achat de fourniture'), ('Achat de meuble', 'Achat de meuble'), ('Entretien du bureau', 'Entretien du bureau'), ('Reparation', 'Reparation'), ('Autres', 'Autres')], max_length=100)),
                ('description_depense', models.CharField(blank=True, max_length=255, null=True)),
                ('prix_ht_depense', models.IntegerField()),
                ('quantite_depense', models.IntegerField(default=0)),
                ('total_depense', models.IntegerField(default=0)),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Personel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_personnel', models.CharField(max_length=20)),
                ('prenom_personnel', models.CharField(max_length=20)),
                ('salaire_personnel', models.IntegerField(default=50000)),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
                ('fonction_personnel', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Ventes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description_vente', models.CharField(blank=True, max_length=255)),
                ('prix_vente', models.IntegerField()),
                ('total_vente', models.IntegerField(default=0)),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
                ('article_vente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='book.book')),
            ],
        ),
        migrations.CreateModel(
            name='Payer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solde_paiement', models.IntegerField()),
                ('etat_payer', models.BooleanField(default=False)),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounting.personel')),
            ],
        ),
    ]
