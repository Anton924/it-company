from django.urls import path
from task_manager.views import index, TaskListView
from task_manager.views import TaskUpdateView


urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update")
]

app_name = "task_manager"