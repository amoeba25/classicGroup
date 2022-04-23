from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect

from .forms import rawAddForm, finishedAddForm, utilityAddForm
from .models import RawInventory, FinishedInventory, UtilityInventory


# Create your views here.

# Raw inventory Management
@login_required(login_url="homepage")
@permission_required("sales.view_RawInventory", login_url="notAuthorized")
def rawInvent(request):
    rawInvent = RawInventory.objects.all()
    context = {'rawInvent': rawInvent}
    return render(request, 'inventory/raw/rawInventory.html', context)


@login_required(login_url="homepage")
@permission_required("sales.add_RawInventory", login_url="notAuthorized")
def rawInventAdd(request):
    rawAdd = rawAddForm()
    if request.method == 'POST':
        form = rawAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Added Successfully')
            return redirect('rawInventory')
    context = {'rawAddForm': rawAdd}
    return render(request, 'inventory/raw/rawInventoryAdd.html', context)


@login_required(login_url="homepage")
@permission_required("sales.update_RawInventory", login_url="notAuthorized")
def rawInventUpdate(request, pk):
    raw_Update = RawInventory.objects.get(id=pk)
    form = rawAddForm(instance=raw_Update)
    if request.method == 'POST':
        form = rawAddForm(request.POST, instance=raw_Update)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory Update Successfully')
            return redirect('rawInventory')
    context = {'updateForm': form, 'raw_Update': raw_Update}
    return render(request, 'inventory/raw/rawInventoryUpdate.html', context)


@login_required(login_url="homepage")
@permission_required("sales.delete_RawInventory", login_url="notAuthorized")
def rawInventDelete(request, pk):
    branchDelete = RawInventory.objects.get(id=pk)
    branchDelete.delete()
    messages.success(request, 'Product Destroy Successfully')
    return redirect("rawInventory")


# Utility Inventory Management
@login_required(login_url="homepage")
@permission_required("sales.view_FinishedInventory", login_url="notAuthorized")
def utilityInvent(request):
    utilityInvent = UtilityInventory.objects.all()
    context = {'rawInvent': utilityInvent}
    return render(request, 'inventory/utility/utilityInventory.html', context)


@login_required(login_url="homepage")
@permission_required("sales.add_FinishedInventory", login_url="notAuthorized")
def utilityInventAdd(request):
    utilityAdd = utilityAddForm()
    if request.method == 'POST':
        form = utilityAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Utility Added Successfully')
            return redirect('utilityInventory')
    context = {'utilityAddForm': utilityAdd}
    return render(request, 'inventory/utility/utilityInventoryAdd.html', context)


@login_required(login_url="homepage")
@permission_required("sales.update_FinishedInventory", login_url="notAuthorized")
def utilityInventUpdate(request, pk):
    utility_Update = UtilityInventory.objects.get(id=pk)
    form = utilityAddForm(instance=utility_Update)
    if request.method == 'POST':
        form = utilityAddForm(request.POST, instance=utility_Update)
        if form.is_valid():
            form.save()
            messages.success(request, 'Utility Update Successfully')
            return redirect('utilityInventory')
    context = {'updateForm': form, 'utility_Update': utility_Update}
    return render(request, 'inventory/utility/utilityInventoryUpdate.html', context)


@login_required(login_url="homepage")
@permission_required("sales.delete_FinishedInventory", login_url="notAuthorized")
def utilityInventDelete(request, pk):
    utilityDelete = UtilityInventory.objects.get(id=pk)
    utilityDelete.delete()
    messages.success(request, 'Utility Destroy Successfully')
    return redirect("utilityInventory")


# Finished Inventory Management
@login_required(login_url="homepage")
def finishedInvent(request):
    finishInvent = FinishedInventory.objects.all()
    context = {'finishedInvent': finishInvent}
    return render(request, 'inventory/finish/finishedInventory.html', context)


@login_required(login_url="homepage")
def finishedInventAdd(request):
    finishedAdd = finishedAddForm()
    if request.method == 'POST':
        form = finishedAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Finished Added Successfully')
            return redirect('finishedInventory')
    context = {'finishedAddForm': finishedAdd}
    return render(request, 'inventory/finish/finishedInventoryAdd.html', context)


@login_required(login_url="homepage")
def finishedInventUpdate(request, pk):
    finished_Update = FinishedInventory.objects.get(id=pk)
    form = finishedAddForm(instance=finished_Update)
    if request.method == 'POST':
        form = finishedAddForm(request.POST, instance=finished_Update)
        if form.is_valid():
            form.save()
            messages.success(request, 'Finished Update Successfully')
            return redirect('finishedInventory')
    context = {'updateForm': form, 'finished_Update': finished_Update}
    return render(request, 'inventory/finish/finishedInventoryUpdate.html', context)


@login_required(login_url="homepage")
def finishedInventDelete(request, pk):
    finishedDelete = FinishedInventory.objects.get(id=pk)
    finishedDelete.delete()
    messages.success(request, 'Finished Destroy Successfully')
    return redirect("finishedInventory")
