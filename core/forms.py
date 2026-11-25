import re
from django import forms
from django.core.exceptions import ValidationError
from .models import User, Category, Request

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', min_length=6)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повтор пароля')
    agree = forms.BooleanField(label='Согласен на обработку персональных данных')

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email']
        labels = {
            'full_name': 'ФИО',
            'username': 'Логин',
            'email': 'Email'
        }

    def clean_full_name(self):
        name = self.cleaned_data['full_name']
        if not re.fullmatch(r'[А-Яа-яЁё\-\s]+', name):
            raise ValidationError('Только киррилица, дефис и пробелы')
        return name

    def clean_username(self):
        login = self.cleaned_data['username']
        if not re.fullmatch(r'[A-Za-z\-]+', login):
            raise ValidationError('Только латиница, и дефис')
        if User.objects.filter(username=login).exists():
            raise ValidationError('Логин занят')
        return login

    def clean(self):
        data = super().clean()
        p1 = data.get('password')
        p2 = data.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Пароли не совпадают')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'category', 'photo']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'category': 'Категория',
            'photo': 'Фото помещения',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo.size > 2 * 1024 * 1024:
            raise ValidationError('Файл больше 2 МБ')
        ext = photo.name.split('.')[-1].lower()
        if ext not in ('jpg', 'jpeg', 'png', 'bmp'):
            raise ValidationError('Только jpg, jpeg, png, bmp')
        return photo

class AcceptForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Комментарий'
    )

class CompleteForm(forms.Form):
    design = forms.ImageField(label='Изображение дизайна')

    def clean_design(self):
        img = self.cleaned_data['design']
        if img.size > 2 * 1024 * 1024:
            raise ValidationError('Файл больше 2мб')
        ext = img.name.split('.')[-1].lower()
        if ext not in ('jpg', 'jpeg', 'png', 'bmp'):
            raise ValidationError('Только jpg, jpeg, png, bmp')
        return img

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Название'}