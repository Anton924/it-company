from django.db import models
from django.test import TestCase


from task_manager.models import (
    Tag,
    TaskType,
    Position,
    Worker,
    Team
)


class TagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag = Tag.objects.create(name="Bug", description="Fixing errors")

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


class TaskTypeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.task_type = TaskType.objects.create(name="development")

    def test_name_label(self):
        self.assertEqual(self.task_type._meta.get_field("name").verbose_name, "name")

    def test_name_max_length(self):
        self.assertEqual(self.task_type._meta.get_field("name").max_length, 255)

    def test_object_name_is_name(self):
        self.assertEqual(str(self.task_type), self.task_type.name)


class PositionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="project manager")

    def test_name_label(self):
        self.assertEqual(self.position._meta.get_field("name").verbose_name, "name")

    def test_name_max_length(self):
        self.assertEqual(self.position._meta.get_field("name").max_length, 255)

    def test_object_name_is_name(self):
        self.assertEqual(str(self.position), self.position.name)


class WorkerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pos_developer = Position.objects.create(name="developer")
        cls.worker = Worker.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            email="ivanivanow@gmail.com",
            position=pos_developer
        )

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


class TeamTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pos_developer = Position.objects.create(name="developer")
        pos_designer = Position.objects.create(name="designer")
        team_lead = Worker.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            email="ivanivanow@gmail.com",
            username="ivan",
            position=pos_developer
        )
        workers = [
            Worker.objects.create(
                first_name="Petro",
                last_name="Sydorov",
                email="petrosydorov@gmail.com",
                username="petro",
                position=pos_designer
            ),
            Worker.objects.create(
                first_name="Olga",
                last_name="Melnyk",
                email="olgamelnyk@gmail.com",
                username="olga",
                position=pos_developer
            )
        ]
        cls.team = Team.objects.create(
            name="Alpha",
            team_lead=team_lead
        )

        cls.team.workers.set(workers)


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

