from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('section/<int:pk>/', views.section_detail, name='section_detail'),

    # Auth
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),

    # Dashboard
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/sections/', views.dashboard_sections, name='dashboard_sections'),
    path('dashboard/sections/create/', views.section_create, name='section_create'),
    path('dashboard/sections/<int:pk>/edit/', views.section_edit, name='section_edit'),
    path('dashboard/sections/<int:pk>/delete/', views.section_delete, name='section_delete'),
    path('dashboard/sections/reorder/', views.section_reorder, name='section_reorder'),

    # Media
    path('dashboard/upload/<int:pk>/', views.media_upload, name='media_upload'),
    path('dashboard/media/<int:pk>/delete/', views.media_delete, name='media_delete'),
    path('dashboard/media/<int:pk>/edit/', views.media_edit, name='media_edit'),
    path('dashboard/media/reorder/', views.media_reorder, name='media_reorder'),
    path('dashboard/media/bulk-delete/', views.media_bulk_delete, name='media_bulk_delete'),
    path('dashboard/section/<int:section_pk>/cover/<int:media_pk>/', views.set_cover, name='set_cover'),
]
