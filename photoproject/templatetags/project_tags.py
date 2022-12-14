from datetime import timedelta, datetime
from django import template
from random import randint
from accounts.models import User
import json

register = template.Library()


@register.filter
def index(elem, index):
    return elem[index]


@register.filter
def image_first(elem):
    return elem.first().photo.url
