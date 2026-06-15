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


class TaskTypeListViewTest(LoginClientTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:task-type-list")
        number_task_types = 10
        for num in range(number_task_types):
            TaskType.objects.create(name=f"Task type {num}")

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/task-types/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/task_type_list.html")

    def test_pagination_is_nine(self):
        response = self.client.get(self.url, data={"page": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["task_type_list"]), 9)

    def test_pagination_one(self):
        response = self.client.get(self.url, data={"page": "2"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["task_type_list"]), 1)

    def test_context_data_correct(self):
        response = self.client.get(self.url, data={"name": "1"})
        self.assertIn("segment", response.context)
        self.assertEqual(response.context["segment"], "task types")
        self.assertIn("search_field", response.context)
        self.assertIsInstance(response.context["search_field"], TaskTypeSearchField)
        self.assertEqual(response.context["search_field"].initial.get("name"), "1")

    def test_queryset(self):
        response = self.client.get(reverse("task_manager:task-type-list"), data={"name": "1"})
        self.assertEqual(len(response.context["task_type_list"]), 1)
        self.assertEqual([task_type.name for task_type in response.context["task_type_list"]], ["Task type 1"])


class TaskTypeUpdateViewTest(LoginClientTestMixin, TaskTypeObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:task-type-update", kwargs={"pk": cls.task_type.id})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/task-types/{self.task_type.pk}/update/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/task_type_form.html")

    def test_task_type_update_post(self):
        update_data = {
            "name": f"Updated task type",
        }
        response = self.client.post(self.url, data=update_data)
        self.assertEqual(response.status_code, 302)
        self.task_type.refresh_from_db()
        self.assertEqual(self.task_type.name, "Updated task type")


class TaskTypeDeleteViewTest(LoginClientTestMixin, TaskTypeObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:task-type-delete", kwargs={"pk": cls.task_type.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/task-types/{self.task_type.pk}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/task_type_confirm_delete.html")

    def test_task_type_deletion_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TaskType.objects.filter(name="Task type").exists())


