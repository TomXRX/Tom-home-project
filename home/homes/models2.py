from django.db import models

class Switches(models.Model):
    place = models.CharField(max_length=20)
    active=models.BooleanField(default=True)
    mobile=models.BooleanField(default=False)
    def __str__(self):
        return self.place

class Switch(models.Model):
    inside = models.ForeignKey(Switches, on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    typee=models.CharField(max_length=10)
    typer=models.CharField(max_length=5,default="B")
    reverse=models.BooleanField(default=True)
    def __str__(self):
        return self.name


class EspSaver(models.Model):
    Switcher=models.OneToOneField(Switches,on_delete=models.CASCADE,primary_key=True)
    Place=models.CharField(max_length=20)
    # getted=models.SmallIntegerField(default=0)
    remoting=models.SmallIntegerField(default=0)
    getted=models.BooleanField(default=False)
    # getted=models.IntegerField()
    def __str__(self):
        return self.Place
