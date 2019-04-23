from django.urls import path

from . import views

app_name = 'stats'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('groups/', views.GroupsView.as_view(), name='groups'),
    path('profile/<int:pk>/<str:name>', views.ProfileView.as_view(), name='profile')
]