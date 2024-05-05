from django import template

register = template.Library()


@register.simple_tag
def get_user_can_edit_scholarship(user, scholarship):
    return user.can_edit_scholarship(scholarship)
