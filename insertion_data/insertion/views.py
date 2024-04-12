from django.shortcuts import render
from django.http import HttpResponse
from pandas import read_excel
from insertion.models import Marque
def insertion_marque(request) :
    list_marques = read_excel(io="donnees_fixe.xlsx",sheet_name="Marques")['Marques'].tolist()

    #return HttpResponse(f"<p>{list_marques[1]}</p>")
    try :
        for i in list_marques :
            marque = Marque()
            marque.nom = i
            marque.save()
        return HttpResponse(f"insertion termine!")
    except Exception as e:
        return HttpResponse(f"<p>{str(e)}</p>")
     
