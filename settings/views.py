import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import BranchAddForm
from .models import Branch




# Create your views here.
def LatLongCheck(form):
    form.save()
    api_key = 'AIzaSyA8eM7LY5MYC3FArPRKpey--utiovq66RE'
    address = " ".join([form.cleaned_data['branchAddress1'], form.cleaned_data['branchAddress2'],
                        str(form.cleaned_data['zip_code']), form.cleaned_data['cityName']])
    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key)).json()
    lat = api_response['results'][0]['geometry']['location']['lat']
    long = api_response['results'][0]['geometry']['location']['lng']
    Branch.objects.filter(branchCode=form.cleaned_data['branchCode']).update(latitude=lat, longitude=long)


# All list of branch GET Requests simply
def branch(request):
    branch_all = Branch.objects.all()
    context = {'branch_all': branch_all}
    return render(request, 'settings/branch/branch.html', context)


# Adding in branch Add with POST request
@login_required(login_url="homepage")
@permission_required('setting.add_branch', login_url="notAuthorized")
def branchAdd(request):
    branchAddForm = BranchAddForm()
    if request.method == 'POST':
        form = BranchAddForm(request.POST)
        if form.is_valid():
            LatLongCheck(form)
            messages.success(request, 'Branch Created Successfully')
            return redirect('branch')
    context = {'branchAddForm': branchAddForm}
    return render(request, 'settings/branch/branchAdd.html', context)


# Branch Update
@login_required(login_url="homepage")
@permission_required('setting.change_branch', login_url="notAuthorized")
def branchUpdate(request, pk):
    branch_Update = Branch.objects.get(id=pk)
    form = BranchAddForm(instance=branch_Update)
    if request.method == 'POST':
        form = BranchAddForm(request.POST, instance=branch_Update)
        if form.is_valid():
            LatLongCheck(form)
            messages.success(request, 'Branch Update Successfully')
            return redirect('branch')
    context = {'updateForm': form, 'branch_Update': branch_Update}
    return render(request, 'settings/branch/branchUpdate.html', context)


@login_required(login_url="homepage")
@permission_required('setting.delete_branch', login_url="notAuthorized")
def branchDestroy(request, pk):
    branchDelete = Branch.objects.get(id=pk)
    branchDelete.delete()
    messages.success(request, 'Branch Destroy Successfully')
    return redirect("branch")
