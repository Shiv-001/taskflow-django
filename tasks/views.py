from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from .models import Task, Category
from .forms import TaskForm, CategoryForm, RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        if User.objects.filter(username=username).exists():
            form.add_error('username', 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, password=password)
            # Create default categories
            Category.objects.create(name='Work', color='#3b82f6', user=user)
            Category.objects.create(name='Personal', color='#10b981', user=user)
            Category.objects.create(name='Urgent', color='#ef4444', user=user)
            login(request, user)
            return redirect('dashboard')
    return render(request, 'tasks/register.html', {'form': form})


@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)

    # Filters
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('q', '')

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if category_filter:
        tasks = tasks.filter(category_id=category_filter)
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    # Stats
    all_tasks = Task.objects.filter(user=request.user)
    stats = {
        'total': all_tasks.count(),
        'todo': all_tasks.filter(status='todo').count(),
        'in_progress': all_tasks.filter(status='in_progress').count(),
        'done': all_tasks.filter(status='done').count(),
        'overdue': sum(1 for t in all_tasks if t.is_overdue),
    }

    categories = Category.objects.filter(user=request.user)

    context = {
        'tasks': tasks,
        'stats': stats,
        'categories': categories,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'category_filter': category_filter,
        'search_query': search_query,
    }
    return render(request, 'tasks/dashboard.html', context)


@login_required
def task_create(request):
    form = TaskForm(user=request.user, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, 'Task created!')
        return redirect('dashboard')
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    form = TaskForm(user=request.user, data=request.POST or None, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Task updated!')
        return redirect('dashboard')
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Edit', 'task': task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('dashboard')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_toggle_status(request, pk):
    """Quick status toggle via AJAX or redirect."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if task.status == 'done':
        task.status = 'todo'
    else:
        task.status = 'done'
    task.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': task.status})
    return redirect('dashboard')


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user).annotate(task_count=Count('tasks'))
    form = CategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cat = form.save(commit=False)
        cat.user = request.user
        cat.save()
        messages.success(request, 'Category created!')
        return redirect('categories')
    return render(request, 'tasks/categories.html', {'categories': categories, 'form': form})


@login_required
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Category deleted.')
    return redirect('categories')
