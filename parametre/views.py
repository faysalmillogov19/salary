from django.shortcuts import redirect, render
from parametre.form import TarifHeureSupForm
from parametre.models import*



def indexTaxe(request):
   taxe =Taxe.objects.all()
   return render(request, 'taxe/list.html',{'taxe':taxe})


def update_createTaxe(request, id):
    if id<1:
        taxe = Taxe()
    else:
        taxe = Taxe.objects.get(id=id)
    
    if request.method=="POST":
        taxe.libelle=request.POST.get('libelle')
        taxe.description=request.POST.get('description')
        taxe.save()
        return redirect('listTaxe')
    return render(request, 'taxe/formulaire.html',{'taxe': taxe,'id':id})



def destroyTaxe(request,id):
    taxe=Taxe.objects.get(id=id)
    taxe.delete()
    return redirect("listTaxe")

def indexJourFerie(request):
    jourFerier =JourFerier.objects.all()
    return render(request, 'jourFerier/list.html',{'jourFerier':jourFerier})


def update_createJourFerier(request, id):
    if id<1:
        jourFerier = JourFerier()
    else:
        jourFerier = JourFerier.objects.get(id=id)
    
    if request.method=="POST":
        jourFerier.libelle=request.POST.get('libelle')
        jourFerier.date=request.POST.get('date')
        jourFerier.description=request.POST.get('description')
        jourFerier.save()
        return redirect('listjourFerie')
    return render(request, 'jourFerier/formulaire.html',{'jourFerier': jourFerier,'id':id})


def destroyJourFerier(request,id):
    jourFerier=JourFerier.objects.get(id=id)
    jourFerier.delete()
    return redirect("listjourFerie")


def indexTarifHeureSup(request):
    tarifHeureSup =TarifHeureSup.objects.all()
    return render(request, 'tarifHeure/list.html',{'tarifHeureSup':tarifHeureSup})


def update_createTarifHeureSup(request, id):
    if id<1:
        tarifHeureSup = TarifHeureSup()
    else:
        tarifHeureSup = TarifHeureSup.objects.get(id=id)
    
    if request.method == "POST":
        form = TarifHeureSupForm(request.POST, instance=tarifHeureSup)
        if form.is_valid():
            form.save()
            return redirect('listTarifHeureSup')
    else:
        form = TarifHeureSupForm(instance=tarifHeureSup)
    return render(request, 'tarifHeure/formulaire.html',{'form': form,'id':id})


def destroyTarifHeureSup(request,id):
    tarifHeureSup=TarifHeureSup.objects.get(id=id)
    tarifHeureSup.delete()
    return redirect("listTarifHeureSup")


def indexNuit(request):
    nuit =Nuit.objects.all()
    return render(request, 'elementSalaire/list.html',{'nuit':nuit})


def update_createNuit(request, id):
    if id<1:
        nuit = Nuit()
    else:
        nuit = Nuit.objects.get(id=id)
    
    if request.method=="POST":
        nuit.est_nuit=request.POST.get('est_nuit')
        nuit.save()
        return redirect('listElementsalaire')
    return render(request, 'elementSalaire/formulaire.html',{'nuit': nuit,'id':id})


def destroyNuit(request,id):
    nuit=Nuit.objects.get(id=id)
    nuit.delete()
    return redirect("listElementsalaire")






    

