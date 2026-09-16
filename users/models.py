from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model): # on herite de models
    user = models.OneToOneField(User, on_delete=models.CASCADE) # une relation 1-1 # Si le user est supprime son profil aussi
    image = models.ImageField(default='default.jpg', upload_to='profile_pics') # repertoire -> ou il va stocker les images.

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            outpout_size = (300, 300)
            img.thumbnail(outpout_size)
            img.save(self.image.path)
            