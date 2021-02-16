from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import  ACFT, Appointment, Work_Progress,PT,Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    last_name = forms.CharField(max_length=50)

    class Meta:
        model=User
        fields=['username',"last_name",'email','password1','password2']

class DateInput(forms.DateInput):
    input_type = 'date'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=['rank','height','weight']


class AppointmentForm(forms.ModelForm):
    date=forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Appointment
        fields=['name','date']

class Work_ProgressForm(forms.ModelForm):
    date=forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Work_Progress
        fields=['date','customers','pay_inq','tl','cycles','rejects','recycles','management_notices','rsearch']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model=User
        fields=['username','email']

class PT_Form(forms.ModelForm):
    date=forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model=PT
        fields=['name_of_event','instructor','date']


class AerForm(forms.Form):
    q1 = forms.CharField(label="What suppose to happen?",max_length=200,widget=forms.TextInput(attrs={'class': 'form-control'}))
    q2 = forms.CharField(label="What did happen?",max_length=200,widget=forms.TextInput(attrs={'class': 'form-control'}))
    q3 = forms.CharField(label="What are the sustainments?",max_length=200,widget=forms.TextInput(attrs={'class': 'form-control',"placeholder":"sustainment 1"}))
    q4 = forms.CharField(label=False,max_length=200,widget=forms.TextInput(attrs={'class': 'form-control',"placeholder":"sustainment 2"}))
    q5 = forms.CharField(label=False,max_length=200,widget=forms.TextInput(attrs={'class': 'form-control',"placeholder":"sustainment 3"}))
    q6 = forms.CharField(required=False,label=False,max_length=200,widget=forms.TextInput(attrs={'class': 'form-control',"placeholder":"sustainment 4. Leave blank if none."}))
    q7 = forms.CharField(required=False,label=False,max_length=200,widget=forms.TextInput(attrs={'class': 'form-control',"placeholder":"sustainment 5. Leave blank if none."}))
    q8 = forms.CharField(label="What are the improvements?",max_length=50,widget=forms.TextInput(attrs={'class': 'form-control',"placeholder":"improvement 1"}))
    q9 = forms.CharField(label=False,max_length=200,widget=forms.TextInput(attrs={'class': 'form-control',"placeholder":"improvement 2"}))
    q10 = forms.CharField(required=False,label=False,max_length=200,widget=forms.TextInput(attrs={'class': 'form-control',"placeholder":"improvement 3. Leave blank if none."}))
    q11 = forms.CharField(required=False,label=False,max_length=200,widget=forms.TextInput(attrs={'class': 'form-control',"placeholder":"improvement 4. Leave blank if none."}))
    q12 = forms.CharField(required=False,label=False,max_length=200,widget=forms.TextInput(attrs={'class': 'form-control',"placeholder":"improvement 5. Leave blank if none."}))
    q13 = forms.CharField(required=False,label="What are the alibis?",max_length=200,widget=forms.TextInput(attrs={'class': 'form-control',"placeholder":"alibi 1. Leave blank if none."}))
    q14 = forms.CharField(required=False,label=False,max_length=200,widget=forms.TextInput(attrs={'class': 'form-control',"placeholder":"alibi 2. Leave blank if none."}))

class NumbersForm(forms.Form):
    date=forms.DateField(widget=forms.SelectDateWidget())


class ACFTForm(forms.ModelForm):
    class Meta:
        model=ACFT
        fields=['pushups', 'ball','sprint_drag','leg_tucks','run','dead_lift']
        widgets = {
            'ball': forms.TextInput(attrs={'placeholder': 'format 0.0'}),
            'sprint_drag': forms.TextInput(attrs={'placeholder': 'format 00:00'}),
            'run': forms.TextInput(attrs={'placeholder': 'format 00:00'}),
        }























