from django.db import models
import datetime
from django.contrib.auth.models import User
from PIL import Image,ExifTags
from django.urls import reverse
from django.dispatch import receiver
import os



class Profile(models.Model):
    created_by = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    rank = models.CharField(max_length=3,null=True,blank=True)
    height=models.CharField(max_length=3,null=True,blank=True)
    weight= models.CharField(max_length=3,null=True,blank=True)

    def __str__(self):
        return f'{self.created_by} Profile'



class Appointment(models.Model):
    created_by=models.ForeignKey(User,null=True,on_delete= models.CASCADE)
    name =models.CharField(max_length=100)
    date = models.DateField()
    def __str__(self):
        return f'{self.name}'

class PT(models.Model):
    users=[i.last_name for i in User.objects.all()]
    instructors=[tuple([i,i]) for i in users]
    name_of_event=models.CharField(max_length=100)
    instructor=models.CharField(choices=instructors, max_length=100)
    date = models.DateField()
    def __str__(self):
        return f'{self.name_of_event}'



class Work_Progress(models.Model):
    created_by=models.ForeignKey(User,null=True,on_delete= models.CASCADE)
    date = models.DateField()
    customers=models.IntegerField(null=True,max_length=100,default=0)
    pay_inq=models.IntegerField(null=True,max_length=100,default=0)
    tl=models.IntegerField(null=True,max_length=100,default=0)
    cycles=models.IntegerField(null=True,max_length=100,default=0)
    rejects=models.IntegerField(null=True,max_length=100,default=0)
    recycles=models.IntegerField(null=True,max_length=100,default=0)
    management_notices=models.IntegerField(null=True,max_length=100,default=0)
    rsearch=models.IntegerField(null=True,max_length=100,default=0)
    def __str__(self):
        return f'{self.created_by}'




class ACFT(models.Model):
    pushaps_choices=[tuple([x,x]) for x in range(1,61)]
    dead_lift_choices=[tuple([x,x]) for x in range(140,341,10)]
    leg_tucks_choices=[tuple([x,x]) for x in range(21)]


    owner=models.ForeignKey(User,null=True,on_delete= models.CASCADE)
    pushups=models.IntegerField(choices=pushaps_choices, max_length=2)
    ball=models.CharField(blank=True, max_length=4)
    sprint_drag=models.CharField(blank=True, max_length=5)
    leg_tucks=models.IntegerField(choices=leg_tucks_choices, max_length=2)
    run=models.CharField(blank=True, max_length=5)
    dead_lift=models.IntegerField(choices=dead_lift_choices, max_length=3)
    def __str__(self):
        return f'{self.owner} ACFT'




