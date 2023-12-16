from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Post, Group
from http import HTTPStatus

User = get_user_model()


class StaticURLTests(TestCase):
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
            text='Cупернигер супергуд вагин покфын ыфпфыпф'

        )

    def setUp(self):
        # Неавторизованный клиент
        self.guest_client = Client()

        #  Авторизованный клиент
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_list_url_exists_at_desired_location_client_and_authorized(self):
        urls_for_client = ('/',
                           '/groups/testslug/',
                           '/profile/HasNoName/',
                           '/posts/1/',
                           )

        urls_for_authorized = ('/',
                               '/groups/testslug/',
                               '/profile/HasNoName/',
                               '/posts/1/',
                               '/posts/create/',
                               )

        for url in urls_for_client:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

        for url in urls_for_authorized:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_templates(self):
        """URL-адрес использует соответствующий шаблон."""

        Post.objects.create(author=self.user, text='asgasfa')

        templates_urls_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/groups/testslug/',
            'posts/create_post.html': '/posts/create/',
            'posts/profile.html': '/profile/HasNoName/',
            'posts/post_detail.html': '/posts/1/',
            'posts/create_post.html': '/posts/2/edit/',
        }

        for template, address in templates_urls_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_list_url_redirect_anonymous_on_login(self):
        templates_urls_names = {
            '/posts/create/': '/auth/login/?next=/posts/create/',
            '/posts/1/edit/': '/auth/login/?next=/posts/1/edit/',
            '/posts/1/comment/': '/auth/login/?next=/posts/1/comment/'
        }
        for url, redirect in templates_urls_names.items():
            with self.subTest(redirect=redirect):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, redirect)

    def test_url_redirect_authorized_on_edit(self):
        response = self.authorized_client.get('/posts/1/edit/', follow=True)
        self.assertRedirects(response, '/posts/1/')
