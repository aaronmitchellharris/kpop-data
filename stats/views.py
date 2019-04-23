from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Group, Video


class IndexView(generic.ListView):
    template_name = 'stats/index.html'
    model = Group

class AboutView(generic.ListView):
    template_name = 'stats/about.html'
    model = Group

class GroupsView(generic.ListView):
    template_name = 'stats/groups.html'
    model = Group

class ProfileView(generic.DetailView):
    template_name = 'stats/profile.html'
    model = Group

class CategoriesView(generic.ListView):
    template_name = 'stats/categories.html'
    model = Group