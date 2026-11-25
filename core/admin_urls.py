from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('requests/', views.admin_requests, name='admin_requests'),
    path('requests/<int:pk>/accept/', views.admin_request_accept, name='admin_request_accept'),
    path('requests/<int:pk>/complete/', views.admin_request_complete, name='admin_request_complete'),
    path('categories/', views.admin_categories, name='admin_categories'),
    path('categories/<int:pk>/delete/', views.admin_category_delete, name='admin_category_delete'),
]