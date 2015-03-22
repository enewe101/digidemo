# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digidemo', '0004_proposalversion_proposal_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='proposal_image',
            field=models.ImageField(default=b'digidemo/proposal-images/', upload_to=b'proposal_avatars', verbose_name='issue image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposalversion',
            name='proposal_image',
            field=models.ImageField(default=b'digidemo/proposal-images/default.jpg', upload_to=b'proposal-images', verbose_name='issue image'),
            preserve_default=True,
        ),
    ]
