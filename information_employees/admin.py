from django.contrib import admin

from .models import Contrat, Departement, Employe


@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ("nom", "responsable", "nombre_employes", "date_creation")
    search_fields = ("nom", "responsable")

    def nombre_employes(self, obj):
        return obj.employes.count()


class ContratInline(admin.TabularInline):
    model = Contrat
    extra = 0
    fields = ("type_contrat", "date_debut", "date_fin", "salaire", "actif")


@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = (
        "matricule",
        "nom_complet",
        "poste",
        "departement",
        "date_embauche",
        "situation",
    )
    list_filter = ("departement", "situation", "genre")
    search_fields = ("matricule", "prenom", "nom", "email", "poste")
    inlines = [ContratInline]


@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    list_display = (
        "employe",
        "type_contrat",
        "date_debut",
        "date_fin",
        "salaire",
        "actif",
    )
    list_filter = ("type_contrat", "actif", "date_debut")
    search_fields = ("employe__prenom", "employe__nom", "employe__matricule")
