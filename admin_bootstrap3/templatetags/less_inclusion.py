from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('admin/includes/less_include.html', takes_context=True)
def less_include(context):
    less_file = getattr(settings, 'ADMIN_LESS_FILE', None)
    if less_file:
        context['less_file'] = less_file
        return context
    return None
