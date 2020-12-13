from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:user_id>/', views.my_profile, name='profile_page')
]