class TaskTypeCreateViewTest(LoginClientTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:task-type-create")

        cls.task_type = {
            "name": "Task type"
        }

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/task-types/create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/task_type_form.html")

    def test_task_type_create_post(self):
        response = self.client.post(self.url, data=self.task_type)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(TaskType.objects.filter(name="Task type").exists())

    def test_task_type_create_invalid_data(self):
        invalid_data = {
            "name": ""
        }
        response = self.client.post(self.url, data=invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(TaskType.objects.filter(name="").exists())


class TagListViewTest(LoginClientTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:tag-list")
        number_tags = 10
        for num in range(number_tags):
            Tag.objects.create(name=f"Tag {num}")

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/tags/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/tag_list.html")

    def test_pagination_is_nine(self):
        response = self.client.get(self.url, data={"page": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["tag_list"]), 9)

    def test_pagination_one(self):
        response = self.client.get(self.url, data={"page": "2"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["tag_list"]), 1)

    def test_context_data_correct(self):
        response = self.client.get(self.url, data={"name": "1"})
        self.assertIn("segment", response.context)
        self.assertEqual(response.context["segment"], "tags")
        self.assertIn("search_field", response.context)
        self.assertIsInstance(response.context["search_field"], TagSearchField)
        self.assertEqual(response.context["search_field"].initial.get("name"), "1")

    def test_queryset(self):
        response = self.client.get(self.url, data={"name": "1"})
        self.assertEqual(len(response.context["tag_list"]), 1)
        self.assertEqual([tag.name for tag in response.context["tag_list"]], ["Tag 1"])


class TagUpdateViewTest(LoginClientTestMixin, TagObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:tag-update", kwargs={"pk": cls.tag.id})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/tags/{self.tag.pk}/update/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/tag_form.html")

    def test_tag_update_post(self):
        update_data = {
            "name": f"Updated tag",
        }
        response = self.client.post(self.url, data=update_data)
        self.assertEqual(response.status_code, 302)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, "Updated tag")


class TagDeleteViewTest(LoginClientTestMixin, TagObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:tag-delete", kwargs={"pk": cls.tag.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/tags/{self.tag.pk}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/tag_confirm_delete.html")

    def test_tag_deletion_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TaskType.objects.filter(name="Tag").exists())


class TagCreateViewTest(LoginClientTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:tag-create")

        cls.tag = {
            "name": "Tag"
        }

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/tags/create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/tag_form.html")

    def test_tag_create_post(self):
        response = self.client.post(self.url, data=self.tag)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tag.objects.filter(name="Tag").exists())

    def test_tag_create_invalid_data(self):
        invalid_data = {
            "name": ""
        }
        response = self.client.post(self.url, data=invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tag.objects.filter(name="").exists())


class PositionListViewTest(LoginClientTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:position-list")
        number_positions = 10
        for num in range(number_positions):
            Position.objects.create(name=f"Position {num}")

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/positions/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/position_list.html")

    def test_pagination_is_nine(self):
        response = self.client.get(self.url, data={"page": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["position_list"]), 9)

    def test_pagination_one(self):
        response = self.client.get(self.url, data={"page": "2"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["position_list"]), 2) # one more was created in LoginClientTestMixin

    def test_context_data_correct(self):
        response = self.client.get(self.url, data={"name": "1"})
        self.assertIn("segment", response.context)
        self.assertEqual(response.context["segment"], "positions")
        self.assertIn("search_field", response.context)
        self.assertIsInstance(response.context["search_field"], PositionSearchField)
        self.assertEqual(response.context["search_field"].initial.get("name"), "1")

    def test_queryset(self):
        response = self.client.get(self.url, data={"name": "1"})
        self.assertEqual(len(response.context["position_list"]), 1)
        self.assertEqual([task_type.name for task_type in response.context["position_list"]], ["Position 1"])


class PositionUpdateViewTest(LoginClientTestMixin, PositionObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:position-update", kwargs={"pk": cls.position.id})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/positions/{self.position.pk}/update/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/position_form.html")

    def test_position_update_post(self):
        update_data = {
            "name": f"Updated position",
        }
        response = self.client.post(self.url, data=update_data)
        self.assertEqual(response.status_code, 302)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Updated position")


class PositionDeleteViewTest(LoginClientTestMixin, PositionObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:position-delete", kwargs={"pk": cls.position.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/positions/{self.position.pk}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/position_confirm_delete.html")

    def test_position_deletion_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Position.objects.filter(name="project manager").exists())


class PositionCreateViewTest(LoginClientTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:position-create")

        cls.position = {
            "name": "Position"
        }

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/positions/create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/position_form.html")

    def test_position_create_post(self):
        response = self.client.post(self.url, data=self.position)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Position.objects.filter(name="Position").exists())

    def test_position_create_invalid_data(self):
        invalid_data = {
            "name": ""
        }
        response = self.client.post(self.url, data=invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Position.objects.filter(name="").exists())


class TeamListViewTest(LoginClientTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        number_teams = 10
        pos_developer = Position.objects.create(name="developer")
        worker = Worker.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            username="ivan",
            email="ivanivanow@gmail.com",
            position=pos_developer
        )
        for num in range(number_teams):
            Team.objects.create(
                name=f"Team {num}",
                team_lead=worker
            )
        cls.url = reverse("task_manager:team-list")

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/teams/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/team_list.html")

    def test_pagination_is_nine(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["team_list"]), 9)

    def test_pagination_is_one(self):
        response = self.client.get(self.url, data={"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["team_list"]), 1)

    def test_context_data(self):
        response = self.client.get(self.url, data={"name": "n"})
        self.assertIn("segment", response.context)
        self.assertEqual(response.context["segment"], "teams")
        self.assertIn("search_field", response.context)
        self.assertIsInstance(response.context["search_field"], TeamSearchField)
        self.assertEqual(response.context["search_field"].initial.get("name"), "n")

    def test_queryset(self):
        response = self.client.get(self.url, data={"name": "1"})

        self.assertEqual(len(response.context["team_list"]), 1)
        self.assertEqual([team.name for team in response.context["team_list"]], ["Team 1"])


class TeamUpdateViewTest(LoginClientTestMixin, TeamObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:team-update", kwargs={"pk": cls.team.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/teams/{self.team.pk}/update/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/team_form.html")

    def test_team_update_post(self):
        update_data = {
            "name": "Updated team",
            "team_lead": self.worker.pk
        }
        response = self.client.post(self.url, data=update_data)
        self.assertEqual(response.status_code, 302)
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, "Updated team")


class TeamDetailViewTest(LoginClientTestMixin, TeamObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:team-detail", kwargs={"pk": cls.team.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/teams/{self.team.pk}/detail/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/team_detail.html")


class TeamDeleteViewTest(LoginClientTestMixin, TeamObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:team-delete", kwargs={"pk": cls.team.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/teams/{self.team.pk}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/team_confirm_delete.html")

    def test_team_deletion_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Team.objects.filter(name="Team").exists())


