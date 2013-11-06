from django import template


register = template.Library()


class ResultNode(template.Node):
    def __init__(self, result):
        self.result = template.Variable(result)

    def render(self, context):
        try:
            self.item = self.result.resolve(context)
            if 'icon-no.gif' in self.item:
                self.item = '<td>No</td>'
            if 'icon-yes.gif' in self.item:
                self.item = '<td>Yes</td>'

            return self.item
        except template.VariableDoesNotExist:
            return ''


@register.tag()
def tidy_result(parser, token):
    tag_name, result = token.split_contents()
    return ResultNode(result)
