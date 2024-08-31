from django.db import models
# from django.contrib.auth.models import AbstractUser
from datetime import datetime,timedelta, time
from django.utils import timezone
from django.core.exceptions import ValidationError


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.department.name} - {self.name}"

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length = 15)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"



class Equipment(models.Model):
    CONDITION_CHOICES = [
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    name = models.CharField(max_length=30)
    serial_num = models.CharField(max_length=100, unique=True, null=True, blank=True)
    tag_num = models.CharField(max_length=100, unique=True, null=True, blank=True)
    model_num = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    purchase_date = models.DateField()
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=40)
    condition = models.CharField(max_length=30,choices=CONDITION_CHOICES,default='good')

    def __str__(self):
        return str(self.name)+"["+str(self.tag_num)+']'

    def check_availability(self):
        return self.is_available

def get_expiry():
    return datetime.today() + timedelta(days=15)

def default_return_by():
    now = timezone.now()
    return datetime.combine(now.date(), time(17, 0, 0))

class StudentEquipment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date= models.DateTimeField(null=True, blank=True, default=default_return_by)
    date_returned = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} borrowed {self.equipment} on {self.borrow_date}"

    def return_equipment(self):
        self.date_returned= timezone.now()
        self.equipment.is_available = True
        self.equipment.save()
        self.save()

    def borrow_equipment(self):        
        self.equipment.is_available = False
        self.equipment.save()
        self.save()

    def add(self):
        if not self.equipment.check_availability():
            raise ValidationError(f'Equipment {self.equipment.name} is not available for borrowing.')
        super().save(*args, **kwargs)
        self.equipment.is_available = False
        self.equipment.save()
    
        def is_late(self):
            if self.date_returned:
                return self.date_returned > self.return_date
            # If date_returned is not set, check if the current date is past the return_date
            return self.return_date < timezone.now()





