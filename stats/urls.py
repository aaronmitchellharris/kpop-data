from django.urls import path

from . import views

app_name = 'stats'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('groups/', views.GroupsView.as_view(), name='groups'),
    path('groups/hottest', views.GroupsViewHottest.as_view(), name='hottest'),
    path('groups/alphabetical', views.GroupsViewAlpha.as_view(), name='alphabetical'),
    path('groups/oldest', views.GroupsViewOldest.as_view(), name='oldest'),
    path('groups/newest', views.GroupsViewNewest.as_view(), name='newest'),
    path('profile/<int:pk>/<str:name>', views.ProfileView.as_view(), name='profile')
]