from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Count
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import TaskForm
from task_manager.models import Task, Project, Team


def index(request: HttpRequest):
    total_tasks_in_process = Task.objects.filter(is_completed=False).count()
    total_projects = Project.objects.count()
    total_workers = get_user_model().objects.count()
    total_teams = Team.objects.count()
    tasks = None
    if request.user.is_authenticated:
        tasks = Task.objects.filter(is_completed=False, assignees=request.user).order_by("deadline")[:10]
    visit_times = request.session.get("visit_times", 0) + 1
    request.session["visit_times"] = visit_times

    context = {
        "total_tasks_in_process": total_tasks_in_process,
        "total_projects": total_projects,
        "total_workers": total_workers,
        "total_teams": total_teams,
        "segment": "dashboard",
        "projects": Project.objects.annotate(
            total_tasks=Count("tasks", distinct=True),
            total_teams=Count("teams", distinct=True)
        ),
        "tasks": tasks,
        "visit_times": visit_times
    }

    return render(request, template_name="task_manager/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context["segment"] = "tasks"

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("task_type", "project").prefetch_related("assignees", "tags")

        return queryset


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "task edit"

        return context


class TaskDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["segment"] = "delete task"

        return context


class TaskCreateView(generic.CreateView, LoginRequiredMixin):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "create task"

        return context



