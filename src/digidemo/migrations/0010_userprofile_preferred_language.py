# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digidemo', '0009_auto_20150328_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='preferred_language',
            field=models.CharField(default=b'en-ca', max_length=5, verbose_name='preferred language', choices=[(b'en-ca', 'English'), (b'fr-ca', 'French')]),
            preserve_default=True,
        ),
    ]
