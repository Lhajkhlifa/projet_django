from csv import DictReader
from django.core.management import BaseCommand
from insertion.models import Data
fichier_csv = open('./data.csv','r')
class Command(BaseCommand):
    def handle(self, *args, **options):
        for ligne in DictReader(fichier_csv):
            data = Data()
            data.id = ligne['id']
            data.nom = ligne['nom']
            data.save()
        fichier_csv.close()