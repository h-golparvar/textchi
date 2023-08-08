from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User
from home.models import PlayList


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['name', 'phone_number', 'is_admin']
    list_filter = ['is_admin']
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name')}),
        ('info', {'fields': ('phone_number', 'email')}),
        ('manage', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2')}),
    )
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    ordering = ('first_name', 'last_name')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(PlayList)
