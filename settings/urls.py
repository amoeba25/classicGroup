from django.urls import path
from . import views


urlpatterns = [
    path('branch/', views.branch, name='branch'),
    path('branch-add/', views.branchAdd, name='branch-add'),
    path('branch-delete/<str:pk>', views.branchDestroy, name='branch-destroy'),
    path('branch-update/<str:pk>', views.branchUpdate, name='branch-update')
]
