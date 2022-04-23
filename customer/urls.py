from django.urls import path
from . import views

urlpatterns = [
    path('master/', views.customer, name='customerHome'),
    path('cust-add/', views.customerAdd, name='customerAdd'),
    path('cust-delete/<str:pk>/', views.customerDelete, name='customerDelete'),
    path('cust-update/<str:pk>/', views.customerUpdate, name='customerUpdate'),

]
