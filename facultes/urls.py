from django.urls import path, include
from . import views
from django.conf.urls.static import static 
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    # faculte urls
    path("faculte/", views.faculte_list, name="faculte-list"),
    path("faculte-add/", views.faculte_save, name="faculte-add"),
    path("faculte-delete/<int:id>/", views.faculte_delete, name="faculte-delete"),
    path("faculte-edit/<int:id>/", views.faculte_edit, name="faculte-edit"),

    # facultaire urls
    path("facultaire/", views.facultaire_list, name="facultaire-list"),
    path("facultaire-add/", views.facultaire_save, name="facultaire-add"),
    path("facultaire-delete/<int:id>/", views.facultaire_edit, name="facultaire-delete"),
    path("facultaire-edit/<int:id>/", views.facultaire_delete, name="facultaire-edit"),

    # departement urls
    path("departement/", views.departement_list, name="departement-list"),
    path("departement-add/", views.departement_save, name="departement-add"),
    path("departement-delete/<int:id>/", views.departement_delete, name="departement-delete"),
    path("departement-edit/<int:id>/", views.departement_edit, name="departement-edit"),
]