from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.forms import modelformset_factory, inlineformset_factory
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.functions import TruncMonth, ExtractMonth, ExtractYear
from django.db.models import Count, Sum
from datetime import datetime, timedelta
import operator
from .models import Group, Video
from . import vids
from .forms import VidForm

class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

def IndexView(request):
    object_list = Group.objects.all()
    bp = Group.objects.filter(pk='1')

    #if request.method == 'GET':
    #    search_query = request.GET.get('search_box', None)

    if 'search' in request.GET:
        search_term = request.GET['search']

    return render(request, 'stats/index.html', {"object_list": object_list, "bp":bp})

class AboutView(generic.ListView):
    template_name = 'stats/about.html'
    model = Group

def ComparingView(request, pk, pk2):

    g1 = Group.objects.get(pk=pk)
    g2 = Group.objects.get(pk=pk2)

    g1stats = [Video.objects.filter(group=g1).order_by('view_count').reverse()[0],
               Video.objects.filter(group=g1).order_by('upload_date').reverse()[0],
               Video.objects.filter(group=g1).order_by('upload_date')[0]]

    g2stats = [Video.objects.filter(group=g2).order_by('view_count').reverse()[0],
               Video.objects.filter(group=g2).order_by('upload_date').reverse()[0],
               Video.objects.filter(group=g2).order_by('upload_date')[0]]

    dV = [['Jan', 0, 0], ['Feb', 0, 0], ['Mar', 0, 0], ['Apr', 0, 0], ['May', 0, 0], ['Jun', 0, 0], ['Jul', 0, 0],
          ['Aug', 0, 0], ['Sep', 0, 0], ['Oct', 0, 0], ['Nov', 0, 0], ['Dec', 0, 0]]

    dateVids1 = Video.objects.filter(group=g1).annotate(month=ExtractMonth('upload_date')).values('month').annotate(
        c=Count('id')).values('month', 'c')

    for v in dateVids1:
        dV[v['month'] - 1][1] = v['c']

    dateVids2 = Video.objects.filter(group=g2).annotate(month2=ExtractMonth('upload_date')).values('month2').annotate(
        c2=Count('id')).values('month2', 'c2')

    for v in dateVids2:
        dV[v['month2'] - 1][2] = v['c2']

    yV1 = Video.objects.filter(group=g1).annotate(year=ExtractYear('upload_date')).values('year').annotate(
        cy=Sum('view_count')).values('year', 'cy')
    yV2 = Video.objects.filter(group=g2).annotate(year=ExtractYear('upload_date')).values('year').annotate(
        cy2=Sum('view_count')).values('year', 'cy2')

    hold = []
    for y in yV1:
        hold.append(y['year'])
    for y in yV2:
        hold.append(y['year'])

    last = max(hold)
    first = min(hold)

    yV = list(range(first, last+1))

    for i, item in enumerate(yV):
        yV[i] = [item, 0, 0]

    for y in yV1:
        for item in yV:
            if y['year'] == item[0]:
                item[1] = y['cy']

    for y in yV2:
        for item in yV:
            if y['year'] == item[0]:
                item[2] = y['cy2']

    return render(request, 'stats/comparing.html',{"g1": g1, "g2": g2, "g1stats": g1stats, "g2stats": g2stats, "dV": dV,
                                                   "yV": yV})

def CompareView(request, pk, name):
    object_list = Group.objects.exclude(pk=pk).order_by('total_view_count').reverse()
    sort = "Most Viewed"
    company_list = Group.objects.exclude(pk=pk).order_by('company').distinct('company')
    return render(request, 'stats/compare.html', {"name": name, "opk": pk, "object_list": object_list, "sort": sort, "company_list": company_list})

def GroupsView(request):
    object_list = Group.objects.all().order_by('total_view_count').reverse()
    sort = "Most Viewed"
    company_list = Group.objects.order_by('company').distinct('company')

    search_term = ''

    if 'search' in request.GET:
        search_term = request.GET['search']
        object_list = Group.objects.filter(name__icontains=search_term)
        ol2 = Group.objects.filter(company__icontains=search_term)
        object_list = object_list.union(ol2).order_by('total_view_count').reverse()

    return render(request, 'stats/groups.html',{"object_list": object_list, "sort": sort, "company_list": company_list, "search_term": search_term})

