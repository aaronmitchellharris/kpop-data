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

# used for authorization of staff pages
class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

# home view
def IndexView(request):
    object_list = Group.objects.all()

    '''
    object_list: all elements of Group model
    '''
    return render(request, 'stats/index.html', {"object_list": object_list, "bp":bp})

# about view
class AboutView(generic.ListView):
    template_name = 'stats/about.html'
    model = Group

# view for comparing 2 artists
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

    '''
    g1, g2: element of first and second group
    g1stats, g2stats: view count and upload dates for first and second group
    dV: g1,g2 data by month
    yV: g1,g2 data by year
    '''
    return render(request, 'stats/comparing.html',{"g1": g1, "g2": g2, "g1stats": g1stats, "g2stats": g2stats, "dV": dV,
                                                   "yV": yV})
# view for selecting second group to compare with
def CompareView(request, pk, name):
    object_list = Group.objects.exclude(pk=pk).order_by('total_view_count').reverse()
    sort = "Most Viewed"
    company_list = Group.objects.exclude(pk=pk).order_by('company').distinct('company')

    '''
    name: group name
    opk: primary key for group
    object_list: elements of Group model excluding 'opk' group
    sort: setting for sort button
    company_list: distinct 'company' elements of Group model elements excluding 'opk' group
    '''
    return render(request, 'stats/compare.html', {"name": name, "opk": pk, "object_list": object_list, "sort": sort,
                                                  "company_list": company_list})

# view for displaying artists
def GroupsView(request):
    object_list = Group.objects.all().order_by('total_view_count').reverse()
    sort = "Most Viewed"
    company_list = Group.objects.order_by('company').distinct('company')

    search_term = ''

    # searching capabilities by artist name or company name
    if 'search' in request.GET:
        search_term = request.GET['search']
        object_list = Group.objects.filter(name__icontains=search_term)
        ol2 = Group.objects.filter(company__icontains=search_term)
        object_list = object_list.union(ol2).order_by('total_view_count').reverse()

    '''
    object_list: elements of Group model
    sort: setting for sort button
    company_list: distinct 'company' elements of Group model elements
    search_term: item searched for by user
    '''
    return render(request, 'stats/groups.html', {"object_list": object_list, "sort": sort, "company_list": company_list,
                                                 "search_term": search_term})

# view for selecting second group to compare with sorted by hottest
def CompareViewHottest(request, pk, name):
    start_date = timezone.now()-timezone.timedelta(days=90)
    end_date = timezone.now()
    group = Group.objects.exclude(pk=pk).order_by('total_view_count').reverse()
    hot = []
    for i,g in enumerate(group):
        hot.append([g, 0])
        if Video.objects.filter(group=g, upload_date__range=(start_date, end_date)).order_by('upload_date').reverse():
            for v in Video.objects.filter(group=g, upload_date__range=(start_date, end_date)).order_by('upload_date')\
                    .reverse():
                hot[i][1] += v.view_count
    hot.sort(key=operator.itemgetter(1), reverse=True)
    object_list = []
    for h in hot:
        object_list.append(h[0])
    sort = "Hottest"
    company_list = Group.objects.exclude(pk=pk).order_by('company').distinct('company')

    '''
    name: group name
    opk: primary key for group
    object_list: elements of Group model sorted by 'hottest'
    sort: setting for sort button
    company_list: distinct 'company' elements of Group model elements
    '''
    return render(request, 'stats/compare.html', {"name": name, "opk": pk, "object_list": object_list, "sort": sort,
                                                  "company_list": company_list})

# view for displaying artists sorted by hottest
def GroupsViewHottest(request):
    start_date = timezone.now()-timezone.timedelta(days=90)
    end_date = timezone.now()
    group = Group.objects.all().order_by('total_view_count').reverse()
    hot = []
    for i,g in enumerate(group):
        hot.append([g, 0])
        if Video.objects.filter(group=g, upload_date__range=(start_date, end_date)).order_by('upload_date').reverse():
            for v in Video.objects.filter(group=g, upload_date__range=(start_date, end_date)).order_by('upload_date')\
                    .reverse():
                hot[i][1] += v.view_count
    hot.sort(key=operator.itemgetter(1), reverse=True)
    object_list = []
    for h in hot:
        object_list.append(h[0])
    sort = "Hottest"
    company_list = Group.objects.order_by('company').distinct('company')

    '''
    object_list: elements of Group model
    sort: setting for sort button
    company_list: distinct 'company' elements of Group model elements
    '''
    return render(request, 'stats/groups.html', {"object_list": object_list, "sort": sort,
                                                 "company_list": company_list})

