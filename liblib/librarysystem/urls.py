from . import views 
from django.urls import path
# from django.conf.urls import url
from django.urls import re_path as url

from django.conf import settings
from django.conf.urls.static import static
from librarysystem.views import BookList,aboutus_view,add_equipment,adminclick_view,adminsignup_view,dashboard,view_equipment,assigned_equipment,viewissuedbookbystudent,viewstudent_view

urlpatterns = [
    

    # path(r'^books/(?P<id>\d+)/delete$', views.removebook_view, name='removebook'),
    url(r'^api/book/$', views.BookList.as_view()),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)