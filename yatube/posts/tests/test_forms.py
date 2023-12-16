from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from posts.models import Post, Group, Comment
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import shutil
import tempfile

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class PostFormTests(TestCase):
    """
    Тестирование создание и изменение пользователем через форму объекта модели Post
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='new')
        cls.Post = Post.objects.create(text='askasgkasgk', author=cls.user)

    def setUp(self) -> None:
        # Авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)

    def test_create_record(self):
        # Проверка: создание поста пользователем
        form_data = {
            'text': 'Лылфыплффптфыпо'
        }

        response = self.authorized_client.post(reverse('posts:create'), data=form_data, follow=True)

        self.assertEqual(Post.objects.get(id=2).id, 2)
        self.assertEqual(response.status_code, 200)

    def test_edit_record(self):
        # Проверка: редактирование поста пользователем и соответствующее изменение данных
        form_data = {
            'text': 'фытпфытьпфып'
        }
        self.authorized_client.post(reverse('posts:update', kwargs={'post_id': 1}), data=form_data,
                                               follow=True)
        self.assertEqual(Post.objects.get(id=1).text, 'фытпфытьпфып')

    def test_comment_record(self):
        # Проверка: создание комментарий пользователем
        form_data = {
            'text': 'Это тестовый комментарий'
        }
        self.authorized_client.post(reverse('posts:add_comment', kwargs={'post_id': 1}), data=form_data,
                                    follow=True)
        self.assertTrue(Comment.objects.get(id=1))


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ImagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём байтово картинку
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        # Загружаем
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.user = User.objects.create_user(username='testname')
        cls.Group = Group.objects.create(title='Тестовая группа', slug='testslug', description='Тестовое описание')
        cls.Post = Post.objects.create(text='Тестовый текст', image=cls.uploaded, author=cls.user, group=cls.Group)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(ImagesTests.user)

    def test_pages_records_images(self):
        """
        Тест существования изображения в Post объекте
        """
        reverses = {
            'posts:index': {},
            'posts:groups': {'slug': 'testslug'},
            'posts:profile': {'username': 'testname'}
        }

        for name_reverse, context in reverses.items():
            with self.subTest(name_reverse=name_reverse):
                response = self.authorized_client.get(reverse(name_reverse, kwargs=context))
                self.assertTrue(response.context['page_obj'][0].image)

    def test_creation_record_with_postform(self):
        """
        Тест создания объекта Post с помощью формы
        """
        posts_count = Post.objects.count()

        form_data = {
            'text': 'Новый тест',
            'image': ImagesTests.uploaded
        }

        response = self.authorized_client.post(reverse('posts:create'), form_data)
        #print(response.content_params)
        print(posts_count)
        print(Post.objects.count())
        #self.assertTrue(posts_count, Post.objects.count())
        #self.assertEqual(response.status_code, 201)
