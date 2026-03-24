from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from todos.models import Task
from datetime import timedelta

class Command(BaseCommand):
    help = "Send reminders for upcoming tasks"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        reminder_before = timedelta(minutes=10)  # change this (e.g., 30 for half-hour before)

        upcoming_tasks = Task.objects.filter(
            reminder_time__range=(now + reminder_before, now + reminder_before + timedelta(minutes=1))
        )

        for task in upcoming_tasks:
            send_mail(
                subject=f"Reminder: {task.title}",
                message=f"Hi, don't forget your task: {task.title}\n\n{task.description}",
                from_email="tatikondasravya9@gmail.com",
                recipient_list=["tatikondasravya9@gmail.com"],  # ideally, task.user.email
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"Reminder sent for task: {task.title}"))
