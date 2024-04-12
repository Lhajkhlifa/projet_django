# Generated by Django 4.2.7 on 2024-04-12 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('insertion', '0002_alter_data_nom'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('email_address', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Controle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rapport', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Emplacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut_emplacement', models.CharField(choices=[('libre', 'libre'), ('occupé', 'occupé')], default='libre', max_length=50)),
                ('type_emplacement', models.CharField(choices=[('regulier', 'regulier'), ('delestage', 'delestage'), ('tube_individuel', 'tube_individuel'), ('debordement', 'debordement')], default='regulier', max_length=50)),
                ('utilisable', models.BooleanField(default=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('allee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.allee')),
            ],
        ),
        migrations.CreateModel(
            name='EntreeSortieIndividuel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('informations_supplementaires', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EntrepriseTransport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, unique=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueVehicule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('ancient_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ancient_client', to='insertion.client')),
                ('nouveau_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nouveau_client', to='insertion.client')),
                ('service_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_client', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IndexLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_lot', models.CharField(choices=[('entree', 'entree'), ('sortie', 'sortie'), ('entree_individuel', 'entree_individuel'), ('sortie_individuel', 'sortie_individuel')], max_length=255)),
                ('cloture_date', models.DateTimeField(blank=True, null=True)),
                ('sortie_date', models.DateTimeField(blank=True, null=True)),
                ('num_lot_outils_transport', models.CharField(blank=True, max_length=255, null=True)),
                ('date_prevision', models.DateTimeField(blank=True, null=True)),
                ('controles_effectues', models.IntegerField(default=0)),
                ('statut_lot', models.CharField(blank=True, choices=[('init_entree', 'init_entree'), ('init_sortie', 'init_sortie')], max_length=255, null=True)),
                ('categorie_lot', models.CharField(choices=[('uni', 'uni'), ('non_uni', 'non_uni')], default='uni', max_length=255)),
                ('type_enlevement', models.CharField(choices=[('direct', 'direct'), ('outil_transport', 'outil_transport')], default='direct', max_length=255)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('controleur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='controleurs', to=settings.AUTH_USER_MODEL)),
                ('createur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createurs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LotUserEntreeSortie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('agent_poste_de_garde', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_poste_de_garde', to=settings.AUTH_USER_MODEL)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.lot')),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_date', models.DateField(blank=True, null=True)),
                ('date_fin_maintenance', models.DateField(blank=True, null=True)),
                ('statut_maintenance', models.CharField(choices=[('maintenance_en_attente', 'maintenance_en_attente'), ('maintenance_encours', 'maintenance_encours'), ('maintenance_annulée', 'maintenance_annulée'), ('maintenance_fini', 'maintenance_fini')], default='maintenance_en_attente', max_length=55)),
                ('type_maintenance', models.CharField(choices=[('par_frequence', 'par_frequence'), ('ponctuelle', 'ponctuelle'), ('initiale', 'initiale')], default='par_frequence', max_length=55)),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceDateProchaine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prochaine_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceLot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequence', models.IntegerField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='insertion.client')),
                ('createur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_maintenance', models.CharField(max_length=255, unique=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Marque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mouvement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_mouvement', models.CharField(choices=[('interne', 'interne'), ('entree', 'entree'), ('sortie', 'sortie'), ('debordement', 'debordement')], max_length=55)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('lot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='insertion.lot')),
            ],
        ),
        migrations.CreateModel(
            name='Origine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actif', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.client')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.profile')),
            ],
        ),
        migrations.CreateModel(
            name='ResultatControle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultat', models.CharField(max_length=255)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('controle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.controle')),
            ],
        ),
        migrations.CreateModel(
            name='StaticData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('static_file', models.FileField(default='vide', upload_to='files_excel/')),
            ],
        ),
        migrations.CreateModel(
            name='Stationnement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_entree_emplacement', models.DateTimeField(blank=True, null=True)),
                ('date_sortie_emplacement', models.DateTimeField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('emplacement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.emplacement')),
                ('mouvement_entree', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mouvement_entree', to='insertion.mouvement')),
                ('mouvement_sortie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mouvement_sortie', to='insertion.mouvement')),
            ],
        ),
        migrations.CreateModel(
            name='StatutControle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatutMouvement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatutTube',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('immatriculation', models.CharField(max_length=255, unique=True)),
                ('existe', models.BooleanField(default=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.client')),
                ('entreprise_transport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.entreprisetransport')),
                ('origine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='insertion.origine')),
            ],
        ),
        migrations.CreateModel(
            name='TransportLot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.lot')),
                ('transport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.transport')),
            ],
        ),
        migrations.CreateModel(
            name='Tube',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, unique=True)),
                ('type_tube', models.CharField(choices=[('commun', 'commun'), ('individuel', 'individuel')], default='commun', max_length=55)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('statut_controle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.statutcontrole')),
                ('statut_tube', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.statuttube')),
                ('transport', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='insertion.transport')),
            ],
        ),
        migrations.CreateModel(
            name='TypeControle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, unique=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeLotMaintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('maintenance_lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.maintenancelot')),
                ('maintenance_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.maintenancetype')),
            ],
        ),
        migrations.CreateModel(
            name='TypeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_profile', models.CharField(max_length=255, unique=True)),
                ('actif', models.BooleanField(default=True)),
                ('modifiable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('immatriculation', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('model', models.CharField(blank=True, max_length=255, null=True)),
                ('couleur', models.CharField(blank=True, max_length=255, null=True)),
                ('kilometrage', models.IntegerField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('complet', models.BooleanField(default=False)),
                ('existe', models.BooleanField(default=True)),
                ('disponible', models.BooleanField(default=False)),
                ('qr_code', models.ImageField(blank=True, upload_to='qr_codes')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.client')),
                ('marque', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='insertion.marque')),
            ],
        ),
        migrations.CreateModel(
            name='VehiculeLot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.lot')),
                ('vehicule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.vehicule')),
            ],
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('index_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='insertion.indexlink')),
            ],
        ),
        migrations.CreateModel(
            name='ViewTypeProfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('type_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.typeprofile')),
                ('view', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.view')),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, unique=True)),
                ('type_zone', models.CharField(choices=[('stockage', 'stockage'), ('debordement', 'debordement'), ('delestage', 'delestage')], default='stockage', max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='ZoneClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.client')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.zone')),
            ],
        ),
        migrations.DeleteModel(
            name='Data',
        ),
        migrations.AddField(
            model_name='zone',
            name='zone_client',
            field=models.ManyToManyField(through='insertion.ZoneClient', to='insertion.client'),
        ),
        migrations.AddField(
            model_name='view',
            name='view_type_profil',
            field=models.ManyToManyField(through='insertion.ViewTypeProfil', to='insertion.typeprofile'),
        ),
        migrations.AddField(
            model_name='vehicule',
            name='vehicule_lot',
            field=models.ManyToManyField(through='insertion.VehiculeLot', to='insertion.lot'),
        ),
        migrations.AddField(
            model_name='transport',
            name='transport_lot',
            field=models.ManyToManyField(through='insertion.TransportLot', to='insertion.lot'),
        ),
        migrations.AddField(
            model_name='stationnement',
            name='vehicule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.vehicule'),
        ),
        migrations.AddField(
            model_name='resultatcontrole',
            name='type_controle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='insertion.typecontrole'),
        ),
        migrations.AddField(
            model_name='profile',
            name='type_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.typeprofile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mouvement',
            name='statut_mouvement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.statutmouvement'),
        ),
        migrations.AddField(
            model_name='mouvement',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mouvement',
            name='vehicule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.vehicule'),
        ),
        migrations.AddField(
            model_name='maintenancetype',
            name='type_lot_maintenance',
            field=models.ManyToManyField(through='insertion.TypeLotMaintenance', to='insertion.maintenancelot'),
        ),
        migrations.AddField(
            model_name='maintenancedateprochaine',
            name='maintenance_lot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.maintenancelot'),
        ),
        migrations.AddField(
            model_name='maintenancedateprochaine',
            name='vehicule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.vehicule'),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='maintenance_lot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='insertion.maintenancelot'),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='vehicule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.vehicule'),
        ),
        migrations.AddField(
            model_name='lot',
            name='tube',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='insertion.tube'),
        ),
        migrations.AddField(
            model_name='historiquevehicule',
            name='vehicule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.vehicule'),
        ),
        migrations.AddField(
            model_name='entreesortieindividuel',
            name='lot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.lot'),
        ),
        migrations.AddField(
            model_name='emplacement',
            name='stationnement_vehicule',
            field=models.ManyToManyField(through='insertion.Stationnement', to='insertion.vehicule'),
        ),
        migrations.AddField(
            model_name='controle',
            name='lot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.lot'),
        ),
        migrations.AddField(
            model_name='controle',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='controle',
            name='vehicule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.vehicule'),
        ),
        migrations.AddField(
            model_name='allee',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insertion.zone'),
        ),
    ]