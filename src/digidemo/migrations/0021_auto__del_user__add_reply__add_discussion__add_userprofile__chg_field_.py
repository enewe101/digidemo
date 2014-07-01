# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'digidemo_user')

        # Adding model 'Reply'
        db.create_table(u'digidemo_reply', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('discussion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Discussion'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('score', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('is_open', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'digidemo', ['Reply'])

        # Adding model 'Discussion'
        db.create_table(u'digidemo_discussion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proposal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Proposal'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('score', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('is_open', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('last_activity_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'digidemo', ['Discussion'])

        # Adding model 'UserProfile'
        db.create_table(u'digidemo_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('email_validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('avatar_img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('rep', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
        ))
        db.send_create_signal(u'digidemo', ['UserProfile'])


        # Changing field 'LetterVote.user'
        db.alter_column(u'digidemo_lettervote', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Proposal.author'
        db.alter_column(u'digidemo_proposal', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'ProposalVote.user'
        db.alter_column(u'digidemo_proposalvote', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Letter.sender'
        db.alter_column(u'digidemo_letter', 'sender_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Comment.author'
        db.alter_column(u'digidemo_comment', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

    def backwards(self, orm):
        # Adding model 'User'
        db.create_table(u'digidemo_user', (
            ('province', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('avatar_name', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=20)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email_validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('rep', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lname', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('fname', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('avatar_img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'digidemo', ['User'])

        # Deleting model 'Reply'
        db.delete_table(u'digidemo_reply')

        # Deleting model 'Discussion'
        db.delete_table(u'digidemo_discussion')

        # Deleting model 'UserProfile'
        db.delete_table(u'digidemo_userprofile')


        # Changing field 'LetterVote.user'
        db.alter_column(u'digidemo_lettervote', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.User']))

        # Changing field 'Proposal.author'
        db.alter_column(u'digidemo_proposal', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.User']))

        # Changing field 'ProposalVote.user'
        db.alter_column(u'digidemo_proposalvote', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.User']))

        # Changing field 'Letter.sender'
        db.alter_column(u'digidemo_letter', 'sender_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.User']))

        # Changing field 'Comment.author'
        db.alter_column(u'digidemo_comment', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.User']))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'digidemo.capability': {
            'Meta': {'object_name': 'Capability'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Sector']"})
        },
        u'digidemo.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Letter']"}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        u'digidemo.discussion': {
            'Meta': {'object_name': 'Discussion'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_activity_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Proposal']"}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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
            'parent_letter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Letter']", 'null': 'True', 'blank': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Proposal']"}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'letters'", 'symmetrical': 'False', 'to': u"orm['digidemo.Position']"}),
            'resenders': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'resent_letters'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'valence': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'digidemo.lettervote': {
            'Meta': {'unique_together': "(('user', 'letter'),)", 'object_name': 'LetterVote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Letter']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
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
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'proposal_image': ('django.db.models.fields.files.ImageField', [], {'default': "'/digidemo/proposal-images/'", 'max_length': '100'}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'sector': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'proposals'", 'symmetrical': 'False', 'to': u"orm['digidemo.Sector']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'digidemo.proposalvote': {
            'Meta': {'unique_together': "(('user', 'proposal'),)", 'object_name': 'ProposalVote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Proposal']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'valence': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'digidemo.reply': {
            'Meta': {'object_name': 'Reply'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digidemo.Discussion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'digidemo.sector': {
            'Meta': {'object_name': 'Sector'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'digidemo.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'avatar_img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'email_validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'rep': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['digidemo']