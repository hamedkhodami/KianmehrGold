from django import template
from django.utils import timezone
from khayyam import JalaliDatetime


register = template.Library()


@register.filter
def jalali(value):
    try:
        local_time = timezone.localtime(value)
        return JalaliDatetime(local_time).strftime("%Y/%m/%d %H:%M")
    except:
        return value
