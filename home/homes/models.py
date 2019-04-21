from django.db import models


class Switcher(models.Model):
    name = models.CharField(max_length=20,default="")
    place = models.CharField(max_length=20,default="")
    lastV = models.DateTimeField('lastVerified')
    lastVP=models.CharField(max_length=20)
    visible=models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Switchee(models.Model):
    switcher = models.ForeignKey(Switcher, on_delete=models.CASCADE)
    name = models.CharField(max_length=20,default="")
    place = models.CharField(max_length=20,default="")
    state = models.IntegerField(default=0)
    reverse=models.BooleanField(default=True)
    # typ = models.CharField(max_length=5, default="")
    # class Meta:
    #     abstract = True
    def __str__(self):
        return self.switcher.name+"::"+self.name

class Input(Switchee, models.Model):
    typ=models.CharField(max_length=5,default="I")


class Switch(Switchee, models.Model):
    typ = models.CharField(max_length=5, default="S")

class PWM(Switchee, models.Model):
    typ = models.CharField(max_length=5, default="P")
    max=models.PositiveSmallIntegerField(default=1024)
    min=models.SmallIntegerField(default=0)
    # freq=models.SmallIntegerField(default=50)



class Esper(models.Model):

    switcher=models.OneToOneField(Switcher, on_delete=models.CASCADE)
    mobile = models.BooleanField(default=False)
    inited=models.BooleanField(default=False)
    place=models.CharField(max_length=20,default="")
    keep=models.PositiveSmallIntegerField(default=0)

    name=models.CharField(max_length=20,default="")
    enabled=models.BooleanField(default=True)
    def __str__(self):
        return self.name
