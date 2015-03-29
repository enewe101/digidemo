# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digidemo', '0006_auto_20150321_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='anchor',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='discussion',
            name='is_inline',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='discussion',
            name='quote',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
