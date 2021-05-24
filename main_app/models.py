from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

USER = get_user_model()


class Category(models.Model):
    """Категория продукта"""
    title = models.CharField(max_length=250, verbose_name='Наименование категории')
    slug = models.SlugField(unique=True)  # нужен для того, что бы у нас был некий конечный end point в нашей модели.
    # То есть чтобы мы могли перейти по ссылке ..../category/smartphones, вот smartphones и есть slug.

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    """Сам продукт"""

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

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class CartProduct(models.Model):
    """Модель добавления продукта в корзину"""
    customer = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    # так же зададим related_name дабы различать поля в базе и можно было получать query сеты, например
    # "cart".related_products.all() выдаст нам сет со всеми продуктами в данной корзине
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Всего к оплате')

    def __str__(self):
        return f'Product: {self.product.title} для корзины'

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    """Сама модель корзины"""
    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    # связь многие к многим к нашей модели CartProduct
    # так же зададим related_name дабы различать поля в базе и можно было получать query сеты, например
    # "cartproduct".related_cart.all() выдаст нам сет со всеми корзинами содержащими нужный нам продукт

    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Всего к оплате')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    """Модель пользователя"""
    user = models.ForeignKey(USER, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=250, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_customer')

    def __str__(self):
        return f'Покупатель: {self.user.first_name}, {self.user.last_name}'


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(
        Customer, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1000, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(
        max_length=100, verbose_name='Тип заказа', choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)





