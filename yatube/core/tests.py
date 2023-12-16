from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()


class PageNotFoundTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='main')
        self.client = Client()

    def test_page_not_found(self):
        # Проверка: шаблон и код при неверном запросе
        response = self.client.get('/something/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'core/404.html')
