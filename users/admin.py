from django.contrib import admin

from users.models import CustomGroup, Users, Roles
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import Group
import uuid
# Register your models here.
admin.site.register(Users)
admin.site.register(Roles)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'name')
    exclude = ('name',)  # Exclude name from the admin form
    def save_model(self, request, obj, form, change):
        # If the 'name' field is not set, generate it based on the 'title'
        if not obj.name and obj.title:
            unique_id = uuid.uuid4().hex[:8]
            obj.name = f"{obj.title}_{unique_id}"  # Modify as needed for your naming convention
        super().save_model(request, obj, form, change)

# Register your custom model without unregistering the default Group
admin.site.register(CustomGroup, CustomGroupAdmin)
