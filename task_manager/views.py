from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Count
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import (
    TaskForm,
    TeamForm,
    WorkerCreationForm,
    WorkerUpdateForm,
    ProjectForm
)
from task_manager.models import (
    Task,
    Project,
    Team,
    Tag,
    TaskType,
    Position,
    Worker
)


def index(request: HttpRequest):
    total_tasks_in_process = Task.objects.filter(is_completed=False).count()
    total_projects = Project.objects.filter(status="IN_PROCESS").count()
    total_workers = get_user_model().objects.count()
    total_teams = Team.objects.count()
    teams =  Team.objects.prefetch_related("workers")
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
        ).filter(status="IN_PROCESS"),
        "visit_times": visit_times,
        "teams": teams
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


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "task edit"

        return context

    def get_success_url(self):
        next_url = self.request.POST.get("next")
        if self.request.POST.get("next"):
            return next_url
        else:
            return reverse_lazy("task_manager:task-list")




class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "task in details"

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("project").prefetch_related("assignees","tags")

        return queryset


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["segment"] = "delete task"

        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "create task"

        return context


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "tags"

        return context


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "delete tag"

        return context


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "edit tag"

        return context


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "create task"

        return context


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "task types"

        return context


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    context_object_name = "task_type"
    success_url = reverse_lazy("task_manager:task-type-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "delete task type"

        return context


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "edit task type"

        return context


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "create task type"

        return context


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "positions"

        return context


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "edit position"

        return context


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "delete position"

        return context


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "create position"

        return context


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "teams"

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.select_related("team_lead").prefetch_related("workers", "projects")

        return queryset

class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "edit team"

        return context


    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return next_url
        else:
            return reverse_lazy("task_manager:team-list")


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "detail team"

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("team_lead").prefetch_related("workers", "projects")

        return queryset


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("task_manager:team-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["segment"] = "delete team"

        return context



class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("task_manager:team-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["segment"] = "create team"

        return context


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "workers"

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("teams_team_lead", "teams", "tasks").select_related("position")

        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "worker details"
        context["undone_tasks"] = Task.objects.filter(is_completed=False, assignees=self.request.user).order_by("deadline")
        context["done_tasks"] = Task.objects.filter(is_completed=True, assignees=self.request.user).order_by("deadline")

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("teams__workers", "teams__team_lead").select_related("position")

        return queryset


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "create worker"

        return context


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "update worker"

        return context

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return next_url
        return reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "delete worker"

        return context


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "projects"

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("teams", "tasks")

        return queryset


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "detail project"

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("tasks", "teams", "teams__team_lead", "teams__workers")

        return queryset


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "update project"

        return context

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return next_url
        return reverse_lazy("task_manager:project-list")



class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("task_manager:project-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "create project"

        return context

