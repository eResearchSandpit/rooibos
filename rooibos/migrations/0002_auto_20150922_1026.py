# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooibos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobinfo',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='fieldset',
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='presentationitem',
            name='presentation',
        ),
        migrations.RemoveField(
            model_name='presentationitem',
            name='record',
        ),
        migrations.RemoveField(
            model_name='presentationiteminfo',
            name='item',
        ),
        migrations.RemoveField(
            model_name='presentationiteminfo',
            name='media',
        ),
        migrations.DeleteModel(
            name='JobInfo',
        ),
        migrations.DeleteModel(
            name='Presentation',
        ),
        migrations.DeleteModel(
            name='PresentationItem',
        ),
        migrations.DeleteModel(
            name='PresentationItemInfo',
        ),
    ]
