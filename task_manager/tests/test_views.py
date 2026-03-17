from datetime import date

from django.test import TestCase
from django.urls import reverse

from task_manager.forms import (
    TaskSearchField,
    TaskTypeSearchField,
    TagSearchField,
    PositionSearchField,
    TeamSearchField,
    WorkerSearchField,
    ProjectSearchField
)
from task_manager.models import (
    Tag,
    TaskType,
    Position,
    Worker,
    Team,
    Project,
    Task
)


class LoginClientTestMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.position = Position.objects.create(name="project manager")
        cls.user = Worker.objects.create(
            first_name="User", # for testing worker list view, the first_name or last_name can not have letter "a"
            email="admin@gmail.com",
            position=cls.position
        )
    def setUp(self):
        self.client.force_login(self.user)


class TaskObjectCreationMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.tag = Tag.objects.create(name="Bug", description="Fixing errors")
        cls.task_type = TaskType.objects.create(name="development")  # used
        cls.pos_developer = Position.objects.create(name="developer")
        cls.pos_designer = Position.objects.create(name="designer")
        cls.worker = Worker.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            username="ivan",
            email="ivanivanow@gmail.com",
            position=cls.pos_developer
        )  # used
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
        )  # used

        cls.team.workers.set(cls.workers)  # used

        cls.project = Project.objects.create(
            name="Mobile App",
            budget=50000,
            description="We are creating the best app ever!",
            status="IN_PROGRESS"
        )  # used

        cls.project.teams.set((cls.team,))


class TaskTypeObjectCreatingMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.task_type = TaskType.objects.create(name="Task type")


class TagObjectCreatingMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.tag = Tag.objects.create(name="Tag")


class PositionObjectCreatingMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.position = Position.objects.create(
            name="Position"
        )


class TeamObjectCreatingMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pos_developer = Position.objects.create(name="developer")
        cls.worker = Worker.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            username="ivan",
            email="ivanivanow@gmail.com",
            position=pos_developer
        )
        cls.team = Team.objects.create(
            name="Team",
            team_lead=cls.worker
        )

class WorkerObjectCreatingMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.pos_developer = Position.objects.create(name="developer")
        cls.worker = Worker.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            username="ivan",
            email="ivanivanow@gmail.com",
            position=cls.pos_developer
        )


class ProjectObjectCreatingMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(
            name="Project",
            budget=1000,
            description="Working with team",
            status="IN_PROCESS",
        )

class TaskListViewTest(LoginClientTestMixin, TaskObjectCreationMixin):
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
        cls.url = reverse("task_manager:task-list")

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_pagination_is_nine(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["task_list"]), 9)

    def test_pagination_is_one(self):
        response = self.client.get(self.url, data={"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["task_list"]), 1)

    def test_context_data(self):
        response = self.client.get(self.url, data={"name": "n"})
        self.assertIn("segment", response.context)
        self.assertEqual(response.context["segment"], "tasks")
        self.assertIn("search_field", response.context)
        self.assertIsInstance(response.context["search_field"], TaskSearchField)
        self.assertEqual(response.context["search_field"].initial.get("name"), "n")

    def test_queryset(self):
        response = self.client.get(self.url, data={"name": "1"})

        self.assertEqual(len(response.context["task_list"]), 1)
        self.assertEqual([task.name for task in response.context["task_list"]], ["Task 1"])


class TaskUpdateViewTest(LoginClientTestMixin, TaskObjectCreationMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.task = Task.objects.create(
            name="Task",
            description="Need some time",
            deadline=date(2026, 2, 25),
            is_completed=False,
            priority="LOW",
            task_type=cls.task_type,
            project=cls.project
        )

        cls.url = reverse("task_manager:task-update", kwargs={"pk": cls.task.id})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/tasks/{self.task.pk}/update/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/task_form.html")

    def test_task_update_post(self):
        update_data = {
            "name": "Updated task",
            "description": "Need some time",
            "deadline": date(2026, 2, 25),
            "is_completed": False,
            "priority": "LOW",
            "task_type": self.task_type.id,
            "project": self.project.id,
            "tags": [self.tag.id],
            "assignees": [worker.pk for worker in self.workers]
        }
        response = self.client.post(self.url, data=update_data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated task")


class TaskDetailViewTest(LoginClientTestMixin, TaskObjectCreationMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.task = Task.objects.create(
            name="Task",
            description="Need some time",
            deadline=date(2026, 2, 25),
            is_completed=False,
            priority="LOW",
            task_type=cls.task_type,
            project=cls.project
        )
        cls.url = reverse("task_manager:task-detail", kwargs={"pk": cls.task.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/tasks/{self.task.pk}/detail/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/task_detail.html")


class TaskDeleteViewTest(LoginClientTestMixin, TaskObjectCreationMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.task = Task.objects.create(
            name="Task",
            description="Need some time",
            deadline=date(2026, 2, 25),
            is_completed=False,
            priority="LOW",
            task_type=cls.task_type,
            project=cls.project
        )

        cls.url = reverse("task_manager:task-delete", kwargs={"pk": cls.task.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/tasks/{self.task.pk}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/task_confirm_delete.html")

    def test_task_deletion_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name="Task").exists())


class TaskCreateViewTest(LoginClientTestMixin, TaskObjectCreationMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:task-create")

        cls.task = {
            "name": "Task",
            "description": "Need some time",
            "deadline": date(2026, 2, 25),
            "is_completed": False,
            "priority": "LOW",
            "task_type": cls.task_type.id,
            "project": cls.project.id,
            "tags": [cls.tag.id],
            "assignees": [worker.pk for worker in cls.workers]
        }

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/tasks/create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/task_form.html")

    def test_task_create_post(self):
        response = self.client.post(self.url, data=self.task)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="Task").exists())

    def test_task_create_invalid_data(self):
        invalid_data = {
            "name": ""
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(name="").exists())


class CheckInLoggedInLoggedOutRedirection(TestCase):
    def test_user_logged_out_redirection(self):
        response = self.client.get(reverse("task_manager:task-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/tasks/")

    def test_user_logged_in(self):
        pos_developer = Position.objects.create(name="developer")
        worker = Worker.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            username="ivan",
            email="ivanivanow@gmail.com",
            position=pos_developer
        )
        self.client.force_login(worker)
        response = self.client.get(reverse("task_manager:task-list"))
        self.assertTrue(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "Ivan Ivanov")
        self.assertTemplateUsed(response, "task_manager/task_list.html")



