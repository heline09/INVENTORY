from django.contrib import admin
from .models import Equipment, StudentEquipment, Course,Student,Department
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Equipment, BookAdmin)


class StudentEquipmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentEquipment)

admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Student)