class TeamCreateViewTest(LoginClientTestMixin, TeamObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.team_data = {
            "name": "Alpha",
            "team_lead": cls.worker.pk
        }
        cls.url = reverse("task_manager:team-create")

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/teams/create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/team_form.html")

    def test_team_create_post(self):
        response = self.client.post(self.url, data=self.team_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Team.objects.filter(name="Alpha").exists())

    def test_team_create_invalid_data(self):
        invalid_data = {
            "name": ""
        }
        response = self.client.post(self.url, data=invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Team.objects.filter(name="").exists())
# ------------------

class WorkerListViewTest(LoginClientTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        number_workers = 10 # also one from LoginClientTestMixin
        pos_developer = Position.objects.create(name="developer")
        chars = "abcdefghij"
        if len(chars) == number_workers:
            for char in chars:
                Worker.objects.create(
                    first_name=f"{char}",
                    last_name=f"{char}",
                    username=f"username {char}",
                    position=pos_developer
                )
        cls.url = reverse("task_manager:worker-list")

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/workers/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/worker_list.html")

    def test_pagination_is_nine(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["worker_list"]), 9)

    def test_pagination_is_one(self):
        response = self.client.get(self.url, data={"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["worker_list"]), 2) # the second one it is loigin user

    def test_context_data(self):
        response = self.client.get(self.url, data={"full_name": "n"})
        self.assertIn("segment", response.context)
        self.assertEqual(response.context["segment"], "workers")
        self.assertIn("search_field", response.context)
        self.assertIsInstance(response.context["search_field"], WorkerSearchField)
        self.assertEqual(response.context["search_field"].data.get("full_name"), "n")

    def test_queryset(self):
        response = self.client.get(self.url, data={"full_name": "a"})
        self.assertEqual(len(response.context["worker_list"]), 1)
        self.assertEqual([worker.first_name for worker in response.context["worker_list"]], ["a"])


class WorkerUpdateViewTest(LoginClientTestMixin, WorkerObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:worker-update", kwargs={"pk": cls.worker.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/workers/{self.worker.pk}/update/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/worker_form.html")

    def test_team_update_post(self):
        update_data = {
            "first_name": "Updated_first_name",
            "last_name": "Ivanov",
            "username": "ivan",
            "email": "ivanivanow@gmail.com",
            "position": self.pos_developer.pk
        }
        response = self.client.post(self.url, data=update_data)
        self.assertEqual(response.status_code, 302)
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.first_name, "Updated_first_name")


class WorkerDetailViewTest(LoginClientTestMixin, WorkerObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:worker-detail", kwargs={"pk": cls.worker.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/workers/{self.worker.pk}/detail/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/worker_detail.html")


class WorkerDeleteViewTest(LoginClientTestMixin, WorkerObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:worker-delete", kwargs={"pk": cls.worker.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/workers/{self.worker.pk}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/worker_confirm_delete.html")

    def test_team_deletion_post(self):
        self.assertTrue(Worker.objects.filter(first_name="Ivan").exists())
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Worker.objects.filter(first_name="Ivan").exists())


class WorkerCreateViewTest(LoginClientTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.worker_data = {
            "first_name": "Anton",
            "last_name": "Ivanov",
            "username": "ivan",
            "email": "ivanivanow@gmail.com",
            "position": cls.position.pk,
            "password1": "Ivan12345",
            "password2": "Ivan12345",
        }
        cls.url = reverse("task_manager:worker-create")

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/workers/create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/worker_form.html")

    def test_team_create_post(self):
        response = self.client.post(self.url, data=self.worker_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Worker.objects.filter(first_name="Anton").exists())

    def test_team_create_invalid_data(self):
        invalid_data = {
            "first_name": ""
        }
        response = self.client.post(self.url, data=invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Worker.objects.filter(first_name="").exists())

# ----------------------------------------------
class ProjectListViewTest(LoginClientTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        number_projects = 10
        for num in range(number_projects):
            Project.objects.create(
                name=f"Project {num}",
                budget=1000,
                description="Working with team",
                status="IN_PROCESS",
            )
        cls.url = reverse("task_manager:project-list")

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/projects/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/project_list.html")

    def test_pagination_is_nine(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["project_list"]), 9)

    def test_pagination_is_one(self):
        response = self.client.get(self.url, data={"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["project_list"]), 1)

    def test_context_data(self):
        response = self.client.get(self.url, data={"name": "n"})
        self.assertIn("segment", response.context)
        self.assertEqual(response.context["segment"], "projects")
        self.assertIn("search_field", response.context)
        self.assertIsInstance(response.context["search_field"], ProjectSearchField)
        self.assertEqual(response.context["search_field"].data.get("name"), "n")

    def test_queryset(self):
        response = self.client.get(self.url, data={"name": "1"})
        self.assertEqual(len(response.context["project_list"]), 1)
        self.assertEqual([project.name for project in response.context["project_list"]], ["Project 1"])


class ProjectUpdateViewTest(LoginClientTestMixin, ProjectObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:project-update", kwargs={"pk": cls.project.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/projects/{self.project.pk}/update/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/project_form.html")

    def test_team_update_post(self):
        update_data = {
            "name": "Updated Project",
            "budget": 1000,
            "description": "Working with team",
            "status": "IN_PROCESS",
        }
        response = self.client.post(self.url, data=update_data)
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Updated Project")


class ProjectDetailViewTest(LoginClientTestMixin, ProjectObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:project-detail", kwargs={"pk": cls.project.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/projects/{self.project.pk}/detail/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/project_detail.html")


class ProjectDeleteViewTest(LoginClientTestMixin, ProjectObjectCreatingMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("task_manager:project-delete", kwargs={"pk": cls.project.pk})

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f"/projects/{self.project.pk}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/project_confirm_delete.html")

    def test_team_deletion_post(self):
        self.assertTrue(Project.objects.filter(name="Project").exists())
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(name="Project").exists())


class ProjectCreateViewTest(LoginClientTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.project_data = {
            "name": "New Project",
            "budget": 1000,
            "description": "Working with team",
            "status": "IN_PROCESS",
        }
        cls.url = reverse("task_manager:project-create")

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/projects/create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/project_form.html")

    def test_team_create_post(self):
        response = self.client.post(self.url, data=self.project_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(name="New Project").exists())

    def test_team_create_invalid_data(self):
        invalid_data = {
            "name": ""
        }
        response = self.client.post(self.url, data=invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Project.objects.filter(name="").exists())