# view for selecting second group to compare with sorted by alphabetical
def CompareViewAlpha(request, pk, name):
    object_list = Group.objects.exclude(pk=pk).order_by('name')
    sort = "Alphabetical"
    company_list = Group.objects.exclude(pk=pk).order_by('company').distinct('company')

    '''
    name: group name
    opk: primary key for group
    object_list: elements of Group model sorted by 'hottest'
    sort: setting for sort button
    company_list: distinct 'company' elements of Group model elements
    '''
    return render(request, 'stats/compare.html', {"name": name, "opk": pk, "object_list": object_list, "sort": sort,
                                                  "company_list": company_list})

# view for displaying artists sorted by alphabetical
def GroupsViewAlpha(request):
    object_list = Group.objects.all().order_by('name')
    sort = "Alphabetical"
    company_list = Group.objects.order_by('company').distinct('company')

    '''
    object_list: elements of Group model
    sort: setting for sort button
    company_list: distinct 'company' elements of Group model elements
    '''
    return render(request, 'stats/groups.html', {"object_list": object_list, "sort": sort,
                                                 "company_list": company_list})

# view for selecting second group to compare with sorted by oldest
def CompareViewOldest(request, pk, name):
    object_list = Group.objects.exclude(pk=pk).order_by('debut_date')
    sort = "Oldest"
    company_list = Group.objects.exclude(pk=pk).order_by('company').distinct('company')

    '''
    name: group name
    opk: primary key for group
    object_list: elements of Group model sorted by 'hottest'
    sort: setting for sort button
    company_list: distinct 'company' elements of Group model elements
    '''
    return render(request, 'stats/compare.html', {"name": name, "opk": pk, "object_list": object_list, "sort": sort,
                                                  "company_list": company_list})

# view for displaying artists sorted by oldest
def GroupsViewOldest(request):
    object_list = Group.objects.all().order_by('debut_date')
    sort = "Oldest"
    company_list = Group.objects.order_by('company').distinct('company')

    '''
    object_list: elements of Group model
    sort: setting for sort button
    company_list: distinct 'company' elements of Group model elements
    '''
    return render(request, 'stats/groups.html', {"object_list": object_list, "sort": sort,
                                                 "company_list": company_list})

# view for selecting second group to compare with sorted by newest
def CompareViewNewest(request, pk, name):
    object_list = Group.objects.exclude(pk=pk).order_by('debut_date').reverse()
    sort = "Newest"
    company_list = Group.objects.exclude(pk=pk).order_by('company').distinct('company')

    '''
    name: group name
    opk: primary key for group
    object_list: elements of Group model sorted by 'hottest'
    sort: setting for sort button
    company_list: distinct 'company' elements of Group model elements
    '''
    return render(request, 'stats/compare.html', {"name": name, "opk": pk, "object_list": object_list, "sort": sort,
                                                  "company_list": company_list})

# view for displaying artists sorted by newest
def GroupsViewNewest(request):
    object_list = Group.objects.all().order_by('debut_date').reverse()
    sort = "Newest"
    company_list = Group.objects.order_by('company').distinct('company')

    '''
    object_list: elements of Group model
    sort: setting for sort button
    company_list: distinct 'company' elements of Group model elements
    '''
    return render(request, 'stats/groups.html', {"object_list": object_list, "sort": sort,
                                                 "company_list": company_list})

# view for artist profiles
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

    '''
    group: artist's element from Group model
    vid_list: video objects from Video model tied to 'group'
    maxVid: video by artist with highest view count
    dV: data for artist videos by month
    '''
    return render(request, 'stats/profile.html', {'group': group, 'vid_list': vid_list, 'maxVid': maxVid, 'dV': dV})

