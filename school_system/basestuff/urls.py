from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('profiles/<int:pk>/', views.profile, name='see_profile')
]