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


class TestFormMixin(TestCase):
    def create_all(self):
        self.tag = Tag.objects.create(name="Bug", description="Fixing errors")

        self.task_type = TaskType.objects.create(name="development")
        self.pos_developer = Position.objects.create(name="developer")
        self.pos_designer = Position.objects.create(name="designer")

        self.worker = Worker.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            username="ivan",
            email="ivanivanow@gmail.com",
            position=self.pos_developer
        )
        self.team = Team.objects.create(
                        name="Alpha",
                        team_lead=self.worker
                    )
        self.project = Project.objects.create(
            name="Mobile App",
            budget=50000,
            description="We are creating the best app ever!",
            status="IN_PROGRESS"
        )
        self.project.teams.set((self.team,))

        self.workers = [
            Worker.objects.create(
                first_name="Petro",
                last_name="Sydorov",
                email="petrosydorov@gmail.com",
                username="petro",
                position=self.pos_developer
            ),
            Worker.objects.create(
                first_name="Olga",
                last_name="Melnyk",
                email="olgamelnyk@gmail.com",
                username="olga",
                position=self.pos_designer
            )
        ]

    @property
    def task_data(self):
        return {
            "name": "Fix Auth Bug",
            "description": "Need some time",
            "deadline": date(2026, 2, 25),
            "is_completed": False,
            "priority": "LOW",
            "task_type": self.task_type.pk,
            "project": self.project.pk,
            "tags": [self.tag.pk],
            "assignees": [worker.pk for worker in self.workers]
        }

    @property
    def team_data(self):
        return {
            "name": "Alpha",
            "team_lead": self.worker.pk,
            "workers": [worker.pk for worker in self.workers]
        }

    @property
    def worker_data(self):
        return {
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "username": "ivan",
            "email": "ivanivanow@gmail.com",
            "position": self.pos_developer,
            "password1": "Password1234!",
            "password2": "Password1234!"
        }

    @property
    def worker_update_data(self):
        return  {
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": "ivanivanow@gmail.com",
            "position": self.pos_developer,
        }

    @property
    def project_data(self):
        return {
            "name": "Mobile App",
            "budget": 50000,
            "description": "We are creating the best app ever!",
            "status": "IN_PROCESS",
            "teams": [team.pk for team in (self.team,)]
        }


