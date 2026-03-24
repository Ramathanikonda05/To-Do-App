from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone   
from .models import Task
from .forms import TaskForm, UserRegisterForm

from datetime import timedelta


@login_required
def task_list(request):
    # Show only tasks of the logged-in user
    tasks = Task.objects.filter(owner=request.user)
    return render(request, 'todos/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()

            recipients = []
            if request.user.email:  # if user has email
                recipients.append(request.user.email)
            
            # always add your Gmail
            recipients.append("ramadevithanikonda09@gmail.com")

            send_mail(
                subject=f"Task Created: {task.title}",
                message=f"Your task '{task.title}' was created successfully.",
                from_email="ramadevithanikonda09@gmail.com",
                recipient_list=recipients,
                fail_silently=False,
            )

            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "todos/task_form.html", {"form": form})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todos/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    return render(request, 'todos/task_confirm_delete.html', {'task': task})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # log in new user immediately
            return redirect("task_list")
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def toggle_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    # Cycle through statuses
    if task.status == Task.Status.TODO:
        task.status = Task.Status.IN_PROGRESS
    elif task.status == Task.Status.IN_PROGRESS:
        task.status = Task.Status.COMPLETE
    else:
        task.status = Task.Status.TODO

    task.save()
    return redirect("task_list")

