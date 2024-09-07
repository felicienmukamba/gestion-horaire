from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from facultes.models import Departement, Facultaire, Faculte
from users.models import Enseignant

from .forms import FacultaireForm, FaculteForm, DepartementForm

# Faculte views.
def faculte_save(request):
    if request.method == 'POST':
        form = FaculteForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True,  'message': 'Ajout de du Faculte reussie!'}) 
    else:
        form = FaculteForm()
    return JsonResponse({'success': False,  'message': 'POST only supported!'}, 400) 

def faculte_delete(request, id):
    try:
        Faculte_on_database = Faculte.objects.get(pk=id) 
        Faculte_on_database.delete() 
        return JsonResponse({'success': True,  'message': 'Faculte supprimé avec succès!'}) 
    except Faculte.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Faculte non supprimé."}, status=404)

def faculte_edit(request,id ):
    faculte_to_edit = get_object_or_404(Faculte, pk=id)
    print(request.POST)
    if request.method == 'POST':
        designation = request.POST.get('designation') 
        faculte_to_edit.designation = designation
        faculte_to_edit.save()
        return JsonResponse({'success': True, 'message': "Faculte modifiée avec succès."})
    else:
        return JsonResponse({'success': False, 'message': "Une erreur est survenue. Veuillez corriger les champs du formulaire."})


# Facultaire cours views.
def facultaire_save(request):
    if request.method == 'POST':
        form = FacultaireForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True,  'message': 'facultaire de du cours reussie!'}) 
    else:
        form = FacultaireForm()
    return JsonResponse({'success': False,  'message': 'POST only supported!'}, 400) 

def facultaire_delete(request, id):
    try:
        facultaire_on_database = Facultaire.objects.get(pk=id) 
        facultaire_on_database.delete() 
        return JsonResponse({'success': True,  'message': 'facultaire supprimé avec succès!'}) 
    except Departement.DoesNotExist:
        return JsonResponse({'success': False, 'message': "facultaire non supprimé."}, status=404)
    
def facultaire_edit(request, id):
    facultaire_to_edit = get_object_or_404(Facultaire, pk=id)
    print(request.POST)
    if request.method == 'POST':
        faculte = request.POST.get('faculte')
        enseignant = request.POST.get('enseignant')
        facultaire = get_object_or_404(Facultaire, pk=request.POST.get('facultaire'))
        facultaire_to_edit.enseignant = enseignant
        facultaire_to_edit.faculte = faculte
        facultaire_to_edit.facultaire = facultaire
        facultaire_to_edit.save()
        return JsonResponse({'success': True, 'message': "facultaire cours modifiée avec succès."})
    else:
        return JsonResponse({'success': False, 'message': "Une erreur est survenue. Veuillez corriger les champs du formulaire."})



# Departement cours views.
def departement_save(request):
    if request.method == 'POST':
        form = DepartementForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True,  'message': 'Departement de du cours reussie!'}) 
    else:
        form = DepartementForm()
    return JsonResponse({'success': False,  'message': 'POST only supported!'}, 400) 

def departement_delete(request, id):
    try:
        departement_on_database = Departement.objects.get(pk=id) 
        departement_on_database.delete() 
        return JsonResponse({'success': True,  'message': 'departement supprimé avec succès!'}) 
    except Departement.DoesNotExist:
        return JsonResponse({'success': False, 'message': "departement non supprimé."}, status=404)
    
def departement_edit(request, id):
    departement_to_edit = get_object_or_404(Departement, pk=id)
    print(request.POST)
    if request.method == 'POST':
        designation = request.POST.get('designation')
        faculte = get_object_or_404(Faculte, pk=request.POST.get('faculte'))
        departement_to_edit.designation = designation
        departement_to_edit.faculte = faculte
        departement_to_edit.save()
        return JsonResponse({'success': True, 'message': "Departement cours modifiée avec succès."})
    else:
        return JsonResponse({'success': False, 'message': "Une erreur est survenue. Veuillez corriger les champs du formulaire."})


def faculte_list(request):
    context = {
        'facultes': Faculte.objects.all(),
    }

    return render(request, 'facultes/list.html', context)


def departement_list(request):
    context = {
        'departements': Departement.objects.all(),
        'facultes': Faculte.objects.all(),
    }

    return render(request, 'facultes/departement/list.html', context)


def facultaire_list(request):
    context = {
        'facultes': Faculte.objects.all(),
        'facultaires': Facultaire.objects.all(),
        'enseignants': Enseignant.objects.all(),
    }

    return render(request, 'facultes/facultaire/list.html', context)
