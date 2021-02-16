from django.contrib import admin
from .models import Profile,ACFT,Appointment,Work_Progress,PT

# Register your models here.

admin.site.register(Work_Progress)
admin.site.register(ACFT)
admin.site.register(Appointment)
admin.site.register(Profile)
admin.site.register(PT)

