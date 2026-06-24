from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Contrat, Departement, Employe


class DateInput(forms.DateInput):
    input_type = "date"


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check-input")
            else:
                widget.attrs.setdefault("class", "form-control form-control-sm")


class DepartementForm(StyledModelForm):
    class Meta:
        model = Departement
        fields = ["nom", "responsable", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class EmployeForm(StyledModelForm):
    class Meta:
        model = Employe
        fields = [
            "matricule",
            "prenom",
            "nom",
            "genre",
            "date_naissance",
            "adresse",
            "telephone",
            "email",
            "poste",
            "departement",
            "date_embauche",
            "situation",
            "notes",
        ]
        widgets = {
            "date_naissance": DateInput(),
            "date_embauche": DateInput(),
            "adresse": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class ContratForm(StyledModelForm):
    class Meta:
        model = Contrat
        fields = [
            "employe",
            "type_contrat",
            "date_debut",
            "date_fin",
            "salaire",
            "actif",
            "fichier_reference",
            "observations",
        ]
        widgets = {
            "date_debut": DateInput(),
            "date_fin": DateInput(),
            "observations": forms.Textarea(attrs={"rows": 3}),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check-input")
            else:
                widget.attrs.setdefault("class", "form-control form-control-sm")
            widget.attrs.setdefault("placeholder", field.label)
