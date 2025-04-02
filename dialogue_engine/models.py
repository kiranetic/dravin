from django.db import models

# Create your models here.

class Query(models.Model):
    text = models.TextField()
    label = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
