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


class TaskFormTest(TestFormMixin):
    def setUp(self):
        self.create_all()
        self.form = TaskForm()

    def test_task_form_labels_are_customized(self):
        self.assertEqual(self.form.fields["task_type"].empty_label, "Choose type of task...")
        self.assertEqual(self.form.fields["project"].empty_label, "Choose project this task belong...")

    def test_task_widgets_are_correct(self):
        self.assertIsInstance(self.form.fields["tags"].widget, CheckboxSelectMultiple)
        self.assertIsInstance(self.form.fields["assignees"].widget, CheckboxSelectMultiple)
        self.assertEqual(self.form.fields["deadline"].widget.__class__.__name__, "DateTimeInput")
        self.assertEqual(self.form.fields["deadline"].widget.format, "%Y-%m-%d")
        html = str(self.form["deadline"])
        self.assertIn('type="date"', html)

    def test_task_form_model(self):
        self.assertEqual(self.form.Meta.model, Task)

    def test_task_form_valid_data(self):
        form = TaskForm(data=self.task_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_task_form_invalid_data(self):
        test_data = self.task_data
        test_data["name"] = ""
        form = TaskForm(data=test_data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn("name", form.errors)



class TeamFormTest(TestFormMixin):
    def setUp(self):
        self.create_all()
        self.form = TeamForm()

    def test_team_form_label_customized(self):
        self.assertEqual(self.form.fields["team_lead"].empty_label, "Choose team leader...")

    def test_team_widgets_are_correct(self):
        self.assertIsInstance(self.form.fields["workers"].widget, CheckboxSelectMultiple)

    def test_team_form_model(self):
        self.assertEqual(self.form.Meta.model, Team)

    def test_team_form_valid_data(self):
        form = TeamForm(self.team_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_team_form_invalid_data(self):
        test_data = self.team_data
        test_data["name"] = ""
        form = TeamForm(test_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class WorkerCreationFormTest(TestFormMixin):
    def setUp(self):
        self.create_all()
        self.form = WorkerCreationForm()

    def test_worker_create_form_label_customized(self):
        self.assertEqual(self.form.fields["position"].empty_label, "Choose position...")

    def test_worker_create_form_model(self):
        self.assertEqual(self.form.Meta.model, Worker)

    def test_worker_create_form_valid_data(self):
        form = WorkerCreationForm(self.worker_data)

        self.assertTrue(form.is_valid(), form.errors)

    def test_worker_create_form_invalid_data(self):
        test_data = self.worker_data
        test_data["password1"] = ""
        form = WorkerCreationForm(test_data)

        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)


class WorkerUpdateFormTest(TestFormMixin):
    def setUp(self):
        self.create_all()
        self.form = WorkerUpdateForm()

    def test_worker_update_form_model(self):
        self.assertEqual(self.form.Meta.model, Worker)

    def test_worker_update_form_fields(self):
        fields = (
            "first_name",
            "last_name",
            "email",
            "position",
        )

        self.assertEqual(self.form.Meta.fields, fields)

    def test_worker_update_form_valid_data(self):
        form = WorkerUpdateForm(self.worker_update_data)
        self.assertTrue(form.is_valid())


class ProjectFormTest(TestFormMixin):
    def setUp(self):
        self.create_all()
        self.form = ProjectForm()

    def test_project_widgets_are_correct(self):
        self.assertIsInstance(self.form.fields["teams"].widget, CheckboxSelectMultiple)

    def test_project_form_model(self):
        self.assertEqual(self.form.Meta.model, Project)

    def test_project_form_valid_data(self):
        form = ProjectForm(self.project_data)

        self.assertTrue(form.is_valid(), form.errors)

    def test_project_form_invalid_data(self):
        test_data = self.project_data
        test_data["name"] = ""
        form = ProjectForm(test_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TaskSearchFieldTest(TestCase):
    def setUp(self):
        self.test_forms = [
            TaskSearchField(),
            TagSearchField(),
            TaskTypeSearchField(),
            PositionSearchField(),
            TeamSearchField(),
            ProjectSearchField()
        ]

    def test_search_form_field_not_required(self):
        for form in self.test_forms:
            self.assertFalse(form.fields["name"].required)

    def test_search_form_field_label(self):
        for form in self.test_forms:
            self.assertEqual(form.fields["name"].label, "")

    def test_search_widget_are_correct(self):
        for form in self.test_forms:
            self.assertIsInstance(form.fields["name"].widget, forms.TextInput)

    def test_task_search_form_widget_attributes_correct(self):
        placeholders = [
            "Enter name of the task...",
            "Enter name of the tag...",
            "Enter name of the task type...",
            "Enter name of the position...",
            "Enter name of the team...",
            "Enter name of the project..."
        ]
        for idx in range(len(self.test_forms)):
            self.assertEqual(self.test_forms[idx].fields["name"].widget.attrs["placeholder"], placeholders[idx])

    def test_task_search_form_checking_for_required(self):
        test_data = {"name": ""}
        test_forms = [
            TaskSearchField,
            TagSearchField,
            TaskTypeSearchField,
            PositionSearchField,
            TeamSearchField,
            ProjectSearchField
        ]
        for form in test_forms:
            form = form(test_data)
            self.assertTrue(form.is_valid())


