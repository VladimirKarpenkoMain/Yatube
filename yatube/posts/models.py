from django.db import models
from django.contrib.auth import get_user_model
from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField()
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации', db_index=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Группа',
                              help_text='Выберите группу')
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, verbose_name='Пост')
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, verbose_name='Автор')
    text = models.CharField(max_length=156, verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата комментирования')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий в посте {self.post.text[:15]} от {self.author}'


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Подписчик', related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='', related_name='following')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'