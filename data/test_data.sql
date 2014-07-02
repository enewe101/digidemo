-- MySQL dump 10.13  Distrib 5.5.25a, for osx10.6 (i386)
--
-- Host: localhost    Database: digidemo
-- ------------------------------------------------------
-- Server version	5.5.25a-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
REPLACE INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add migration history',7,'add_migrationhistory'),(20,'Can change migration history',7,'change_migrationhistory'),(21,'Can delete migration history',7,'delete_migrationhistory'),(22,'Can add user',8,'add_user'),(23,'Can change user',8,'change_user'),(24,'Can delete user',8,'delete_user'),(25,'Can add proposal',9,'add_proposal'),(26,'Can change proposal',9,'change_proposal'),(27,'Can delete proposal',9,'delete_proposal'),(28,'Can add letter',10,'add_letter'),(29,'Can change letter',10,'change_letter'),(30,'Can delete letter',10,'delete_letter'),(31,'Can add comment',11,'add_comment'),(32,'Can change comment',11,'change_comment'),(33,'Can delete comment',11,'delete_comment'),(34,'Can add person',12,'add_person'),(35,'Can change person',12,'change_person'),(36,'Can delete person',12,'delete_person'),(37,'Can add organization',13,'add_organization'),(38,'Can change organization',13,'change_organization'),(39,'Can delete organization',13,'delete_organization'),(40,'Can add position',14,'add_position'),(41,'Can change position',14,'change_position'),(42,'Can delete position',14,'delete_position'),(43,'Can add capability',15,'add_capability'),(44,'Can change capability',15,'change_capability'),(45,'Can delete capability',15,'delete_capability'),(46,'Can add factor',16,'add_factor'),(47,'Can change factor',16,'change_factor'),(48,'Can delete factor',16,'delete_factor'),(49,'Can add sector',17,'add_sector'),(50,'Can change sector',17,'change_sector'),(51,'Can delete sector',17,'delete_sector'),(52,'Can add proposal vote',18,'add_proposalvote'),(53,'Can change proposal vote',18,'change_proposalvote'),(54,'Can delete proposal vote',18,'delete_proposalvote'),(55,'Can add letter vote',19,'add_lettervote'),(56,'Can change letter vote',19,'change_lettervote'),(57,'Can delete letter vote',19,'delete_lettervote'),(58,'Can add user profile',20,'add_userprofile'),(59,'Can change user profile',20,'change_userprofile'),(60,'Can delete user profile',20,'delete_userprofile');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
REPLACE INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES (1,'pbkdf2_sha256$12000$vdIKgzqx54r5$J3tT4LmxhxzRu/4YX8kPVNcf7GdGYbCDfBrkbUQ6NaI=','2014-06-15 03:38:24',1,'superuser','super','user','super.user@email.com',1,1,'2014-06-15 03:38:24'),(2,'pbkdf2_sha256$12000$LvEWg7RRIxvY$nK9r1ddB9vUhVIc5ORAzES/+rKZHxMFXJQnwkdyIAt8=','2014-07-01 05:20:13',0,'regularuser','regular','user','regular.user@email.com',0,1,'2014-07-01 05:22:06');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_capability`
--

LOCK TABLES `digidemo_capability` WRITE;
/*!40000 ALTER TABLE `digidemo_capability` DISABLE KEYS */;
REPLACE INTO `digidemo_capability` (`id`, `name`, `description`, `sector_id`) VALUES (3,'~ obtain quality education','Universal access to quality education, including: literacy, numeracy, computer skills; history, human rights, political rights and process; self esteem, morality, automomy; natural sciences, cosmological and ecological origins; life skills, practical arts, expressive arts.',4),(4,'~ live in harmony with the natural world','A lifestyle that, without unusual inconvenience, does not pollute the environment in a way that renders it unfit or unpleasant, nor brings hopeless struggle or devastation to other life, and which provides access to nature and tranquility, and extracts resources from nature only at a rate that is either replenished, or exausted in a timeframe that allows our adaptation to alternatives',2),(5,'~ be represented politically','The capability to have one\'s interests and stakes in society considered, guarded, and improved by a political process that reconciles these stakes with those of others in a way that is fair, proportionate, efficient, and transparent',8),(6,'~ have meaningful political participation','The ability to participate in collective decisionmaking regarding matters with one holds stake, and for that participation to have substancial effect, in proportion to one\'s stake and that of others, and to be safe from harm, discrimination, or retribution for one\'s participation.',8),(8,'safeguarding capabilities with good international relations','Diplomatic cooperation and coordination which fosters amicable relations, through demands on and compromises with other nations, which are compatible with the longterm flourishing of human capabilities.',5),(9,'~ live a healthy life to its natural end','The ability to live a healthy life, to have full use of one\'s body, to be free of suffering and disease, and to live a long life to its natural end.',3),(10,'~ be free from undue descrimination','The ability to embrace one\'s nature, including for example body form and appearance, language, sexality, and so on, insofar as it does no harm to others, without being arbitrarily descriminated against.',6),(11,'safeguarding capabilities with security and readiness','Collective readiness to make use of natural resources, in a way that is sustainable, or consistent with reasonable expectations for adaptive exit, and exact gains in the national wealth by such usage',7),(12,'safeguarding capabilities with security','Collective readiness to defend the security of the nation, for example, defending sovereign territory from invasion and exploit, to protect against excessive foreign economic claim, to protect the integrity of computer systems and networks, and exert reasonable and proportionate pressure in the maintenance of treaty agreements.',7),(13,'~ to live free from harm and hazards','The ability to live without the fear or risk of hazards from reasonably forseable sources, including protection against natural disaster, economic disaster, and negligence in business and professional practice.',7),(14,'~ obtain the material necessities of life','The ability to obtain the basics of food, shelter, clothing, transportation, access to hygiene facilities, transportation, and communication which are necessary to live most lifestyles.',1),(15,'~ do meaningful work','The ability to earn the basic necessities of life through meaninful activities that contribute to society and make effecient use of ones talents, without putting oneself or others at risk.',1),(16,'~ enjoy freedom of choice in lifestyle','The capability to gain a sufficiency of income such that, after securing ones basic necessities, one still has some time and income to dispose of, in the ways of ones choosing, such as for entertainment, relaxation, intellectual or cultural enrichment, artistic expression, political engagement, human relationships, and so on.',1);
/*!40000 ALTER TABLE `digidemo_capability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_comment`
--

LOCK TABLES `digidemo_comment` WRITE;
/*!40000 ALTER TABLE `digidemo_comment` DISABLE KEYS */;
REPLACE INTO `digidemo_comment` (`id`, `author_id`, `letter_id`, `body`, `score`) VALUES (1,1,1,'@normaluser I agree with you but I think that you should consider offering some concrete evidence for what you are saying -- back up how the environmental losses will arise and why they are certain.  There\'s plenty of facts in the issue \nwiki to choose from.',1),(2,1,1,'ll',0),(3,1,1,'lll\r\n',0);
/*!40000 ALTER TABLE `digidemo_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_factor`
--

LOCK TABLES `digidemo_factor` WRITE;
/*!40000 ALTER TABLE `digidemo_factor` DISABLE KEYS */;
REPLACE INTO `digidemo_factor` (`id`, `proposal_id`, `description`, `capability_id`, `valence`) VALUES (1,1,'Transport of crude oil by pipeline is safer than by truck and train, which are the current alternatives',13,1),(2,1,'The operation of pipelines for the transport of crude oil poses environmental risks due to the eventuality of leaks',4,-1),(3,1,'Canada\'s readiness to make use of its natural resources will be increased',11,1),(4,1,'Facilitating the development of the tarsands will create additional wealth and income in Canada.',15,1);
/*!40000 ALTER TABLE `digidemo_factor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_letter`
--

LOCK TABLES `digidemo_letter` WRITE;
/*!40000 ALTER TABLE `digidemo_letter` DISABLE KEYS */;
REPLACE INTO `digidemo_letter` (`id`, `parent_letter_id`, `proposal_id`, `valence`, `sender_id`, `body`, `score`) VALUES (1,NULL,1,-1,2,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',2);
/*!40000 ALTER TABLE `digidemo_letter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_letter_recipients`
--

LOCK TABLES `digidemo_letter_recipients` WRITE;
/*!40000 ALTER TABLE `digidemo_letter_recipients` DISABLE KEYS */;
REPLACE INTO `digidemo_letter_recipients` (`id`, `letter_id`, `position_id`) VALUES (1,1,1);
/*!40000 ALTER TABLE `digidemo_letter_recipients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_letter_resenders`
--

LOCK TABLES `digidemo_letter_resenders` WRITE;
/*!40000 ALTER TABLE `digidemo_letter_resenders` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_letter_resenders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_lettervote`
--

