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


class ViewsTestMixin(TestCase):
    def setUp(self):
        position = Position.objects.create(name="project manager")
        user = Worker.objects.create(
            first_name="Admin",
            email="admin@gmail.com",
            position=position
        )
        self.client.force_login(user)


    @classmethod
    def setUpTestData(cls):
        cls.tag = Tag.objects.create(name="Bug", description="Fixing errors") # used
        cls.task_type = TaskType.objects.create(name="development") # used
        cls.pos_developer = Position.objects.create(name="developer")
        cls.pos_designer = Position.objects.create(name="designer")
        cls.worker = Worker.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            username = "ivan",
            email="ivanivanow@gmail.com",
            position=cls.pos_developer
        ) # used
        cls.workers = [
            Worker.objects.create(
                first_name="Petro",
                last_name="Sydorov",
                email="petrosydorov@gmail.com",
                username="petro",
                position=cls.pos_designer
            ),
            Worker.objects.create(
                first_name="Olga",
                last_name="Melnyk",
                email="olgamelnyk@gmail.com",
                username="olga",
                position=cls.pos_developer
            )
        ]  # used
        cls.team = Team.objects.create(
            name="Alpha",
            team_lead=cls.worker
        ) # used

        cls.team.workers.set(cls.workers)  # used

        cls.project = Project.objects.create(
            name="Mobile App",
            budget=50000,
            description="We are creating the best app ever!",
            status="IN_PROGRESS"
        ) # used

        cls.project.teams.set((cls.team,)) # used


