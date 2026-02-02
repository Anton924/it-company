from django.urls import path
from task_manager.views import index, TaskListView, TaskDeleteView, TaskCreateView
from task_manager.views import TaskUpdateView


urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create")
]

app_name = "task_manager"