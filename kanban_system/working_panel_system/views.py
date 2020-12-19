from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from base_stuff_system.models import ExtendedUser, Todo, Company, Notes
from .forms import TodoForm, NotesForm, CompanyForm
from django.db.models import ObjectDoesNotExist


def my_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    add_info = ExtendedUser.objects.get(user=user)
    return render(request, 'user_profile.html', {'user_info': user,
                                                 'additional': add_info})


def show_pers_kanban(request, user_id):
    todos = Todo.objects.select_related('company__user')
    user_groups = {f"{company.title}": company.employee.all() for company in Company.objects.filter(user=request.user)}
    if request.method == 'POST':
        try:
            todo = Todo.objects.get(pk=request.POST['todo'])
            user = User.objects.get(username=request.POST['username'])
            if todo.user == user:
                todo.form_error = True
            else:
                todo.user = user
            todo.save()
            return render(request, 'show_user_kanban.html', {'todos': todos,
                                                             'groups': user_groups})
        except (ObjectDoesNotExist, KeyError):
            return render(request, 'access/not_authorized.html')
    for todo in todos:
        todo.form_error = False
    return render(request, 'show_user_kanban.html', {'todos': todos,
                                                     'groups': user_groups})


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


def show_todo_description(request, user_id, todo_id):
    notes = Notes.objects.all()
    try:
        todo = Todo.objects.get(pk=todo_id)
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return render(request, 'access/not_authorized.html')
    if request.method == 'POST':
        if 'delete' in request.POST:
            try:
                note = Notes.objects.get(pk=request.POST['delete'])
                note.delete()
                return redirect('show_todo', request.user.pk, todo.pk)
            except ObjectDoesNotExist:
                return render(request, 'access/not_authorized.html')

        form = NotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = user
            note.todo = todo
            note.save()

    else:
        form = NotesForm()
    context = {
        'todo': todo,
        'form': form,
        'notes': notes
    }

    return render(request, 'show_description.html', context)


def edit_user_todo(request, user_id, todo_id):
    try:
        todo = Todo.objects.get(pk=todo_id)
        print(todo)
        user = User.objects.get(pk=user_id)
        print(user)
        if todo.user != request.user:
            print(todo.user)
            print(request.user)
            return render(request, 'access/not_authorized.html')
    except ObjectDoesNotExist:
        return render(request, 'access/not_authorized.html')
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('show_user_kanban', request.user.pk)
    else:
        form = TodoForm(instance=todo)
        form.fields['company'].queryset = Company.objects.filter(user=request.user)
    context = {
        'form': form
    }
    return render(request, 'create_some_todo.html', context)


def delete_user_todo(request, user_id, todo_id):
    try:
        user = User.objects.get(pk=user_id)
        todo = Todo.objects.get(pk=todo_id)
        if todo.user != user or todo.user != request.user:
            return render(request, 'access/not_authorized.html')
        todo.delete()
    except ObjectDoesNotExist:
        return render(request, 'access/not_authorized.html')
    return redirect('show_user_kanban', request.user.pk)


def start_todo(request, user_id, kanban_id):
    try:
        todo = Todo.objects.get(pk=kanban_id)
    except ObjectDoesNotExist:
        return render(request, 'access/not_authorized.html')
    if todo.company:
        if todo.user == request.user or todo.company.user == request.user:
            pass
        else:
            return render(request, 'access/not_authorized.html')
    todo.in_progress = True
    todo.save()
    return redirect('show_user_kanban', request.user.pk)


def finish_todo(request, user_id, kanban_id):
    try:
        todo = Todo.objects.get(pk=kanban_id)
    except ObjectDoesNotExist:
        return render(request, 'access/not_authorized.html')
    if todo.company:
        if todo.user == request.user or todo.company.user == request.user:
            pass
        else:
            return render(request, 'access/not_authorized.html')
    todo.in_progress = False
    todo.is_done = True
    todo.save()
    return redirect('show_user_kanban', request.user.pk)


def restart_todo(request, user_id, kanban_id):
    try:
        todo = Todo.objects.get(pk=kanban_id)
    except ObjectDoesNotExist:
        return render(request, 'access/not_authorized.html')
    if todo.company:
        if todo.user == request.user or todo.company.user == request.user:
            pass
        else:
            return render(request, 'access/not_authorized.html')
    todo.is_done = False
    todo.in_progress = False
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
    return render(request, 'show_user_companies.html', context)


def create_company(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return render(request, 'access/not_authorized.html')
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = user
            company.save()
            return redirect('show_user_companies', request.user.pk)
    else:
        form = CompanyForm()
        form.fields['user'].queryset = User.objects.filter(pk=user_id)
    return render(request, 'create_new_company.html', {'form': form})


def show_company_info(request, user_id, company_id):
    try:
        user = User.objects.get(pk=user_id)
        company = Company.objects.get(pk=company_id)
        if company.user != request.user:
            return render(request, 'access/not_authorized.html')
    except ObjectDoesNotExist:
        return render(request, 'access/not_authorized.html')
    employees = company.employee.all()
    context = {
        'company': company,
        'employees': employees
    }
    return render(request, 'show_specific_company.html', context)


def remove_user(request,user_id,company_id,employee_id):
    if request.method == 'POST':
        try:
            company = Company.objects.get(pk=company_id)
            employee = User.objects.get(pk=employee_id)
            user = User.objects.get(pk=user_id)
            if company.user != user or request.user != user:
                return render(request, 'access/not_authorized.html')
            employee.delete()
            return redirect('show_company',request.user.pk, company.pk)
        except ObjectDoesNotExist:
            return render(request, 'access/not_authorized.html')
    else:
        return render(request, 'access/not_authorized.html')


def hired_by(request, user_id):
    return render(request, 'show_hired_by.html')
