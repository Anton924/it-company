from django.http import HttpRequest

from task_manager.models import Task

def pending_tasks(request: HttpRequest) -> dict:
    if request.user.is_authenticated:
        user_tasks = Task.objects.filter(
            is_completed=False, assignees=request.user
        ).order_by("deadline")[:10]

        return {"user_tasks": user_tasks}
    return {"user_tasks": []}


# def pages(request: HttpRequest) -> dict:
#     return None