def CompareViewHottest(request, pk, name):
    start_date = timezone.now()-timezone.timedelta(days=90)
    end_date = timezone.now()
    group = Group.objects.exclude(pk=pk).order_by('total_view_count').reverse()
    hot = []
    for i,g in enumerate(group):
        hot.append([g, 0])
        if Video.objects.filter(group=g, upload_date__range=(start_date, end_date)).order_by('upload_date').reverse():
            for v in Video.objects.filter(group=g, upload_date__range=(start_date, end_date)).order_by('upload_date').reverse():
                hot[i][1] += v.view_count
    hot.sort(key=operator.itemgetter(1), reverse=True)
    object_list = []
    for h in hot:
        object_list.append(h[0])
    sort = "Hottest"
    company_list = Group.objects.exclude(pk=pk).order_by('company').distinct('company')
    return render(request, 'stats/compare.html',{"name": name, "opk": pk, "object_list": object_list, "sort": sort, "company_list": company_list})

def GroupsViewHottest(request):
    start_date = timezone.now()-timezone.timedelta(days=90)
    end_date = timezone.now()
    group = Group.objects.all().order_by('total_view_count').reverse()
    hot = []
    for i,g in enumerate(group):
        hot.append([g, 0])
        if Video.objects.filter(group=g, upload_date__range=(start_date, end_date)).order_by('upload_date').reverse():
            for v in Video.objects.filter(group=g, upload_date__range=(start_date, end_date)).order_by('upload_date').reverse():
                hot[i][1] += v.view_count
    hot.sort(key=operator.itemgetter(1), reverse=True)
    object_list = []
    for h in hot:
        object_list.append(h[0])
    sort = "Hottest"
    company_list = Group.objects.order_by('company').distinct('company')
    return render(request, 'stats/groups.html',{"object_list": object_list, "sort": sort, "company_list": company_list})

def CompareViewAlpha(request, pk, name):
    object_list = Group.objects.exclude(pk=pk).order_by('name')
    sort = "Alphabetical"
    company_list = Group.objects.exclude(pk=pk).order_by('company').distinct('company')
    return render(request, 'stats/compare.html',{"name": name, "opk": pk, "object_list": object_list, "sort": sort, "company_list": company_list})

def GroupsViewAlpha(request):
    object_list = Group.objects.all().order_by('name')
    sort = "Alphabetical"
    company_list = Group.objects.order_by('company').distinct('company')
    return render(request, 'stats/groups.html',{"object_list": object_list, "sort": sort, "company_list": company_list})

def CompareViewOldest(request, pk, name):
    object_list = Group.objects.exclude(pk=pk).order_by('debut_date')
    sort = "Oldest"
    company_list = Group.objects.exclude(pk=pk).order_by('company').distinct('company')
    return render(request, 'stats/compare.html', {"name": name, "opk": pk, "object_list": object_list, "sort": sort,
                                                  "company_list": company_list})

def GroupsViewOldest(request):
    object_list = Group.objects.all().order_by('debut_date')
    sort = "Oldest"
    company_list = Group.objects.order_by('company').distinct('company')
    return render(request, 'stats/groups.html',{"object_list": object_list, "sort": sort, "company_list": company_list})

def CompareViewNewest(request, pk, name):
    object_list = Group.objects.exclude(pk=pk).order_by('debut_date').reverse()
    sort = "Newest"
    company_list = Group.objects.exclude(pk=pk).order_by('company').distinct('company')
    return render(request, 'stats/compare.html', {"name": name, "opk": pk, "object_list": object_list, "sort": sort,
                                                  "company_list": company_list})

def GroupsViewNewest(request):
    object_list = Group.objects.all().order_by('debut_date').reverse()
    sort = "Newest"
    company_list = Group.objects.order_by('company').distinct('company')
    return render(request, 'stats/groups.html',{"object_list": object_list, "sort": sort, "company_list": company_list})

