from django import template
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.urlresolvers import reverse
from django.forms import ModelChoiceField, DateField, ModelMultipleChoiceField
from django.template.loader import get_template
from django.template import Context
from django.forms.fields import SplitDateTimeField
from django.utils.safestring import mark_safe

register = template.Library()


class BootstrapWidgetNode(template.Node):
    def __init__(self, field_name, attributes):
        self.attributes = attributes
        if 'is_inlines' in attributes:
            self.is_inlines = attributes.pop('is_inlines') == 'True'
        else:
            self.is_inlines = False
        self.field_name = field_name
        self.field = template.Variable(field_name)

    def render(self, context):
        try:
            actual_field = self.field.resolve(context)
            if isinstance(actual_field.field, ReadOnlyPasswordHashField):
                return self.render_readonly_widgets(actual_field)

            if isinstance(actual_field.field, SplitDateTimeField):
                return self.render_date_time_widgets(actual_field)

            if isinstance(actual_field.field, ModelMultipleChoiceField):
                return self.render_model_multiple_choice_widgets(actual_field)

            if isinstance(actual_field.field, ModelChoiceField):
                return self.render_model_choice_widgets(actual_field)

            if isinstance(actual_field.field, DateField):
                return self.render_date_widgets(actual_field)

            if hasattr(actual_field.field.widget, 'widgets'):
                pass

            if 'class' in actual_field.field.widget.attrs:
                self.attributes['class'] = 'form-control {}'.format(actual_field.field.widget.attrs['class'])
                # actual_field.field.widget.attrs = self.attributes
                # if actual_field.field.required and not self.is_inlines:
                #     self.attributes['required'] = ''
                # actual_field.field.widget.attrs.update(self.attributes)
                # return actual_field.as_widget()
            # else:
            if actual_field.field.required and not self.is_inlines:
                self.attributes['required'] = ''
            return actual_field.as_widget(attrs=self.attributes)
        except template.VariableDoesNotExist:
            return ''

    def render_date_time_widgets(self, field):
        date_widget = field.field.widget.widgets[0]
        date_widget.attrs['class'] = 'date-field form-control'
        time_widget = field.field.widget.widgets[1]
        time_widget.attrs['class'] = 'time-field form-control'
        time_widget.attrs['size'] = 10
        values = field.value()
        if not isinstance(values, list):
            values = field.field.widget.decompress(field.value())
        output = get_template('admin/widgets/date_time_widget.html')
        html_output = output.render(Context({
            'date_widget': date_widget.render('{}_0'.format(field.name), values[0]),
            'time_widget': time_widget.render('{}_1'.format(field.name), values[1]),
        }))
        return html_output

    def render_date_widgets(self, field):
        date_widget = field.field.widget
        date_widget.attrs['class'] = 'date-field form-control'
        value = field.value()
        # if not isinstance(values, list):
        #     values = field.field.widget.decompress(field.value())
        output = get_template('admin/widgets/date_widget.html')
        html_output = output.render(Context({
            'date_widget': date_widget.render(field.name, value),
        }))
        return html_output

    def render_model_choice_widgets(self, field):
        # import ipdb;ipdb.set_trace()
        # field.field.widget_attrs['class'] = 'form-control'
        widget = field.field.widget
        can_add_related = False
        if hasattr(field.field.widget, 'widget'):
            widget = field.field.widget.widget
        else:
            field.field.widget.attrs['class'] = 'form-control'
            return field.as_widget()
        if hasattr(field.field.widget, 'can_add_related'):
            can_add_related = field.field.widget.can_add_related
        related_url = None
        if can_add_related:
            rel_to = field.field.widget.rel.to
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = reverse('admin:%s_%s_add' % info, current_app=field.field.widget.admin_site.name)
        widget.attrs['class'] = 'form-control'
        widget.attrs['id'] = 'id_{}'.format(field.name)
        if field.field.required and not self.is_inlines:
            widget.attrs['required'] = ''
        output = get_template('admin/widgets/model_select_widget.html')
        html_output = output.render(Context({
            'model_select_widget': widget.render(field.name, field.value(), attrs={
                'id': field.auto_id,
                'name': field.html_name,
            }),
            'related_url': related_url,
            'name': 'add_id_{}'.format(field.name)
        }))
        return html_output

    def render_model_multiple_choice_widgets(self, field):
        widget = field.field.widget.widget
        field.help_text = ''
        can_add_related = field.field.widget.can_add_related
        related_url = None
        if can_add_related:
            rel_to = field.field.widget.rel.to
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = reverse('admin:%s_%s_add' % info, current_app=field.field.widget.admin_site.name)
        widget.attrs['id'] = 'id_{}'.format(field.name)
        if field.field.required and not self.is_inlines:
            widget.attrs['required'] = ''
        output = get_template('admin/widgets/model_select_widget.html')
        rendered_output = widget.render(field.name, field.value(), attrs={'class': 'form-control'})
        rendered_output = rendered_output.replace('SelectFilter.init(', 'ActivateChosen(')
        rendered_output = rendered_output.replace('selectfilter', 'selectfilter form-control')
        html_output = output.render(Context({
            'model_select_widget': mark_safe(rendered_output),
            'related_url': related_url,
            'name': 'add_id_{}'.format(field.name)
        }))
        return html_output

    def render_readonly_widgets(self, field):
        widget = field.field.widget
        widget.attrs['id'] = 'id_{}'.format(field.name)
        rendered_output = widget.render(field.name, field.value(), attrs={
            'id': 'id_{}'.format(field.name),
            'class': 'form-control-static',
        })
        return rendered_output


@register.tag()
def bootstrap_widget(parser, token):
    contents = token.split_contents()
    attributes = {}
    if len(contents) > 2:
        for a in contents[2:]:
            kv = a.split('=')
            key = kv[0]
            value = kv[1]
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            attributes[key] = value
        is_inlines=contents[2].split('=')[1] == 'True'
    else:
        is_inlines=False
    field_name = contents[1]
    attributes['class'] = 'form-control'
    return BootstrapWidgetNode(field_name, attributes)
