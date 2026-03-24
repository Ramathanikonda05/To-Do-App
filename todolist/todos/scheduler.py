import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from django.core.mail import send_mail

def send_task_reminders():
    from .models import Task
 
    ist = pytz.timezone("Asia/Kolkata")
    now = timezone.now().astimezone(ist)
    window_start = now
    window_end = now + datetime.timedelta(minutes=1)

    # Convert window back to UTC for DB query
    window_start_utc = window_start.astimezone(pytz.UTC)
    window_end_utc = window_end.astimezone(pytz.UTC)

    tasks = Task.objects.filter(
        reminder__gte=window_start_utc,
        reminder__lt=window_end_utc
    )

    print(f"⏰ Scheduler running at {now} IST, found {tasks.count()} tasks")

    for task in tasks:
        recipients = []
        if task.owner.email:
            recipients.append(task.owner.email)
        recipients.append("ramadevithanikonda09@gmail.com") 

        send_mail(
            subject=f"Reminder: {task.title}",
            message=f"Hi {task.owner.username},\n\nThis is a reminder for your task: {task.title}\n\n{task.description}",
            from_email="ramadevithanikonda09@gmail.com",
            recipient_list=recipients,
            fail_silently=False,
        )

        print(f"📧 Sent reminder for task: {task.title} to {recipients}")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_task_reminders, "interval", minutes=1)
    scheduler.start()
    print("🚀 Scheduler started...")
