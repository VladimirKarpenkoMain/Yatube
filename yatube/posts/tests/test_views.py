from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Post, Group
from django import forms
from django.urls import reverse

User = get_user_model()


class ViewsTests(TestCase):
    """
    Проверка шаблонов и контекста всех views
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='auth')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='testslug',
            description='Тестовое описание'
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text='Cупернигер супергуд вагин покфын ыфпфыпф',
            group=cls.group,

        )

    def setUp(self) -> None:
        #  Авторизованный клиент
        self.user = User.objects.create_user(username='VladimirKarpenko')
        self.authorized_client = Client()
        self.authorized_client.force_login(ViewsTests.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_pages_names = {
            'posts/create_post.html': reverse('posts:create'),
            'posts/create_post.html': reverse('posts:update', kwargs={'post_id': 1}),
            'posts/index.html': reverse('posts:index'),
            'posts/post_detail.html': reverse('posts:post_detail', kwargs={'post_id': 1}),
            'posts/profile.html': reverse('posts:profile', kwargs={'username': 'VladimirKarpenko'}),
            'posts/group_list.html': reverse('posts:groups', kwargs={'slug': 'testslug'})
        }

        for template, view in templates_pages_names.items():
            with self.subTest(view=view):
                response = self.authorized_client.get(view)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        # Проверка: контекст домашней страницы корректен
        response = self.authorized_client.get(reverse('posts:index'))

        self.assertEqual(response.context['title'], 'Главная страница')
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.text, 'Cупернигер супергуд вагин покфын ыфпфыпф')
        self.assertEqual(first_object.author, ViewsTests.user)
        self.assertEqual(first_object.group, ViewsTests.group)

    def test_list_page_show_correct_context(self):
        # Проверка: контекст страницы группы корректен
        response = self.authorized_client.get(reverse('posts:groups', kwargs={'slug': 'testslug'}))

        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.text, 'Cупернигер супергуд вагин покфын ыфпфыпф')
        self.assertEqual(first_object.author, ViewsTests.user)
        self.assertEqual(first_object.group, ViewsTests.group)

        self.assertEqual(response.context['title'], 'Здесь будет информация о группах проекта Yatube')
        self.assertEqual(response.context['group'], ViewsTests.group)

    def test_detail_page_show_correct_context(self):
        # Проверка: контекст страницы конкретного поста корректен
        response = self.authorized_client.get(reverse('posts:post_detail', kwargs={'post_id': 1}))

        self.assertEqual(response.context.get('post').text, 'Cупернигер супергуд вагин покфын ыфпфыпф')
        self.assertEqual(response.context.get('post').author, ViewsTests.user)
        self.assertEqual(response.context.get('post').group, ViewsTests.group)
        self.assertEqual(response.context.get('post').id, 1)

    def test_create_page_show_correct_context(self):
        # Проверка: контекст страницы создания Post корректен
        response = self.authorized_client.get(reverse('posts:create'))

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.ModelChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value).__class__
                self.assertEqual(form_field, expected)

    def test_edit_page_show_correct_context(self):
        # Проверка: контекст страницы редактирования Post корректен
        response = self.authorized_client.get(reverse('posts:update', kwargs={'post_id': 1}))

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.ModelChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value).__class__
                self.assertEqual(form_field, expected)

        self.assertEqual(response.context['is_edit'], True)

    def test_profile_page_show_correct_context(self):
        # Проверка: контекст страницы профиля корректен
        response = self.authorized_client.get(reverse('posts:profile', kwargs={'username': 'VladimirKarpenko'}))

        self.assertEqual(response.context.get('user').username, 'VladimirKarpenko')
        self.assertEqual(response.context.get('count'), 0)

    def test_creat_post_work_correct(self):
        New_Post = Post.objects.create(
            author=ViewsTests.user,
            text='Лютый пост',
            group=ViewsTests.group,
        )
        response_index = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response_index.context['page_obj'].object_list[0], New_Post)

        response_group = self.authorized_client.get(reverse('posts:groups', kwargs={'slug': 'testslug'}))
        self.assertEqual(response_group.context['page_obj'][0], New_Post)

        response_profile = self.authorized_client.get(reverse('posts:profile', kwargs={'username': 'auth'}))
        self.assertEqual(response_profile.context['page_obj'][0], New_Post)


class PaginatorViewsTest(TestCase):
    """
    Проверка паджинации posts:index, posts:group, posts:profile
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='bigeg')

        cls.GroupOne = Group.objects.create(title='База',
                                            slug='baza',
                                            description='Да, это база')

    def setUp(self) -> None:
        # Авторизованный клиент
        self.user = User.objects.create_user(username='VladimirKarpenko')
        self.authorized_client = Client()
        self.authorized_client.force_login(PaginatorViewsTest.user)

        # Создание 13 объектов модели Post
        for _ in range(13):
            Post.objects.create(
                author=PaginatorViewsTest.user,
                text='Cупернигер супергуд вагин покфын ыфпфыпф',
                group=PaginatorViewsTest.GroupOne
            )

    def test_home_first_page_contains_ten_records(self):
        # Проверка: на домашней первой странице должно быть десять постов
        response = self.authorized_client.get(reverse('posts:index'))

        self.assertEqual(len(response.context['page_obj']), 10)

    def test_home_second_page_contains_three_records(self):
        # Проверка: на домашней второй странице должно быть три поста
        response = self.authorized_client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_first_page_contains_ten_records(self):
        # Проверка: на второй странице группы должно быть десять постов
        response = self.authorized_client.get(reverse('posts:groups', kwargs={'slug': 'baza'}))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_group_second_page_contains_three_records(self):
        # Проверка: на второй странице группы должно быть три поста
        response = self.authorized_client.get(reverse('posts:groups', kwargs={'slug': 'baza'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_has_relevant_records(self):
        # Проверка: страница группы содержит записи только этой группы
        response = self.authorized_client.get(reverse('posts:groups', kwargs={'slug': 'baza'}))

        for post in response.context['page_obj'].object_list:
            with self.subTest(post=post):
                self.assertEqual(post.group, PaginatorViewsTest.GroupOne)

    def test_profile_first_page_contains_ten_records(self):
        # Проверка: на второй странице профиля должно быть десять постов
        response = self.authorized_client.get(reverse('posts:profile', kwargs={'username': 'bigeg'}))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_profile_second_page_contains_ten_records(self):
        # Проверка: на второй странице профиля должно быть три поста
        response = self.authorized_client.get(reverse('posts:profile', kwargs={'username': 'bigeg'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_profile_first_page_has_relevant_records(self):
        # Проверка: первая страница профиля содержит записи только этого пользователя
        response = self.authorized_client.get(reverse('posts:groups', kwargs={'slug': 'baza'}))

        for post in response.context['page_obj'].object_list:
            with self.subTest(post=post):
                self.assertEqual(post.author, PaginatorViewsTest.user)

    def test_profile_second_page_has_relevant_records(self):
        # Проверка: вторая страница профиля содержит записи только этого пользователя
        response = self.authorized_client.get(reverse('posts:groups', kwargs={'slug': 'baza'}) + '?page=2')

        for post in response.context['page_obj'].object_list:
            with self.subTest(post=post):
                self.assertEqual(post.author, PaginatorViewsTest.user)
