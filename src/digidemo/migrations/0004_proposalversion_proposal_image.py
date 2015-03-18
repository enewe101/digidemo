# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digidemo', '0003_proposalversion_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalversion',
            name='proposal_image',
            field=models.ImageField(default=b'/digidemo/proposal-images/', upload_to=b'proposal_avatars', verbose_name='issue image'),
            preserve_default=True,
        ),
    ]
