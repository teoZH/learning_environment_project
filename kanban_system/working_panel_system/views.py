from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from authentication_system.forms import ExtendedProfileInfoForm
from base_stuff_system.models import ExtendedUser, Todo, Company, Notes
from .forms import TodoForm, NotesForm, CompanyForm, EditProfileInfo, AddUserForm
from django.db.models import ObjectDoesNotExist
from .validators import check_for_object_availability, check_correct_user


@check_correct_user
def my_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    check_profile = False
    add_info = ExtendedUser.objects.get(user=user)
    return render(request, 'user_profile.html', {'user_info': user,
                                                 'additional': add_info,
                                                 'check': check_profile})


@check_correct_user
def edit_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    check_profile = False
    add_info = ExtendedUser.objects.get(user=user)

    if request.method == 'POST':
        user_form = EditProfileInfo(request.POST, instance=user)
        additional_form = ExtendedProfileInfoForm(request.POST, request.FILES, instance=add_info)
        if user_form.is_valid() and additional_form.is_valid():
            user = user_form.save()
            more = additional_form.save(commit=False)
            more.user = user
            more.save()
            return redirect('profile_page', request.user.pk)
    else:
        user_form = EditProfileInfo(instance=user)
        additional_form = ExtendedProfileInfoForm(instance=add_info)
    context = {
        'form': user_form,
        'additional': additional_form
    }
    return render(request, 'edit_my_profile.html', context)


@check_correct_user
def see_other_profile(request, user_id, profile_id):
    check_profile = True
    other_user = check_for_object_availability(profile_id, User)
    if not other_user:
        return render(request, 'access/not_authorized.html')
    add_info = ExtendedUser.objects.get(user=other_user)
    return render(request, 'user_profile.html', {'user_info': other_user,
                                                 'additional': add_info,
                                                 'check': check_profile})


@check_correct_user
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

        except (ObjectDoesNotExist, KeyError):
            return render(request, 'access/not_authorized.html')
    if request.method == "GET":
        for todo in todos:
            todo.form_error = False
    return render(request, 'show_user_kanban.html', {'todos': todos,
                                                     'groups': user_groups})


@check_correct_user
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


@check_correct_user
def show_todo_description(request, user_id, todo_id):
    notes = Notes.objects.all()
    user = User.objects.get(pk=user_id)
    todo = check_for_object_availability(todo_id, Todo)
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


@check_correct_user
def edit_user_todo(request, user_id, todo_id):
    user = User.objects.get(pk=user_id)
    todo = check_for_object_availability(todo_id, model=Todo)
    if not todo:
        return render(request, 'access/not_authorized.html')
    if todo.company.user != request.user:
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


@check_correct_user
def delete_user_todo(request, user_id, todo_id):
    user = User.objects.get(pk=user_id)

    todo = check_for_object_availability(todo_id, Todo)
    if not todo:
        return render(request, 'access/not_authorized.html')
    if todo.user != user or todo.user != request.user:
        return render(request, 'access/not_authorized.html')

    todo.delete()

    return redirect('show_user_kanban', request.user.pk)


@check_correct_user
def start_todo(request, user_id, kanban_id):
    todo = check_for_object_availability(kanban_id, Todo)
    if not todo:
        return render(request, 'access/not_authorized.html')
    if todo.company:
        if todo.user == request.user or todo.company.user == request.user:
            pass
        else:
            return render(request, 'access/not_authorized.html')
    todo.in_progress = True
    todo.save()
    return redirect('show_user_kanban', request.user.pk)


@check_correct_user
def finish_todo(request, user_id, kanban_id):
    todo = check_for_object_availability(kanban_id, Todo)
    if not todo:
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


@check_correct_user
def restart_todo(request, user_id, kanban_id):
    todo = check_for_object_availability(kanban_id, Todo)
    if not todo:
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


@check_correct_user
def show_companies(request, user_id):
    success = None
    error = None
    companies = Company.objects.filter(user=request.user)

    if request.method == 'POST':
        username = request.POST['username']
        try:
            company = Company.objects.get(pk=request.POST['company'])
            employees = company.employee.all()
            if company.user != request.user:
                error = 'Invalid request!'
        except ObjectDoesNotExist:
            return render(request, 'access/not_authorized.html')

        form = AddUserForm(request.POST)
        form.fields['username'].model_company = company
        form.fields['username'].model_user = User
        form.fields['username'].request_user = request.user
        if form.is_valid():
            other_user = User.objects.get(username=username)
            company.employee.add(other_user)
            company.save()
            success = f'User {username} added successfully!'

    else:
        form = AddUserForm()
    context = {
        'companies': companies,
        'success': success,
        'error': error,
        'form': form
    }
    return render(request, 'show_user_companies.html', context)


@check_correct_user
def create_company(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = user
            company.save()
            return redirect('show_user_companies', request.user.pk)
    else:
        form = CompanyForm()
    return render(request, 'create_new_company.html', {'form': form})


@check_correct_user
def delete_company(request, user_id, company_id):
    company = check_for_object_availability(company_id, Company)
    if not company:
        return render(request, 'access/not_authorized.html')
    if not company.user == request.user:
        return render(request, 'access/not_authorized.html')
    company.delete()
    return redirect('show_user_companies', request.user.pk)


@check_correct_user
def show_company_info(request, user_id, company_id):
    success = None
    error = None
    company = check_for_object_availability(company_id, Company)
    if not company:
        return render(request, 'access/not_authorized.html')
    if company.user != request.user:
        return render(request, 'access/not_authorized.html')
    if request.method == "POST":
        if 'username' in request.POST:
            form = CompanyForm()
            username = request.POST['username']
            form_add_user = AddUserForm(request.POST)
            form_add_user.fields['username'].model_company = company
            form_add_user.fields['username'].model_user = User
            form_add_user.fields['username'].request_user = request.user
            if form_add_user.is_valid():
                new_user = User.objects.get(username=username)
                company.employee.add(new_user)
                company.save()
                success = f'You successfully added {new_user}'

        elif 'title' in request.POST:
            form_add_user = AddUserForm()
            form = CompanyForm(request.POST, instance=company)
            if form.is_valid():
                form.save()
                success = 'You successfully changed your title!'
            else:
                error = 'Invalid request!'
    else:
        form_add_user = AddUserForm()
        form = CompanyForm()

    context = {
        'company': company,
        'employees': list(company.employee.all()),
        'error': error,
        'success': success,
        'form': form,
        'form_add_user': form_add_user
    }
    return render(request, 'show_specific_company.html', context)


@check_correct_user
def remove_user(request, user_id, company_id, employee_id):
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        try:
            company = Company.objects.get(pk=company_id)
            employee = User.objects.get(pk=employee_id)
            if company.user != user or request.user != user:
                return render(request, 'access/not_authorized.html')
            company.employee.remove(employee)
            company.save()
            return redirect('show_company', request.user.pk, company.pk)
        except ObjectDoesNotExist:
            return render(request, 'access/not_authorized.html')
    else:
        return render(request, 'access/not_authorized.html')


@check_correct_user
def show_hired_by(request, user_id):
    user = User.objects.get(pk=user_id)
    companies = Company.objects.all()
    valid_companies = [c for c in companies if user in c.employee.all()]
    context = {
        'companies': valid_companies
    }
    return render(request, 'show_user_companies.html', context)


@check_correct_user
def leave_company(request, user_id, company_id):
    company = check_for_object_availability(company_id, Company)
    if not company_id:
        return render(request, 'access/not_authorized.html')
    company.employee.remove(request.user)
    return redirect('show_hired',request.user.pk)
