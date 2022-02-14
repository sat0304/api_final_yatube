from django.contrib import admin

from .models import Comment, Follow, Group, Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Перечисляем поля, которые должны отображаться в админке."""
    list_display = ('pk', 'text', 'created', 'author', 'post', )
    """Добавляем интерфейс для поиска по тексту комментариев."""
    search_fields = ('text', )
    """Добавляем поле выбора поста."""
    list_editable = ('post', )
    """Добавляем возможность фильтрации по дате."""
    list_filter = ('created', )
    """Добавляем значение для пустого поля."""
    empty_value_display = '-пусто-'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Перечисляем поля, которые должны отображаться в админке."""
    list_display = ('pk', 'text', 'pub_date', 'author', 'group', )
    """Добавляем интерфейс для поиска по тексту постов."""
    search_fields = ('text', )
    """Добавляем поле редактирования групп."""
    list_editable = ('group', )
    """Добавляем возможность фильтрации по дате."""
    list_filter = ('pub_date', )
    """Добавляем значение для пустого поля."""
    empty_value_display = '-пусто-'


admin.site.register(Group)
# admin.site.register(Post, PostAdmin)
admin.site.register(Follow)
