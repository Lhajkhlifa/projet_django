#from django.db import models
#class Data(models.Model):
 #   id = models.IntegerField(primary_key=True)
  #  nom = models.CharField(max_length=20)
from django.contrib.auth.models import User
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


# class StatutEmplacement(models.Model):
#     """Statut-Emplacements """
#     statut = models.CharField(max_length=255, unique=True)
#
#     def __str__(self):
#         return self.statut


class StatutTube(models.Model):
    """Statut-Tube """
    statut = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.statut


class StatutMouvement(models.Model):
    """Statut-Mouvement """
    statut = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.statut


class StatutControle(models.Model):
    """Table Statut Controle """
    statut = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.statut


class Client(models.Model):
    """Table Clients """
    nom = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=128)
    email_address = models.EmailField(max_length=254)

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        """Créer user utilisant client"""
        if Client:
            if self.user is None:
                user = User()
                user.username = self.nom
                user.set_password(self.password)
                user.email = self.email_address
                user.save()
                profile = Profile()
                profile.user = user
                profile.type_profile = TypeProfile.objects.get(type_profile='CLIENT')
                profile.save()
                self.user = user
            else:
                self.user.username = self.nom
                self.user.set_password(self.password)
                self.user.email = self.email_address
                self.user.save()
        super().save(*args, **kwargs)


class EntrepriseTransport(models.Model):
    """Table Entreprises-Transport """
    nom = models.CharField(max_length=255, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class Tube(models.Model):
    """Table Tube """
    nom = models.CharField(max_length=255, unique=True)
    statut_tube = models.ForeignKey(StatutTube, on_delete=models.CASCADE)
    statut_controle = models.ForeignKey(StatutControle, on_delete=models.CASCADE)
    type_tube = models.CharField(max_length=55, choices=[("commun", "commun"), ("individuel", "individuel")],
                                 default="commun")
    transport = models.ForeignKey('Transport', on_delete=models.CASCADE, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom}"


class Lot(models.Model):
    """Table Lot"""
    type_lot = models.CharField(max_length=255, choices=[("entree", "entree"), ("sortie", "sortie"),
                                                         ("entree_individuel", "entree_individuel"),
                                                         ("sortie_individuel", "sortie_individuel")])
    # Controle du Lot est fini
    cloture_date = models.DateTimeField(null=True, blank=True)

    sortie_date = models.DateTimeField(null=True, blank=True)
    num_lot_outils_transport = models.CharField(max_length=255, null=True, blank=True)
    date_prevision = models.DateTimeField(null=True, blank=True)
    controles_effectues = models.IntegerField(default=0)
    statut_lot = models.CharField(max_length=255, choices=[("init_entree", "init_entree"),
                                                           ("init_sortie", "init_sortie")], null=True, blank=True)
    categorie_lot = models.CharField(max_length=255, choices=[("uni", "uni"),
                                                              ("non_uni", "non_uni")], default="uni")
    type_enlevement = models.CharField(max_length=255, choices=[("direct", "direct"),
                                                                ("outil_transport", "outil_transport")], default="direct")
    tube = models.ForeignKey(Tube, on_delete=models.CASCADE, null=True, blank=True)
    controleur = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='controleurs')
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='createurs')
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"

    def vehicule_exist_in_lot(self, vehicule_id):
        """Retourner le vehicule s'il appartient au lot"""
        try:
            vehicule_lot = VehiculeLot.objects.get(lot=self, vehicule__id=vehicule_id)
            return vehicule_lot.vehicule
        except ObjectDoesNotExist:
            return False

    def nombre_vehicule_par_lot(self):
        """Nombre de vehicules par lot"""
        return VehiculeLot.objects.filter(lot=self.id).count()

    def get_creation_date(self):
        """ creation_date en format %d/%m/%Y %H:%M """
        return self.creation_date.strftime('%d/%m/%Y %H:%M')

    def get_vehicules(self):
        """Les vehicules du lot"""
        current_lot_vehicules = []
        vehicules_lot = VehiculeLot.objects.filter(lot__id=self.id)
        for vehicule_lot in vehicules_lot:
            current_lot_vehicules.append(vehicule_lot.vehicule)
        return current_lot_vehicules

    def get_lot_transport(self):
        """Le transport du lot"""
        transport_lot = TransportLot.objects.filter(lot=self).first()
        return transport_lot.transport


class LotUserEntreeSortie(models.Model):
    """Table LotUserEntreeSortie"""
    agent_poste_de_garde = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_poste_de_garde')
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)


class Origine(models.Model):
    """Table de Origine de Transport"""
    nom = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.nom}"


