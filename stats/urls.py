from django.urls import path

from . import views

app_name = 'stats'
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('groups/', views.GroupsView, name='groups'),
    path('groups/hottest', views.GroupsViewHottest, name='hottest'),
    path('groups/alphabetical', views.GroupsViewAlpha, name='alphabetical'),
    path('groups/oldest', views.GroupsViewOldest, name='oldest'),
    path('groups/newest', views.GroupsViewNewest, name='newest'),
    path('profile/<int:pk>/<str:name>', views.ProfileView, name='profile'),
    path('addvideos/', views.AddVideos.as_view(), name='addvideos'),
    path('addvideos/<int:pk>/<str:name>', views.GroupEdit, name='groupedit'),
    #path('delete/', views.deleteVids, name='deletevids'),
    path('graph/<str:gender>', views.GraphView, name='graph'),
    path('compare/<int:pk>/<str:name>', views.CompareView, name='compare'),
    path('compare/hottest/<int:pk>/<str:name>', views.CompareViewHottest, name='comparehottest'),
    path('compare/alphabetical/<int:pk>/<str:name>', views.CompareViewAlpha, name='comparealphabetical'),
    path('compare/oldest/<int:pk>/<str:name>', views.CompareViewOldest, name='compareoldest'),
    path('compare/newest/<int:pk>/<str:name>', views.CompareViewNewest, name='comparenewest'),
    path('comparing/<int:pk>/<int:pk2>', views.ComparingView, name='comparing'),
    path('data/', views.DataView, name='data'),
    path('data/gender/', views.GenderDataView, name='genderData'),
    path('data/company/', views.CompanyDataView, name='companyData'),
]