from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO
from django.forms.models import model_to_dict

from inventory.models import TotalInventory
from .models import SalesPlanning, PerformaInvoice, SaleOrder
from settings.models import Branch
from .forms import PlanningForm, PerformaBasicForm, SalesOrderForm


# Create your views here.
# Sales Planning Views
@login_required(login_url="homepage")
def salesPlanning(request):
    planData = SalesPlanning.objects.all()
    context = {'planData': planData}
    return render(request, 'sales/planning/salesPlanning.html', context)


@login_required(login_url="homepage")
def salesPlanningAdd(request):
    planning = PlanningForm()
    if request.method == 'POST':
        form = PlanningForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Planning Added Successfully')
            return redirect('salesPlanning')
    context = {'planning': planning}
    return render(request, 'sales/planning/salesPlanningAdd.html', context)


@login_required(login_url="homepage")
def salesPlanningUpdate(request, pk):
    sp_Update = SalesPlanning.objects.get(id=pk)
    form = PlanningForm(instance=sp_Update)
    print(form.instance.pk)
    if request.method == 'POST':
        form = PlanningForm(request.POST, instance=sp_Update)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sale Plan Updated Successfully')
            return redirect('salesPlanning')
    context = {'updateForm': form, 'raw_Update': sp_Update}
    return render(request, 'sales/planning/salesPlanningUpdate.html', context)
    

@login_required(login_url="homepage")
def salesPlanningDelete(request, pk):
    spDelete = SalesPlanning.objects.get(id=pk)
    spDelete.delete()
    messages.success(request, 'Sales Plan Destroy Successfully')
    return redirect("salesPlanning")

#convert to pdf    
@login_required(login_url="homepage")
def salesPlanningPDF(request, pk):
    sp_Update = SalesPlanning.objects.get(id=pk)
    data = model_to_dict(sp_Update)
    pdf = render_to_pdf('sales/planning/pdf_template.html', data)
    return HttpResponse(pdf, content_type = 'application/pdf')

# Ajax Function
def fetchSales(request):
    branch = request.GET.get('branchData')
    branch_name_extract = Branch.objects.filter(id=branch)
    branch_name = ''
    for i in branch_name_extract:
        branch_name = i
    item = TotalInventory.objects.filter(select_branch=branch_name)
    context = {'item': item}
    return render(request, 'sales/planning/dependent/branch_dropdown.html', context)


def fetchQuantity(request):
    itemID = request.GET.get('itemData')
    item = TotalInventory.objects.filter(id=itemID)
    context = {'item': item}
    return render(request, 'sales/planning/dependent/qt_fetch.html', context)


def fetchReserved(request):
    itemID = request.GET.get('reservedQt')
    item = TotalInventory.objects.filter(id=itemID)
    context = {'item': item}
    return render(request, 'sales/planning/dependent/rt_fetch.html', context)


def fetchAvailable(request):
    itemID = request.GET.get('availableQt')
    item = TotalInventory.objects.filter(id=itemID)
    context = {'item': item}
    return render(request, 'sales/planning/dependent/av_fetch.html', context)

    # Performa Invoice Views


@login_required(login_url="homepage")
def performaInvoice(request):
    piData = PerformaInvoice.objects.all()
    context = {'piData': piData}
    return render(request, 'sales/performa/performaInvoice.html', context)


@login_required(login_url="homepage")
def performaInvoiceAdd(request):
    form = PerformaBasicForm(request.POST or None)
    print(form)
    context = {
        "basic": form
    }
    if form.is_valid():
        form.save()
        messages.success(request, "PI Created Successfully")
        return redirect("performaInvoice")
    return render(request, 'sales/performa/performaInvoiceAdd.html', context)


@login_required(login_url="homepage")
def performaInvoiceUpdate(request, pk):
    pi_Update = PerformaInvoice.objects.get(id=pk)
    form = PerformaBasicForm(instance=pi_Update)
    print(form.instance.pk)
    if request.method == 'POST':
        form = PerformaBasicForm(request.POST, instance=pi_Update)
        if form.is_valid():
            form.save()
            messages.success(request, 'Performa Invoice Updated Successfully')
            return redirect('performaInvoice')
    context = {'updateForm': form, 'raw_Update': pi_Update}
    return render(request, 'sales/performa/performaInvoiceUpdate.html', context)


@login_required(login_url="homepage")
def performaInvoiceDelete(request, pk):
    piData = PerformaInvoice.objects.get(id=pk)
    piData.delete()
    messages.success(request, 'PI Deleted Successfully')
    return redirect('performaInvoice')

#convert to pdf    
@login_required(login_url="homepage")
def performaInvoicePDF(request, pk):
    pi_Update = PerformaInvoice.objects.get(id=pk)
    data = model_to_dict(pi_Update)
    data['product'] = str(pi_Update.product)
    data['selectCustomer'] = str(pi_Update.selectCustomer)
    data['select_branch'] = str(pi_Update.select_branch)
    pdf = render_to_pdf('sales/performa/performaInvoicepdf.html', data)
    return HttpResponse(pdf, content_type = 'application/pdf')


@login_required(login_url="homepage")
def salesOrder(request):
    orderData = SaleOrder.objects.all()
    context = {'orderData': orderData}
    return render(request, 'sales/order/salesOrder.html', context)


@login_required(login_url="homepage")
def salesOrderAdd(request):
    order = SalesOrderForm()
    if request.method == 'POST':
        form = SalesOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order Added Successfully')
            return redirect('salesOrder')
    context = {"order": order}
    return render(request, 'sales/order/salesOrderAdd.html', context)


@login_required(login_url="homepage")
def salesOrderUpdate(request, pk):
    so_Update = SaleOrder.objects.get(id= pk)
    form = SalesOrderForm(instance = so_Update)
    print(form.instance.pk)
    if request.method == "POST":
        form = SalesOrderForm(request.POST, instance= so_Update)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sale Order Updated Successfully')
            return redirect('salesOrder')
    context = {"orderForm": form, 'raw_Update': so_Update}
    return render(request, 'sales/order/salesOrderUpdate.html', context)


@login_required(login_url="homepage")
def salesOrderDelete(request, pk):
    soDelete = SaleOrder.objects.get(id= pk)
    soDelete.delete()
    messages.success(request, 'Sales Order Destroy Successfully')
    return redirect('salesOrder')

#convert to pdf    
@login_required(login_url="homepage")
def salesOrderPDF(request, pk):
    so_Update = SaleOrder.objects.get(id=pk)
    data = model_to_dict(so_Update)
    print(so_Update.piRef)
    data['piRef'] = str(so_Update.piRef)
    data['selectCustomer'] = str(so_Update.selectCustomer)
    data['loadingFrom'] = str(so_Update.loadingFrom)
    data['product'] = str(so_Update.product)
    pdf = render_to_pdf('sales/order/salesOrderpdf.html', data)
    return HttpResponse(pdf, content_type = 'application/pdf')


#convert to pdf helper function
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src) 
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None