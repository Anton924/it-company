from datetime import date

from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.test import TestCase

from task_manager.forms import (
    TaskForm,
    TeamForm,
    WorkerCreationForm,
    WorkerUpdateForm,
    ProjectForm,
    TaskSearchField,
    TagSearchField,
    TaskTypeSearchField,
    PositionSearchField,
    TeamSearchField,
    ProjectSearchField,
    WorkerSearchField
)
from task_manager.models import (
    Task,
    Team,
    Worker,
    TaskType,
    Position,
    Project,
    Tag
)
