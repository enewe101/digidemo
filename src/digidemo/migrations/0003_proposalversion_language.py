# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digidemo', '0002_auto_20150309_0437'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalversion',
            name='language',
            field=models.CharField(default=b'en-ca', max_length=5, verbose_name='language', choices=[(b'en-ca', 'English'), (b'fr-ca', 'French')]),
            preserve_default=True,
        ),
    ]
