from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class History(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    search_history = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add= True)
