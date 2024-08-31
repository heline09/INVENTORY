from rest_framework import serializers
from .models import Student,Equipment,StudentEquipment

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields= "__all__"

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields= "__all__"

class StudentEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEquipment
        fields= "__all__"