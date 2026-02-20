from django.test import TestCase


from task_manager.models import Tag, TaskType, Position


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