from datetime import timedelta, date

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


def default_deadline():
    return date.today() + timedelta(days=10)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        related_name="workers",
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

class Team(models.Model):
    name = models.CharField(max_length=255)
    team_lead = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="teams_team_lead",
        blank=True
    )
    workers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="teams", blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = (
        ("IN_PROCESS", "in process"),
        ("DONE", "done"),
        ("PAUSED", "paused"),
        ("CANCELED", "canceled")
    )
    name = models.CharField(max_length=255)
    teams = models.ManyToManyField(Team, related_name="projects", blank=True)
    budget = models.IntegerField()
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        default="IN_PROCESS"
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("CRITICAL", "Urgent"),
        ("HIGH", "High"),
        ("MEDIUM", "Medium"),
        ("LOW", "Low")
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField(default=default_deadline)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=255,
        choices=PRIORITY_CHOICES,
        default="MEDIUM"
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, related_name="tasks", null=True, blank=True)
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")
    tags = models.ManyToManyField(Tag, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")

    def __str__(self):
        return self.name
