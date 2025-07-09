"""
URL configuration for teq_wish project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from teq_wish_app import views
from teq_wish_app.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('get/',Student.as_view(),name="get"),
    path('post/',Student.as_view(),name="post"),
    path('put/<str:regNo>/',Student.as_view(),name="put"),
    path('delete/<str:regNo>/',Student.as_view(),name="delete"),
    path('get/<str:regNo>/',student_update.as_view(),name="stud_up"),
    #path('api/download-csv/', ImageZipDownloadView.as_view(), name='download_csv'),
    path('mail/',views.send_birthday_emails,name='mail'),
    path('download/',views.download_students_zip,name='downloadfile'),

]
