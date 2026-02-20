from django.test import TestCase


from task_manager.models import Tag


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

    def test_object_name_is_name(self):
        self.assertEqual(str(self.tag), self.tag.name)



