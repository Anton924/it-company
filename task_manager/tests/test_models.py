from django.db import models
from django.test import TestCase


from task_manager.models import (
    Tag,
    TaskType,
    Position,
    Worker,
    Team,
    Project
)


class TestMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag = Tag.objects.create(name="Bug", description="Fixing errors")
        cls.task_type = TaskType.objects.create(name="development")
        cls.position = Position.objects.create(name="project manager")
        cls.pos_developer = Position.objects.create(name="developer")
        cls.pos_designer = Position.objects.create(name="designer")
        cls.worker = Worker.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            email="ivanivanow@gmail.com",
            position=cls.pos_developer
        )
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
        ]
        cls.team = Team.objects.create(
            name="Alpha",
            team_lead=cls.worker
        )

        cls.team.workers.set(cls.workers)

        cls.project = Project.objects.create(
            name="Mobile App",
            budget=50000,
            description="We are creating the best app ever!",
            status="IN_PROGRESS"
        )

        cls.project.teams.set((cls.team,))

        cls.STATUS_CHOICES = (
            ("IN_PROCESS", "in process"),
            ("DONE", "done"),
            ("PAUSED", "paused"),
            ("CANCELED", "canceled")
        )

        cls.task = Task.objects.create(
            name="Fix Auth Bug",
            description="Need some time",
            deadline=date(2026, 2, 25),
            is_completed=False,
            priority="LOW",
            task_type=cls.task_type,
            project=cls.project
        )

        cls.task.assignees.set(cls.workers)
        cls.task.tags.set((cls.tag,))

        cls.PRIORITY_CHOICES = (
            ("CRITICAL", "Urgent"),
            ("HIGH", "High"),
            ("MEDIUM", "Medium"),
            ("LOW", "Low")
        )

class TagModelTest(TestMixin):
    def test_name_label(self):
        self.assertEqual(self.tag._meta.get_field("name").verbose_name,"name")

    def test_description_label(self):
        self.assertEqual(self.tag._meta.get_field("description").verbose_name, "description")

    def test_name_max_length(self):
        self.assertEqual(self.tag._meta.get_field("name").max_length, 255)

    def test_description_blank_state(self):
        self.assertTrue(self.tag._meta.get_field("description").blank)

    def test_object_name_is_name(self):
        self.assertEqual(str(self.tag), self.tag.name)


class TaskTypeTest(TestMixin):
    def test_name_label(self):
        self.assertEqual(self.task_type._meta.get_field("name").verbose_name, "name")

    def test_name_max_length(self):
        self.assertEqual(self.task_type._meta.get_field("name").max_length, 255)

    def test_object_name_is_name(self):
        self.assertEqual(str(self.task_type), self.task_type.name)


class PositionTest(TestMixin):
    def test_name_label(self):
        self.assertEqual(self.position._meta.get_field("name").verbose_name, "name")

    def test_name_max_length(self):
        self.assertEqual(self.position._meta.get_field("name").max_length, 255)

    def test_object_name_is_name(self):
        self.assertEqual(str(self.position), self.position.name)


class WorkerTest(TestMixin):
    def test_position_label(self):
        self.assertEqual(self.worker._meta.get_field("position").verbose_name, "position")

    def test_position_foreign_key_model(self):
        self.assertEqual(self.worker._meta.get_field("position").remote_field.model, Position)

    def test_position_on_delete_and_null_state(self):
        # Checking on_delete to be set to SET_NULL
        self.assertEqual(self.worker._meta.get_field("position").remote_field.on_delete, models.SET_NULL)
        # Checking so that field can store Null value
        self.assertTrue(self.worker._meta.get_field("position").remote_field.null)

    def test_position_related_name(self):
        self.assertEqual(self.worker._meta.get_field("position").remote_field.related_name, "workers")

    def test_object_name_is_first_name_and_last_name(self):
        object_name = f"{self.worker.first_name} {self.worker.last_name}"
        self.assertEqual(str(self.worker), object_name)


class TeamTest(TestMixin):
    def test_name_label(self):
        self.assertEqual(self.team._meta.get_field("name").verbose_name, "name")

    def test_name_max_length(self):
        self.assertEqual(self.team._meta.get_field("name").max_length, 255)

    def test_team_lead_label(self):
        self.assertEqual(self.team._meta.get_field("team_lead").verbose_name, "team lead")

    def test_team_lead_foreign_key_model(self):
        self.assertEqual(self.team._meta.get_field("team_lead").remote_field.model, Worker)

    def test_team_lead_on_delete_and_null_state(self):
        # Checking on_delete to be set to SET_NULL
        self.assertEqual(self.team._meta.get_field("team_lead").remote_field.on_delete, models.SET_NULL)
        # Checking so that field can store Null value
        self.assertTrue(self.team._meta.get_field("team_lead").remote_field.null)

    def test_team_lead_related_name(self):
        self.assertEqual(self.team._meta.get_field("team_lead").remote_field.related_name, "teams_team_lead")

    def test_workers_label(self):
        self.assertEqual(self.team._meta.get_field("workers").verbose_name, "workers")

    def test_workers_many2many_model(self):
        self.assertEqual(self.team._meta.get_field("workers").remote_field.model, Worker)

    def test_workers_related_name(self):
        self.assertEqual(self.team._meta.get_field("workers").remote_field.related_name, "teams")

    def test_object_name_is_name(self):
        self.assertEqual(str(self.team), self.team.name)


