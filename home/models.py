from django.db import models

# Create your models here.
class Project_add(models.Model):
    name=models.CharField(max_length=200)
    desc=models.CharField(max_length=700)
    link=models.CharField(max_length=200)
    stack=models.CharField(max_length=300)
    date = models.CharField(max_length=100)

    def __str__(self):
        return self.name