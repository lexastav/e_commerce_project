from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelForm
from django.utils.safestring import mark_safe

from .models import *

from PIL import Image


class SmartphoneAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if not instance.sd_card:
            self.fields['sd_volume_max'].widget.attrs.update({
                'readonly': True, 'style': 'background: lightgray'
            })

    def clean(self):
        if not self.cleaned_data['sd_card']:
            self.cleaned_data['sd_volume_max'] = None
        return self.cleaned_data


class NotebookAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            f'<span style="color:green;">Изображение будет обрезано если оно будет больше </span>'
            f'<span style="color:green;">{Product.MAX_VALID_RESOLUTION[0]} x {Product.MAX_VALID_RESOLUTION[1]} </span>'
        )

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_VALID_RESOLUTION
        max_height, max_width = Product.MAX_VALID_RESOLUTION

        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер файла не должен превышать 3MB')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Загружаемое изображение имеет разрешение меньше минимльно допустимого')

        if img.height > max_height or img.width > max_width:
            raise ValidationError('Загружаемое изображение имеет разрешение больше максимально допустимого')

        return image


class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name is 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    change_form_template = 'admin.html'
    form = SmartphoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name is 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
