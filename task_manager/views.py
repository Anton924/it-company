from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.aggregates import Count
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic


from view_breadcrumbs import (
    ListBreadcrumbMixin,
    UpdateBreadcrumbMixin,
    CreateBreadcrumbMixin,
    DeleteBreadcrumbMixin,
    DetailBreadcrumbMixin,
    UpdateWithNoDetailBreadcrumbMixin
)

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
    WorkerSearchField,
    ProjectSearchField
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
        "teams": teams,
    }

    return render(request, template_name="task_manager/index.html", context=context)


class TaskListView(LoginRequiredMixin, ListBreadcrumbMixin, generic.ListView):
    model = Task
    paginate_by = 9

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["segment"] = "tasks"
        context["search_field"] = TaskSearchField(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type", "project").prefetch_related("assignees", "tags")
        form = TaskSearchField(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class TaskUpdateView(LoginRequiredMixin, UpdateBreadcrumbMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        next_url = self.request.POST.get("next")
        if self.request.POST.get("next"):
            return next_url
        else:
            return reverse_lazy("task_manager:task-list")


class TaskDetailView(LoginRequiredMixin, DetailBreadcrumbMixin, generic.DetailView):
    model = Task

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("project").prefetch_related("assignees","tags")

        return queryset


class TaskDeleteView(LoginRequiredMixin, DeleteBreadcrumbMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskCreateView(LoginRequiredMixin, CreateBreadcrumbMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")
    crumbs = [("Add Task", reverse_lazy("task_manager:task-create"))]



class TagListView(LoginRequiredMixin, ListBreadcrumbMixin, generic.ListView):
    model = Tag
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", None)
        context["segment"] = "tags"
        context["search_field"] = TagSearchField(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TagSearchField(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class TagDeleteView(LoginRequiredMixin, DeleteBreadcrumbMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")


class TagUpdateView(LoginRequiredMixin, UpdateWithNoDetailBreadcrumbMixin, generic.UpdateView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")
    fields = "__all__"


class TagCreateView(LoginRequiredMixin, CreateBreadcrumbMixin, generic.CreateView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")
    fields = "__all__"


class TaskTypeListView(LoginRequiredMixin, ListBreadcrumbMixin, generic.ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", None)
        context["segment"] = "task types"
        context["search_field"] = TaskTypeSearchField(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TaskTypeSearchField(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class TaskTypeDeleteView(LoginRequiredMixin, DeleteBreadcrumbMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    context_object_name = "task_type"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, UpdateWithNoDetailBreadcrumbMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeCreateView(LoginRequiredMixin, CreateBreadcrumbMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class PositionListView(LoginRequiredMixin, ListBreadcrumbMixin, generic.ListView):
    model = Position
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", None)
        context["segment"] = "positions"
        context["search_field"] = PositionSearchField(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = PositionSearchField(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class PositionUpdateView(LoginRequiredMixin, UpdateWithNoDetailBreadcrumbMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, DeleteBreadcrumbMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class PositionCreateView(LoginRequiredMixin, CreateBreadcrumbMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class TeamListView(LoginRequiredMixin, ListBreadcrumbMixin, generic.ListView):
    model = Team
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", None)
        context["segment"] = "teams"
        context["search_field"] = TeamSearchField(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TeamSearchField(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])

        queryset = queryset.select_related("team_lead").prefetch_related("workers", "projects")

        return queryset

class TeamUpdateView(LoginRequiredMixin, UpdateBreadcrumbMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm


    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return next_url
        else:
            return reverse_lazy("task_manager:team-list")


class TeamDetailView(LoginRequiredMixin, DetailBreadcrumbMixin, generic.DetailView):
    model = Team

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("team_lead").prefetch_related("workers", "projects")

        return queryset


class TeamDeleteView(LoginRequiredMixin, DeleteBreadcrumbMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("task_manager:team-list")


class TeamCreateView(LoginRequiredMixin, CreateBreadcrumbMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("task_manager:team-list")


class WorkerListView(LoginRequiredMixin, ListBreadcrumbMixin, generic.ListView):
    model = Worker
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = WorkerSearchField(self.request.GET)
        if self.form.is_valid():
            full_name = str(self.form.cleaned_data["full_name"]).split()
            if len(full_name) == 2:
                val_1, val_2 = full_name
            elif len(full_name) == 1:
                val_1 = full_name[0]
                val_2 = ""
            else:
                val_1, val_2 = "", ""

            queryset = queryset.filter(Q(Q(first_name__icontains=val_1), Q(last_name__icontains=val_2)) | Q(Q(first_name__icontains=val_2), Q(last_name__icontains=val_1)))

        queryset = queryset.prefetch_related("teams_team_lead", "teams", "tasks").select_related("position")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "workers"
        context["search_field"] = self.form


        return context


class WorkerDetailView(LoginRequiredMixin, DetailBreadcrumbMixin, generic.DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["undone_tasks"] = Task.objects.filter(is_completed=False, assignees=self.object.pk).order_by("deadline")
        context["done_tasks"] = Task.objects.filter(is_completed=True, assignees=self.object.pk).order_by("deadline")

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("teams__workers", "teams__team_lead").select_related("position")

        return queryset


class WorkerCreateView(LoginRequiredMixin, CreateBreadcrumbMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, UpdateBreadcrumbMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return next_url
        return reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, DeleteBreadcrumbMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


class ProjectListView(LoginRequiredMixin, ListBreadcrumbMixin, generic.ListView):
    model = Project
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "projects"
        context["search_field"] = self.form

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("teams", "tasks")
        self.form = ProjectSearchField(self.request.GET)
        if self.form.is_valid():
            queryset = queryset.filter(name__icontains=self.form.cleaned_data["name"])

        return queryset


class ProjectDetailView(LoginRequiredMixin, DetailBreadcrumbMixin, generic.DetailView):
    model = Project

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("tasks", "teams", "teams__team_lead", "teams__workers")

        return queryset


class ProjectUpdateView(LoginRequiredMixin, UpdateBreadcrumbMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return next_url
        return reverse_lazy("task_manager:project-list")



class ProjectCreateView(LoginRequiredMixin, CreateBreadcrumbMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("task_manager:project-list")


class ProjectDeleteView(LoginRequiredMixin, DeleteBreadcrumbMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("task_manager:project-list")
