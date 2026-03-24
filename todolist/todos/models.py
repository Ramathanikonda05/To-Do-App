from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "TODO", "Todo"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETE = "COMPLETE", "Complete"

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    user_task_number = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    reminder = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only assign when creating a new task
            last_task = Task.objects.filter(owner=self.owner).order_by("-user_task_number").first()
            self.user_task_number = (last_task.user_task_number + 1) if last_task else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.owner.username} - {self.title}"
