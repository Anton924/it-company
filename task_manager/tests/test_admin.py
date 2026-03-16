from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position


class AdminPanelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="12345678"
        )
        pos_developer = Position.objects.create(name="developer")
        cls.worker = get_user_model().objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            username="ivan",
            email="ivanivanow@gmail.com",
            position=pos_developer
        )

    def setUp(self):
        self.client.force_login(self.admin)

    def test_worker_position_listed(self):
        response = self.client.get(reverse("admin:task_manager_worker_changelist"))
        self.assertContains(response, self.worker.position)

    def test_worker_detail_position_listed(self):
        response = self.client.get(reverse("admin:task_manager_worker_change", args=(self.worker.pk,)))
        self.assertContains(response, self.worker.position)

    def test_worker_create_position_listed(self):
        response = self.client.get(reverse("admin:task_manager_worker_add"))
        self.assertContains(response, self.worker.position)

