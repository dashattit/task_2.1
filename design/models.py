from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

class AddUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    patronym = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    password_confirm = models.CharField(max_length=100, blank=True)

    groups = models.ManyToManyField(
        Group, related_query_name='adduser',
        blank=True, help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        blank=True, help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username



class Category(models.Model):
    name=models.CharField(max_length=150)

    def __str__(self):
        return self.name



class Request(models.Model):
    user = models.ForeignKey(AddUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image_sale = models.FileField(blank=True, upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    STATUS_CHOICES = [
        ('N', 'Новая'),
        ('P', 'Принято в работу'),
        ('C', 'Выполнено'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')

    def __str__(self):
        return self.title
