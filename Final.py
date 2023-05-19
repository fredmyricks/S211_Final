from django.db import models

# Create your models here.

class Blogs(models.Model):
  Image = models.ImageField(null=True, blank=True)
  title = models.CharField(max_length=200, null=True)
  description = models.CharField(max_length=1200, null=True)
  date = models.DateField(auto_now_add=True, null=True)
  likes = models.IntegerField(default=0)

# Create one .py file "forms.py"

from .models import *
from django import forms
from django.forms import ModelForm

class blogForm(ModelForm):
  class Meta:
    model = Blogs
    fields = '__all__'
    exclude = ['likes', 'date']

# Create manage.py file "Py manage.py createsuperuser"

# After creating super user we need to register the model in admin.py

from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Blogs)

# settings.py

STATIC_URL = '/static/'
MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# CREATE URL's .py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog.views import *

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', home, name='home'),
  path('add/', addBlog, name='addblog'),
  path('like/<str:pk>', likeBlog, name='like'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# views.py

from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.

def home(request):
  AllBlogs = Blogs.objects.all()
  context = {
    'blogs': AllBlogs,
  }
  print(AllBlogs)
  return render(request, 'home.html', context)

def addBlog(request):
  form = blogForm()
  if request.method == 'POST':
    form = blogForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('/')

  context = {
    'form': form,
  }
  return render(request, 'addblog.html', context)

def likeBlog(request, pk):
  blog = Blogs.objects.get(id=pk)
  blog.likes += 1
  blog.save()
  return redirect('/')



# Blog objects in ‘AllBlogs’ and pass them to home.html

# Home.html

{% load static %}
<html>
  <head>
    <title>
      Techvidvan Blog Application
    </title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
    <link rel="stylesheet" href=" {% static '/css/main.css' %} ">
  </head>
  <body>
    {% block content %}
    <div class="container">
      <a href="{% url 'addblog' %}" class='btn btn-primary'>Add Blog</a>
      <br>
    {% for b in blogs %}
      <br>
        <div class="row">
          <div class="col-md-3">
            <div class="card" style="width: 22rem;">
