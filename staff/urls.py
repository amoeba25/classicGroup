
from django.urls import path
from . import views

urlpatterns = [
    path('roles/', views.roles, name='roles'),
    path('rolesAdd/', views.rolesAdd, name='rolesAdd'),
    path('rolesDelete/<str:pk>', views.rolesDelete, name='rolesDelete'),
    path('rolesUpdate/<str:pk>', views.rolesUpdate, name='rolesUpdate'),
    path('employee/', views.employee, name='employee'),
    path('employeeAdd/', views.employeeAdd, name='employeeAdd'),
    path('employeeDelete/<str:pk>', views.employeeDelete, name='employeeDelete'),
    path('employeeUpdate/<str:pk>', views.employeeUpdate, name='employeeUpdate'),
    path('profileView/<str:pk>/', views.profileView, name='profileDetails'),
    path('profileUpdate/<str:pk>', views.profileUpdate, name='profileUpdate')
]