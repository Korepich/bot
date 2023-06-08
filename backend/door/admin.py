from django.contrib import admin

from .models import Action, Door, Breaking


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "is_open", "created", "user")


@admin.register(Breaking)
class ActionAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "id", "door")


@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "owner", "created")
