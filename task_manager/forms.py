from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from task_manager.models import Tag, Task


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