# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

from rooibos.util.database_operations import db_table_exists

MIGRATION_DEPS = [
    ('contenttypes', '0002_remove_content_type_name'),
    ('auth', '0006_require_contenttypes_0002'),
    ('flatpages', '__first__'),
    ('admin', '__first__'),
    ('sessions', '__first__'),
    ('sites', '__first__'),
    ('redirects', '__first__'),
    ('django_comments', '__first__'),
    ('impersonate', '__first__'),
    ('util', '__first__'),
    ('migration', '__first__'),
    ('tagging', '__first__'),
    migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]

if db_table_exists('django_content_type'):
    FIRST_DEPS = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
else:
    FIRST_DEPS = [
        ('contenttypes', '__first__'),
    ]

# DEPENDENCIES = FIRST_DEPS + MIGRATION_DEPS
DEPENDENCIES = MIGRATION_DEPS

print 'Rooibos Migration using Migration Dependencies: %s' % str(DEPENDENCIES)


class Migration(migrations.Migration):
    dependencies = DEPENDENCIES

    operations = [
        migrations.CreateModel(
            name='AccessControl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(db_index=True)),
                ('read', models.NullBooleanField()),
                ('write', models.NullBooleanField()),
                ('manage', models.NullBooleanField()),
                ('restrictions_repr', models.TextField(default=b'', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'access_accesscontrol',
            },
        ),
        migrations.CreateModel(
            name='AccumulatedActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(null=True, db_index=True)),
                ('date', models.DateField(db_index=True)),
                ('event', models.CharField(max_length=64, db_index=True)),
                ('final', models.BooleanField(default=False)),
                ('count', models.IntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
            options={
                'db_table': 'statistics_accumulatedactivity',
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(null=True, db_index=True)),
                ('date', models.DateField(db_index=True)),
                ('time', models.TimeField()),
                ('event', models.CharField(max_length=64, db_index=True)),
                ('data_field', models.TextField(db_column=b'data', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
                ('user_field',
                 models.ForeignKey(db_column=b'user_id', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'statistics_activity',
            },
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'access_attribute',
            },
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=255)),
                ('attribute', models.ForeignKey(to='rooibos.Attribute')),
            ],
            options={
                'db_table': 'access_attributevalue',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('name', models.SlugField(unique=True, blank=True)),
                ('hidden', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('agreement', models.TextField(null=True, blank=True)),
                ('password', models.CharField(max_length=32, blank=True)),
                ('children',
                 models.ManyToManyField(to='rooibos.Collection', db_table=b'data_collection_children', blank=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['title'],
                'db_table': 'data_collection',
            },
        ),
        migrations.CreateModel(
            name='CollectionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hidden', models.BooleanField(default=False)),
                ('collection', models.ForeignKey(to='rooibos.Collection')),
            ],
            options={
                'db_table': 'data_collectionitem',
            },
        ),
        migrations.CreateModel(
            name='ExtendedGroup',
            fields=[
                ('group_ptr',
                 models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False,
                                      to='auth.Group')),
                ('type', models.CharField(max_length=1, choices=[(b'A', b'Authenticated'), (b'I', b'IP Address based'),
                                                                 (b'P', b'Attribute based'), (b'E', b'Everybody')])),
            ],
            options={
                'db_table': 'access_extendedgroup',
            },
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100)),
                ('name', models.SlugField()),
                ('old_name', models.CharField(max_length=100, null=True, blank=True)),
                ('equivalent', models.ManyToManyField(related_name='equivalent_rel_+', null=True, to='rooibos.Field',
                                                      db_table=b'data_field_equivalent', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'data_field',
            },
        ),
        migrations.CreateModel(
            name='FieldSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('name', models.SlugField()),
                ('standard', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['title'],
                'db_table': 'data_fieldset',
            },
        ),
        migrations.CreateModel(
            name='FieldSetField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100, null=True, blank=True)),
                ('order', models.IntegerField(default=0)),
                ('importance', models.SmallIntegerField(default=1)),
                ('field', models.ForeignKey(to='rooibos.Field')),
                ('fieldset', models.ForeignKey(to='rooibos.FieldSet')),
            ],
            options={
                'ordering': ['order'],
                'db_table': 'data_fieldsetfield',
            },
        ),
        migrations.CreateModel(
            name='FieldValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('refinement', models.CharField(max_length=100, null=True, blank=True)),
                ('label', models.CharField(max_length=100, null=True, blank=True)),
                ('hidden', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
                ('group', models.IntegerField(null=True, blank=True)),
                ('value', models.TextField()),
                ('index_value', models.CharField(max_length=32, db_index=True)),
                ('date_start', models.DecimalField(null=True, max_digits=12, decimal_places=0, blank=True)),
                ('date_end', models.DecimalField(null=True, max_digits=12, decimal_places=0, blank=True)),
                ('numeric_value', models.DecimalField(null=True, max_digits=18, decimal_places=4, blank=True)),
                ('language', models.CharField(max_length=5, null=True, blank=True)),
                ('context_id', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ['order'],
                'db_table': 'data_fieldvalue',
            },
        ),
        migrations.CreateModel(
            name='JobInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('func', models.CharField(max_length=128)),
                ('arg', models.TextField()),
                ('status', models.TextField(null=True, blank=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('status_time', models.DateTimeField(null=True, blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('result', models.TextField()),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['completed', '-created_time'],
                'db_table': 'workers_jobinfo',
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField()),
                ('url', models.CharField(max_length=1024)),
                ('mimetype', models.CharField(default=b'application/binary', max_length=128)),
                ('width', models.IntegerField(null=True)),
                ('height', models.IntegerField(null=True)),
                ('bitrate', models.IntegerField(null=True)),
                ('master', models.ForeignKey(related_name='derivatives', to='rooibos.Media', null=True)),
            ],
            options={
                'db_table': 'storage_media',
                'verbose_name_plural': 'media',
            },
        ),
        migrations.CreateModel(
            name='MetadataStandard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('name', models.SlugField(unique=True)),
                ('prefix', models.CharField(unique=True, max_length=16)),
            ],
            options={
                'db_table': 'data_metadatastandard',
            },
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('name', models.SlugField(unique=True)),
                ('hidden', models.BooleanField(default=False)),
                ('source', models.CharField(max_length=1024, null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('password', models.CharField(max_length=32, null=True, blank=True)),
                ('hide_default_data', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('fieldset', models.ForeignKey(to='rooibos.FieldSet', null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'presentation_presentation',
                'permissions': (('publish_presentations', 'Can publish presentations'),),
            },
        ),
        migrations.CreateModel(
            name='PresentationItemInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('info', models.TextField(blank=True)),
                ('item', models.ForeignKey(related_name='media', to='presentation.PresentationItem')),
                ('media', models.ForeignKey(to='rooibos.Media')),
            ],
            options={
                'db_table': 'presentation_presentationiteminfo',
            },
        ),
        migrations.CreateModel(
            name='ProxyUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=36)),
                ('url', models.CharField(max_length=1024)),
                ('context', models.CharField(max_length=256, null=True, blank=True)),
                ('user_backend', models.CharField(max_length=256, null=True, blank=True)),
                ('last_access', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'storage_proxyurl',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(unique=True)),
                ('source', models.CharField(max_length=1024, null=True, blank=True)),
                ('manager', models.CharField(max_length=50, null=True, blank=True)),
                ('next_update', models.DateTimeField(null=True, blank=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', models.ForeignKey(blank=True, to='rooibos.Record', null=True)),
            ],
            options={
                'db_table': 'data_record',
            },
        ),
        migrations.CreateModel(
            name='PresentationItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hidden', models.BooleanField(default=False)),
                ('type', models.CharField(max_length=16, blank=True)),
                ('order', models.SmallIntegerField()),
                ('presentation', models.ForeignKey(related_name='items', to='presentation.Presentation')),
                ('record', models.ForeignKey(to='rooibos.Record')),
            ],
            options={
                'ordering': ['order'],
                'db_table': 'presentation_presentationitem',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('name', models.SlugField()),
                ('system', models.CharField(max_length=50)),
                ('base',
                 models.CharField(help_text=b'Absolute path to server directory containing files.', max_length=1024,
                                  null=True)),
                ('urlbase', models.CharField(
                    help_text=b'URL at which stored file is available, e.g. through streaming. May contain %(filename)s placeholder, which will be replaced with the media url property.',
                    max_length=1024, null=True, verbose_name=b'URL base', blank=True)),
                ('deliverybase', models.CharField(db_column=b'serverbase', max_length=1024, blank=True,
                                                  help_text=b'Absolute path to server directory in which a temporary symlink to the actual file should be created when the file is requested e.g. for streaming.',
                                                  null=True, verbose_name=b'server base')),
                ('derivative', models.IntegerField(null=True, db_column=b'derivative_id')),
            ],
            options={
                'db_table': 'storage_storage',
                'verbose_name_plural': 'storage',
            },
        ),
        migrations.CreateModel(
            name='Subnet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subnet', models.CharField(max_length=80)),
                ('group', models.ForeignKey(to='rooibos.ExtendedGroup')),
            ],
            options={
                'db_table': 'access_subnet',
            },
        ),
        migrations.CreateModel(
            name='TrustedSubnet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subnet', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'storage_trustedsubnet',
            },
        ),
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('name', models.SlugField()),
                ('description', models.TextField(null=True, blank=True)),
                ('standard', models.NullBooleanField()),
                ('origin', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'data_vocabulary',
                'verbose_name_plural': 'vocabularies',
            },
        ),
        migrations.CreateModel(
            name='VocabularyTerm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.TextField()),
                ('vocabulary', models.ForeignKey(to='rooibos.Vocabulary')),
            ],
            options={
                'db_table': 'data_vocabularyterm',
            },
        ),
        migrations.CreateModel(
            name='DisplayFieldValue',
            fields=[
                ('fieldvalue_ptr',
                 models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False,
                                      to='rooibos.FieldValue')),
            ],
            options={
                'db_table': 'data_displayfieldvalue',
            },
            bases=('rooibos.fieldvalue',),
        ),
        migrations.AddField(
            model_name='proxyurl',
            name='subnet',
            field=models.ForeignKey(to='rooibos.TrustedSubnet'),
        ),
        migrations.AddField(
            model_name='proxyurl',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='media',
            name='record',
            field=models.ForeignKey(to='rooibos.Record'),
        ),
        migrations.AddField(
            model_name='media',
            name='storage',
            field=models.ForeignKey(to='rooibos.Storage'),
        ),
        migrations.AddField(
            model_name='fieldvalue',
            name='context_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='fieldvalue',
            name='field',
            field=models.ForeignKey(to='rooibos.Field'),
        ),
        migrations.AddField(
            model_name='fieldvalue',
            name='owner',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='fieldvalue',
            name='record',
            field=models.ForeignKey(editable=False, to='rooibos.Record'),
        ),
        migrations.AddField(
            model_name='fieldset',
            name='fields',
            field=models.ManyToManyField(to='rooibos.Field', through='rooibos.FieldSetField'),
        ),
        migrations.AddField(
            model_name='fieldset',
            name='owner',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='standard',
            field=models.ForeignKey(blank=True, to='rooibos.MetadataStandard', null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='vocabulary',
            field=models.ForeignKey(blank=True, to='rooibos.Vocabulary', null=True),
        ),
        migrations.AddField(
            model_name='collectionitem',
            name='record',
            field=models.ForeignKey(to='rooibos.Record'),
        ),
        migrations.AddField(
            model_name='collection',
            name='records',
            field=models.ManyToManyField(to='rooibos.Record', through='rooibos.CollectionItem'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='group',
            field=models.ForeignKey(to='rooibos.ExtendedGroup'),
        ),
        migrations.AddField(
            model_name='accesscontrol',
            name='usergroup',
            field=models.ForeignKey(blank=True, to='auth.Group', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='media',
            unique_together=set([('record', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='field',
            unique_together=set([('name', 'standard')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='field',
            order_with_respect_to='standard',
        ),
        migrations.AlterUniqueTogether(
            name='accesscontrol',
            unique_together=set([('content_type', 'object_id', 'user', 'usergroup')]),
        ),
    ]
