from django.urls import path

from . import views

urlpatterns = [
    path('raw/', views.rawInvent, name='rawInventory'),
    path('raw-inventAdd/', views.rawInventAdd, name='rawInventoryAdd'),
    path('raw-inventUpdate/<str:pk>', views.rawInventUpdate, name='rawInventoryUpdate'),
    path('raw-inventDelete/<str:pk>', views.rawInventDelete, name='rawInventoryDelete'),
    path('utility/', views.utilityInvent, name='utilityInventory'),
    path('utility-inventAdd/', views.utilityInventAdd, name='utilityInventoryAdd'),
    path('utility-inventUpdate/<str:pk>', views.utilityInventUpdate, name='utilityInventoryUpdate'),
    path('utility-inventDelete/<str:pk>', views.utilityInventDelete, name='utilityInventoryDelete'),
    path('finished/', views.finishedInvent, name='finishedInventory'),
    path('finished-inventAdd/', views.finishedInventAdd, name='finishedInventoryAdd'),
    path('finished-inventUpdate/<str:pk>', views.finishedInventUpdate, name='finishedInventoryUpdate'),
    path('finished-inventDelete/<str:pk>', views.finishedInventDelete, name='finishedInventoryDelete'),
]
