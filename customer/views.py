from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer
from django.contrib.auth.decorators import login_required
from .forms import CustomerAddForm


# Create your views here.

@login_required(login_url="homepage")
def customer(request):
    cusData = Customer.objects.all()
    context = {'cusData': cusData}
    return render(request, 'customer/customer.html', context)


@login_required(login_url="homepage")
def customerAdd(request):
    cusAdd = CustomerAddForm()
    if request.method == 'POST':
        form = CustomerAddForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
            messages.success(request, 'Customer Added Successfully')
            return redirect('customerHome')
    context = {'cusAddForm': cusAdd}
    return render(request, 'customer/customerAdd.html', context)


@login_required(login_url="homepage")
def customerDelete(request, pk):
    custDelete = Customer.objects.get(id=pk)
    custDelete.delete()
    messages.success(request, 'Customer Destroy Successfully')
    return redirect("customerHome")


@login_required(login_url="homepage")
def customerUpdate(request, pk):
    custUpdate = Customer.objects.get(id=pk)
    form = CustomerAddForm(instance=custUpdate)
    if request.method == 'POST':
        form = CustomerAddForm(request.POST, instance=custUpdate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer Update Successfully')
            return redirect('customerHome')
    context = {'updateForm': form, 'customer_Update': custUpdate}
    return render(request, 'customer/customerUpdate.html', context)
