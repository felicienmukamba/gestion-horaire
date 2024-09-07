from facultes.models import Faculte, Departement,Facultaire
from django.contrib.auth.models import Group
from postes.models import Commenter
from postes.models import Poste
from cours.models import Cours, Attribuer, Dispenser
from anneeAcademiques.models import AnneeAcademique
from salles.models import Salle
from promotions.models import Promotion
from users.models import Etudiant, Enseignant, Disponibilite
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "login", "password", "fonction"]
        read_only_fields = ["fonction"]

    def validate(self, data):
        password = data.get("password")
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)
            raise exceptions.ValidationError(
                {"password": serializer_errors["non_field_errors"]}
            )
        return data


class UserSerialiser(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "login", "fonction", "password", "groups"]
        read_only_fields = ["login", "password"]

    def get_groups(self, obj):
        if obj.is_superuser:
            groups = ["all"]
        else:
            groups = [group.name for group in obj.groups.all()]
        return groups

class UserSerialiser(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "login", "fonction", "groups"]
        read_only_fields = ["login","fonction"]

    def get_groups(self, obj):
        if obj.is_superuser:
            groups = ["all"]
        else:
            groups = [group.name for group in obj.groups.all()]
        return groups


class UserChangeFunction(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "fonction", "groups"]


class UserChangePasswordSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "login", "fonction", "password"]
        read_only_fields = ["fonction", "login"]

    def validate(self, data):
        password = data.get("password")
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)
            raise exceptions.ValidationError(
                {"password": serializer_errors["non_field_errors"]}
            )
        return data


class EtudiantCreateSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = [
            "id",
            "matricule",
            "nom",
            "postnom",
            "prenom",
            "sexe",
            "telephone",
            "login",
            "password",
            "fonction",
            "promotion",
            "departement"
        ]
        read_only_fields = ["login", "password", "fonction"]

class EtudiantSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = [
            "id",
            "matricule",
            "nom",
            "postnom",
            "prenom",
            "sexe",
            "telephone",
            "login",
            "password",
            "fonction",
            "promotion",
            "departement"
        ]
        read_only_fields = ["login", "password", "fonction"]
        depth=1
        
class EnseignantSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Enseignant
        fields = [
            "id",
            "titreAcademique",
            "nom",
            "postnom",
            "prenom",
            "sexe",
            "login",
            "password",
            "fonction",
        ]
        read_only_fields = ["login", "password", "fonction"]


class PromotionSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ["id", "designation", "actif"]


class SalleSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = ["id", "designation"]


class PosteCreateSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Poste
        fields = ["id", "titre", "contenu", "image", "slug"]


class PosteListRetrieveSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Poste
        fields = ["id", "titre", "contenu", "image", "slug","date"]
        read_only_fields = ["slug","image"]
        


class CommentaireSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Commenter
        fields = ["id", "contenu", "poste", "user"]
        read_only_fields = ["slug","user","poste"]
    

class PosteSerialiser(serializers.ModelSerializer):
    commentaires=serializers.SerializerMethodField()
    class Meta:
        model = Poste
        fields = ["id", "titre", "contenu", "image", "slug","date","commentaires"]
        read_only_fields = ["slug","image","commentaires"]
        
    def get_commentaires(self, obj):
        commentaires=Commenter.objects.filter(poste=obj.id)
        commentaires_list=[]
        for commentaire in commentaires:
            user=User.objects.get(id=commentaire.user.id)
            commentaires_list.append({
                "id":commentaire.id,
                "contenu":commentaire.contenu,
                "user":{
                    "id":user.id,
                    "login":user.login
                },
                "date":commentaire.date
            })
        return commentaires_list

class CoursSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Cours
        fields = ["id", "designation"]



class AttributionListSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Attribuer
        fields = [
            "id",
            "cours",
            "anneeAcademique",
            "promotion",
            "departement",
            "enseignant",
            "nbreHeure",
        ]
        depth=1
class AttributionSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Attribuer
        fields = [
            "id",
            "cours",
            "anneeAcademique",
            "promotion",
            "departement",
            "enseignant",
            "nbreHeure",
        ]


class DispenserListSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Dispenser
        fields = [
            "id",
            "vacation",
            "prester",
            "cours",
            "anneeAcademique",
            "promotion",
            "departement",
            "salle",
            "date",
        ]
        depth=1
        
class DispenserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Dispenser
        fields = [
            "id",
            "vacation",
            "prester",
            "cours",
            "anneeAcademique",
            "promotion",
            "departement",
            "salle",
            "date",
        ]


class AnneeAcademiqueSerialiser(serializers.ModelSerializer):
    class Meta:
        model = AnneeAcademique
        fields = ["id", "designation"]


class FaculteSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Faculte
        fields = [
            "id",
            "designation",
        ]
        
class FacultaireSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Facultaire
        fields = [
            "id",
            "enseignant",
            "faculte",
            "actif",
        ]
        
class FacultaireListSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Facultaire
        fields = [
            "id",
            "enseignant",
            "faculte",
            "actif"
        ]
        depth=1
        


class DepartementSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Departement
        fields = [
            "id",
            "designation",
            "faculte"
        ]
        depth=1


class DepartementCreateSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Departement
        fields = [
            "id",
            "designation",
            "faculte"
        ]
        
class DisponibiliteSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Disponibilite
        fields = ["id", "vacation","enseignant", "date"]
        read_only_fields=["enseignant"]
        
class DisponibiliteListSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Disponibilite
        fields = ["id", "vacation","enseignant", "date"]
        read_only_fields=["enseignant"]
        depth=1
class HoraireSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Dispenser
        fields = ["vacation"]