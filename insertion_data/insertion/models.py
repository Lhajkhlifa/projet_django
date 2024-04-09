from django.db import models
class Data(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=20)