class ProjectTest(TestMixin):
    def test_name_label(self):
        self.assertEqual(self.project._meta.get_field("name").verbose_name, "name")

    def test_teams_label(self):
        self.assertEqual(self.project._meta.get_field("teams").verbose_name, "teams")

    def test_teams_foreign_key_model(self):
        self.assertEqual(self.project._meta.get_field("teams").remote_field.model, Team)

    def test_teams_foreign_key_related_name(self):
        self.assertEqual(self.project._meta.get_field("teams").remote_field.related_name, "projects")

    def test_budget_label(self):
        self.assertEqual(self.project._meta.get_field("budget").verbose_name, "budget")

    def test_description_label(self):
        self.assertEqual(self.project._meta.get_field("description").verbose_name, "description")

    def test_description_blank_state(self):
        self.assertTrue(self.project._meta.get_field("description").blank)

    def test_status_label(self):
        self.assertEqual(self.project._meta.get_field("status").verbose_name, "status")

    def test_status_max_length(self):
        self.assertEqual(self.project._meta.get_field("status").max_length, 255)

    def test_status_choices(self):
        self.assertEqual(self.project._meta.get_field("status").choices, self.STATUS_CHOICES)

    def test_object_name_is_name(self):
        self.assertEqual(str(self.project), self.project.name)


class TaskTest(TestMixin):
    def test_name_label(self):
        self.assertEqual(self.task._meta.get_field("name").verbose_name, "name")

    def test_name_max_length(self):
        self.assertEqual(self.task._meta.get_field("name").max_length, 255)

    def test_description_label(self):
        self.assertEqual(self.task._meta.get_field("description").verbose_name, "description")

    def test_deadline_label(self):
        self.assertEqual(self.task._meta.get_field("deadline").verbose_name, "deadline")

    def test_is_completed_label(self):
        self.assertEqual(self.task._meta.get_field("is_completed").verbose_name, "is completed")

    def test_priority_label(self):
        self.assertEqual(self.task._meta.get_field("priority").verbose_name, "priority")

    def test_priority_max_length(self):
        self.assertEqual(self.task._meta.get_field("priority").max_length, 255)

    def test_priority_choices(self):
        self.assertEqual(self.task._meta.get_field("priority").choices, self.PRIORITY_CHOICES)

    def test_task_type_label(self):
        self.assertEqual(self.task._meta.get_field("task_type").verbose_name, "task type")

    def test_task_type_foreign_key_model(self):
        self.assertEqual(self.task._meta.get_field("task_type").remote_field.model, TaskType)

    def test_task_type_on_delete_and_null_state(self):
        # Checking on_delete to be set to SET_NULL
        self.assertEqual(self.task._meta.get_field("task_type").remote_field.on_delete, models.SET_NULL)
        # Checking so that field can store Null value
        self.assertTrue(self.task._meta.get_field("task_type").null)

    def test_task_type_related_name(self):
        self.assertEqual(self.task._meta.get_field("task_type").remote_field.related_name, "tasks")

    def test_assignees_label(self):
        self.assertEqual(self.task._meta.get_field("assignees").verbose_name, "assignees")

    def test_assignees_many2many_model(self):
        self.assertEqual(self.task._meta.get_field("assignees").remote_field.model, Worker)

    def test_assignees_related_name(self):
        self.assertEqual(self.task._meta.get_field("assignees").remote_field.related_name, "tasks")

    def test_tags_label(self):
        self.assertEqual(self.task._meta.get_field("tags").verbose_name, "tags")

    def test_tags_many2many_model(self):
        self.assertEqual(self.task._meta.get_field("tags").remote_field.model, Tag)

    def test_tags_related_name(self):
        self.assertEqual(self.task._meta.get_field("tags").remote_field.related_name, "tasks")

    def test_project_label(self):
        self.assertEqual(self.task._meta.get_field("project").verbose_name, "project")

    def test_project_foreign_key_model(self):
        self.assertEqual(self.task._meta.get_field("project").remote_field.model, Project)

    def test_project_on_delete_and_null_state(self):
        # Checking on_delete to be set to SET_NULL
        self.assertEqual(self.task._meta.get_field("project").remote_field.on_delete, models.SET_NULL)
        # Checking so that field can store Null value
        self.assertTrue(self.task._meta.get_field("project").null)

    def test_project_blank(self):
        self.assertTrue(self.task._meta.get_field("project").blank)

    def test_project_related_name(self):
        self.assertEqual(self.task._meta.get_field("project").remote_field.related_name, "tasks")

    def test_object_name_is_name(self):
        self.assertEqual(str(self.task), self.task.name)
