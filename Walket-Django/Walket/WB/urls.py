from django.urls import path
from . import views

urlpatterns=[
        path('',views.upload,name="home"),
        path('upload',views.output)
         
]
