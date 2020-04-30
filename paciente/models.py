from django.db import models

# Create your models here.
class Paciente(models.Model):
    nome = models.IntegerField(default=0)
    febreM = models.IntegerField(default=0)
    febreA = models.IntegerField(default=0)
    tosseP = models.IntegerField(default=0)
    tosseS = models.IntegerField(default=0)
    fdeAr = models.IntegerField(default=0)
    dparaResp = models.IntegerField(default=0)
    pGastrico = models.IntegerField(default=0)
    diarreia = models.IntegerField(default=0)
    infectado = models.IntegerField(blank=True, null=True)

    def getDados(self):
        return [[self.febreM, self.febreA, self.tosseP, self.tosseS, self.fdeAr, self.dparaResp, self.pGastrico, self.diarreia]]

    def informar(self):
        return [[self.febreM, self.febreA, self.tosseP, self.tosseS, self.fdeAr, self.dparaResp, self.pGastrico, self.diarreia]]

    def imprimir(self):
        infectado = self.infectado == 1
        print("{}, Infectado {}".format(self.nome, infectado))
        return "{}, Infectado {}".format(self.nome, infectado)