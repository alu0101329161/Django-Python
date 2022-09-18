from distutils import text_file
from django.db import models
from django.contrib.auth.models import User

# Pincipal model
class Project(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Song model
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title + ' - ' + self.project.name