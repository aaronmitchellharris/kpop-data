from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.forms import modelformset_factory, inlineformset_factory
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from .models import Group, Video
from . import vids
from .forms import VidForm

class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class IndexView(generic.ListView):
    template_name = 'stats/index.html'
    model = Group

class AboutView(generic.ListView):
    template_name = 'stats/about.html'
    model = Group

def GroupsView(request):
    object_list = Group.objects.all().order_by('total_view_count').reverse()
    sort = "Most Viewed"
    company_list = Group.objects.distinct() #order_by('company').distinct('company')
    return render(request, 'stats/groups.html', {"object_list": object_list, "sort": sort, "company_list": company_list})

def GroupsViewHottest(request):
    object_list = Group.objects.all().order_by('total_view_count').reverse()
    sort = "Hottest"
    return render(request, 'stats/groups.html', {"object_list":object_list, "sort":sort})

def GroupsViewAlpha(request):
    object_list = Group.objects.all().order_by('name')
    sort = "Alphabetical"
    return render(request, 'stats/groups.html', {"object_list": object_list, "sort": sort})

def GroupsViewOldest(request):
    object_list = Group.objects.all().order_by('debut_date')
    sort = "Oldest"
    return render(request, 'stats/groups.html', {"object_list": object_list, "sort": sort})

def GroupsViewNewest(request):
    object_list = Group.objects.all().order_by('debut_date').reverse()
    sort = "Newest"
    return render(request, 'stats/groups.html', {"object_list": object_list, "sort": sort})

def ProfileView(request, pk, name):
    group = Group.objects.get(pk=pk)
    vid_list = Video.objects.filter(group=pk).order_by('upload_date').reverse()
    return render(request, 'stats/profile.html', {'group':group, 'vid_list':vid_list})

class CategoriesView(generic.ListView):
    template_name = 'stats/categories.html'
    model = Group

def deleteVids(request):
    Video.objects.all().delete()
    context={}
    return render(request,'stats/groupedit.html',context)


'''
@staff_member_required
def AddVideos(request):
    template_name = 'stats/addvideos.html'
    try:
        g = Group.objects.all()
    except Group.DoesNotExist:
        raise Http404("Group does not exist")
    return render(request, template_name, {'group': g})
'''

class AddVideos(AdminStaffRequiredMixin, generic.ListView):
    template_name = 'stats/addvideos.html'
    model = Group

'''
class GroupEdit(AdminStaffRequiredMixin, generic.DetailView):
    template_name = 'stats/groupedit.html'
    model = Group
'''
#@staff_member_required
def GroupEdit(request, pk, name):
    group = Group.objects.get(pk=pk)
    VidFormSet = inlineformset_factory(Group, Video, fields=('group','title','upload_date','yt_video_id','thumbnail_url'), extra=50)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formset = VidFormSet(request.POST, request.FILES, instance=group)
        # check whether it's valid:
        if formset.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            formset.save()
            # redirect to a new URL:

    # if a GET (or any other method) we'll create a blank form
    else:
        formset = VidFormSet(instance=group)

    channel = Group.objects.filter(name=name)[0].yt_channel_id

    return render(request, 'stats/groupedit.html', {'formset': formset, 'group': name, 'pk':pk, 'channel':channel})

