
from django.utils import timezone
from django.core.mail import send_mail
from .models import Task

def send_task_reminders():
    now = timezone.now()
    tasks = Task.objects.filter(reminder_time__lte=now, status="Pending")

    for task in tasks:
        if task.owner and task.owner.email:  # only if user has email
            send_mail(
                subject=f"Reminder: {task.title}",
                message=f"Hi {task.owner.username},\n\n"
                        f"This is a reminder for your task:\n\n"
                        f"{task.title}\n{task.description}\n\n"
                        f"Due at: {task.reminder_time}",
                from_email=None,
                recipient_list=[task.owner.email],
            )
