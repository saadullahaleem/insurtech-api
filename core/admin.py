from django.contrib import admin
from django.contrib.auth import get_user_model
from simple_history.admin import SimpleHistoryAdmin

from core.models import Policy

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email',
                    'is_customer', 'is_active')
    list_filter = ('is_active', 'is_customer',)
    list_display_links = ('id',)
    search_fields = ('email', 'username', 'first_name', 'last_name')


class PolicyAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'customer', 'premium', 'cover', 'state')


admin.site.register(User, UserAdmin)
admin.site.register(Policy, PolicyAdmin)
