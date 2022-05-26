from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import LeaveApp
from .forms import LeaveAppForm


# see all leave applications view
@login_required(login_url="homepage")
def leave(request):
    if(request.user.username == 'admin'):
        print("admin")
        leaveData = LeaveApp.objects.all()
        context = {'leaveData': leaveData}
        return render(request, 'leave/admin_leave.html', context= context)
    
    leaveData = LeaveApp.objects.filter(user = request.user.username)
    context = {"leaveData": leaveData}
    return render(request, 'leave/leave.html', context= context)

# add new leave application
@login_required(login_url="homepage")
def leaveAdd(request):
    leave = LeaveAppForm()
    
    if request.method == 'POST':
        form = LeaveAppForm(request.POST)
        
        #check if valid
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leave Application added Successfully')
            return redirect('leaveApplication')
    
    context = {"leave": leave}
    return render(request, "leave/leaveAdd.html", context)   


#updating existing applications
@login_required(login_url="homepage")
def leaveUpdate(request, id):
    leave_update = LeaveApp.objects.get(id =id) 
    form = LeaveAppForm(instance = leave_update)
    print(form.instance.id)
    context = {"updateForm": form}
    
    #admin can change the status
    if(request.user.username == 'admin'):
        print("admin")
        if request.method == 'POST':
            form = LeaveAppForm(request.POST, instance = leave_update)
            if form.is_valid():
                form.save()
                messages.success(request, 'Leave Application updated Successfully')
                return redirect('leaveApplication')
        return render(request, 'leave/admin_leaveUpdate.html', context)
    
    # if its not the admin
    if request.method == 'POST':
        form = LeaveAppForm(request.POST, instance = leave_update)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leave Application updated Successfully')
            return redirect('leaveApplication')
    return render(request, "leave/leaveUpdate.html", context)

# deletes any applications
@login_required(login_url="homepage")
def leaveDelete(request, id):
    app = LeaveApp.objects.get(id= id)
    app.delete()
    messages.success(request, "Application deleted")
    return redirect("leaveApplication")