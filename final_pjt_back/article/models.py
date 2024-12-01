from django.db import models
# from django.contrib.auth.models import User 
from django.conf import settings

# Create your models here.
class ArticleFree(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class FreeRecommend(models.Model):
    articlefree = models.ForeignKey(ArticleFree, on_delete=models.CASCADE)
    recommend_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()