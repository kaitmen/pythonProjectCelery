import re

from django import template

register = template.Library()

CENSORED_WORDS = ('some', 'bad', 'words', 'Article4')
VOWEL='aeoyui'

def check_word(word):
    if word in CENSORED_WORDS:
        word = re.sub(r'[aeiouy]', '*', word)
    return word


@register.filter(name="my_censor")
def censor(value):
    words = value.split()
    words = [check_word(word) for word in words]
    return ' '.join(words)