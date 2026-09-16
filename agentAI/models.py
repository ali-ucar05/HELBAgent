from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class AIAgent(models.Model):
    AI_MODEL_CHOICES = [
        ('API', 'API'),
        ('Local', 'Local'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    initial_prompt = models.TextField(default='You are an AI that answers questions.')
    model = models.CharField(max_length=100, choices=AI_MODEL_CHOICES, default='API')
    cooldown = models.IntegerField(default=0)
    discussion = models.TextField(default='')
    image = models.ImageField(default='default-AI.jpg', upload_to='agent_images/')
    date_posted = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ai_agent_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300,300))
            img.save(self.image.path)
