# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sector'
        db.create_table(u'digidemo_sector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'digidemo', ['Sector'])

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

        # Adding model 'Proposal'
        db.create_table(u'digidemo_proposal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('score', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('proposal_image', self.gf('django.db.models.fields.files.ImageField')(default='/digidemo/proposal-images/', max_length=100)),
        ))
        db.send_create_signal(u'digidemo', ['Proposal'])

        # Adding M2M table for field sector on 'Proposal'
        m2m_table_name = db.shorten_name(u'digidemo_proposal_sector')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('proposal', models.ForeignKey(orm[u'digidemo.proposal'], null=False)),
            ('sector', models.ForeignKey(orm[u'digidemo.sector'], null=False))
        ))
        db.create_unique(m2m_table_name, ['proposal_id', 'sector_id'])

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

        # Adding model 'ProposalVote'
        db.create_table(u'digidemo_proposalvote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('proposal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Proposal'])),
            ('valence', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'digidemo', ['ProposalVote'])

        # Adding unique constraint on 'ProposalVote', fields ['user', 'proposal']
        db.create_unique(u'digidemo_proposalvote', ['user_id', 'proposal_id'])

        # Adding model 'Capability'
        db.create_table(u'digidemo_capability', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Sector'])),
        ))
        db.send_create_signal(u'digidemo', ['Capability'])

        # Adding model 'Factor'
        db.create_table(u'digidemo_factor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proposal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Proposal'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('capability', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Capability'])),
            ('valence', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'digidemo', ['Factor'])

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

        # Adding model 'Organization'
        db.create_table(u'digidemo_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('legal_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('legal_classification', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('revenue', self.gf('django.db.models.fields.BigIntegerField')()),
            ('operations_summary', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'digidemo', ['Organization'])

        # Adding model 'Position'
        db.create_table(u'digidemo_position', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Person'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Organization'])),
            ('salary', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('mandate_summary', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'digidemo', ['Position'])

        # Adding model 'Letter'
        db.create_table(u'digidemo_letter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_letter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Letter'], null=True, blank=True)),
            ('proposal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Proposal'])),
            ('valence', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('score', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'digidemo', ['Letter'])

        # Adding M2M table for field resenders on 'Letter'
        m2m_table_name = db.shorten_name(u'digidemo_letter_resenders')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('letter', models.ForeignKey(orm[u'digidemo.letter'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['letter_id', 'user_id'])

        # Adding M2M table for field recipients on 'Letter'
        m2m_table_name = db.shorten_name(u'digidemo_letter_recipients')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('letter', models.ForeignKey(orm[u'digidemo.letter'], null=False)),
            ('position', models.ForeignKey(orm[u'digidemo.position'], null=False))
        ))
        db.create_unique(m2m_table_name, ['letter_id', 'position_id'])

        # Adding model 'LetterVote'
        db.create_table(u'digidemo_lettervote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('letter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Letter'])),
            ('valence', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'digidemo', ['LetterVote'])

        # Adding unique constraint on 'LetterVote', fields ['user', 'letter']
        db.create_unique(u'digidemo_lettervote', ['user_id', 'letter_id'])

        # Adding model 'Comment'
        db.create_table(u'digidemo_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('letter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digidemo.Letter'])),
            ('body', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('score', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'digidemo', ['Comment'])


    def backwards(self, orm):
        # Removing unique constraint on 'LetterVote', fields ['user', 'letter']
        db.delete_unique(u'digidemo_lettervote', ['user_id', 'letter_id'])

        # Removing unique constraint on 'ProposalVote', fields ['user', 'proposal']
        db.delete_unique(u'digidemo_proposalvote', ['user_id', 'proposal_id'])

        # Deleting model 'Sector'
        db.delete_table(u'digidemo_sector')

        # Deleting model 'UserProfile'
        db.delete_table(u'digidemo_userprofile')

        # Deleting model 'Proposal'
        db.delete_table(u'digidemo_proposal')

        # Removing M2M table for field sector on 'Proposal'
        db.delete_table(db.shorten_name(u'digidemo_proposal_sector'))

        # Deleting model 'Discussion'
        db.delete_table(u'digidemo_discussion')

        # Deleting model 'Reply'
        db.delete_table(u'digidemo_reply')

        # Deleting model 'ProposalVote'
        db.delete_table(u'digidemo_proposalvote')

        # Deleting model 'Capability'
        db.delete_table(u'digidemo_capability')

        # Deleting model 'Factor'
        db.delete_table(u'digidemo_factor')

        # Deleting model 'Person'
        db.delete_table(u'digidemo_person')

        # Deleting model 'Organization'
        db.delete_table(u'digidemo_organization')

        # Deleting model 'Position'
        db.delete_table(u'digidemo_position')

        # Deleting model 'Letter'
        db.delete_table(u'digidemo_letter')

        # Removing M2M table for field resenders on 'Letter'
        db.delete_table(db.shorten_name(u'digidemo_letter_resenders'))

        # Removing M2M table for field recipients on 'Letter'
        db.delete_table(db.shorten_name(u'digidemo_letter_recipients'))

        # Deleting model 'LetterVote'
        db.delete_table(u'digidemo_lettervote')

        # Deleting model 'Comment'
        db.delete_table(u'digidemo_comment')


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