# view for categories, not currently accessible
class CategoriesView(generic.ListView):
    template_name = 'stats/categories.html'
    model = Group

# view for deleting all videos in database
#def deleteVids(request):
#    Video.objects.all().delete()
#    context={}
#    return render(request,'stats/groupedit.html',context)

# view for displaying visualizations of data
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

    groupYear = group.annotate(year=ExtractYear('debut_date')).values('year').annotate(c=Count('id'))\
        .values('year', 'c')

    videos = Video.objects.all()

    company = group.values('company').annotate(Views=Sum('total_view_count'), Vids=Sum('video_count'),
                                               c=Count('company')).values('company', 'Views', 'Vids', 'c')

    '''
    group: all elements of Group model
    company: all company names
    gender: data grouped by gender
    genderCount: data counting by gender
    videos: all elements of Video model
    groupYear: data on artists by year
    '''
    return render(request, 'stats/data.html', {"group": group, "company": company, "gender": gender,
                                               "genderCount": genderCount, "videos": videos, "groupYear": groupYear})

# view for displaying data on artists grouped by gender
def GenderDataView(request):
    gender = Group.objects.all().values('gender').annotate(g=Count('id'),
                                                           v=Sum('video_count'), i=Sum('current_member_count'),
                                                           views=Sum('total_view_count')).values('gender', 'g', 'v',
                                                                                                 'i', 'views')
    for i, g in enumerate(gender):
        if g['gender'] == 'B':
            gender[i]['gender'] = 'Boys'
        elif g['gender'] == 'G':
            gender[i]['gender'] = 'Girls'
        elif g['gender'] == 'M':
            gender[i]['gender'] = 'Mixed'

    genderYear = Group.objects.all().values('gender').annotate(year=ExtractYear('debut_date'), gcount=Count('gender'))\
        .values('gender', 'year', 'gcount')

    genderY = []

    minYear = Group.objects.all().annotate(year=ExtractYear('debut_date')).values('year').order_by('year')[0]['year']
    maxYear = Group.objects.all().annotate(year=ExtractYear('debut_date')).values('year').order_by('year')\
        .reverse()[0]['year']

    for i in range(minYear, maxYear+1):
        genderY.append([i, 0, 0, 0])

    for j in genderYear:
        if j['gender'] == 'B':
            for e in genderY:
                if e[0] >= j['year']:
                    e[1] += j['gcount']
        if j['gender'] == 'G':
            for e in genderY:
                if e[0] >= j['year']:
                    e[2] += j['gcount']
        if j['gender'] == 'M':
            for e in genderY:
                if e[0] >= j['year']:
                    e[3] += j['gcount']

    '''
    gender: Group model data by gender
    genderYear: gender data by year
    minYear: earliest year by gender
    maxYear: most recent year by gender
    genderY: more data by year
    '''
    return render(request, 'stats/genderData.html', {"gender": gender, "genderYear": genderYear, "minYear": minYear,
                                                     "maxYear": maxYear, "genderY": genderY})

# view for displaying data on artists grouped by company
def CompanyDataView(request):
    group = Group.objects.all()
    company = group.values('company').annotate(Views=Sum('total_view_count'), Vids=Sum('video_count'),
                                               c=Count('company')).values('company', 'Views', 'Vids', 'c')

    '''
    group: all elements of Group model
    company: list of companies
    '''
    return render(request, 'stats/companyData.html', {"group": group, "company": company})

# view for displaying a graph of all data
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

    '''
    group: all elements of Group model
    videos: video data
    last: data using only latest music video
    top: data using only best 3 music videos
    recent: data using only latest 3 music videos
    gender: data by gender
    '''
    return render(request, 'stats/graph.html', {'group': group, 'videos': videos, 'last': last, 'top': top,
                                                'recent': recent, 'gender': gender})

# admin view for adding videos to database
class AddVideos(AdminStaffRequiredMixin, generic.ListView):
    template_name = 'stats/addvideos.html'
    model = Group

# admin view for editing Group model elements
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

