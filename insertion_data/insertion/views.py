from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
import pandas
import insertion.models
from insertion.models import Client
from datetime import datetime
from pytz import UTC

#def lire_fichier(fichier):
 #   return 
def insertion_marque() :
    list_marques = set(pandas.read_excel(io="Exportpark.xls")['Marque'].tolist())
    try :
        for i in list_marques :
            marque = insertion.models.Marque()
            marque.nom = i
            marque.save()
        return "insertion termine!"
    except Exception as e:
        return str(e)
     
def insertion_vehicule():
    def ignore_null(x) :
        if pandas.notnull(x) :
            return x
        else :
            return None
          
    list_vehicules = pandas.read_excel(io="Exportpark.xls",sheet_name="A")
    list_vehicules["Immatriculation"] = list(map(ignore_null,list_vehicules["Immatriculation"].tolist()))
    xls = ["VIN","Modèle","Couleur","Kilometrage","Immatriculation"]
    model = ["vin","model","couleur","kilometrage","immatriculation"]
    #print(len(list_vehicules["Immatriculation"].tolist()))
    try:
        l = len(list_vehicules["VIN"].tolist())
        l1 = len(list_vehicules["Immatriculation"])
        print(l)
        print(l1)
        for y in range(l) :
            vehicule = insertion.models.Vehicule()
            for i,j in zip(xls,model):
                    setattr(vehicule, j,list_vehicules[i].tolist()[y])
            client_id = Client.objects.get(nom=list_vehicules["Client"].tolist()[y]).id
            marque_id = insertion.models.Marque.objects.get(nom=list_vehicules["Marque"].tolist()[y]).id
            vehicule.client_id = client_id
            vehicule.marque_id = marque_id
            vehicule.creation_date = datetime.today().strftime('%Y-%m-%d')
            vehicule.save()
        return HttpResponse("<p>insertion termine!</p>")
    except Exception as e :
        return str(e)

def insertion_client():
    list_clients = pandas.read_excel(io="Exportpark.xls")['Client'].tolist()
    set_clients = set(list_clients)
    #return HttpResponse(f"{set_clients}")    
    try :
        for i in set_clients :
            client = Client()
            client.nom = i
            
            try :
                client.user = User.objects.get(username=i)
            except Exception as e :
                if str(e) == "User matching query does not exist." :
                    client.user = User()
                    client.username = i
            client.save()
        return "insertion termine!"
    except Exception as e :
        return str(e)
def insertion_donnees(request):
    reponseC = insertion_client()
    reponseM = insertion_marque()
    reponseV = insertion_vehicule()
    return HttpResponse(f"{reponseC}, {reponseV}, {reponseM}")