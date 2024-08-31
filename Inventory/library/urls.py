"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import re_path as url
from django.urls import path
from librarysystem import views
from django.contrib.auth.views import LoginView,LogoutView
from librarysystem import views



urlpatterns = [
    path('admin/', admin.site.urls),

    # path('admin/', admin.site.urls),
    path('',include('librarysystem.urls')),

    path('accounts/',include('django.contrib.auth.urls') ),
    path('', views.home_view),

    # path(r'^books/(?P<id>\d+)/delete$', views.removebook_view),

    path('adminclick', views.adminclick_view),
    path('studentclick', views.studentclick_view),

    # path(r'^api/book/$', views.BookList.as_view()),


    path('adminsignup', views.adminsignup_view, name = 'register'),
    path('studentsignup', views.studentsignup_view),
    path('adminlogin', LoginView.as_view(template_name='library/adminlogin.html'),  name='login'),
    path('studentlogin', LoginView.as_view(template_name='library/studentlogin.html')),

    path('logout', LogoutView.as_view(template_name='library/index.html'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search_students/', views.search_students, name='search_students'),
    path('search_equipment/', views.search_equipment, name='search_equipment'),
    path('add_equipment/', views.add_equipment, name = 'add_equipment'),
    path('view_equipment/', views.view_equipment, name = 'view_equipment'),
    path('edit_equipment/<int:id>', views.edit_equipment, name = 'edit_equipment'),
    path('add_student/', views.add_student, name = 'add_student'),
    path('borrow_equipment/<int:student_id>/', views.borrow_equipment, name = 'borrow_equipment'),
    path('borrow_equipment/', views.borrow_equipment, name = 'borrow_equipment2'),
    path('return_equipment/<int:id>/', views.return_equipment, name='return_equipment'),
    path('assigned_equipment/', views.assigned_equipment, name = 'assigned_equipment'),
    path('viewstudent', views.viewstudent_view),
    path('viewissuedbookbystudent', views.viewissuedbookbystudent),
    # path ('removebook', views.removebook_view),

    path('aboutus', views.aboutus_view),
    # path('contactus', views.contactus_view),

]

