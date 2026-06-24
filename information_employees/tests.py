from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Contrat, Departement, Employe


class GestionRHTests(TestCase):
    def setUp(self):
        self.departement = Departement.objects.create(
            nom="Ressources humaines",
            responsable="Awa Diop",
        )
        self.employe = Employe.objects.create(
            matricule="EMP-001",
            prenom="Moussa",
            nom="Fall",
            genre="M",
            email="moussa.fall@example.com",
            poste="Charge RH",
            departement=self.departement,
            date_embauche=date(2026, 1, 10),
        )

    def test_tableau_de_bord_est_accessible(self):
        response = self.client.get(reverse("tableau_de_bord"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tableau de bord RH")

    def test_employe_est_lie_a_un_departement(self):
        self.assertEqual(self.employe.departement.nom, "Ressources humaines")
        self.assertEqual(self.departement.employes.count(), 1)

    def test_contrat_refuse_date_fin_avant_date_debut(self):
        contrat = Contrat(
            employe=self.employe,
            type_contrat="cdd",
            date_debut=date(2026, 6, 1),
            date_fin=date(2026, 5, 1),
            salaire=350000,
        )

        with self.assertRaises(ValidationError):
            contrat.full_clean()
