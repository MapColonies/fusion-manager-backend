from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    version = models.PositiveIntegerField()
    extent = models.CharField(max_length=50)
    thumbnail = models.ImageField()
    takenAt = models.DateField()
    resolution = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name','version'),)

class Project(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    version = models.PositiveIntegerField()
    resources = models.ManyToManyField(Resource, through='ProjectResources')
    # resources = models.ManyToManyField(Resource)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name','version'),)

class ProjectResources(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('project','resource'),)