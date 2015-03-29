# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digidemo', '0007_auto_20150328_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='target_part',
            field=models.CharField(default=b'na', max_length=16, choices=[(b'summary', b'summary'), (b'text', b'text'), (b'na', b'na')]),
            preserve_default=True,
        ),
    ]
