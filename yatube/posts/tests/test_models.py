from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post, Group

User = get_user_model()


class PostsModelsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание'
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text='Cупернигер супергуд вагин покфын ыфпфыпф'

        )

    def test_models_have_correct_object_names(self):
        """ Объекты Post и Group имееют верные __str__"""
        Post = PostsModelsTests.post
        Group = PostsModelsTests.group

        self.assertEqual(Group.title, str(Group))
        self.assertEqual(Post.text[:15], str(Post))

    def test_first_fifteen_symbols_of_title_Post(self):
        Post = PostsModelsTests.post
        expected_value = 'Cупернигер супе'

        self.assertEqual(expected_value, Post.text[:15])

    def test_Post_have_correct_verbose_name(self):
        Post = PostsModelsTests.post
        filed_verboses = {
            'text': 'Текст поста',
            'author': 'Автор',
            'pub_date': 'Дата публикации',
            'group': 'Группа'
        }

        for field, expected_value in filed_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(Post._meta.get_field(field).verbose_name, expected_value)
