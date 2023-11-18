from django.contrib import admin

from users.models import User


@admin.register(User)
class AdminGroupManager(admin.ModelAdmin):
    list_display = ['email']

    def get_readonly_fields(self, request, obj=None):
        print(request.user.groups.filter(name='Manager').exists())
        if request.user.is_staff:  # when editing an object
            return ['email', 'first_name', 'last_name', 'avatar', 'phone', 'date_joined', 'last_login', 'groups',
                    'is_superuser', 'password', 'user_permissions']
        return self.readonly_fields
