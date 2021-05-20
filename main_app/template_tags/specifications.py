from django import template
from django.utils.safestring import mark_safe

register = template.Library()

TABLE_HEAD = """
                <table class="table">
                     <tbody>
             """
TABLE_TAIL = """
                    </tbody>
                </table>
             """
TABLE_CONTENT = """
                    <tr>
                      <td>{name}</td>
                      <td>{value}</td>>
                    </tr>
                """
PRODUCT_SPEC = {
    'notebook': {
        'Тип экрана': 'display_type',
        'Диагональ экрана': 'diagonal',
        'Частота процессора': 'cpu_freq',
        'Оперативная память': 'ram',
        'Графический процессор': 'gpu',
        'Емкость батареи': 'battery_capacity',
        'Время автономной рвботы': 'time_without_charge',
    },
    'smartphone': {
        'Тип экрана': 'display_type',
        'Диагональ экрана': 'diagonal',
        'Разрешение экрана': 'resolution_display',
        'Частота процессора': 'cpu_freq',
        'Оперативная память': 'ram',
        'Емкость батареи': 'battery_capacity',
        'Поддержка карты памяти': 'sd_card',
        'Максимальный объем карты памяти': 'sd_volume_max',
        'Встроенная память': 'built_in_memory',
        'Основная камера': 'main_cam_mp',
        'Фронтальная камера': 'front_cam_mp',
    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
