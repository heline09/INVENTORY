from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from . import forms,models
from .forms import StudentForm,BorrowForm,EquipmentForm
from django.contrib.auth.forms import AuthenticationForm    
from django.contrib.auth import login 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Student,Equipment,StudentEquipment, Department, Course
from .serializer import StudentSerializer, EquipmentSerializer, StudentEquipmentSerializer
from datetime import date
# PDF Generation
from reportlab.pdfgen import canvas
from io import BytesIO
# for XHTML to PDF Conversion
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import os



#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')

#for showing signup/login button for teacher
def adminclick_view(request):
        form = AuthenticationForm()
        if request.user.is_authenticated:
                return redirect('dashboard')  # Redirect to the dashboard if the user is already authenticated
    
    # If the user is not authenticated, render the login form
        if request.method == 'POST':
                form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            form = AuthenticationForm()  # Display an empty login form for GET requests

        return render(request, 'library/adminlogin.html', {'form': form})


def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()

            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'library/adminsignup.html',{'form':form})

def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def dashboard(request):
    if is_admin(request.user):
        return render(request,'library/adminafterlogin.html')
    else:
        return render(request,'library/studentafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def add_equipment(request):
    #now it is empty book form for sending to html
    form=forms.EquipmentForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.EquipmentForm(request.POST)
        if form.is_valid():
            user=form.save()
            messages.success(request, "Equipment added successfully.")
            return render(request,'library/adminafterlogin.html')

    return render(request,'library/add_equipment.html',{'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def view_equipment(request):
    equipments = Equipment.objects.filter(is_available=True)
    return render(request,'library/view_equipment.html',{'equipments':equipments})


def add_student(request):
   if request.method == 'POST': 
        selected_department_id = request.POST.get("id_department")
        selected_courses = request.POST.getlist("id_course")

        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()

            # Add selected courses to the student's profile
            if selected_courses:  # Ensure courses are selected
                for course_id in selected_courses:
                    course = Course.objects.get(id=course_id)
                    student.courses.add(course)  # Assuming 'courses' is the FK field

            return redirect('borrow_equipment', student.id)
        else:
            print(form.errors)
   else:
        form = StudentForm()
        select_options = {}
        for department in Department.objects.all():
            courses = [{'id': course.id, 'name': course.name} for course in department.courses.all()]
            select_options[department.id] = courses    

        courses = Course.objects.all()

        selected_department_id = request.POST.get("id_department")
        if selected_department_id:  
            courses = Course.objects.filter(department_id=selected_department_id)

        context = {
            'form': form,
            'departments': Department.objects.all(),
            'select_options': select_options,
            'courses': courses
        }
    
   return render(request, 'library/student.html', context)

def borrow_equipment(request, student_id=None):
    student = None
    if student_id:
        student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        selected_equipment_ids = request.POST.getlist('equipment')  # Make sure this matches the form field name
      
        if form.is_valid():           
            return_date = form.cleaned_data['return_date']
            student = form.cleaned_data['student']
                        
            # Check if all selected equipment is available using check_availability() method
            unavailable_equipment = False 
            for equipment_id in selected_equipment_ids:
                equipment=Equipment.objects.get(id=equipment_id)
                if equipment.is_available == False:
                    unavailable_equipment = True
                    messages.error(request, f'The following equipment is not available for borrowing: {equipment.tag_num}-{equipment.name}')
                else:
                    record = StudentEquipment.objects.create(student=student, equipment=equipment, return_date=return_date)
                    record.borrow_equipment()

            if unavailable_equipment == False:
                messages.success(request, "Equipments borrowed successfully.")
                return redirect('assigned_equipment')
        else:
            # Print form errors for debugging
            print(form.errors)
    else:
        form = BorrowForm({'student': student})
    
    
    return render(request, 'library/borrow_equipment.html', {'form': form})

 
def edit_equipment(request, id):
    equipment = Equipment.objects.get(id=id)

    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        form.save()
        messages.success(request, 'Your form is updated and submitted successfully!') 
        return redirect('view_equipment') 

    else:
        form = EquipmentForm(instance=equipment)  # Pre-populate the form

    return render(request, 'library/updateform.html', {'form':form})

def remove_equipment(request, equipment_id):
    equipment = Equipment.objects.get(pk=equipment_id)
    equipment.is_available = False
    equipment.save()
    return redirect('view_equipment')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def assigned_equipment(request):    
    assigned_equipment = StudentEquipment.objects.filter(date_returned=None)
    return render(request,'library/assigned_equipment.html',{'assigned_equipment':assigned_equipment})

def return_equipment(request, id):
    equipment = get_object_or_404(StudentEquipment, id=id)
   
    equipment.return_equipment()
    return redirect('assigned_equipment')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'library/viewstudent.html',{'students':students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)

    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,student[0].branch,book.name,book.author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)

    return render(request,'library/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})

def aboutus_view(request):
    return render(request,'library/aboutus.html')

def LogoutView(request):
     logout(request)
     return redirect('adminlogin')

class BookList(APIView):
    def get(self, request, format=None):
        books = Book.objects.all()
        serializers = BookSerializer(books, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        pk = self.kwargs.get('pk')
        # appointments = self.get_object(pk)
        books = BookSerializer.filter(pk = pk)
        books.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


def search_students(request):
    search_term = request.GET.get('search_term')
    students = []
    if search_term:
        results = Student.objects.filter(student_id__icontains=search_term) | Student.objects.filter(last_name__icontains=search_term) | Student.objects.filter(first_name__icontains=search_term)
        for result in results:
            students.append({'id': result.id,
                             'student_id': result.student_id,
                             'first_name': result.first_name,
                             'last_name': result.last_name,
                             })
          
    return JsonResponse(students, safe=False)

def search_equipment(request):
    search_term = request.GET.get('search_term')
    equipments = []
    if search_term:
        assets = Equipment.objects.filter(is_available=True)
        assets = assets.filter(tag_num__icontains=search_term) | assets.filter(name__icontains=search_term)
        for asset in assets:
            equipments.append({
                'id': asset.id,
                'tag_num': asset.tag_num,
                'name': asset.name,
            })
            # print("Equipment results:", equipments)
    return JsonResponse(equipments, safe=False)

def generate_report(request):
    equipment = Equipment.objects.all()
    template_path = 'library/available_report.html'
