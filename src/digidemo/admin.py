from django.contrib import admin
from digidemo.models import *
from django.db.models import get_models, get_app

for model in get_models(get_app('digidemo')):
    admin.site.register(model)

