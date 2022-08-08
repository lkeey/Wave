from django import template
from django import template  

register = template.Library()


@register.simple_tag
def get_companion(user, chat):
    for u in chat.members.all():
        if u != user:
            return u
    return None

@register.simple_tag
def myDate(value):
    #arg is optional and not needed but you could supply your own formatting if you want.
    # dateformatted = value.strftime("%b %d, %Y at %I:%M %p")
    dateformatted = value.strftime("%I:%M %p")
    return dateformatted