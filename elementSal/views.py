from django.shortcuts import get_object_or_404, redirect, render
#from elementSal.forms import ElementsalaireForm
from elementSal.models import Elementsalaire


def index(request):
    elementsalaires=Elementsalaire.objects.all()
    return render(request, 'elementSalaire/list.html',{'elementsalaires':elementsalaires})


def update_create(request, id):
    if id<1:
        element = Elementsalaire()
    else:
        element = Elementsalaire.objects.get(id=id)
    
    if request.method=="POST":
        element.intitule_element=request.POST.get('intitule_element')
        element.description=request.POST.get('description')
        element.save()
        return redirect('listElementsalaire')
    return render(request, 'elementSalaire/formulaire.html',{'element': element,'id':id})



def destroy(request,id):
    elementsalaire=Elementsalaire.objects.get(id=id)
    elementsalaire.delete()
    return redirect("listElementsalaire")

def elmt_sal(request):
    intitule_element_sals=Elementsalaire.objects.get('intitule_element')
    return render(request, 'element_salaire_contrat/ajout_element_sal_contrat.html',
        {'intitule_elemenst':intitule_element_sals})  

