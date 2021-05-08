from django import template
from datetime import datetime

register = template.Library()


@register.filter
def format_datetime(date):
    # This is a custom filter which format datetime string
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    date = date.strftime("%d/%m/%Y %H:%M:%S")
    return date
