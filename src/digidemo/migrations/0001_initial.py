# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('score', models.SmallIntegerField(default=0, editable=False)),
                ('text', models.CharField(max_length=8192)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnswerComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('score', models.SmallIntegerField(default=0, editable=False)),
                ('text', models.CharField(max_length=8192)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnswerVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('valence', models.SmallIntegerField(choices=[(-1, b'down vote'), (0, b'non vote'), (1, b'up vote')])),
                ('target', models.ForeignKey(to='digidemo.Answer')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('score', models.SmallIntegerField(default=0, editable=False)),
                ('text', models.CharField(max_length=8192)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('valence', models.SmallIntegerField(choices=[(-1, b'down vote'), (0, b'non vote'), (1, b'up vote')])),
                ('target', models.ForeignKey(to='digidemo.Comment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('score', models.SmallIntegerField(default=0, editable=False)),
                ('text', models.CharField(max_length=8192)),
                ('title', models.CharField(max_length=256)),
                ('is_open', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiscussionComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('score', models.SmallIntegerField(default=0, editable=False)),
                ('text', models.CharField(max_length=8192)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiscussionVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('valence', models.SmallIntegerField(choices=[(-1, b'down vote'), (0, b'non vote'), (1, b'up vote')])),
                ('target', models.ForeignKey(to='digidemo.Discussion')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailRecipient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('email', models.EmailField(max_length=254)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('code', models.CharField(max_length=60)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeedbackNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.CharField(max_length=b'1024')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('valence', models.SmallIntegerField(null=True, choices=[(1, b'support'), (-1, b'oppose'), (0, b'ammend')])),
                ('score', models.SmallIntegerField(default=1)),
                ('title', models.CharField(max_length=256)),
                ('text', models.TextField()),
                ('parent_letter', models.ForeignKey(related_name='resent_letters', blank=True, to='digidemo.Letter', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LetterVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('valence', models.SmallIntegerField(choices=[(-1, b'down vote'), (0, b'non vote'), (1, b'up vote')])),
                ('target', models.ForeignKey(to='digidemo.Letter')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('event_type', models.CharField(max_length=20, choices=[(b'ISSUE', b'issue'), (b'EDIT_ISSUE', b'edit issue'), (b'QUESTION', b'question'), (b'ANSWER', b'answer'), (b'DISCUSSION', b'discussion'), (b'REPLY', b'reply'), (b'COMMENT', b'comment'), (b'LETTER', b'letter'), (b'SIGN_LETTER', b'sign letter'), (b'VOTE', b'vote'), (b'SYSTEM', b'system')])),
                ('reason', models.CharField(max_length=20, choices=[(b'AUTHOR', b'author'), (b'COMMENTER', b'commenter'), (b'SUBSCRIBED', b'actively subscribed'), (b'EDITOR', b'edited related content')])),
                ('event_data', models.CharField(max_length=2048)),
                ('link_back', models.URLField(max_length=512, null=True)),
                ('was_seen', models.BooleanField(default=False)),
                ('was_checked', models.BooleanField(default=False)),
                ('was_mailed', models.BooleanField(default=False)),
                ('source_user', models.ForeignKey(related_name='triggered_notifications', to=settings.AUTH_USER_MODEL, null=True)),
                ('target_user', models.ForeignKey(related_name='received_notifications', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('short_name', models.CharField(max_length=64)),
                ('legal_name', models.CharField(max_length=128)),
                ('legal_classification', models.CharField(max_length=48, choices=[(b'NP', b'non profit'), (b'NFP', b'not for profit'), (b'CH', b'charity'), (b'CPN', b'corporation'), (b'CRN', b'crown corporation'), (b'GVA', b'government agency'), (b'NPT', b'national political party'), (b'PPT', b'provincial political party'), (b'CTY', b'city / municipal administration'), (b'FND', b'foundation'), (b'COL', b'university or college'), (b'PRO', b'professional standards body'), (b'PRG', b'provincial regulatory association'), (b'NRG', b'national regulatory association'), (b'NGO', b'non-governmental organization'), (b'IG', b'industry group'), (b'LBU', b'labour union'), (b'OIG', b'other interest group')])),
                ('revenue', models.BigIntegerField()),
                ('operations_summary', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=8192)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('fname', models.CharField(max_length=48)),
                ('lname', models.CharField(max_length=48)),
                ('portrait_url', models.CharField(max_length=256)),
                ('wikipedia_url', models.CharField(max_length=256)),
                ('bio_summary', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('name', models.CharField(max_length=128)),
                ('salary', models.DecimalField(max_digits=11, decimal_places=2)),
                ('telephone', models.CharField(max_length=14)),
                ('email', models.EmailField(max_length=254)),
                ('mandate_summary', models.TextField()),
                ('organization', models.ForeignKey(to='digidemo.Organization')),
                ('person', models.ForeignKey(to='digidemo.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('is_published', models.BooleanField(default=False)),
                ('score', models.SmallIntegerField(default=0)),
                ('title', models.CharField(max_length=256)),
                ('summary', models.TextField()),
                ('text', models.TextField()),
                ('proposal_image', models.ImageField(default=b'/digidemo/proposal-images/', upload_to=b'proposal_avatars')),
                ('original_user', models.ForeignKey(related_name='initiated_proposals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'creation_date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('title', models.CharField(max_length=256)),
                ('summary', models.TextField()),
                ('text', models.TextField()),
                ('proposal', models.ForeignKey(blank=True, to='digidemo.Proposal', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('valence', models.SmallIntegerField(choices=[(-1, b'down vote'), (0, b'non vote'), (1, b'up vote')])),
                ('target', models.ForeignKey(to='digidemo.Proposal')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('event_type', models.CharField(max_length=20, choices=[(b'ISSUE', b'issue'), (b'EDIT_ISSUE', b'edit issue'), (b'QUESTION', b'question'), (b'ANSWER', b'answer'), (b'DISCUSSION', b'discussion'), (b'REPLY', b'reply'), (b'COMMENT', b'comment'), (b'LETTER', b'letter'), (b'SIGN_LETTER', b'sign letter'), (b'VOTE', b'vote'), (b'SYSTEM', b'system')])),
                ('was_posted', models.BooleanField(default=False)),
                ('event_data', models.CharField(max_length=2048)),
                ('link_back', models.URLField(max_length=512, null=True)),
                ('source_user', models.ForeignKey(related_name='publications', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('score', models.SmallIntegerField(default=0, editable=False)),
                ('text', models.CharField(max_length=8192)),
                ('title', models.CharField(max_length=256, verbose_name=b'question title')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('score', models.SmallIntegerField(default=0, editable=False)),
                ('text', models.CharField(max_length=8192)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('valence', models.SmallIntegerField(choices=[(-1, b'down vote'), (0, b'non vote'), (1, b'up vote')])),
                ('target', models.ForeignKey(to='digidemo.Question')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('score', models.SmallIntegerField(default=0, editable=False)),
                ('text', models.CharField(max_length=8192)),
                ('is_open', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReplyComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('score', models.SmallIntegerField(default=0, editable=False)),
                ('text', models.CharField(max_length=8192)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReplyVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('valence', models.SmallIntegerField(choices=[(-1, b'down vote'), (0, b'non vote'), (1, b'up vote')])),
                ('target', models.ForeignKey(to='digidemo.Reply')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('short_name', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('reason', models.CharField(max_length=20, choices=[(b'AUTHOR', b'author'), (b'COMMENTER', b'commenter'), (b'SUBSCRIBED', b'actively subscribed'), (b'EDITOR', b'edited related content')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubscriptionId',
            fields=[
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('subscription_id', models.AutoField(serialize=False, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('name', models.CharField(max_length=48)),
                ('sector', models.ForeignKey(to='digidemo.Sector', null=True)),
                ('subscription_id', models.ForeignKey(editable=False, to='digidemo.SubscriptionId')),
                ('target', models.ForeignKey(to='digidemo.Tag', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('email_validated', models.BooleanField(default=False)),
                ('avatar_img', models.ImageField(upload_to=b'avatars')),
                ('rep', models.IntegerField(default=0)),
                ('street', models.CharField(max_length=128)),
                ('zip_code', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=64, choices=[(b'ABW', b'Aruba'), (b'AFG', b'Afghanistan'), (b'AGO', b'Angola'), (b'AIA', b'Anguilla'), (b'ALA', b'\xc3\x85land Islands'), (b'ALB', b'Albania'), (b'AND', b'Andorra'), (b'ARE', b'United Arab Emirates'), (b'ARG', b'Argentina'), (b'ARM', b'Armenia'), (b'ASM', b'American Samoa'), (b'ATA', b'Antarctica'), (b'ATF', b'French Southern Territories'), (b'ATG', b'Antigua and Barbuda'), (b'AUS', b'Australia'), (b'AUT', b'Austria'), (b'AZE', b'Azerbaijan'), (b'BDI', b'Burundi'), (b'BEL', b'Belgium'), (b'BEN', b'Benin'), (b'BES', b'Bonaire, Sint Eustatius and Saba'), (b'BFA', b'Burkina Faso'), (b'BGD', b'Bangladesh'), (b'BGR', b'Bulgaria'), (b'BHR', b'Bahrain'), (b'BHS', b'Bahamas'), (b'BIH', b'Bosnia and Herzegovina'), (b'BLM', b'Saint Barth\xc3\xa9lemy'), (b'BLR', b'Belarus'), (b'BLZ', b'Belize'), (b'BMU', b'Bermuda'), (b'BOL', b'Bolivia, Plurinational State of'), (b'BRA', b'Brazil'), (b'BRB', b'Barbados'), (b'BRN', b'Brunei Darussalam'), (b'BTN', b'Bhutan'), (b'BVT', b'Bouvet Island'), (b'BWA', b'Botswana'), (b'CAF', b'Central African Republic'), (b'CAN', b'Canada'), (b'CCK', b'Cocos (Keeling) Islands'), (b'CHE', b'Switzerland'), (b'CHL', b'Chile'), (b'CHN', b'China'), (b'CIV', b"C\xc3\xb4te d'Ivoire"), (b'CMR', b'Cameroon'), (b'COD', b'Congo, the Democratic Republic of the'), (b'COG', b'Congo'), (b'COK', b'Cook Islands'), (b'COL', b'Colombia'), (b'COM', b'Comoros'), (b'CPV', b'Cabo Verde'), (b'CRI', b'Costa Rica'), (b'CUB', b'Cuba'), (b'CUW', b'Cura\xc3\xa7ao'), (b'CXR', b'Christmas Island'), (b'CYM', b'Cayman Islands'), (b'CYP', b'Cyprus'), (b'CZE', b'Czech Republic'), (b'DEU', b'Germany'), (b'DJI', b'Djibouti'), (b'DMA', b'Dominica'), (b'DNK', b'Denmark'), (b'DOM', b'Dominican Republic'), (b'DZA', b'Algeria'), (b'ECU', b'Ecuador'), (b'EGY', b'Egypt'), (b'ERI', b'Eritrea'), (b'ESH', b'Western Sahara'), (b'ESP', b'Spain'), (b'EST', b'Estonia'), (b'ETH', b'Ethiopia'), (b'FIN', b'Finland'), (b'FJI', b'Fiji'), (b'FLK', b'Falkland Islands (Malvinas)'), (b'FRA', b'France'), (b'FRO', b'Faroe Islands'), (b'FSM', b'Micronesia, Federated States of'), (b'GAB', b'Gabon'), (b'GBR', b'United Kingdom'), (b'GEO', b'Georgia'), (b'GGY', b'Guernsey'), (b'GHA', b'Ghana'), (b'GIB', b'Gibraltar'), (b'GIN', b'Guinea'), (b'GLP', b'Guadeloupe'), (b'GMB', b'Gambia'), (b'GNB', b'Guinea-Bissau'), (b'GNQ', b'Equatorial Guinea'), (b'GRC', b'Greece'), (b'GRD', b'Grenada'), (b'GRL', b'Greenland'), (b'GTM', b'Guatemala'), (b'GUF', b'French Guiana'), (b'GUM', b'Guam'), (b'GUY', b'Guyana'), (b'HKG', b'Hong Kong'), (b'HMD', b'Heard Island and McDonald Islands'), (b'HND', b'Honduras'), (b'HRV', b'Croatia'), (b'HTI', b'Haiti'), (b'HUN', b'Hungary'), (b'IDN', b'Indonesia'), (b'IMN', b'Isle of Man'), (b'IND', b'India'), (b'IOT', b'British Indian Ocean Territory'), (b'IRL', b'Ireland'), (b'IRN', b'Iran, Islamic Republic of'), (b'IRQ', b'Iraq'), (b'ISL', b'Iceland'), (b'ISR', b'Israel'), (b'ITA', b'Italy'), (b'JAM', b'Jamaica'), (b'JEY', b'Jersey'), (b'JOR', b'Jordan'), (b'JPN', b'Japan'), (b'KAZ', b'Kazakhstan'), (b'KEN', b'Kenya'), (b'KGZ', b'Kyrgyzstan'), (b'KHM', b'Cambodia'), (b'KIR', b'Kiribati'), (b'KNA', b'Saint Kitts and Nevis'), (b'KOR', b'Korea, Republic of'), (b'KWT', b'Kuwait'), (b'LAO', b"Lao People's Democratic Republic"), (b'LBN', b'Lebanon'), (b'LBR', b'Liberia'), (b'LBY', b'Libya'), (b'LCA', b'Saint Lucia'), (b'LIE', b'Liechtenstein'), (b'LKA', b'Sri Lanka'), (b'LSO', b'Lesotho'), (b'LTU', b'Lithuania'), (b'LUX', b'Luxembourg'), (b'LVA', b'Latvia'), (b'MAC', b'Macao'), (b'MAF', b'Saint Martin (French part)'), (b'MAR', b'Morocco'), (b'MCO', b'Monaco'), (b'MDA', b'Moldova, Republic of'), (b'MDG', b'Madagascar'), (b'MDV', b'Maldives'), (b'MEX', b'Mexico'), (b'MHL', b'Marshall Islands'), (b'MKD', b'Macedonia, the former Yugoslav Republic of'), (b'MLI', b'Mali'), (b'MLT', b'Malta'), (b'MMR', b'Myanmar'), (b'MNE', b'Montenegro'), (b'MNG', b'Mongolia'), (b'MNP', b'Northern Mariana Islands'), (b'MOZ', b'Mozambique'), (b'MRT', b'Mauritania'), (b'MSR', b'Montserrat'), (b'MTQ', b'Martinique'), (b'MUS', b'Mauritius'), (b'MWI', b'Malawi'), (b'MYS', b'Malaysia'), (b'MYT', b'Mayotte'), (b'NAM', b'Namibia'), (b'NCL', b'New Caledonia'), (b'NER', b'Niger'), (b'NFK', b'Norfolk Island'), (b'NGA', b'Nigeria'), (b'NIC', b'Nicaragua'), (b'NIU', b'Niue'), (b'NLD', b'Netherlands'), (b'NOR', b'Norway'), (b'NPL', b'Nepal'), (b'NRU', b'Nauru'), (b'NZL', b'New Zealand'), (b'OMN', b'Oman'), (b'PAK', b'Pakistan'), (b'PAN', b'Panama'), (b'PCN', b'Pitcairn'), (b'PER', b'Peru'), (b'PHL', b'Philippines'), (b'PLW', b'Palau'), (b'PNG', b'Papua New Guinea'), (b'POL', b'Poland'), (b'PRI', b'Puerto Rico'), (b'PRK', b"Korea, Democratic People's Republic of"), (b'PRT', b'Portugal'), (b'PRY', b'Paraguay'), (b'PSE', b'Palestine, State of'), (b'PYF', b'French Polynesia'), (b'QAT', b'Qatar'), (b'REU', b'R\xc3\xa9union'), (b'ROU', b'Romania'), (b'RUS', b'Russian Federation'), (b'RWA', b'Rwanda'), (b'SAU', b'Saudi Arabia'), (b'SDN', b'Sudan'), (b'SEN', b'Senegal'), (b'SGP', b'Singapore'), (b'SGS', b'South Georgia and the South Sandwich Islands'), (b'SHN', b'Saint Helena, Ascension and Tristan da Cunha'), (b'SJM', b'Svalbard and Jan Mayen'), (b'SLB', b'Solomon Islands'), (b'SLE', b'Sierra Leone'), (b'SLV', b'El Salvador'), (b'SMR', b'San Marino'), (b'SOM', b'Somalia'), (b'SPM', b'Saint Pierre and Miquelon'), (b'SRB', b'Serbia'), (b'SSD', b'South Sudan'), (b'STP', b'Sao Tome and Principe'), (b'SUR', b'Suriname'), (b'SVK', b'Slovakia'), (b'SVN', b'Slovenia'), (b'SWE', b'Sweden'), (b'SWZ', b'Swaziland'), (b'SXM', b'Sint Maarten (Dutch part)'), (b'SYC', b'Seychelles'), (b'SYR', b'Syrian Arab Republic'), (b'TCA', b'Turks and Caicos Islands'), (b'TCD', b'Chad'), (b'TGO', b'Togo'), (b'THA', b'Thailand'), (b'TJK', b'Tajikistan'), (b'TKL', b'Tokelau'), (b'TKM', b'Turkmenistan'), (b'TLS', b'Timor-Leste'), (b'TON', b'Tonga'), (b'TTO', b'Trinidad and Tobago'), (b'TUN', b'Tunisia'), (b'TUR', b'Turkey'), (b'TUV', b'Tuvalu'), (b'TWN', b'Taiwan, Province of China'), (b'TZA', b'Tanzania, United Republic of'), (b'UGA', b'Uganda'), (b'UKR', b'Ukraine'), (b'UMI', b'United States Minor Outlying Islands'), (b'URY', b'Uruguay'), (b'USA', b'United States'), (b'UZB', b'Uzbekistan'), (b'VAT', b'Holy See (Vatican City State)'), (b'VCT', b'Saint Vincent and the Grenadines'), (b'VEN', b'Venezuela, Bolivarian Republic of'), (b'VGB', b'Virgin Islands, British'), (b'VIR', b'Virgin Islands, U.S.'), (b'VNM', b'Viet Nam'), (b'VUT', b'Vanuatu'), (b'WLF', b'Wallis and Futuna'), (b'WSM', b'Samoa'), (b'YEM', b'Yemen'), (b'ZAF', b'South Africa'), (b'ZMB', b'Zambia'), (b'ZWE', b'Zimbabwe')])),
                ('province', models.CharField(blank=True, max_length=32, choices=[(b'AB', b'Alberta'), (b'BC', b'British Columbia'), (b'MB', b'Manitoba'), (b'SK', b'Saskatchewan'), (b'PE', b'Prince Edward Island'), (b'QC', b'Quebec'), (b'NL', b'Newfoundland and Labrador'), (b'NU', b'Nunavut'), (b'YT', b'Yukon'), (b'NS', b'Nova Scotia'), (b'NB', b'New Brunswick'), (b'NT', b'Northwest Territories'), (b'ON', b'Ontario')])),
                ('do_email_news', models.BooleanField(default=True)),
                ('do_email_responses', models.BooleanField(default=True)),
                ('do_email_petitions', models.BooleanField(default=True)),
                ('do_email_watched', models.BooleanField(default=True)),
                ('followedProposals', models.ManyToManyField(to='digidemo.Proposal', null=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='subscription',
            name='subscription_id',
            field=models.ForeignKey(related_name='subscriptions', to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(related_name='subscriptions', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sector',
            name='subscription_id',
            field=models.ForeignKey(editable=False, to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='replyvote',
            unique_together=set([('user', 'target')]),
        ),
        migrations.AddField(
            model_name='replycomment',
            name='subscription_id',
            field=models.ForeignKey(editable=False, to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='replycomment',
            name='target',
            field=models.ForeignKey(related_name='comment_set', to='digidemo.Reply'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='replycomment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reply',
            name='subscription_id',
            field=models.ForeignKey(editable=False, to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reply',
            name='target',
            field=models.ForeignKey(related_name='replies', to='digidemo.Discussion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reply',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='questionvote',
            unique_together=set([('user', 'target')]),
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='subscription_id',
            field=models.ForeignKey(editable=False, to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='target',
            field=models.ForeignKey(related_name='comment_set', to='digidemo.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='subscription_id',
            field=models.ForeignKey(editable=False, to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='target',
            field=models.ForeignKey(to='digidemo.Proposal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publication',
            name='subscription_id',
            field=models.ForeignKey(related_name='publications', to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='proposalvote',
            unique_together=set([('user', 'target')]),
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='sectors',
            field=models.ManyToManyField(related_name='proposal_versions', null=True, to='digidemo.Sector', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='tags',
            field=models.ManyToManyField(related_name='proposal_versions', null=True, to='digidemo.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposal',
            name='sectors',
            field=models.ManyToManyField(related_name='proposals', null=True, to='digidemo.Sector', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposal',
            name='subscription_id',
            field=models.ForeignKey(editable=False, to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposal',
            name='tags',
            field=models.ManyToManyField(related_name='proposals', null=True, to='digidemo.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposal',
            name='user',
            field=models.ForeignKey(related_name='proposals_rectently_edited', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='lettervote',
            unique_together=set([('user', 'target')]),
        ),
        migrations.AddField(
            model_name='letter',
            name='recipients',
            field=models.ManyToManyField(related_name='letters', to='digidemo.Position'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='letter',
            name='subscription_id',
            field=models.ForeignKey(editable=False, to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='letter',
            name='target',
            field=models.ForeignKey(to='digidemo.Proposal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='letter',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='discussionvote',
            unique_together=set([('user', 'target')]),
        ),
        migrations.AddField(
            model_name='discussioncomment',
            name='subscription_id',
            field=models.ForeignKey(editable=False, to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='discussioncomment',
            name='target',
            field=models.ForeignKey(related_name='comment_set', to='digidemo.Discussion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='discussioncomment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='discussion',
            name='subscription_id',
            field=models.ForeignKey(editable=False, to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='discussion',
            name='target',
            field=models.ForeignKey(to='digidemo.Proposal', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='discussion',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='commentvote',
            unique_together=set([('user', 'target')]),
        ),
        migrations.AddField(
            model_name='comment',
            name='subscription_id',
            field=models.ForeignKey(editable=False, to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='target',
            field=models.ForeignKey(related_name='comment_set', to='digidemo.Letter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='answervote',
            unique_together=set([('user', 'target')]),
        ),
        migrations.AddField(
            model_name='answercomment',
            name='subscription_id',
            field=models.ForeignKey(editable=False, to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answercomment',
            name='target',
            field=models.ForeignKey(related_name='comment_set', to='digidemo.Answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answercomment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='subscription_id',
            field=models.ForeignKey(editable=False, to='digidemo.SubscriptionId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='target',
            field=models.ForeignKey(related_name='replies', to='digidemo.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
