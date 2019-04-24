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
    def get_queryset(self):
        return Group.objects.all().order_by('total_view_count').reverse()

class GroupsViewHottest(generic.ListView):
    template_name = 'stats/groups.html'
    model = Group
    def get_queryset(self):
        return Group.objects.all().order_by('total_view_count').reverse()

class GroupsViewAlpha(generic.ListView):
    template_name = 'stats/groups.html'
    model = Group
    def get_queryset(self):
        return Group.objects.all().order_by('name')

class GroupsViewOldest(generic.ListView):
    template_name = 'stats/groups.html'
    model = Group
    def get_queryset(self):
        return Group.objects.all().order_by('debut_date')

class GroupsViewNewest(generic.ListView):
    template_name = 'stats/groups.html'
    model = Group
    def get_queryset(self):
        return Group.objects.all().order_by('debut_date').reverse()

class ProfileView(generic.DetailView):
    template_name = 'stats/profile.html'
    model = Group

class CategoriesView(generic.ListView):
    template_name = 'stats/categories.html'
    model = Group