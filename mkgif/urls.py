#this file doesnt exist by default I have to create this url file

from django.urls import path
from . import views

#the app name from inside templates, app name comes from there its predefined - find it
app_name = 'mkgif'

urlpatterns = [
        #index points to the index view
        path('', views.index, name='index'),
        #this is new, thats a name parameter - I want an integer and want to assign it to a pk
        path('details/<int:pk>/', views.details, name='details'),
        path('delete/<int:pk>/', views.delete_animation, name='delete_animation'),
]
