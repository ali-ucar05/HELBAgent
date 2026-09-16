from django.db import models
from django.utils import timezone # fixer la date à partir de la location.
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
# on creer des models pour la db avec manage.py makemigrations
# faire des migrations pour mettre à jour la base de donné.

class Post(models.Model):
    title = models.CharField(max_length=100) #Entré texte pour le titre
    content = models.TextField() # Entré bloc de texte pour le contenu
    date_posted = models.DateTimeField(default=timezone.now) # Entré date pour la date de poste
    author = models.ForeignKey(User, on_delete=models.CASCADE) # à la suprimmation de l'utilisateur nous allons supprimés tout les postes lié à cet utilisateur. # le foreign key permet de relier avec la table user

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk' : self.pk})