class Transport(models.Model):
    """Table Transport"""
    immatriculation = models.CharField(max_length=255, unique=True)
    origine = models.ForeignKey(Origine, on_delete=models.CASCADE, null=True, blank=True)
    entreprise_transport = models.ForeignKey(EntrepriseTransport, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    transport_lot = models.ManyToManyField(Lot, through='TransportLot')
    existe = models.BooleanField(default=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def stationné_dans_tube(self):
        """Verifier si le transport est stationné dans un tube"""
        current_tube = Tube.objects.filter(transport=self).first()
        if current_tube:
            return current_tube
        else:
            return None

    def encours_chargement_dechargement(self):
        """Verifier si le transport est occupé"""
        try:
            transport_occupé_statuts = StatutTube.objects.filter(statut__in=["chargement_en_cours", "chargement_en_attente",
                                                                             "chargement_fin",
                                                                             "dechargement_en_cours",
                                                                             "dechargement_en_attente"])
            TransportLot.objects.get(transport=self, lot__tube__statut_tube__in=transport_occupé_statuts)
            return True
        except ObjectDoesNotExist:
            return False

    def __str__(self):
        return f"{self.immatriculation}/{self.entreprise_transport}"


class TransportLot(models.Model):
    """"Table TransportLot"""
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)


class Zone(models.Model):
    """Table Zone"""
    nom = models.CharField(max_length=255, unique=True)
    zone_client = models.ManyToManyField(Client, through='ZoneClient')
    type_zone = models.CharField(max_length=55, choices=[("stockage", "stockage"), ("debordement", "debordement"), ("delestage", "delestage")], default="stockage")

    def __str__(self):
        return self.nom


class ZoneClient(models.Model):
    """"Table ZoneClient"""
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    priority = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)


class Allee(models.Model):
    """Table Allee"""
    nom = models.CharField(max_length=255, unique=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.zone}/{self.nom}"


class Marque(models.Model):
    """Table de Marque de Véhicule"""
    nom = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.nom}"


class Vehicule(models.Model):
    """Table Vehicule"""
    vin = models.CharField(max_length=255, unique=True, null=True, blank=True)
    immatriculation = models.CharField(max_length=255, unique=True, null=True, blank=True)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    couleur = models.CharField(max_length=255, null=True, blank=True)
    kilometrage = models.IntegerField(null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    vehicule_lot = models.ManyToManyField(Lot, through='VehiculeLot')
    complet = models.BooleanField(default=False)
    existe = models.BooleanField(default=True)
    disponible = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return str(self.id)

    def all_entrees_dates(self):
        """Toutes les entrees du vehicules"""
        vehicule_lots = [vehicule_lot.lot.get_creation_date for vehicule_lot in VehiculeLot.objects.filter(vehicule=self, lot__type_lot="entree")]

    def en_mouvement(self):
        """Verifier si le Véhicule est en mouvement"""
        try:
            statuts = StatutMouvement.objects.filter(statut__in=["mouvement en attente", "mouvement en cours"])
            Mouvement.objects.get(vehicule=self, statut_mouvement__in=statuts)
            return True
        except ObjectDoesNotExist:
            return False

    def is_disponible(self):
        """Verifier si le Véhicule existe dans un lot en cours"""
        vehicule_lots = VehiculeLot.objects.filter(vehicule=self)
        not_dispo_tube_statuts = StatutTube.objects.filter(statut__in=["chargement_en_cours", "chargement_en_attente",
                                                                       "dechargement_en_cours", "dechargement_en_attente"])

        list_lots = [vl.lot for vl in vehicule_lots if vl.lot.tube.statut_tube in not_dispo_tube_statuts]
        list_lots += [vl.lot for vl in vehicule_lots if vl.lot.type_lot == "sortie" and vl.lot.sortie_date is None]
        return not bool(list_lots)

    def dernier_stationnement(self):
        """Afficher dernier emplacement du vehicule pour le bon du transport en
        poste de garde sortie"""
        current_stationnement = Stationnement.objects.filter(vehicule=self).order_by('-creation_date').first()
        return current_stationnement.emplacement

    def prochain_stationnement(self):
        """Afficher emplacement prochain du vehicule(le prochain stationnement est créé dans la page du bureau park)"""
        stationnement = Stationnement.objects.filter(vehicule=self, date_entree_emplacement=None,
                                                     date_sortie_emplacement=None).order_by("-creation_date").first()
        return stationnement.emplacement

    def precedent_stationnement(self):
        """Afficher emplacement precedent du vehicule(pour la page du details_mouvement)"""
        stationnement = Stationnement.objects.filter(vehicule=self).exclude(date_entree_emplacement=None,
                                                                            date_sortie_emplacement=None).order_by("-creation_date").first()
        return stationnement.emplacement

    def current_stationnement(self):
        """Afficher l'emplacement actuel du vehicule"""
        current_stationnement = Stationnement.objects.filter(vehicule=self, date_sortie_emplacement=None).\
            exclude(date_entree_emplacement=None).order_by("-creation_date").first()
        if current_stationnement is None:
            current_stationnement = "__"
        return current_stationnement.emplacement

    def save(self, *args, **kwargs):
        """Créer un code QR en utilisant le VIN"""
        if self.vin:
            # liste_infos = (self.vin, self.immatriculation, self.marque, self.model, self.couleur)
            string_to_qr = f"{self.vin}"
            # qrcode_img = qrcode.make(string_to_qr)
            qr = qrcode.QRCode(
                version=3,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(string_to_qr)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            canvas = Image.new('RGB', (380, 380), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(img)
            fname = f'qr_code_{self.vin}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
        super().save(*args, **kwargs)


class HistoriqueVehicule(models.Model):
    """HistoriqueVehicule Table"""
    service_client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_client')
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    ancient_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='ancient_client')
    nouveau_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='nouveau_client')
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)


