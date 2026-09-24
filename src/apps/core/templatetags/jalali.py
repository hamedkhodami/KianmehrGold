from datetime import date, datetime

from django import template
from django.utils import timezone
from khayyam import JalaliDatetime


register = template.Library()


@register.filter
def jalali(value, arg=None):
    try:
        if isinstance(value, date) and not isinstance(value, datetime):
            value = datetime.combine(value, datetime.min.time())

        local_time = timezone.localtime(value)

        format_string = arg if arg else "%Y/%m/%d"

        return JalaliDatetime(local_time).strftime(format_string)
    except:
        return value
