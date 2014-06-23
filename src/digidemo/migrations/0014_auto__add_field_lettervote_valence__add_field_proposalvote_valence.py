# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'LetterVote.valence'
        db.add_column(u'digidemo_lettervote', 'valence',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'ProposalVote.valence'
        db.add_column(u'digidemo_proposalvote', 'valence',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'LetterVote.valence'
        db.delete_column(u'digidemo_lettervote', 'valence')

        # Deleting field 'ProposalVote.valence'
        db.delete_column(u'digidemo_proposalvote', 'valence')


    models = {
        u'digidemo.capability': {
            'Meta': {'object_name': 'Capability'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Sector']"})
        },
        u'digidemo.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.User']"}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Letter']"}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        u'digidemo.factor': {
            'Meta': {'object_name': 'Factor'},
            'capability': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Capability']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Proposal']"}),
            'valence': ('django.db.models.fields.SmallIntegerField', [], {})
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
        u'digidemo.lettervote': {
            'Meta': {'unique_together': "(('user', 'letter'),)", 'object_name': 'LetterVote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Letter']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.User']"}),
            'valence': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'digidemo.organization': {
            'Meta': {'object_name': 'Organization'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legal_classification': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'legal_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'operations_summary': ('django.db.models.fields.TextField', [], {}),
            'revenue': ('django.db.models.fields.BigIntegerField', [], {}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
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
            'sector': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'proposals'", 'symmetrical': 'False', 'to': u"orm['digidemo.Sector']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'digidemo.proposalvote': {
            'Meta': {'unique_together': "(('user', 'proposal'),)", 'object_name': 'ProposalVote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Proposal']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.User']"}),
            'valence': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'digidemo.sector': {
            'Meta': {'object_name': 'Sector'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '3'})
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
            'rep': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['digidemo']