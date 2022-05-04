from django.urls import path

from . import views

urlpatterns = [
    # production  Urls
    path('production/', views.viewPlant, name="ProductionPlant"),
    path('production-add/', views.ProductionAdd, name="ProductionAdd"),
    path('production-delete/<str:pk>/', views.ProductionDelete, name="ProductionDelete"),
    path('production-Update/<str:pk>/', views.ProductionUpdate, name="ProductionUpdate"),
] 