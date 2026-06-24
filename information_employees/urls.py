from django.urls import path

from . import views


urlpatterns = [
    path("", views.VueTableauDeBord.as_view(), name="tableau_de_bord"),
    path("employes/", views.VueListeEmployes.as_view(), name="employe_list"),
    path("employes/ajouter/", views.VueCreationEmploye.as_view(), name="employe_create"),
    path("employes/<int:pk>/", views.VueDetailEmploye.as_view(), name="employe_detail"),
    path("employes/<int:pk>/modifier/", views.VueModificationEmploye.as_view(), name="employe_update"),
    path("employes/<int:pk>/supprimer/", views.VueSuppressionEmploye.as_view(), name="employe_delete"),
    path("departements/", views.VueListeDepartements.as_view(), name="departement_list"),
    path("departements/ajouter/", views.VueCreationDepartement.as_view(), name="departement_create"),
    path("departements/<int:pk>/modifier/", views.VueModificationDepartement.as_view(), name="departement_update",
    ),
    path("departements/<int:pk>/supprimer/", views.VueSuppressionDepartement.as_view(), name="departement_delete"),
    path("contrats/", views.VueListeContrats.as_view(), name="contrat_list"),
    path("contrats/ajouter/", views.VueCreationContrat.as_view(), name="contrat_create"),
    path(
        "contrats/<int:pk>/modifier/",
        views.VueModificationContrat.as_view(),
        name="contrat_update",
    ),
    path(
        "contrats/<int:pk>/supprimer/",
        views.VueSuppressionContrat.as_view(),
        name="contrat_delete",
    ),
]
