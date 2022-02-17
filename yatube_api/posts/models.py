from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Таблица, содержащая группы пользователей."""
    title = models.CharField('Сообщество', max_length=200)
    slug = models.SlugField(
        unique=True,
        default='title',
    )
    description = models.TextField('Записи сообщества')

    class Meta:
        verbose_name_plural = 'Сообщества'

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    """Таблица, содержащая сообщения (посты) пользователей."""
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Выберите группу',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='posts/',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return self.text[:15]


class Comment(models.Model):
    """Таблица, содержащая комментарии пользователей."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария',
    )
    created = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):
    """Таблица, содержащая подписки пользователей на
    избранных авторов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow',
        verbose_name='Hа автора'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='one_following'
            ),
            models.CheckConstraint(
                check=~models.Q(
                    user=models.F('following')), name='user_not_author'
            )
        ]

    def __str__(self):
        return f'Подписчик: {self.user}, на автора: {self.following}'
