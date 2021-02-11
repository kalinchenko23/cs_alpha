from django import forms



class SawSome(forms.Form):
    issue = forms.CharField(widget=forms.Textarea())