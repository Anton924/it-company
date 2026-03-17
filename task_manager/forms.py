from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxSelectMultiple
from django.core.exceptions import ValidationError

from task_manager.models import (
    Task,
    Team,
    Worker,
    Project
)


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
            "username",
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


class TaskSearchField(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget= forms.TextInput(
            attrs={
                "placeholder": "Enter name of the task...",
            }
        )
    )


class TagSearchField(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter name of the tag..."
            }
        )
    )


class TaskTypeSearchField(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter name of the task type..."
            }
        )
    )


class PositionSearchField(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter name of the position..."
            }
        )
    )


class TeamSearchField(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter name of the team..."
            }
        )
    )

def validate_full_name(full_name: str) -> str:
    if full_name:
        errors = []
        test_str = full_name.replace(" ", "")
        if not test_str.isalpha():
            errors.append(
                "First name ot Last name have to consist only from letters"
            )
        if len(full_name.split()) > 2:
            errors.append("Field only search for First name and Last name(maximum 2 words)")

        if errors:
            raise ValidationError(errors)

    return full_name

class WorkerSearchField(forms.Form):
    full_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter first name or/and last name"
            }
        ),
        validators=(validate_full_name,)
    )


class ProjectSearchField(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter name of the project..."
            }
        )
    )

















