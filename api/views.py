# Persmision
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.parsers import MultiPartParser, FormParser

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import Response, APIView
from django.utils import timezone
from django.db.models import Q
from .serializers import *
from slugify import slugify
from .Horaire import PDF
from .Horaire import firstDay, lastDay
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
import os
from django.conf import settings
# Create your views here.

# Securiser les requêtes GET sur autorisation


class PermissionsOnly(DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


def makeHoraire():
    anneeAcademique_now = AnneeAcademique.objects.all().order_by('-id')
    if anneeAcademique_now.exists():
        anneeAcademique_now = anneeAcademique_now[0]
        horaires = Dispenser.objects.filter(
            anneeAcademique=anneeAcademique_now).order_by('-date')
        if horaires.exists():
            vacations = ['Jour', 'Soir']
            path = []
            for vacation in vacations:
                promotions = Promotion.objects.filter(
                    actif=True).order_by('designation')
                departements = Departement.objects.all().order_by('designation')
                horaire = PDF(Dispenser, Attribuer, departements, promotions, Enseignant,
                              Cours, Salle, anneeAcademique_now.id, vacation, 'L', 'mm', 'Letter')
                horaire.set_title("HORAIRE DE LA SEMAINE")
                horaire.set_author('UNIC - BUKAVU')
                horaire.alias_nb_pages()
                horaire.add_page()
                horaire.set_auto_page_break(auto=True, margin=5)
                horaire.body()
                media_path = os.path.join(
                    settings.MEDIA_ROOT, f'horaire_{vacation}.pdf')
                horaire.output(media_path)
                path.append(media_path)
            return path
        return False
    return False


class Horaire(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pdf_writer = PdfWriter()
        rs = makeHoraire()
        if rs:
            for path in rs:
                pdf = PdfReader(path)
                for i in range(len(pdf.pages)):
                    page = pdf.pages[i]
                    pdf_writer.add_page(page)
            pdf_writer.write('media/horaires.pdf')
            return Response({"success": request.build_absolute_uri('/media/horaires.pdf')}, status=status.HTTP_201_CREATED)
        return Response({"fail": "Pas d'année academique disponible ou pas d'horaire élaborée"}, status=status.HTTP_204_NO_CONTENT)


class HoraireWeek(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DispenserListSerialiser

    def get(self, request):
        now = timezone.now().date()
        horaires = Dispenser.objects.filter(
            Q(date__lte=lastDay(now)) & Q(date__gte=firstDay(now)))
        return Response(self.serializer_class(horaires, many=True).data, status=status.HTTP_200_OK)


class UserCreate(generics.CreateAPIView):
    serializer_class = UserCreateSerialiser
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            login = serializer.data.get("login")
            fonction = "Internaute"
            password = serializer.data.get("password")
            user = User.objects.filter(login=login)
            if not user.exists():
                user = User.objects.create_user(
                    login=login, password=password, fonction=fonction
                )
                user.save()
                return Response(
                    self.serializer_class( 
                        user).data, status=status.HTTP_201_CREATED
                )
            return Response({"message": "Pseudo existant"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = UserSerialiser
    queryset = User.objects.filter(is_superuser=False)


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = UserSerialiser
    queryset = User.objects.all()


class UserChangeFunction(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = UserSerialiser
    queryset = User.objects.all()

    def put(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(id=pk)
            if user.exists():
                user = user[0]
                admin = Group.objects.get(name='Admin')
                if user.fonction == "Admin":
                    user.groups.remove(admin)
                    if user.groups.count() > 0:
                        group = user.groups.filter(name='Facultaire')
                        if group.exists():
                            user.fonction = 'Facultaire'
                        else:
                            user.fonction = 'Enseignant'
                    else:
                        user.fonction = "Internaute"
                else:
                    user.groups.add(admin)
                    user.fonction = 'Admin'
                user.save(update_fields=["fonction"])
                return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)
            return Response({"BAD REQUEST": "utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserChangePassword(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = UserChangePasswordSerialiser
    queryset = User.objects.all()

    def put(self, request, pk):
        user = User.objects.filter(id=pk)
        if user.exists():
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = user[0]
                user.set_password(serializer.data.get("password"))
                user.save()
                return Response(
                    self.serializer_class(user).data, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({}, status=status.HTTP_404_NOT_FOUND)


class AuthChangePassword(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerialiser
    queryset = User.objects.all()

    def put(self, request):
        user = User.objects.filter(id=request.user.id)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = user[0]
            user.set_password(serializer.data.get("password"))
            user.save()
            return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class Auth(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerialiser

    def get(self, request):
        user = request.user
        user = self.serializer_class(user)
        return Response(user.data, status=status.HTTP_200_OK)


class EtudiantList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = EtudiantSerialiser
    queryset = Etudiant.objects.all()


class EtudiantCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = EtudiantCreateSerialiser
    queryset = Etudiant.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            today = timezone.now()
            matricule = serializer.data.get("matricule")
            nom = serializer.data.get("nom")
            postnom = serializer.data.get("postnom")
            prenom = serializer.data.get("prenom")
            telephone = serializer.data.get("telephone")
            promotion = serializer.data.get("promotion")
            departement = serializer.data.get("departement")
            promotion = Promotion.objects.get(id=promotion)
            departement = Departement.objects.get(id=departement)
            login = serializer.data.get("telephone")
            sexe = serializer.data.get("sexe")
            password = serializer.data.get("matricule")
            fonction = "Etudiant"
            etudiant = Etudiant.objects.create(
                login=login,
                nom=nom,
                postnom=postnom,
                prenom=prenom,
                telephone=telephone,
                matricule=matricule,
                fonction=fonction,
                sexe=sexe,
                promotion=promotion,
                departement=departement
            )
            etudiant.set_password(password)
            etudiant.save()
            groupe = Group.objects.filter(name="Etudiant")
            if groupe.exists():
                etudiant.groups.add(groupe[0])
            return Response(
                self.serializer_class(
                    etudiant).data, status=status.HTTP_201_CREATED
            )
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class EtudiantDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = EtudiantCreateSerialiser
    queryset = Etudiant.objects.all()


class EnseignantCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = EnseignantSerialiser
    queryset = Enseignant.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            today = timezone.now()
            titreAcademique = serializer.data.get("titreAcademique")
            nom = serializer.data.get("nom")
            postnom = serializer.data.get("postnom")
            prenom = serializer.data.get("prenom")
            sexe = serializer.data.get("sexe")
            enseignant = Enseignant.objects.filter(nom=nom)
            if enseignant.exists():
                login = nom.lower() + str(enseignant.count())
            login = str(serializer.data.get("nom")).lower()
            password = (
                login.lower()
                + "@"
                + str(today.year)
                + "@"
                + str(today.month)
                + "@"
                + str(today.day)
            )
            fonction = "Enseignant"
            enseignant = Enseignant.objects.create(
                login=login,
                nom=nom,
                postnom=postnom,
                prenom=prenom,
                titreAcademique=titreAcademique,
                fonction=fonction,
                sexe=sexe,
            )
            enseignant.set_password(password)
            enseignant.save()
            group = Group.objects.get(name="Enseignant")
            enseignant.groups.add(group)
            return Response(
                self.serializer_class(
                    enseignant).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class EnseignantDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = EnseignantSerialiser
    queryset = Enseignant.objects.all()


class PromotionCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = PromotionSerialiser
    queryset = Promotion.objects.all()


class PromotionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = PromotionSerialiser
    queryset = Promotion.objects.all()


class FaculteCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = FaculteSerialiser
    queryset = Faculte.objects.all()


class FaculteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = FaculteSerialiser
    queryset = Faculte.objects.all()


class FacultaireCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = FacultaireSerialiser
    queryset = Facultaire.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            enseignant = serializer.data.get("enseignant")
            faculte = serializer.data.get("faculte")
            enseignant = Enseignant.objects.get(id=enseignant)
            faculte = Faculte.objects.get(id=faculte)
            factutaire = Facultaire.objects.create(
                enseignant=enseignant,
                faculte=faculte,
            )
            enseignant.fonction = "Facultaire"
            enseignant.save(update_fields=["fonction"])
            groupe = Group.objects.get(name="Facultaire")
            enseignant.groups.add(groupe)
            return Response(
                self.serializer_class(
                    factutaire).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class FacultaireList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = FacultaireListSerialiser
    queryset = Facultaire.objects.all()


class FacultaireDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = FacultaireSerialiser
    queryset = Facultaire.objects.all()

    def put(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            enseignant = serializer.data.get("enseignant")
            faculte = serializer.data.get("faculte")
            actif = serializer.data.get("actif")
            enseignant = Enseignant.objects.get(id=enseignant)
            faculte = Faculte.objects.get(id=faculte)
            factutaire = Facultaire.objects.get(id=pk)
            factutaire.enseignant = enseignant
            factutaire.faculte = faculte
            factutaire.actif = actif
            groupe = Group.objects.get(name="Facultaire")
            if not actif:
                enseignant.fonction = "Enseignant"
                enseignant.groups.remove(groupe)
            else:
                enseignant.fonction = "Facultaire"
                enseignant.groups.add(groupe)
            enseignant.save(update_fields=["fonction"])

            return Response(
                self.serializer_class(
                    factutaire).data, status=status.HTTP_202_ACCEPTED
            )
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class DepartementList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = DepartementSerialiser
    queryset = Departement.objects.all()


class DepartementCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = DepartementCreateSerialiser
    queryset = Departement.objects.all()


class DepartementDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = DepartementSerialiser
    queryset = Departement.objects.all()


class SalleCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = SalleSerialiser
    queryset = Salle.objects.all()


class SalleDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = SalleSerialiser
    queryset = Salle.objects.all()


class PosteCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    # parser_classes=[MultiPartParser,FormParser]
    # utile pour le APIView pour la prise en charge de fichier
    serializer_class = PosteCreateSerialiser
    queryset = Poste.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        image = request.data.get('image')

        if serializer.is_valid():
            titre = serializer.data.get("titre")
            contenu = serializer.data.get("contenu")
            slug = serializer.data.get("slug")
            poste = Poste.objects.filter(titre=titre)
            if poste.exists():
                slug = titre + " " + str(poste.count())
            poste = Poste.objects.create(
                titre=titre, contenu=contenu, image=image, slug=slugify(slug)
            )
            return Response(
                self.serializer_class(
                    poste).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class PosteList(generics.ListAPIView):
    serializer_class = PosteListRetrieveSerialiser
    queryset = Poste.objects.all()


class PosteDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = PosteSerialiser
    queryset = Poste.objects.all()


class PosteRetrieve(generics.RetrieveAPIView):
    serializer_class = PosteSerialiser
    queryset = Poste.objects.all()

    def get(self, request, slug):
        poste = Poste.objects.filter(slug=slug)
        if poste.exists():
            poste_data = self.serializer_class(poste[0]).data
            request_url = request.build_absolute_uri(poste_data['image'])
            poste_data['image'] = request_url
            return Response(poste_data, status=status.HTTP_200_OK)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


class PosteUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = PosteListRetrieveSerialiser
    queryset = Poste.objects.all()


class CommentaireCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentaireSerialiser
    queryset = Commenter.objects.all()

    def post(selft, request, slug):
        print(request.data)
        serializer = selft.serializer_class(data=request.data)
        if serializer.is_valid():
            contenu = serializer.data.get('contenu')
            poste = Poste.objects.filter(slug=slug)
            if poste.exists():
                commentaire = Commenter.objects.create(
                    poste=poste[0], contenu=contenu, user=request.user)
                return Response(selft.serializer_class(commentaire).data, status=status.HTTP_201_CREATED)
            return Response({"Bad Request": "Poste non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.error_messages, status=status.HTTP_406_NOT_ACCEPTABLE)


class CommentaireDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentaireSerialiser
    queryset = Commenter.objects.all()


class CoursCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = CoursSerialiser
    queryset = Cours.objects.all()


class CoursDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = CoursSerialiser
    queryset = Cours.objects.all()


class AttributionCoursList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = AttributionListSerialiser
    queryset = Attribuer.objects.all()

    def get(self, request):
        anneeAcademique = AnneeAcademique.objects.all().order_by('-id')
        if anneeAcademique.exists():
            if request.user.fonction == "Enseignant":
                enseignant = Enseignant.objects.get(id=request.user.id)
                disponibilites = Attribuer.objects.filter(
                    enseignant=enseignant, anneeAcademique=anneeAcademique[0].id)
            else:
                disponibilites = Attribuer.objects.filter(
                    anneeAcademique=anneeAcademique[0].id)
            return Response(self.serializer_class(disponibilites, many=True).data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_200_OK)


class AttributionCoursListNow(generics.ListAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = AttributionListSerialiser
    anneeAcademique = AnneeAcademique.objects.all().order_by('-id')
    if anneeAcademique.exists():
        queryset = Attribuer.objects.filter(
            anneeAcademique=anneeAcademique[0].id)
    queryset = Attribuer.objects.all()


class AttributionCoursCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = AttributionSerialiser
    queryset = Attribuer.objects.all()


class AttributionCoursDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = AttributionSerialiser
    queryset = Attribuer.objects.all()


class DispenserCoursListNow(generics.ListAPIView):
    # permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = DispenserListSerialiser
    anneeAcademique = AnneeAcademique.objects.all().order_by('-id')
    if anneeAcademique.exists():
        queryset = Dispenser.objects.filter(
            anneeAcademique=anneeAcademique[0].id)
    queryset = Dispenser.objects.all()


class DispenserCoursList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = DispenserListSerialiser
    queryset = Dispenser.objects.all()


class DispenserCoursCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = DispenserSerialiser
    queryset = Dispenser.objects.all()


class DispenserCoursDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = DispenserSerialiser
    queryset = Dispenser.objects.all()


class AnneeAcademiqueCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = AnneeAcademiqueSerialiser
    queryset = AnneeAcademique.objects.all()


class AnneeAcademiqueDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = AnneeAcademiqueSerialiser
    queryset = AnneeAcademique.objects.all()


class DisponibiliteCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = DisponibiliteSerialiser
    queryset = Disponibilite.objects.all()

    def get(self, request):
        self.serializer_class = DisponibiliteListSerialiser
        if request.user.fonction == "Enseignant":
            enseignant = Enseignant.objects.get(id=request.user.id)
            disponibilites = Disponibilite.objects.filter(
                enseignant=enseignant)
        else:
            disponibilites = Disponibilite.objects.all()
        return Response(self.serializer_class(disponibilites, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            vacation = serializer.data.get('vacation')
            enseignant = Enseignant.objects.get(id=request.user.id)
            date = serializer.data.get('date')
            disponibilite = Disponibilite.objects.create(
                vacation=vacation, enseignant=enseignant, date=date)
            disponibilite.save()
            return Response(self.serializer_class(disponibilite).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class DisponibiliteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, PermissionsOnly]
    serializer_class = DisponibiliteSerialiser
    queryset = Disponibilite.objects.all()

    def get(self, request, pk):
        enseignant = Enseignant.objects.get(id=request.user.id)
        disponibilite = Disponibilite.objects.filter(
            enseignant=enseignant, id=pk)
        return Response(self.serializer_class(disponibilite[0]).data, status=status.HTTP_200_OK)
