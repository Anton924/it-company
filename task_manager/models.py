from django.contrib.auth.models import AbstractUser
from django.db import models
from it_company import settings


class Tag(models.Model):
    name = models.CharField(max_length=255)

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
        related_name="workers"
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
        related_name="teams_team_lead",
        null=True
    )
    workers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="teams")


class Project(models.Model):
    name = models.CharField(max_length=255)
    teams = models.ManyToManyField(Team, related_name="projects")
    budget = models.IntegerField()

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
    deadline = models.DateField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=255,
        choices=PRIORITY_CHOICES,
        default="MEDIUM"
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")
    tags = models.ManyToManyField(Tag, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
