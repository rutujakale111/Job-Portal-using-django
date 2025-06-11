from django.urls import path
from . import views
from .views import HomeView
from .views import create_or_update_profile
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import logout_confirm_view

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', LogoutView.as_view(next_page='job_list'), name='logout'),
    path('logout/confirm/', logout_confirm_view, name='logout_confirm'),
    path('profile/', views.create_or_update_profile, name='create_or_update_profile'),


    path('', views.HomeView.as_view(), name='job_list'),
    path('', HomeView.as_view(), name='home'),
    path('job/new/', views.JobCreateView.as_view(), name='job_create'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('apply/<int:pk>/', views.apply_job, name='apply_job'),
    path('add-job/', views.add_job,name='add_job'),
    path('profile/', views.create_or_update_profile, name='create_or_update_profile'),

]
