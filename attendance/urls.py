from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name= "attendanceView"),
    path("/in/<str:id>", views.punchIn, name="attendanceIn"),
    path("/out/<str:id>", views.punchOut, name="attendanceOut"),
]