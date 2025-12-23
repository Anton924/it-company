from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from task_manager.models import (
    Tag,
    TaskType,
    Position,
    Worker,
    Task,
    Team,
    Project
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
     list_display = UserAdmin.list_display + ("position", )
     search_fields = UserAdmin.search_fields + ("position__name", ) # foreign key

     add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info", {"fields": ("position", )}
        ),
     )

     fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info", {"fields": ("position", )}
        ),
     )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name", "description",
        "deadline", "is_completed",
        "priority", "task_type",
        "get_assignees", "get_tags"
    )
    search_fields = ("name", "assignees__first_name", "assignees__last_name")
    list_filter = ("deadline", "is_completed", "priority", "task_type", "tags__name")


    def get_assignees(self, obj):
        return ", ".join([str(worker) for worker in obj.assignees.all()])

    def get_tags(self, obj):
        return ", ".join([str(tag) for tag in obj.tags.all()])


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "team_lead", "get_workers")
    search_fields = (
        "name",
        "team_lead__first_name",
        "team_lead__last_name",
        "workers__first_name",
        "workers__last_name"
    )

    def get_workers(self, obj):
        return ", ".join([str(worker) for worker in obj.workers.all()])


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "get_tasks", "get_teams")
    search_fields = ("name", "tasks__name", "teams__name")

    @admin.display(description="Tasks")
    def get_tasks(self, obj):
        return ", ".join([task.name for task in obj.tasks.all()])

    @admin.display(description="Teams")
    def get_teams(self, obj):
        return ", ".join([team.name for team in obj.teams.all()])



