from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginReq, name='homepage'),
    path('notAuthorized/', views.notAuthorized, name="notAuthorized"),
    path("logout", views.logoutReq, name="logout")
]
