from django import template

register = template.Library()

# Список нецензурных слов
CENSORED_WORDS = ['редиска', 'нехороший', 'плохой']


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр 'censor' применяется только к строкам")

    for word in CENSORED_WORDS:
        # Заменяем слово на звёздочки
        value = value.replace(word, word[0] + '*' * (len(word) - 1))
        value = value.replace(word.capitalize(), word[0].capitalize() + '*' * (len(word) - 1))

    return value
