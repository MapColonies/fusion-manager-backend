from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='projects-home'),
    path('about/', views.about, name='projects-about'),
    path('resource/', views.resource, name='projects-resource'),
    path('project/', views.project, name='projects-project'),
]