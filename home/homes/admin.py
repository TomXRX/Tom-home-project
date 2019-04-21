from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Esper)
admin.site.register(Switcher)
admin.site.register(Switchee)
admin.site.register(Switch)
admin.site.register(Input)
admin.site.register(PWM)
