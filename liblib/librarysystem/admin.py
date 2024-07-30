from django.contrib import admin
from .models import Equipment, StudentEquipment
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Equipment, BookAdmin)


class StudentEquipmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentEquipment)
