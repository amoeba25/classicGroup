from django.urls import path
from . import views


urlpatterns = [
    path('', views.leave, name='leaveApplication'), # view all leave applications
    path('add/', views.leaveAdd, name='leaveApplicationAdd'), # add an application
    path('update/<str:id>/', views.leaveUpdate, name='leaveApplicationUpdate') , # update a leave form
    path('delete/<str:id>/', views.leaveDelete, name='leaveApplicationDelete') , # delete a leave form
] 
