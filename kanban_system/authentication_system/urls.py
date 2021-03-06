from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('change-password/<int:user_id>/<str:username>',views.change_password, name='change_pass' ),
    path('reset-password/',views.reset_password, name= 'reset_pass'),
    path('set-new-password/<uidb64>/<token>/',views.set_password, name='set_pass')
]