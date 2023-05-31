from django.contrib import admin

from .models import Action, Door

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'is_open', 'created', 'user', 'is_thief')

@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'owner', 'created')
