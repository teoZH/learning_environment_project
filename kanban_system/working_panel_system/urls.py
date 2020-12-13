from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:user_id>/', views.my_profile, name='profile_page'),
    path('profile/<int:user_id>/kanban/', views.show_pers_kanban, name='show_user_kanban'),
    path('profile/<int:user_id>/kanban/create-a-todo/', views.create_todo, name='create_a_todo'),
    path('profile/<int:user_id>/companies/', views.show_companies, name='show_user_companies'),
    path('profile/<int:user_id>/companies/add-a-company/',views.create_company,name='create_company'),
    path('profile/<int:user_id>/hired-by-companies/', views.hired_by, name='show_user_work_for')
]
