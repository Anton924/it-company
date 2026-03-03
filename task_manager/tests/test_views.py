from datetime import date

from django.test import TestCase
from django.urls import reverse

from task_manager.models import (
    Tag,
    TaskType,
    Position,
    Worker,
    Team,
    Project,
    Task
)


