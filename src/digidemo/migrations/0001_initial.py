# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'digidemo_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('email_validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('avatar_img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('avatar_name', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('fname', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('lname', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
        ))
        db.send_create_signal(u'digidemo', ['User'])

        # Adding model 'Proposal'
        db.create_table(u'digidemo_proposal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.User'])),
        ))
        db.send_create_signal(u'digidemo', ['Proposal'])

        # Adding model 'Letter'
        db.create_table(u'digidemo_letter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.User'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'digidemo', ['Letter'])

        # Adding M2M table for field resenders on 'Letter'
        m2m_table_name = db.shorten_name(u'digidemo_letter_resenders')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('letter', models.ForeignKey(orm[u'digidemo.letter'], null=False)),
            ('user', models.ForeignKey(orm[u'digidemo.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['letter_id', 'user_id'])

        # Adding model 'Comment'
        db.create_table(u'digidemo_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.User'])),
            ('letter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Letter'])),
            ('body', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'digidemo', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'digidemo_user')

        # Deleting model 'Proposal'
        db.delete_table(u'digidemo_proposal')

        # Deleting model 'Letter'
        db.delete_table(u'digidemo_letter')

        # Removing M2M table for field resenders on 'Letter'
        db.delete_table(db.shorten_name(u'digidemo_letter_resenders'))

        # Deleting model 'Comment'
        db.delete_table(u'digidemo_comment')


    models = {
        u'digidemo.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.User']"}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Letter']"}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'digidemo.letter': {
            'Meta': {'object_name': 'Letter'},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resenders': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'resent_letters'", 'symmetrical': 'False', 'to': u"orm['digidemo.User']"}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.User']"})
        },
        u'digidemo.proposal': {
            'Meta': {'object_name': 'Proposal'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.User']"}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'digidemo.user': {
            'Meta': {'object_name': 'User'},
            'avatar_img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'avatar_name': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'email_validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fname': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lname': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['digidemo']