def ProfileView(request, pk, name):
    group = Group.objects.get(pk=pk)
    vid_list = Video.objects.filter(group=pk).order_by('upload_date').reverse()
    maxVid = Video.objects.filter(group=pk).order_by('view_count').reverse()[0]
    dateVids = Video.objects.filter(group=pk).annotate(month=ExtractMonth('upload_date')).values('month').annotate(
        c=Count('id')).values('month', 'c')
    dV = [['Jan',0],['Feb',0],['Mar',0],['Apr',0],['May',0],['Jun',0],['Jul',0],['Aug',0],['Sep',0],['Oct',0],['Nov',0],
          ['Dec',0]]
    for v in dateVids:
        dV[v['month']-1][1] = v['c']
    return render(request, 'stats/profile.html', {'group':group, 'vid_list':vid_list, 'maxVid':maxVid,
                                                  'dV':dV})

class CategoriesView(generic.ListView):
    template_name = 'stats/categories.html'
    model = Group

#def deleteVids(request):
#    Video.objects.all().delete()
#    context={}
#    return render(request,'stats/groupedit.html',context)

def DataView(request):

    group = Group.objects.all()
    gender = group.values('gender').annotate(Views=Sum('total_view_count')).values('gender', 'Views')
    for i,g in enumerate(gender):
        if g['gender'] == 'B':
            gender[i]['gender'] = 'Boys'
        elif g['gender'] == 'G':
            gender[i]['gender'] = 'Girls'
        elif g['gender'] == 'M':
            gender[i]['gender'] = 'Mixed'
    genderCount = group.values('gender').annotate(c=Count('gender')).values('gender', 'c')

    videos = Video.objects.all()

    company = group.values('company').annotate(Views=Sum('total_view_count'), Vids=Sum('video_count'),
                                               c=Count('company')).values('company', 'Views', 'Vids', 'c')

    return render(request, 'stats/data.html', {"group": group, "company": company, "gender": gender,
                                               "genderCount": genderCount, "videos": videos})

def GenderDataView(request):

    gender = Group.objects.all().values('gender')\
        .annotate(g=Count('id'), v=Sum('video_count'), i=Sum('current_member_count'), views=Sum('total_view_count'))\
        .values('gender', 'g', 'v', 'i', 'views')
    for i, g in enumerate(gender):
        if g['gender'] == 'B':
            gender[i]['gender'] = 'Boys'
        elif g['gender'] == 'G':
            gender[i]['gender'] = 'Girls'
        elif g['gender'] == 'M':
            gender[i]['gender'] = 'Mixed'

    return render(request, 'stats/genderData.html', {"gender": gender})

def GraphView(request, gender):

    if gender == 'all':
        group = Group.objects.all().order_by('total_view_count').reverse()
    else:
        group = Group.objects.filter(gender=gender).order_by('total_view_count').reverse()
    videos = []
    last = []
    top = []
    recent = []
    for g in group:
        if Video.objects.filter(group=g):
            videos.append(Video.objects.filter(group=g).order_by('view_count').reverse()[0])
            last.append(Video.objects.filter(group=g).order_by('upload_date').reverse()[0])

            temptop = [g, 0]
            temprecent = [g, 0]

            if len(Video.objects.filter(group=g)) >= 3:
                for i in range(3):
                    temptop[1] += Video.objects.filter(group=g).order_by('view_count').reverse()[i].view_count
                    temprecent[1] += Video.objects.filter(group=g).order_by('upload_date').reverse()[i].view_count
            elif len(Video.objects.filter(group=g)) >= 2:
                for i in range(2):
                    temptop[1] += Video.objects.filter(group=g).order_by('view_count').reverse()[i].view_count
                    temprecent[1] += Video.objects.filter(group=g).order_by('upload_date').reverse()[i].view_count
            elif len(Video.objects.filter(group=g)) == 1:
                temptop[1] += Video.objects.filter(group=g).order_by('view_count').reverse()[0].view_count

                temprecent[1] += Video.objects.filter(group=g).order_by('upload_date').reverse()[0].view_count

            top.append(temptop)
            recent.append(temprecent)

    return render(request, 'stats/graph.html', {'group':group, 'videos':videos, 'last':last, 'top':top, 'recent':recent,
                  'gender':gender})

class AddVideos(AdminStaffRequiredMixin, generic.ListView):
    template_name = 'stats/addvideos.html'
    model = Group

#@staff_member_required
def GroupEdit(request, pk, name):
    group = Group.objects.get(pk=pk)
    VidFormSet = inlineformset_factory(Group, Video, fields=('group', 'title', 'upload_date', 'yt_video_id',
                                                             'thumbnail_url'), extra=50)
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

