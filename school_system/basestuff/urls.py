from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('my-panel/teacher/',include('teacher.urls')),
    path('my-panel/student/',include('student.urls'))
]