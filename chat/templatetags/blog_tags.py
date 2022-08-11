from django import template
from django import template  
from chat.models import Message, Chat
from django.db.models import Q

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

@register.simple_tag
def get_count_unreaded(chat, participant):
    count = Message.unreaded_objects.get_amount_unreaded().all().filter(chat=chat, author=participant).count()
    # names = Message.unreaded_objects.all().filter(chat=chat.id)
    
    return count

@register.simple_tag
def get_all_unreaded(user):

    count = Message.unreaded_objects.get_amount_unreaded().all().filter(chat__members__in=[user.id]).exclude(author=user).count()

    return count

