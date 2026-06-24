from django.db.models import Count, Q
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import ContratForm, DepartementForm, EmployeForm, SignUpForm
from .models import Contrat, Departement, Employe


class ContexteModeleMixin:
    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte["model_verbose_name"] = self.model._meta.verbose_name
        contexte["model_name"] = self.model._meta.model_name
        return contexte


class VueConnexionPersonnalisee(LoginView):
    template_name = "information_employees/login.html"

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte["register_form"] = SignUpForm()
        contexte["login_form"] = contexte.get("form")
        return contexte


class VueInscription(FormView):
    template_name = "information_employees/login.html"
    form_class = SignUpForm
    success_url = reverse_lazy("tableau_de_bord")

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte["register_form"] = contexte.get("form")
        contexte["login_form"] = AuthenticationForm(self.request)
        return contexte

    def form_valid(self, formulaire):
        utilisateur = formulaire.save()
        login(self.request, utilisateur)
        return super().form_valid(formulaire)


class VueTableauDeBord(TemplateView):
    template_name = "information_employees/tableau_de_bord.html"

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte["total_employes"] = Employe.objects.count()
        contexte["total_departements"] = Departement.objects.count()
        contexte["contrats_actifs"] = Contrat.objects.filter(actif=True).count()
        contexte["employes_recents"] = Employe.objects.select_related("departement")[:5]
        contexte["departements"] = Departement.objects.annotate(
            total_employes=Count("employes")
        )
        return contexte


class VueListeEmployes(ListView):
    model = Employe
    template_name = "information_employees/employe_list.html"
    context_object_name = "employes"
    paginate_by = 10

    def get_queryset(self):
        employes = Employe.objects.select_related("departement")
        recherche = self.request.GET.get("q", "").strip()
        departement = self.request.GET.get("departement", "").strip()

        if recherche:
            employes = employes.filter(
                Q(matricule__icontains=recherche)
                | Q(prenom__icontains=recherche)
                | Q(nom__icontains=recherche)
                | Q(email__icontains=recherche)
                | Q(poste__icontains=recherche)
            )
        if departement:
            employes = employes.filter(departement_id=departement)
        return employes

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte["departements"] = Departement.objects.all()
        contexte["q"] = self.request.GET.get("q", "")
        contexte["departement_selectionne"] = self.request.GET.get("departement", "")
        return contexte


class VueDetailEmploye(DetailView):
    model = Employe
    template_name = "information_employees/employe_detail.html"
    context_object_name = "employe"

    def get_queryset(self):
        return Employe.objects.select_related("departement").prefetch_related("contrats")


class VueCreationEmploye(ContexteModeleMixin, CreateView):
    model = Employe
    form_class = EmployeForm
    template_name = "information_employees/formulaire.html"
    success_url = reverse_lazy("employe_list")


class VueModificationEmploye(ContexteModeleMixin, UpdateView):
    model = Employe
    form_class = EmployeForm
    template_name = "information_employees/formulaire.html"
    success_url = reverse_lazy("employe_list")


class VueSuppressionEmploye(DeleteView):
    model = Employe
    template_name = "information_employees/confirmation_suppression.html"
    success_url = reverse_lazy("employe_list")


class VueListeDepartements(ListView):
    model = Departement
    template_name = "information_employees/departement_list.html"
    context_object_name = "departements"

    def get_queryset(self):
        return Departement.objects.annotate(total_employes=Count("employes"))


class VueCreationDepartement(ContexteModeleMixin, CreateView):
    model = Departement
    form_class = DepartementForm
    template_name = "information_employees/formulaire.html"
    success_url = reverse_lazy("departement_list")


class VueModificationDepartement(ContexteModeleMixin, UpdateView):
    model = Departement
    form_class = DepartementForm
    template_name = "information_employees/formulaire.html"
    success_url = reverse_lazy("departement_list")


class VueSuppressionDepartement(DeleteView):
    model = Departement
    template_name = "information_employees/confirmation_suppression.html"
    success_url = reverse_lazy("departement_list")


class VueListeContrats(ListView):
    model = Contrat
    template_name = "information_employees/contrat_list.html"
    context_object_name = "contrats"

    def get_queryset(self):
        return Contrat.objects.select_related("employe", "employe__departement")

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte["contrats_actifs"] = Contrat.objects.filter(actif=True).count()
        contexte["contrats_inactifs"] = Contrat.objects.filter(actif=False).count()
        return contexte


class VueCreationContrat(ContexteModeleMixin, CreateView):
    model = Contrat
    form_class = ContratForm
    template_name = "information_employees/formulaire.html"
    success_url = reverse_lazy("contrat_list")


class VueModificationContrat(ContexteModeleMixin, UpdateView):
    model = Contrat
    form_class = ContratForm
    template_name = "information_employees/formulaire.html"
    success_url = reverse_lazy("contrat_list")


class VueSuppressionContrat(DeleteView):
    model = Contrat
    template_name = "information_employees/confirmation_suppression.html"
    success_url = reverse_lazy("contrat_list")
