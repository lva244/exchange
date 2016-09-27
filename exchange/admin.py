from django.contrib import admin

from . import models
from .form import RegisterLike


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ['email']

    def profile(self, obj):
        profile = models.RegisterLike.objects.get(id=obj.id)
        return profile.name

admin.site.register(models.RegisterLike, TaskAdmin)
