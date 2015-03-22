# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digidemo', '0005_auto_20150321_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='proposal_image',
            field=models.ImageField(default=b'proposal-images/default.jpg', upload_to=b'proposal_avatars', verbose_name='issue image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposalversion',
            name='proposal_image',
            field=models.ImageField(default=b'proposal-images/default.jpg', upload_to=b'proposal-images', verbose_name='issue image'),
            preserve_default=True,
        ),
    ]
