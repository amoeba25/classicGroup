from multiprocessing import context
from django.shortcuts import render, redirect
from .forms import BatchForm, ProductionForm
from .models import ProductionPlant, Batch
from django.forms import inlineformset_factory, modelformset_factory


# plant data view
def viewPlant(request):
    plantData = ProductionPlant.objects.all()
    context = {'plantData': plantData}
    return render(request, 'production/production.html', context)

def ProductionAdd(request):
    context = {}
    plant_form = ProductionForm()
    Batchmodel = modelformset_factory(Batch,
                                    fields=('batch_no','start_time', 'end_time', 'drum_fill', 'batch_hours', 'total_time'), extra= 1)
    batch_form = Batchmodel(queryset=Batch.objects.none())
    
    print(plant_form.errors)
    print(batch_form.errors)
    if request.method == "POST":
        if plant_form.is_valid() and batch_form.is_valid():
            print("this part??")
            parent = plant_form.save(commit= False)
            for form in batch_form:
                child = form.save(commit= False)
                child.production_plant = parent
                child.save()
            return redirect('ProductionPlant')
    context['plantForm'] = plant_form
    context['batchForm'] = batch_form
    return render(request, "production/productionAdd.html", context)

def ProductionDelete(request):
    simpleForm = ProductionForm()
    BatchFormSet = inlineformset_factory(ProductionPlant, Batch, fields=('batch_no','start_time', 'end_time', 'drum_fill', 'batch_hours', 'total_time'), extra= 0)
    formset = BatchFormSet(queryset=Batch.objects.none())
    print(formset)
    if request.method == "POST":
        pass
    context = {"simple_form": simpleForm, "form":formset}
    return render(request, "production/productionAdd.html", context)
    

def ProductionUpdate(request):
    pass