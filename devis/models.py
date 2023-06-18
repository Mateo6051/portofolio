from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
# Create your models here.


class Tache(models.Model):
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    duree = models.IntegerField('Durée en jours')
    devis = models.ForeignKey(
        'Devis', on_delete=models.CASCADE, related_name='taches', null=True, blank=True)

    def __str__(self):
        return self.description

    @ property
    def prix_ht(self):
        return self.prix * self.duree


class Client(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, null=True, blank=True)
    telephone = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.CharField(max_length=50)
    code_postal = models.CharField(max_length=50)
    ville = models.CharField(max_length=50)

    def __str__(self):
        return self.nom + ' ' + self.prenom


class Devis(models.Model):
    numero = models.CharField(max_length=50, editable=False)
    titre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.numero

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        return super(Devis, self).save(*args, **kwargs)

    @ property
    def total_time(self):
        return sum([t.duree for t in self.taches.all()])

    @ property
    def total_price(self):
        return sum([t.prix_ht for t in self.taches.all()])


@receiver(post_save, sender=Devis)
def set_devis_number(sender, instance, created, **kwargs):
    numero = instance.numero
    if len(numero) == 0:
        numero = timezone.now().strftime("%Y%m%d") + str(instance.pk)
    Devis.objects.filter(pk=instance.pk).update(numero=numero)