LOCK TABLES `digidemo_lettervote` WRITE;
/*!40000 ALTER TABLE `digidemo_lettervote` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_lettervote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_organization`
--

LOCK TABLES `digidemo_organization` WRITE;
/*!40000 ALTER TABLE `digidemo_organization` DISABLE KEYS */;
REPLACE INTO `digidemo_organization` (`id`, `short_name`, `legal_name`, `legal_classification`, `revenue`, `operations_summary`) VALUES (1,'The Conservative Party of Canada','The Conservative Party of Canada','NPT',-1,'Stephen Harper’s Conservative Government is focused on the priorities of Canadians – job creation and economic growth.\nWith the support of our Economic Action Plan, the Canadian economy has created approximately one million net new jobs since the depths of the global economic recession.  While the job isn’t done yet, this job creation record is the best in the G7 and shows that Canada is on the right track.');
/*!40000 ALTER TABLE `digidemo_organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_person`
--

LOCK TABLES `digidemo_person` WRITE;
/*!40000 ALTER TABLE `digidemo_person` DISABLE KEYS */;
REPLACE INTO `digidemo_person` (`id`, `fname`, `lname`, `portrait_url`, `wikipedia_url`, `bio_summary`) VALUES (1,'stephen','harper','http://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Stephen_Harper_by_Remy_Steinegger.jpg/800px-Stephen_Harper_by_Remy_Steinegger.jpg','http://en.wikipedia.org/wiki/Stephen_Harper','Stephen Joseph Harper (born April 30, 1959) is a Canadian politician who is the 22nd and current Prime Minister of Canada and the Leader of the Conservative Party. Harper became prime minister in 2006, forming a minority government after the 2006 election. He is the first prime minister to come from the newly reconstituted Conservative Party, which formed after a merger of the Progressive Conservative Party and the Canadian Alliance.');
/*!40000 ALTER TABLE `digidemo_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_position`
--

LOCK TABLES `digidemo_position` WRITE;
/*!40000 ALTER TABLE `digidemo_position` DISABLE KEYS */;
REPLACE INTO `digidemo_position` (`id`, `name`, `person_id`, `organization_id`, `salary`, `telephone`, `email`, `mandate_summary`) VALUES (1,'Prime minister of Canada',1,1,317574.00,'613-992-4211','stephen.harper@parl.gc.ca','');
/*!40000 ALTER TABLE `digidemo_position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_proposal`
--

LOCK TABLES `digidemo_proposal` WRITE;
/*!40000 ALTER TABLE `digidemo_proposal` DISABLE KEYS */;
REPLACE INTO `digidemo_proposal` (`id`, `name`, `title`, `text`, `is_published`, `last_modified`, `creation_date`, `author_id`, `score`, `proposal_image`) VALUES (1,'keystone_xl','Keystone XL Pipeline Extension','<p>The Keystone XL Pipeline is a proposed extension to the existing Keystone Pipeline System, put forward by TransCanada, the corporation that owns the Keystone System. The pipeline would cross the Canada/US border, importing crude oil sourced from the Albertan oil sands, into the United States. The proposal is currently awaiting government approval. The pipeline would be newly constructed, and is similar to existing pipelines in North America.</p><p>The Keystone XL pipeline project is a contentious political issue, owing to probable environmental, economic, and social impacts. Environmentally, the pipeline might present a risk of contaminating groundwater and disturbing sensitive ecosystems, but it might also be a better alternative than ground transport by train or truck. Economically, the pipeline might produce jobs temporarily during its construction, and permanently in additional refinement activities in the US. It would also lead to a redistribution of crude supply, emphasizing export and raising the price of oil in the Midwestern US. Socially, the construction of the pipeline would disturb landowners currently in its path, and would disturb heritage sites of cultural significance.</p>',1,'2014-06-27','2014-06-15',1,0,'/digidemo/proposal-images/'),(2,'test1','no factors','this proposal has no factors',1,'2014-06-20','2014-06-20',1,33,'/digidemo/proposal-images/'),(3,'Quebec','Quebec','a',1,'2014-03-10','2014-02-10',1,-7,'');
/*!40000 ALTER TABLE `digidemo_proposal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_proposal_sector`
--

LOCK TABLES `digidemo_proposal_sector` WRITE;
/*!40000 ALTER TABLE `digidemo_proposal_sector` DISABLE KEYS */;
REPLACE INTO `digidemo_proposal_sector` (`id`, `proposal_id`, `sector_id`) VALUES (1,1,1),(2,1,2);
/*!40000 ALTER TABLE `digidemo_proposal_sector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_proposalvote`
--

LOCK TABLES `digidemo_proposalvote` WRITE;
/*!40000 ALTER TABLE `digidemo_proposalvote` DISABLE KEYS */;
REPLACE INTO `digidemo_proposalvote` (`id`, `user_id`, `proposal_id`, `valence`) VALUES (1,1,1,0);
/*!40000 ALTER TABLE `digidemo_proposalvote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_sector`
--

LOCK TABLES `digidemo_sector` WRITE;
/*!40000 ALTER TABLE `digidemo_sector` DISABLE KEYS */;
REPLACE INTO `digidemo_sector` (`id`, `short_name`, `name`) VALUES (1,'ECO','economy'),(2,'ENV','environment'),(3,'HEA','health'),(4,'EDU','education'),(5,'IR','international relations'),(6,'SOC','society and culture'),(7,'SEC','security and readiness'),(8,'DEM','democratic mechanisms');
/*!40000 ALTER TABLE `digidemo_sector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_userprofile`
--

LOCK TABLES `digidemo_userprofile` WRITE;
/*!40000 ALTER TABLE `digidemo_userprofile` DISABLE KEYS */;
REPLACE INTO `digidemo_userprofile` (`id`, `user_id`, `email_validated`, `avatar_img`, `avatar_name`, `rep`, `street`, `zip_code`, `country`, `province`) VALUES (1,1,1,'avatars/superuser.jpg','superuser',4,'Somewhere','560072','India','Karnatka'),(2,2,1,'avatars/regularuser.jpg','normaluser',12,'56 Long Ave.','51515','CAN','QC');
/*!40000 ALTER TABLE `digidemo_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
REPLACE INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'migration history','south','migrationhistory'),(8,'user','digidemo','user'),(9,'proposal','digidemo','proposal'),(10,'letter','digidemo','letter'),(11,'comment','digidemo','comment'),(12,'person','digidemo','person'),(13,'organization','digidemo','organization'),(14,'position','digidemo','position'),(15,'capability','digidemo','capability'),(16,'factor','digidemo','factor'),(17,'sector','digidemo','sector'),(18,'proposal vote','digidemo','proposalvote'),(19,'letter vote','digidemo','lettervote'),(20,'user profile','digidemo','userprofile');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `south_migrationhistory`
--

LOCK TABLES `south_migrationhistory` WRITE;
/*!40000 ALTER TABLE `south_migrationhistory` DISABLE KEYS */;
REPLACE INTO `south_migrationhistory` (`id`, `app_name`, `migration`, `applied`) VALUES (1,'digidemo','0001_initial','2014-06-15 03:48:03'),(2,'digidemo','0002_auto__add_field_proposal_score__chg_field_comment_score__add_field_let','2014-06-15 04:07:01'),(3,'digidemo','0003_auto__add_field_letter_valence','2014-06-15 04:15:41'),(4,'digidemo','0004_auto__add_organization__add_person__add_position','2014-06-19 01:21:30'),(5,'digidemo','0005_auto__add_field_organization_short_name__add_field_organization_legal_','2014-06-19 05:00:41'),(6,'digidemo','0006_auto__add_field_position_name','2014-06-19 05:22:36'),(7,'digidemo','0007_auto__add_factor__add_capability','2014-06-19 11:14:48'),(8,'digidemo','0008_auto__chg_field_capability_description','2014-06-19 11:31:44'),(9,'digidemo','0009_auto__add_sector__add_field_user_rep','2014-06-20 05:19:07'),(10,'digidemo','0010_auto__del_field_capability_sector','2014-06-20 05:26:02'),(11,'digidemo','0011_auto__add_field_capability_sector','2014-06-20 05:27:26'),(12,'digidemo','0012_auto','2014-06-20 05:39:16'),(13,'digidemo','0013_auto__add_lettervote__add_unique_lettervote_user_letter__add_proposalv','2014-06-27 21:26:09'),(14,'digidemo','0014_auto__add_field_lettervote_valence__add_field_proposalvote_valence','2014-06-27 21:26:11'),(15,'digidemo','0015_auto__add_field_letter_parent','2014-06-27 21:26:12'),(16,'digidemo','0016_auto__chg_field_letter_parent','2014-06-27 21:26:12'),(17,'digidemo','0017_auto__del_field_letter_parent__add_field_letter_parent_id','2014-06-27 21:26:14'),(18,'digidemo','0018_auto__del_field_letter_parent_id__add_field_letter_parent_letter','2014-06-27 21:26:16'),(19,'digidemo','0019_auto__add_field_user_password','2014-06-27 21:26:16'),(20,'digidemo','0020_auto__add_field_proposal_proposal_image__add_field_user_username__chg_','2014-06-27 21:26:18'),(21,'digidemo','0021_auto__del_field_user_username__del_field_user_password__del_field_user','2014-06-27 22:57:45'),(22,'digidemo','0022_auto__del_user__add_userprofile__chg_field_lettervote_user__chg_field_','2014-06-27 22:58:50');
/*!40000 ALTER TABLE `south_migrationhistory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-07-02 19:02:03
