# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.core.management import call_command
from digidemo.settings import INITIAL_DATA_FIXTURE

fixture = INITIAL_DATA_FIXTURE

def load_fixture(apps, schema_editor):
	call_command('loaddata', fixture, app_label='digidemo') 

class Migration(migrations.Migration):

    dependencies = [
        ('digidemo', '0001_initial'),
    ]

    operations = [
		migrations.RunPython(load_fixture),
    ]
