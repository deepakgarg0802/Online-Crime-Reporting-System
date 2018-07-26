from django import template

register = template.Library()

@register.filter
def get_last(value):
    spam = value.split('/')[-1]         # assume value be /python/web-scrapping
                                        # spam would be 'web-scrapping'
    spam = ' '.join(spam.split('-'))    # now spam would be 'web scrapping'
    return spam




@register.filter
def to_class_name(value):
    return value.__class__.__name__