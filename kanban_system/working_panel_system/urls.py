from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:user_id>/', views.my_profile, name='profile_page'),
    path('profile/<int:user_id>/kanban/', views.show_pers_kanban, name='show_user_kanban'),
    path('profile/<int:user_id>/kanban/<int:kanban_id>/start/', views.start_todo, name='start_to_do'),
    path('profile/<int:user_id>/kanban/<int:kanban_id>/finish/', views.finish_todo, name='finish_the_todo'),
    path('profile/<int:user_id>/kanban/<int:kanban_id>/restart-it/', views.restart_todo, name='restart_the_todo'),
    path('profile/<int:user_id>/kanban/create-a-todo/', views.create_todo, name='create_a_todo'),
    path('profile/<int:user_id>/kanban/todo/<int:todo_id>/description/', views.show_todo_description, name='show_todo'),
    path('profile/<int:user_id>/kanban/todo/<int:todo_id>/edit', views.edit_user_todo, name='edit_todo'),
    path('profile/<int:user_id>/kanban/todo/<int:todo_id>/delete/', views.delete_user_todo, name='delete_todo'),
    path('profile/<int:user_id>/companies/', views.show_companies, name='show_user_companies'),
    path('profile/<int:user_id>/companies/add-a-company/', views.create_company, name='create_company'),
    path('profile/<int:user_id>/companies/<int:company_id>/information', views.show_company_info, name='show_company'),
    path('profile/<int:user_id>/company/<int:company_id>/employee/<int:employee_id>/remove',
         views.remove_user, name='remove_employee'),
    path('profile/<int:user_id>/hired-by-companies/', views.hired_by, name='show_user_work_for')
]
