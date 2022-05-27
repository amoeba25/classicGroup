from multiprocessing import context
from django.shortcuts import redirect, render
# import datetime
from datetime import date, datetime

import attendance
from .models import Attendance
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
    
    context ={}
    # today's date
    current_day = date.today()
    
    #if the logged user is superuser
    if request.user.is_superuser:
        user_attendance = Attendance.objects.all()
        context = {"user_attendance" : user_attendance}
        return render(request,  "attendance/adminHome.html", context)
    
    # if normal user - get the user
    user_attendance = Attendance.objects.filter(date = current_day, user = request.user).first()
    
    #if no record exists for the day
    if user_attendance == None:
        attendance1 = Attendance(date = current_day, user = request.user)
        attendance1.save()
    
    #add total hours if time-out given
    if user_attendance.time_out is not None:
        
        # getting the total hours
        difference = datetime.combine(date.today(), user_attendance.time_out) - datetime.combine(date.today(), user_attendance.time_in)
        context['total'] = f"{difference.seconds//3600} : {(difference.seconds//60)%60}"
        print(type(context['total']))
    
    # if time_out is none
    else: 
        # if user hasn't timed-out after 8pm 
        max_timeout = datetime.now().replace(hour=20,minute=0,second=0,microsecond=0)
        if datetime.now() > max_timeout:
            user_attendance.time_out = max_timeout.time()
            user_attendance.save()
            context['auto'] = "Auto timeout" 
    
    context ["user_attendance"] = user_attendance
    print(context)
    return render(request, "attendance/home.html", context= context)

@csrf_exempt
def punchIn(request, id):
    
    current_time = datetime.now().time()
    
    user_attendance = Attendance.objects.get(id= id)
    user_attendance.time_in = current_time
    user_attendance.save()
    
    return redirect('attendanceView')
    

@csrf_exempt
def punchOut(request, id):
    
    current_time = datetime.now().time()
    
    user_attendance = Attendance.objects.get(id= id)
    user_attendance.time_out = current_time
    user_attendance.save()
    
    return redirect('attendanceView')