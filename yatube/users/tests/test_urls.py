from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Post, Group
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


    def test_urls_uses_correct_templates(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_urls_names = {
            'users/login.html': '/auth/login/',
            'users/logged_out.html': '/auth/logout/',
            'users/password_reset_form.html': '/auth/password_reset/',
            'users/password_reset_confirm.html': '/auth/reset/<uidb64>/<token>/',
            'users/password_reset_done.html': '/auth/password_reset_done/',
            'users/password_reset_complete.html': '/auth/reset/done/'
        }

        for template, address in templates_urls_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_list_url_redirect_anonymous_on_login(self):
        response = self.client.get('/auth/password_change/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/auth/password_change/')

        response = self.client.get('/auth/password_change_done/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/auth/password_change_done/')
