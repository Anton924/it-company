from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.shortcuts import render
from task_manager.models import Task, Project, Team

def index(request: HttpRequest):
    total_tasks_in_process = Task.objects.filter(is_completed=False).count()
    total_projects = Project.objects.count()
    total_workers = get_user_model().objects.count()
    total_teams = Team.objects.count()

    context = {
        "total_tasks_in_process": total_tasks_in_process,
        "total_projects": total_projects,
        "total_workers": total_workers,
        "total_teams": total_teams
    }

    return render(request, template_name="index.html", context=context)

