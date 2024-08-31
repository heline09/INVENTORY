from django.db import models
from . import forms
from django import forms
from . import models

from .models import Equipment

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
        fields=['student_id','first_name','last_name','phone_number','email','department','course']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        # Adding a placeholder to the department field
        self.fields['department'].empty_label = "Choose Department"
        
    # def clean_phone_number(self):
    #     phone_number = self.cleaned_data.get('phone_number')
    #     if isinstance(phone_number, int):
    #         phone_number = str(phone_number)
    #     # Additional validation can be added here if needed
    #     return phone_number

class EquipmentForm(forms.ModelForm):
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
   
    class Meta:
        model=models.Equipment
        fields=['name','serial_num','tag_num','model_num','description', 'purchase_date','location', 'condition']
        widgets = {
            'tag_num': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }

class BorrowForm(forms.ModelForm):
    return_date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'datetime-local'}))
    equipment = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.all(),
        widget=forms.SelectMultiple,
    )
    class Meta:
        model = models.StudentEquipment
        fields = ['student','equipment', 'return_date']

    
   
