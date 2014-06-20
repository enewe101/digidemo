# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table(u'digidemo_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('legal_classification', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('revenue', self.gf('django.db.models.fields.BigIntegerField')()),
            ('operations_summary', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'digidemo', ['Organization'])

        # Adding model 'Person'
        db.create_table(u'digidemo_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fname', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('lname', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('portrait_url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('wikipedia_url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('bio_summary', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'digidemo', ['Person'])

        # Adding model 'Position'
        db.create_table(u'digidemo_position', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Person'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Organization'])),
            ('salary', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('mandate_summary', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'digidemo', ['Position'])

        # Adding M2M table for field recipients on 'Letter'
        m2m_table_name = db.shorten_name(u'digidemo_letter_recipients')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('letter', models.ForeignKey(orm[u'digidemo.letter'], null=False)),
            ('position', models.ForeignKey(orm[u'digidemo.position'], null=False))
        ))
        db.create_unique(m2m_table_name, ['letter_id', 'position_id'])


    def backwards(self, orm):
        # Deleting model 'Organization'
        db.delete_table(u'digidemo_organization')

        # Deleting model 'Person'
        db.delete_table(u'digidemo_person')

        # Deleting model 'Position'
        db.delete_table(u'digidemo_position')

        # Removing M2M table for field recipients on 'Letter'
        db.delete_table(db.shorten_name(u'digidemo_letter_recipients'))


    models = {
        u'digidemo.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.User']"}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Letter']"}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        u'digidemo.letter': {
            'Meta': {'object_name': 'Letter'},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Proposal']"}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'letters'", 'symmetrical': 'False', 'to': u"orm['digidemo.Position']"}),
            'resenders': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'resent_letters'", 'symmetrical': 'False', 'to': u"orm['digidemo.User']"}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.User']"}),
            'valence': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'digidemo.organization': {
            'Meta': {'object_name': 'Organization'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legal_classification': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'operations_summary': ('django.db.models.fields.TextField', [], {}),
            'revenue': ('django.db.models.fields.BigIntegerField', [], {})
        },
        u'digidemo.person': {
            'Meta': {'object_name': 'Person'},
            'bio_summary': ('django.db.models.fields.TextField', [], {}),
            'fname': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lname': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'portrait_url': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'wikipedia_url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'digidemo.position': {
            'Meta': {'object_name': 'Position'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandate_summary': ('django.db.models.fields.TextField', [], {}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Organization']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Person']"}),
            'salary': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '14'})
        },
        u'digidemo.proposal': {
            'Meta': {'object_name': 'Proposal'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.User']"}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
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