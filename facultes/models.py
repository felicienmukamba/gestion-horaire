from django.db import models
from django_softdelete.models import SoftDeleteModel
from users.models import Enseignant

class Faculte(SoftDeleteModel):
    designation = models.CharField(max_length=50)
    
    class Meta:
        ordering=('designation',)
    
    def __str__(self):
        return self.designation
    

class Facultaire(SoftDeleteModel):
    actif = models.BooleanField(default=True)
    enseignant=models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    faculte = models.ForeignKey(Faculte, on_delete=models.CASCADE)
    
    class Meta:
            ordering=('faculte',)
    
    def __str__(self):
        return self.enseignant.nom



class Departement(SoftDeleteModel):
    designation = models.CharField(max_length=50)
    faculte = models.ForeignKey(Faculte, on_delete=models.CASCADE)

    class Meta:
        ordering = ("designation",)

    def __str__(self):
        return self.designation
