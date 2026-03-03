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


class TaskListViewTest(ViewsTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        number_tasks = 10

        for task_id in range(number_tasks):
            Task.objects.create(
                name=f"Task {task_id}",
                description="Need some time",
                deadline=date(2026, 2, 25),
                is_completed=False,
                priority="LOW",
                task_type=cls.task_type,
                project=cls.project
            )

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("task_manager:task-list"))
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(reverse("task_manager:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_pagination_is_nine(self):
        response = self.client.get(reverse("task_manager:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["task_list"]), 9)

    def test_pagination_is_one(self):
        response = self.client.get(reverse("task_manager:task-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["task_list"]), 1)

    def test_context_data(self):
        response = self.client.get(reverse("task_manager:task-list"))
        self.assertIn("segment", response.context)


