from django.contrib import admin
from django.urls import path
from teq_wish_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get/', Student.as_view(), name="get"),
    path('post/', Student.as_view(), name="post"),
    path('put/<str:regNo>/', Student.as_view(), name="put"),
    path('delete/<str:regNo>/', Student.as_view(), name="delete"),
    path('get/<str:regNo>/', student_update.as_view(), name="stud_up"),
    path('mail/', send_birthday_emails, name='mail'),
    path('download/', download_students_zip, name='downloadfile'),
]
