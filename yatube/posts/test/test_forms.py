import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    """Создаем тестовые посты, группу и форму."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='leo')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='first',
            description='Тестовый заголовок'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Старый пост',
            group=cls.group
        )

    @classmethod
    def tearDownClass(cls):
        """Удаляем тестовые медиа."""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        """Создаем клиент зарегистрированного пользователя."""
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Новый пост',
            'group': PostFormTests.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        post = Post.objects.first()
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': PostFormTests.user.username}
        ))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(
            post.group, PostFormTests.group
        )
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.author, PostFormTests.user)

    def test_post_edit(self):
        form_data = {
            'text': 'Отредактированный текст поста',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=[self.post.pk]),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', args=[self.post.id])
        )
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                group=self.group.id,
                id=self.post.id,
                author=PostFormTests.user,
            ).exists()
        )
