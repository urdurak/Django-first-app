from django import template
from setuptools.command.register import register

register = template.Library()

@register.filter
def who_is_my_followedes(user,my_followings):
    # for i in my_followings:
    #     if i.followed == user:
    #         print(user)
    if user.username in my_followings:
        return True
    return False