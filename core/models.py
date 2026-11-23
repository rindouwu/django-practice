from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField(max_length = 150, verbose_name = 'ФИО')
    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    def __str__(self):
        return self.name

class Request(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_CHOICES = [
        (STATUS_NEW, 'новая'),
        (STATUS_IN_PROGRESS, 'Принято в работу'),
        (STATUS_DONE, 'Выполнено')
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='requests/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    design_image = models.ImageField(upload_to='designs/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
