from django.db import models


class CategoryFeature(models.Model):

    """Характеристика конкретной категории"""

    category = models.ForeignKey('main_app.Category', verbose_name='Категория', on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=150, verbose_name='Имя характеристики')
    feature_filter_name = models.CharField(max_length=50, verbose_name='Имя для фильтра')
    unit = models.CharField(max_length=50, verbose_name='Единица измерения', null=True, blank=True)

    class Meta:
        unique_together = ('category', 'feature_name', 'feature_filter_name')

    def __str__(self):
        return f'{self.category.title} | {self.feature_name}'


class FeatureValidator(models.Model):
    """
    Этот класс нужен для того, что бы мы могли создавать присваивать уникальные характеристики для каждлой категории
    """

    category = models.ForeignKey('main_app.Category', verbose_name='Категория', on_delete=models.CASCADE)
    feature_key = models.ForeignKey(CategoryFeature, verbose_name='Ключ характеристики', on_delete=models.CASCADE)
    validation_feature_value = models.CharField(max_length=100, verbose_name='Валидное значение')

    def __str__(self):
        return f'Категория - "{self.category.title}" | ' \
               f'Харатеристика - "{self.feature_key.feature_name}" |' \
               f'валидное значение - "{self.validation_feature_value}"'


class ProductFeatures(models.Model):
    """
    Характеристики продукта
    """

    product = models.ForeignKey('main_app.Product', verbose_name='Товар', on_delete=models.CASCADE)
    feature = models.ForeignKey(CategoryFeature, verbose_name='Характеристика', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name='Значение')

    def __str__(self):
        return f'Товар -"{self.product.title}"' \
               f'Характеристика - "{self.feature.feature_name}"' \
               f'Значение - "{self.value}"'


