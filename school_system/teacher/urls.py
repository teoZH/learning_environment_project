from django.urls import path
from . import views
from basestuff.views import profile

urlpatterns = [
    path('profile/<int:pk>', profile, name='see_teacher_profile')
]
