# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digidemo', '0008_discussion_target_part'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='title',
            field=models.CharField(default=b'', max_length=256, verbose_name='title'),
            preserve_default=True,
        ),
    ]
