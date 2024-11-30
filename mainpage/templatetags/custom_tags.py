from django.utils.html import format_html
from django.template import Library

register = Library()

@register.simple_tag
def info_tag(label, value):
    return format_html(
        '''
<p>
    <span class = 'badge bg-warning rounded-pill'>
        <text class = 'text-warn fs-5'>
            {}: 
        </text>
    </span>
    <span class = 'badge bg-info rounded-pill'>
        <text class = 'text-error fs-5'>
            {}
        </text>
    </span>
</p>
''', label, value)

@register.simple_tag
def error_tag(text):
    return format_html('''
<p>
    <span class = 'badge bg-danger rounded-pill'>
        <text class = 'error-text fs-5'>
            {}               
        </text>
    </span>
</p>
''', text)

@register.simple_tag
def button_submit(value, _class):
    return format_html('''
<input type = 'submit' value = '{}' class = '{}'>
''', value, _class)

@register.simple_tag
def table():
    return format_html("<table class = 'table table-dark table-striped'>")

@register.simple_tag
def endtable():
    return format_html('</table>')

@register.simple_tag
def thead(*args):
    s = ''
    for arg in args:
        s += "<th class = 'text-center'>{}</th>\n".format(arg)
    return format_html('<thead>\n' + s + '</thead>\n')

@register.simple_tag
def tr(*args):
    s = ''
    if not args:
        return format_html('<tr>\n')
    for arg in args:
        s += "<td class = 'text-center'>{}</td>\n".format(arg)
    return format_html('<tr>\n' + s + '</tr>\n')

@register.simple_tag
def td(arg = None):
    if arg:
        return format_html("<td class = 'text-center'>{}</td>\n", arg)
    return format_html("<td class = 'text-center'>")

@register.simple_tag
def th(arg):
    return format_html("<th class = 'text-center'>{}</th>\n", arg)

@register.simple_tag
def endtd():
    return format_html('</td>\n')

@register.simple_tag
def endtr():
    return format_html('</tr>\n')

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def bol(value, yn: str):
    return yn.split('|')[0] if value else yn.split('|')[1]

@register.simple_tag
def stack():
    return format_html('''
<div class = 'container-fluid'>
    <div class = 'row'>
''')

@register.simple_tag
def endstack():
    return format_html('''
    </div>
</div>
''')

@register.simple_tag
def stack_el():
    return format_html('<div class = "col">')

@register.simple_tag
def endstack_el():
    return format_html('</div>')

@register.filter
def format(dt, frmt):
    return dt.strftime(frmt)