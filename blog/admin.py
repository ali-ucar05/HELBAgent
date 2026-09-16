from django.contrib import admin
from .models import Post

# Register your models here.
# importer les modeles pour les voir dans la page admin
admin.site.register(Post)