from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from it_company import settings


class Tag(models.Model):
    name = models.CharField(max_length=255)


class TaskType(models.Model):
    name = models.CharField(max_length=255)


class Position(models.Model):
    name = models.CharField(max_length=255)


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        related_name="workers"
    )


class Task(models.Model):

    PRIORITY_CHOICES = (
        ("CRITICAL", "Urgent"),
        ("HIGH", "High"),
        ("MEDIUM", "Medium"),
        ("LOW", "Low")
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=255,
        choices=PRIORITY_CHOICES, default="MEDIUM"
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")
    tags = models.ManyToManyField(Tag, related_name="tasks")


class Team(models.Model):
    name = models.CharField(max_length=255)
    team_lead = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="teams_team_lead", null=True
    )
    workers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="teams")


class Project(models.Model):
    name = models.CharField(max_length=255)
    tasks = models.ManyToManyField(Task, related_name="projects") # I have to decide to user many2many or foreignkey
    teams = models.ManyToManyField(Team, related_name="projects")