class VehiculeLot(models.Model):
    """ManyToMany Table VehiculeLot"""
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)


class EntreeSortieIndividuel(models.Model):
    """Table Entree Sortie Vehicule Individuel"""
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    informations_supplementaires = models.CharField(max_length=255, null=True, blank=True)


class Mouvement(models.Model):
    """Table Mouvement"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    statut_mouvement = models.ForeignKey(StatutMouvement, on_delete=models.CASCADE)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, null=True, blank=True)
    type_mouvement = models.CharField(max_length=55, choices=[("interne", "interne"), ("entree", "entree"),
                                                              ("sortie", "sortie"), ("debordement", "debordement")])
    # priority = models.IntegerField(default=1)
    # display = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}/{self.statut_mouvement}"

    def get_creation_date(self):
        """ creation_date en format %d/%m/%Y %H:%M """
        return self.creation_date.strftime('%d/%m/%Y %H:%M')

    def vehicule_exist_in_lot(self):
        """Savoir si vehicule exist dans lot pour identifier les mouvements de débordement"""
        try:
            vehicule_lot = VehiculeLot.objects.get(vehicule=self.vehicule, lot=self.lot)
            return True
        except ObjectDoesNotExist:
            return False


class Emplacement(models.Model):
    """Table Emplacements"""
    statut_emplacement = models.CharField(max_length=50, choices=[("libre", "libre"), ("occupé", "occupé")],
                                          default="libre")
    type_emplacement = models.CharField(max_length=50, choices=[("regulier", "regulier"), ("delestage", "delestage"),
                                                                ("tube_individuel", "tube_individuel"),
                                                                ("debordement", "debordement")],
                                        default="regulier")
    allee = models.ForeignKey(Allee, on_delete=models.CASCADE)
    utilisable = models.BooleanField(default=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    stationnement_vehicule = models.ManyToManyField(Vehicule, through='Stationnement')

    def __str__(self):
        return f"{self.allee}/{self.id}"


class Stationnement(models.Model):
    """ManyToMany Table Stationnement de Vehicule dans un Emplacement"""
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    emplacement = models.ForeignKey(Emplacement, on_delete=models.CASCADE)
    date_entree_emplacement = models.DateTimeField(null=True, blank=True)
    date_sortie_emplacement = models.DateTimeField(null=True, blank=True)
    mouvement_entree = models.ForeignKey(Mouvement, on_delete=models.CASCADE, related_name='mouvement_entree',
                                         null=True, blank=True)
    mouvement_sortie = models.ForeignKey(Mouvement, on_delete=models.CASCADE, related_name='mouvement_sortie',
                                         null=True, blank=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"in:{self.date_entree_emplacement}/out:{self.date_sortie_emplacement}"

    def get_date_entree_emplacement(self):
        """ date_entree_emplacement en format %d/%m/%Y %H:%M """
        return self.date_entree_emplacement.strftime('%d/%m/%Y %H:%M')

    def get_date_sortie_emplacement(self):
        """ date_sortie_emplacement en format %d/%m/%Y %H:%M """
        return self.date_sortie_emplacement.strftime('%d/%m/%Y %H:%M')

    def get_creation_date(self):
        """ creation_date en format %d/%m/%Y %H:%M """
        return self.creation_date.strftime('%d/%m/%Y %H:%M')


class Controle(models.Model):
    """Table Controle"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    rapport = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}/{self.user}"


