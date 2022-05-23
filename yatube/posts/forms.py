from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Сообщение',
            'group': 'Группа',
            'image': 'Картинка'
        }
        help_texts = {
            'text': 'Введите сообщение',
            'group': 'Выберите группу',
            'image': 'Загрузите картинку'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Комментарий',
        }
        help_texts = {
            'text': 'Напишите комментарий',
        }
