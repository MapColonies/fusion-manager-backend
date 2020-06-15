import os
from django.db import models

# Resource model.
# Represents a fusion resource.
# Defined by name, version, extent, thumbnail, the time the resource was taken, level, and resolution.
class Resource(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    version = models.PositiveIntegerField()
    extent = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='static')
    takenAt = models.DateTimeField()
    level = models.PositiveIntegerField()
    resolution = models.CharField(max_length=25)
    
    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name','version'),)

# Project model.
# Represents a fusion project.
# Defined by name, version and resources.
class Project(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    version = models.PositiveIntegerField()
    resources = models.ManyToManyField(Resource, through='ProjectResources')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name','version'),)

# Project - resource relation model.
# Defines a realtionship between a project and a resource (project has resource).
class ProjectResources(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('project','resource'),)