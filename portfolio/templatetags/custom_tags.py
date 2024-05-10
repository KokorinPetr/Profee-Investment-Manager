from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    price = dictionary.get(key)
    if price == 'Currency not in our base yet':
        return price
    return float(dictionary.get(key))


@register.filter
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
