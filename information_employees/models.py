from django.db import models
from django.core.exceptions import ValidationError


class Departement(models.Model):
    nom = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    responsable = models.CharField(max_length=150, blank=True)
    date_creation = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["nom"]
        verbose_name = "departement"
        verbose_name_plural = "departements"

    def __str__(self):
        return self.nom


class Employe(models.Model):
    GENRE_CHOICES = [
        ("F", "Femme"),
        ("M", "Homme"),
        ("A", "Autre"),
    ]

    SITUATION_CHOICES = [
        ("actif", "Actif"),
        ("conge", "En conge"),
        ("suspendu", "Suspendu"),
        ("sorti", "Sorti"),
    ]

    matricule = models.CharField(max_length=30, unique=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    date_naissance = models.DateField(null=True, blank=True)
    adresse = models.TextField(blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    poste = models.CharField(max_length=150)
    departement = models.ForeignKey(
        Departement,
        on_delete=models.PROTECT,
        related_name="employes",
    )
    date_embauche = models.DateField()
    situation = models.CharField(
        max_length=20,
        choices=SITUATION_CHOICES,
        default="actif",
    )
    notes = models.TextField(blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nom", "prenom"]
        verbose_name = "employe"
        verbose_name_plural = "employes"

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.matricule})"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class Contrat(models.Model):
    TYPE_CHOICES = [
        ("cdi", "CDI"),
        ("cdd", "CDD"),
        ("stage", "Stage"),
        ("prestation", "Prestation"),
        ("consultance", "Consultance"),
    ]

    employe = models.ForeignKey(
        Employe,
        on_delete=models.CASCADE,
        related_name="contrats",
    )
    type_contrat = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    salaire = models.DecimalField(max_digits=12, decimal_places=2)
    actif = models.BooleanField(default=True)
    fichier_reference = models.CharField(max_length=120, blank=True)
    observations = models.TextField(blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_debut"]
        verbose_name = "contrat"
        verbose_name_plural = "contrats"

    def __str__(self):
        return f"{self.get_type_contrat_display()} - {self.employe.nom_complet}"

    def clean(self):
        if self.date_fin and self.date_fin < self.date_debut:
            raise ValidationError(
                {"date_fin": "La date de fin doit etre posterieure a la date de debut."}
            )
