from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("", include("cours.urls")),
    path("", include("promotions.urls")),
    path("", include("facultes.urls")),
    path("", include("salles.urls")),
    path("horaires", Horaire.as_view(), name="horaire-list"),
    path("horaires/now", HoraireWeek.as_view()),
    path("", include("anneeAcademiques.urls")),
    path("", include("users.urls")),
    path("dashbord/", DashbordView.as_view(), name="dashbord")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
