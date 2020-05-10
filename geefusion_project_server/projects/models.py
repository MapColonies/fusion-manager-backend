from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=300)
    version = models.PositiveIntegerField()
    extent = models.CharField(max_length=50)
    thumbnail = models.ImageField()
    takenAt = models.DateField()
    resolution = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    version = models.PositiveIntegerField()
    resources = models.ManyToManyField(Resource, through='ProjectResources')

    def __str__(self):
        return self.name

class ProjectResources(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)