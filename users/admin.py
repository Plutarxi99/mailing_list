from django.contrib import admin

from users.models import User


def get_user_by_email(email):
    """
    Надстройка для поиска по email пользователя
    @param email:
    @return:
    """
    try:
        return User.objects.get(email=email)
    finally:
        return None


class UserEmailSearchAdmin(admin.ModelAdmin):
    def get_search_results(self, request, queryset, search_term):
        user = get_user_by_email(search_term)
        if user is not None:
            queryset = queryset.filter(user_id=user.id)
            use_distinct = False
        else:
            queryset, use_distinct = super().get_search_results(request,
                                                                queryset,
                                                                search_term)
        return queryset, use_distinct


@admin.register(User)
class AdminGroupManager(UserEmailSearchAdmin):
    list_display = ['email']
    search_fields = ['email', ]

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Manager').exists():  # when editing an object
            return ['email', 'first_name', 'last_name', 'avatar', 'phone', 'date_joined', 'last_login', 'groups',
                    'is_superuser', 'password', 'user_permissions']
        return self.readonly_fields
