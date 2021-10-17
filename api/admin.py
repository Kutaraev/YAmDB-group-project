from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comment, Genre, Review, Title, UserRegistration

User = get_user_model()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('email', 'confirmation_code')
    search_fields = ('email',)


class ExtendedUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'first_name', 'last_name')
    list_filter = ('role',)
    fieldsets = (
        *UserAdmin.fieldsets, ('Additional', {'fields': ('role', 'bio')})
    )


admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(User, ExtendedUserAdmin)
