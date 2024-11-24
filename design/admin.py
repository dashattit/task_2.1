from django.contrib import admin
from django import forms
from .models import AddUser, Request, Category

admin.site.register(AddUser)
admin.site.register(Request)
admin.site.register(Category)

# class RequestAdminForm(forms.ModelForm):
#     design_image = forms.ImageField(required=False, label="Изображение дизайна (обязательно при смене статуса на 'Выполнено')")
#     comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}), label="Комментарий обязателен при смене статуса на 'Принято в работу')")
#
#     class Meta:
#         model = Request

