from django.contrib import admin

from facultes.models import Departement, Facultaire, Faculte

# Register your models here.
admin.site.register(Faculte)
admin.site.register(Facultaire)
admin.site.register(Departement)
