from django.db import models
from . import forms
from django import forms
from . import models

from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.contrib.auth.forms import UserCreationForm



class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class StudentForm(forms.ModelForm):
    class Meta:
        model=models.Student
        fields=['student_id','first_name','last_name','email','department','course']

class EquipmentForm(forms.ModelForm):
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model=models.Equipment
        fields=['name','tag_num','description', 'purchase_date','location', 'condition']

class BorrowForm(forms.ModelForm):
    return_date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = models.StudentEquipment
        fields = ['student','equipment', 'return_date']
   
   
