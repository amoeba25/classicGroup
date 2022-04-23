from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect

from .forms import RolesForm, UserForm, ProfileForm
from .models import Profile


# Roles CRUD
# @login_required(login_url="homepage")
def roles(request):
    all_roles = Group.objects.all()
    context = {"all_roles": all_roles}
    return render(request, 'staff/roles/roles.html', context)


# @login_required(login_url="homepage")
# @permission_required('auth.add_role', login_url="notAuthorized")
def rolesAdd(request):
    group_form = RolesForm()
    if request.method == "POST":
        form = RolesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Role Created Successfully")
            return redirect('roles')
    context = {'role_form': group_form}
    return render(request, 'staff/roles/addRole.html', context)


# @login_required(login_url="homepage")
# @permission_required('auth.change_role', login_url="notAuthorized")
def rolesUpdate(request, pk):
    group_update = Group.objects.get(id=pk)
    form = RolesForm(instance=group_update)
    if request.method == 'POST':
        form = RolesForm(request.POST, instance=group_update)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role Updated Successfully')
            return redirect('roles')
    context = {'role_update': group_update, 'role_form': form}
    return render(request, 'staff/roles/updateRole.html', context)


# @login_required(login_url="homepage")
# @permission_required('auth.delete_role', login_url="notAuthorized")
def rolesDelete(request, pk):
    roleDelete = Group.objects.get(id=pk)
    roleDelete.delete()
    messages.success(request, 'Role Deleted Successfully')
    return redirect('roles')


# Employee CRUD
# @login_required(login_url="homepage")
def employee(request):
    user_data = User.objects.all()
    profile = Profile.objects.all()
    context = {'profile': profile, 'user_data': user_data}
    return render(request, 'staff/employee/employee.html', context)


# @login_required(login_url="homepage")
# @permission_required('auth.add_employee', login_url="notAuthorized")
def employeeAdd(request):
    user_form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            password = make_password(form.cleaned_data['password'])
            form.save()
            User.objects.filter(username=form.cleaned_data['username']).update(
                password=password)
            messages.success(request, "Employee Created Successfully")
            return redirect('employee')
    context = {'user_form': user_form}
    return render(request, 'staff/employee/employeeAdd.html', context)


# It deals with User model of django
# @login_required(login_url="homepage")
# @permission_required('auth.update_employee', login_url="notAuthorized")
def employeeUpdate(request, pk):
    user_update = User.objects.get(username=pk)
    form = UserForm(instance=user_update)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_update)
        if form.is_valid():
            password = make_password(form.cleaned_data['password'])
            form.save()
            User.objects.filter(username=form.cleaned_data['username']).update(
                password=password)
            messages.success(request, 'Employee Updated Successfully')
            return redirect('employee')
    context = {'user_update': user_update, 'user_form': form}
    return render(request, 'staff/employee/employeeUpdate.html', context)


# It deals with profile model
# @login_required(login_url="homepage")
@permission_required('profile.update_profile', login_url="notAuthorized")
def profileUpdate(request, pk):
    user_update = Profile.objects.get(id=pk)
    form = ProfileForm(instance=user_update)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_update)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee Profile Updated Successfully')
            return redirect('employee')
    context = {'user_update': user_update, 'user_form': form}
    return render(request, 'staff/profileEmployee/profileUpdate.html', context)


# @login_required(login_url="homepage")
def profileView(request, pk):
    userData = Profile.objects.get(id=pk)
    context = {"userData": userData}
    return render(request, 'staff/profileEmployee/profileView.html', context)


# @login_required(login_url="homepage")
@permission_required('auth.destroy_user', login_url='notAuthorized')
def employeeDelete(request, pk):
    userDelete = Profile.objects.get(id=pk)
    userDelete.delete()
    messages.success(request, 'Employee Deleted Successfully')
    return redirect('employee')
