from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title