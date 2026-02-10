from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxSelectMultiple

from task_manager.models import Task, Team, Worker, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets={
            "tags": CheckboxSelectMultiple,
            "deadline": forms.DateTimeInput(
                format="%Y-%m-%d",
                attrs={"type": "date"}
            ),
            "assignees": CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task_type"].empty_label = "Choose type of task..."
        self.fields["project"].empty_label = "Choose project this task belong..."


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = "__all__"

        widgets = {
            "workers": CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["team_lead"].empty_label = "Choose team leader..."


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = (
            "first_name",
            "last_name",
            "email",
            "position",
        )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["position"].empty_label = "Choose position..."


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = (
            "first_name",
            "last_name",
            "email",
            "position",
        )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"

        widgets = {
            "teams": CheckboxSelectMultiple
        }
