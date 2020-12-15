from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from base_stuff_system.models import ExtendedUser, Todo, Company, Notes
from .forms import TodoForm, NotesForm, CompanyForm, create_choicesPersonalCompany
from django.db.models import ObjectDoesNotExist


def my_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    add_info = ExtendedUser.objects.get(user=user)
    return render(request, 'user_profile.html', {'user_info': user,
                                                 'additional': add_info})


def show_pers_kanban(request, user_id):
    todos = Todo.objects.filter(user=request.user)

    return render(request, 'show_user_kanban.html', {'todos': todos})


def create_todo(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            if todo.user is None:
                todo.user = user
            todo.save()
            return redirect('show_user_kanban', request.user.pk)
    else:
        form = TodoForm()
        form.fields['company'].queryset = Company.objects.filter(user=request.user)
    return render(request, 'create_some_todo.html', {'form': form})


def start_todo(request, user_id, kanban_id):
    todo = Todo.objects.get(pk=kanban_id)
    todo.in_progress = True
    todo.save()
    return redirect('show_user_kanban', request.user.pk)


def show_companies(request, user_id):
    companies = Company.objects.filter(user=request.user)
    context = {
        'companies': companies,
        'success': None,
        'error': None
    }

    if request.method == 'POST':
        username = request.POST['username']
        try:
            company = Company.objects.get(pk=request.POST['company'])
            employees = company.employee.all()
            if company.user != request.user:
                context['error'] = 'Invalid request!'
        except ObjectDoesNotExist:
            context['error'] = 'Invalid request!'

        try:
            user = User.objects.get(username=username)
            if request.user == user:
                context['error'] = 'You cannot add yourself!'
            elif user in employees:
                context['error'] = 'This user is already added!'
            else:
                company.employee.add(user)
                context['success'] = f'User {username} added successfully'
        except ObjectDoesNotExist:
            context['error'] = 'Invalid username! Please try again!'
    print(context)
    return render(request, 'show_user_companies.html', context)


def create_company(request, user_id):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_user_companies', request.user.pk)
    else:
        form = CompanyForm()
        form.fields['user'].queryset = User.objects.filter(pk=user_id)
    return render(request, 'create_new_company.html', {'form': form})


def hired_by(request, user_id):
    return render(request, 'show_hired_by.html')
