from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='intcomma')
@stringfilter
def intcomma(value):
    try:
        value = str(value).replace(',', '')

        if '.' in value:
            int_part, dec_part = value.split('.')
            int_part = _add_commas(int_part)
            return int(f'{int_part}.{dec_part}')
        else:
            return _add_commas(value)

    except ValueError:
        return value


def _add_commas(value):
    reversed_value = value[::-1]
    parts = [reversed_value[i:i+3] for i in range(0, len(reversed_value), 3)]
    formated_value = ','.join(parts)

    return formated_value[::-1]
