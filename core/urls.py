from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('requests/create/', views.request_create, name='request_create'),
    path('requests/<int:pk>/delete/', views.request_delete, name='request_delete'),
]