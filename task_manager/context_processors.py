from django.http import HttpRequest

from task_manager.models import Task

def pending_tasks(request: HttpRequest) -> dict:
    if request.user.is_authenticated:
        tasks = Task.objects.filter(
            is_completed=False, assignees=request.user
        ).order_by("deadline")[:10]

        return {"navigation_tasks": tasks}
    return {"navigation_tasks": []}