class TypeControle(models.Model):
    """Table Types-Contrôle"""
    nom = models.CharField(max_length=255, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class ResultatControle(models.Model):
    """Table ResultatControle"""
    controle = models.ForeignKey(Controle, on_delete=models.CASCADE)
    type_controle = models.ForeignKey(TypeControle, on_delete=models.CASCADE, null=True, blank=True)
    resultat = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}/{self.resultat}"


class MaintenanceLot(models.Model):
    """Cette table est utilisée pour savoir qui a créé un lot de maintenances et pour quel Client"""
    createur = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    frequence = models.IntegerField(null=True, blank=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class MaintenanceType(models.Model):
    """Les types de maintenances"""
    type_maintenance = models.CharField(max_length=255, unique=True)
    type_lot_maintenance = models.ManyToManyField(MaintenanceLot, through='TypeLotMaintenance')

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class TypeLotMaintenance(models.Model):
    """En utilisant cette table, on peut donner un ensemble de types maintenance à un client"""
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.CASCADE)
    maintenance_lot = models.ForeignKey(MaintenanceLot, on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class MaintenanceDateProchaine(models.Model):
    """Les Maintenances réalisées"""
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    prochaine_date = models.DateField()
    maintenance_lot = models.ForeignKey(MaintenanceLot, on_delete=models.CASCADE)

    def get_prochaine_date(self):
        """ prochaine_date en format %d/%m/%Y"""
        return self.prochaine_date.strftime('%d/%m/%Y')

    def __str__(self):
        return f"{self.vehicule}/{self.prochaine_date}"


class Maintenance(models.Model):
    """Les Maintenances réalisées"""
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    maintenance_date = models.DateField(null=True, blank=True)
    date_fin_maintenance = models.DateField(null=True, blank=True)
    statut_maintenance = models.CharField(max_length=55, choices=[("maintenance_en_attente", "maintenance_en_attente"),
                                                                  ("maintenance_encours", "maintenance_encours"),
                                                                  ("maintenance_annulée", "maintenance_annulée"),
                                                                  ("maintenance_fini", "maintenance_fini")],
                                          default="maintenance_en_attente")
    type_maintenance = models.CharField(max_length=55, choices=[("par_frequence", "par_frequence"),
                                                                ("ponctuelle", "ponctuelle"),
                                                                ("initiale", "initiale")], default="par_frequence")
    maintenance_lot = models.ForeignKey(MaintenanceLot, on_delete=models.CASCADE, null=True, blank=True)
    commentaire = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def get_maintenance_date(self):
        """ prochaine_date en format %d/%m/%Y"""
        return self.maintenance_date.strftime('%d/%m/%Y')

    def get_date_fin_maintenance(self):
        """ prochaine_date en format %d/%m/%Y"""
        if self.date_fin_maintenance:
            return self.date_fin_maintenance.strftime('%d/%m/%Y')
        else:
            return self.date_fin_maintenance

    def get_maintenance_types(self):
        """les types du maintenance"""
        maintenance_types = TypeLotMaintenance.objects.filter(maintenance_lot=self.maintenance_lot)
        return maintenance_types

    def __str__(self):
        return f"{self.vehicule.vin}/{self.maintenance_date}"


class TypeProfile(models.Model):
    """Table TypeProfile """
    type_profile = models.CharField(max_length=255, unique=True)
    actif = models.BooleanField(default=True)
    modifiable = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type_profile}"


class Profile(models.Model):
    """Table Profile """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type_profile = models.ForeignKey(TypeProfile, on_delete=models.CASCADE)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type_profile}"

    def user_allowed_links(self):
        """return a list of allowed links"""
        allowed_links = []
        views_types_profil = ViewTypeProfil.objects.filter(type_profile=self.type_profile).exclude(view__index_link=None)
        for vtp in views_types_profil:
            allowed_links.append(vtp.view.index_link.nom)

        return allowed_links


class ProfileClient(models.Model):
    """Table MaintenanceLot"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)


class IndexLink(models.Model):
    """Table des vues définies dans views.py"""
    nom = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class View(models.Model):
    """Table des vues définies dans views.py"""
    nom = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    index_link = models.ForeignKey(IndexLink, on_delete=models.CASCADE, null=True, blank=True)
    view_type_profil = models.ManyToManyField(TypeProfile, through='ViewTypeProfil')

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class ViewTypeProfil(models.Model):
    """Table des vues définies dans views.py"""
    view = models.ForeignKey(View, on_delete=models.CASCADE)
    type_profile = models.ForeignKey(TypeProfile, on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.view}/{self.type_profile}"


class StaticData(models.Model):
    """Store static data"""
    name = models.CharField(max_length=255, unique=True)
    content = models.TextField(null=True, blank=True)
    static_file = models.FileField(upload_to='files_excel/', default="vide")

    def __str__(self):
        return self.name


