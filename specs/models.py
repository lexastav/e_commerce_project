from django.db import models

class CategoryFeature(models.Model):

    """Характеристика конкретной категории"""

    category = models.ForeignKey('main_app.Category', verbose_name='Категория')
