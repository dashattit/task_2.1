from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import AddUser, Request, Category
from django.utils.html import format_html
admin.site.register(AddUser)

class RequestAdminForm(forms.ModelForm):
    design_image = forms.ImageField(
        required=False,
        label="Изображение дизайна (обязательно при смене статуса на 'Выполнено')"
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Комментарий (обязателен при смене статуса на 'Принято в работу')"
    )

    class Meta:
        model = Request
        fields = '__all__'

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)

        if self.instance and self.instance.pk:
            status = self.instance.status

            if status == 'P':
                self.fields['design_image'].widget = forms.HiddenInput()
            elif status == 'C':
                self.fields['comment'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        previous_status = self.instance.status if self.instance else None

        if previous_status in ['P', 'C'] and status != previous_status:
            raise ValidationError("Смена статуса с 'Принято в работу' или 'Выполнено' невозможна.")

        if status == 'P' and not cleaned_data.get('comment'):
            raise ValidationError("Пожалуйста, добавьте комментарий при смене статуса на 'Принято в работу'.")

        if status == 'C' and not cleaned_data.get('design_image'):
            raise ValidationError("Пожалуйста, загрузите изображение дизайна при смене статуса на 'Выполнено'.")

        return cleaned_data

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    form = RequestAdminForm
    list_display = ('title', 'user', 'status', 'created_at', 'category', 'urgent', 'image_link')
    readonly_fields = ('user', 'title', 'description', 'created_at', 'urgent', 'image_link')
    list_filter = ('status', 'category', 'urgent', 'created_at')
    search_fields = ('title', 'user__username', 'description')

    def image_link(self, obj):
        if obj.image_sale:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.image_sale.url, "Просмотр изображения")
        return "Нет изображения"

    image_link.short_description = "Ссылка на изображение"

    def get_fieldsets(self, request, obj=None):
        if obj:
            if obj.status == 'P':
                return (
                    (None, {
                        'fields': (
                        'user', 'title', 'description', 'category', 'status', 'urgent', 'created_at', 'comment')
                    }),
                )
            elif obj.status == 'C':
                return (
                    (None, {
                        'fields': (
                        'user', 'title', 'description', 'category', 'status', 'urgent', 'created_at', 'design_image',
                        'image_link')
                    }),
                )
        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        #определенные поля сделать доступными для чтения администраторам
        if obj:
            return ['title', 'description', 'category', 'image_sale'] + list(self.readonly_fields)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj.comment = form.cleaned_data.get('comment', obj.comment)
            obj.image_sale = form.cleaned_data.get('design_image', obj.image_sale)
            with transaction.atomic():
                obj.save()

    def urgent_status_display(self, obj):
        if obj.urgent:
            return format_html('<span style="color: red;">Срочная заявка</span>')
        return "Обычная заявка"
    urgent_status_display.short_description = "Статус срочности"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def delete_model(self, request, obj):
        # Удаляем связанные заявки при удалении категории
        Request.objects.filter(category=obj).delete()
        super().delete_model(request, obj)


