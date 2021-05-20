import sys
from PIL import Image

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

from io import BytesIO

USER = get_user_model()


def get_product_url(obj, view_name):
    ct_model = obj.__class__.meta.model_name
    return reverse(view_name, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass

# не забыть создать модель Order

# на самом деле в процессе разработки выяснилось, что модель наша весьма корявая, мало того, что так как каждый наш
# продукт может обладать различными моделями характеристик, нам пришлось явно прописывать модели категорий для
# продуктов, потом напихать в них костылей, что бы как бы скрыть их другот друга,так еще теперь и выяснилось,
# что при текущей структуре мы не можем нормальным образом выводить на домашнюю страницу, например, новые поступления.

# По этому попробуем реализовать некий костыль. Это будет класс, иммитирующий поведение модели.


class LatestProductManager:
    """Костыль, с помощью которого мы будем выводить последние поступления на домашнюю страницу"""
    @staticmethod
    def get_products_for_home_page(*args, **kwargs):  # статический метод, которыйбудет доставать список
        # продуктов для отображения на главной странице
        with_respect_to = kwargs.get('with_respect_to')
        ct_models = ContentType.objects.filter(model__in=args)
        products = []
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),
                                  reverse=True
                                  )

        return products


class LatestProducts:
    """Продолжение предыдущего костыля"""
    objects = LatestProductManager


class Category(models.Model):
    """Категория продукта"""
    title = models.CharField(max_length=250, verbose_name='Наименование категории')
    slug = models.SlugField(unique=True)  # нужен для того, что бы у нас был некий конечный end point в нашей модели.
    # То есть чтобы мы могли перейти по ссылке ..../category/smartphones, вот smartphones и есть slug.

    def __str__(self):
        return self.title


class Product(models.Model):
    """Сам продукт"""

    MIN_VALID_RESOLUTION = (200, 200)
    MAX_VALID_RESOLUTION = (2000, 2000)
    MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    # есть такой обязательный аргумент в модели ForeignKey- on_delete, в нем прописывается некий алгоритм удаления
    # объекта в случае необходимости, так как есть связи. В данном случае при помощи CASCADE мы говорим, что нужно
    # удалять все связи.

    title = models.CharField(max_length=250, verbose_name='Наименование продукта')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение продукта')
    description = models.TextField(verbose_name='Описание продукта', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_height, min_width = self.MIN_VALID_RESOLUTION
        max_height, max_width = self.MAX_VALID_RESOLUTION

        if img.height < min_height or img.width < min_width:
            raise MinResolutionErrorException('Загружаемое изображение имеет разрешение меньше минимльно допустимого')

        if img.height > max_height or img.width > max_width:
            raise MaxResolutionErrorException('Загружаемое изображение имеет разрешение больше максимально допустимого')
        # image = self.image
        # img = Image.open(image)
        # new_img = img.convert('RGB')
        # resize_new_img = new_img.resize((720, 344), Image.ANTIALIAS)
        # filestream = BytesIO()
        # resize_new_img.save(filestream, 'JPEG', quality=90)
        # filestream.seek(0)
        # name = f'{self.image.name.split(".")}.jpg'
        # self.image = InMemoryUploadedFile(
        #     filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
        # )

        super().save(*args, **kwargs)


class Notebook(Product):
    display_type = models.CharField(max_length=100, verbose_name='Тип экрана')
    diagonal = models.CharField(max_length=100, verbose_name='Диагональ экрана')
    cpu_freq = models.CharField(max_length=100, verbose_name='Частота процессора')
    ram = models.CharField(max_length=100, verbose_name='Оперативная память')
    gpu = models.CharField(max_length=100, verbose_name='Используемый графический процессор')
    battery_capacity = models.CharField(max_length=100, verbose_name='Емкость батареи')
    time_without_charge = models.CharField(max_length=100, verbose_name='Время работы от батареи')

    def __str__(self):
        return f'{self.category.title} : {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):
    display_type = models.CharField(max_length=100, verbose_name='Тип экрана')
    diagonal = models.CharField(max_length=100, verbose_name='Диагональ экрана')
    resolution_display = models.CharField(max_length=100, verbose_name='Разрешение экрана')
    cpu_freq = models.CharField(max_length=100, verbose_name='Частота процессора')
    ram = models.CharField(max_length=100, verbose_name='Оперативная память')
    sd_card = models.BooleanField(default=True, verbose_name='Поддержка карты памяти')
    sd_volume_max = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='Максимальный объем карты памяти'
    )
    built_in_memory = models.CharField(max_length=100, verbose_name='Встроенная память')
    main_cam_mp = models.CharField(max_length=100, verbose_name='Основная камера')
    front_cam_mp = models.CharField(max_length=100, verbose_name='Фронтальная камера')
    battery_capacity = models.CharField(max_length=100, verbose_name='Емкость батареи')

    def __str__(self):
        return f'{self.category.title} : {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):
    """Модель добавления продукта в корзину"""
    customer = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    # так же зададим related_name дабы различать поля в базе и можно было получать query сеты, например
    # "cart".related_products.all() выдаст нам сет со всеми продуктами в данной корзине

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Всего к оплате')

    def __str__(self):
        return f'Product: {self.content_object.title} для корзины'


class Cart(models.Model):
    """Сама модель корзины"""
    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    # связь многие к многим к нашей модели CartProduct
    # так же зададим related_name дабы различать поля в базе и можно было получать query сеты, например
    # "cartproduct".related_cart.all() выдаст нам сет со всеми корзинами содержащими нужный нам продукт

    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Всего к оплате')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    """Модель пользователя"""
    user = models.ForeignKey(USER, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, verbose_name='Номер телефона')
    address = models.CharField(max_length=250, verbose_name='Адрес')

    def __str__(self):
        return f'Покупатель: {self.user.first_name}, {self.user.last_name}'



