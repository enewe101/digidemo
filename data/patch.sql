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
REPLACE INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add migration history',7,'add_migrationhistory'),(20,'Can change migration history',7,'change_migrationhistory'),(21,'Can delete migration history',7,'delete_migrationhistory'),(22,'Can add sector',8,'add_sector'),(23,'Can change sector',8,'change_sector'),(24,'Can delete sector',8,'delete_sector'),(25,'Can add proposal',9,'add_proposal'),(26,'Can change proposal',9,'change_proposal'),(27,'Can delete proposal',9,'delete_proposal'),(28,'Can add letter',10,'add_letter'),(29,'Can change letter',10,'change_letter'),(30,'Can delete letter',10,'delete_letter'),(31,'Can add comment',11,'add_comment'),(32,'Can change comment',11,'change_comment'),(33,'Can delete comment',11,'delete_comment'),(34,'Can add person',12,'add_person'),(35,'Can change person',12,'change_person'),(36,'Can delete person',12,'delete_person'),(37,'Can add organization',13,'add_organization'),(38,'Can change organization',13,'change_organization'),(39,'Can delete organization',13,'delete_organization'),(40,'Can add position',14,'add_position'),(41,'Can change position',14,'change_position'),(42,'Can delete position',14,'delete_position'),(46,'Can add factor',16,'add_factor'),(47,'Can change factor',16,'change_factor'),(48,'Can delete factor',16,'delete_factor'),(49,'Can add sector',17,'add_sector'),(50,'Can change sector',17,'change_sector'),(51,'Can delete sector',17,'delete_sector'),(52,'Can add proposal vote',18,'add_proposalvote'),(53,'Can change proposal vote',18,'change_proposalvote'),(54,'Can delete proposal vote',18,'delete_proposalvote'),(55,'Can add letter vote',19,'add_lettervote'),(56,'Can change letter vote',19,'change_lettervote'),(57,'Can delete letter vote',19,'delete_lettervote'),(58,'Can add user profile',20,'add_userprofile'),(59,'Can change user profile',20,'change_userprofile'),(60,'Can delete user profile',20,'delete_userprofile'),(61,'Can add comment',21,'add_comment'),(62,'Can change comment',21,'change_comment'),(63,'Can delete comment',21,'delete_comment'),(64,'Can add discussion',22,'add_discussion'),(65,'Can change discussion',22,'change_discussion'),(66,'Can delete discussion',22,'delete_discussion'),(67,'Can add discussion vote',23,'add_discussionvote'),(68,'Can change discussion vote',23,'change_discussionvote'),(69,'Can delete discussion vote',23,'delete_discussionvote'),(70,'Can add reply',24,'add_reply'),(71,'Can change reply',24,'change_reply'),(72,'Can delete reply',24,'delete_reply'),(73,'Can add reply vote',25,'add_replyvote'),(74,'Can change reply vote',25,'change_replyvote'),(75,'Can delete reply vote',25,'delete_replyvote'),(76,'Can add comment vote',26,'add_commentvote'),(77,'Can change comment vote',26,'change_commentvote'),(78,'Can delete comment vote',26,'delete_commentvote');
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
-- Dumping data for table `digidemo_comment`
--

LOCK TABLES `digidemo_comment` WRITE;
/*!40000 ALTER TABLE `digidemo_comment` DISABLE KEYS */;
REPLACE INTO `digidemo_comment` (`id`, `user_id`, `letter_id`, `body`, `score`, `creation_date`, `last_modified`) VALUES (1,1,1,'@normaluser I agree with you but I think that you should consider offering some concrete evidence for what you are saying -- back up how the environmental losses will arise and why they are certain.  There\'s plenty of facts in the issue \nwiki to choose from.',1,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(2,1,1,'ll',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(3,1,1,'lll\r\n',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(4,1,1,'bic!',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(5,1,1,'super',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(6,1,14,'lame!',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(7,1,1,'kilp',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(8,1,1,'froze',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(9,1,1,'Blip',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(10,1,40,'Jimmi',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(11,1,1,'james',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(12,1,14,'blatant comment.',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(13,1,1,'pequifi',0,'0000-00-00 00:00:00','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `digidemo_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_commentvote`
--

LOCK TABLES `digidemo_commentvote` WRITE;
/*!40000 ALTER TABLE `digidemo_commentvote` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_commentvote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_discussion`
--

LOCK TABLES `digidemo_discussion` WRITE;
/*!40000 ALTER TABLE `digidemo_discussion` DISABLE KEYS */;
REPLACE INTO `digidemo_discussion` (`id`, `proposal_id`, `title`, `body`, `user_id`, `score`, `is_open`, `creation_date`, `last_activity_date`) VALUES (1,1,'Social Factors','I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w',1,2,1,'2014-06-30 00:00:00','2014-07-08 00:00:00'),(2,1,'Social Factors','I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w',1,1,1,'2014-07-04 00:00:00','2014-07-04 00:00:00');
/*!40000 ALTER TABLE `digidemo_discussion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_discussionvote`
--

LOCK TABLES `digidemo_discussionvote` WRITE;
/*!40000 ALTER TABLE `digidemo_discussionvote` DISABLE KEYS */;
REPLACE INTO `digidemo_discussionvote` (`id`, `user_id`, `valence`, `creation_date`, `last_modified`, `target_id`) VALUES (1,1,1,'0000-00-00 00:00:00','0000-00-00 00:00:00',1),(2,1,-1,'0000-00-00 00:00:00','0000-00-00 00:00:00',2);
/*!40000 ALTER TABLE `digidemo_discussionvote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_factor`
--

LOCK TABLES `digidemo_factor` WRITE;
/*!40000 ALTER TABLE `digidemo_factor` DISABLE KEYS */;
REPLACE INTO `digidemo_factor` (`id`, `proposal_id`, `description`, `valence`, `creation_date`, `last_modified`, `sector_id`) VALUES (1,1,'Transport of crude oil by pipeline is safer than by truck and train, which are the current alternatives',1,'2014-07-09 05:57:04','2014-07-09 05:57:04',7),(2,1,'The operation of pipelines for the transport of crude oil poses environmental risks due to the eventuality of leaks',-1,'2014-07-09 05:57:04','2014-07-09 05:57:04',2),(3,1,'Canada\'s readiness to make use of its natural resources will be increased',1,'2014-07-09 05:57:04','2014-07-09 05:57:04',7),(4,1,'Facilitating the development of the tarsands will create additional wealth and income in Canada.',1,'2014-07-09 05:57:04','2014-07-09 05:57:04',1);
/*!40000 ALTER TABLE `digidemo_factor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_letter`
--

LOCK TABLES `digidemo_letter` WRITE;
/*!40000 ALTER TABLE `digidemo_letter` DISABLE KEYS */;
REPLACE INTO `digidemo_letter` (`id`, `parent_letter_id`, `proposal_id`, `valence`, `user_id`, `body`, `score`, `creation_date`, `last_modified`) VALUES (1,NULL,1,-1,2,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',1,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(14,NULL,1,0,2,'A new letter!',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(16,NULL,1,1,2,'aoeu',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(38,14,1,0,1,'A new letter!',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(39,1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(40,NULL,1,1,1,'Wadatay',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(41,1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(42,1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(43,1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(44,16,1,1,1,'aoeu',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(45,1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0,'0000-00-00 00:00:00','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `digidemo_letter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_letter_recipients`
--

LOCK TABLES `digidemo_letter_recipients` WRITE;
/*!40000 ALTER TABLE `digidemo_letter_recipients` DISABLE KEYS */;
REPLACE INTO `digidemo_letter_recipients` (`id`, `letter_id`, `position_id`) VALUES (1,1,1),(14,14,1),(16,16,1),(38,38,1),(39,39,1),(40,40,1),(41,41,1),(42,42,1),(43,43,1),(44,44,1),(45,45,1);
/*!40000 ALTER TABLE `digidemo_letter_recipients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_lettervote`
--

LOCK TABLES `digidemo_lettervote` WRITE;
/*!40000 ALTER TABLE `digidemo_lettervote` DISABLE KEYS */;
REPLACE INTO `digidemo_lettervote` (`id`, `user_id`, `valence`, `creation_date`, `last_modified`, `target_id`) VALUES (1,1,-1,'0000-00-00 00:00:00','0000-00-00 00:00:00',1),(2,1,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',16);
/*!40000 ALTER TABLE `digidemo_lettervote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_organization`
--

LOCK TABLES `digidemo_organization` WRITE;
/*!40000 ALTER TABLE `digidemo_organization` DISABLE KEYS */;
REPLACE INTO `digidemo_organization` (`id`, `short_name`, `legal_name`, `legal_classification`, `revenue`, `operations_summary`, `creation_date`, `last_modified`) VALUES (1,'The Conservative Party of Canada','The Conservative Party of Canada','NPT',-1,'Stephen Harper’s Conservative Government is focused on the priorities of Canadians – job creation and economic growth.\nWith the support of our Economic Action Plan, the Canadian economy has created approximately one million net new jobs since the depths of the global economic recession.  While the job isn’t done yet, this job creation record is the best in the G7 and shows that Canada is on the right track.','0000-00-00 00:00:00','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `digidemo_organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_person`
--

LOCK TABLES `digidemo_person` WRITE;
/*!40000 ALTER TABLE `digidemo_person` DISABLE KEYS */;
REPLACE INTO `digidemo_person` (`id`, `fname`, `lname`, `portrait_url`, `wikipedia_url`, `bio_summary`, `creation_date`, `last_modified`) VALUES (1,'stephen','harper','http://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Stephen_Harper_by_Remy_Steinegger.jpg/800px-Stephen_Harper_by_Remy_Steinegger.jpg','http://en.wikipedia.org/wiki/Stephen_Harper','Stephen Joseph Harper (born April 30, 1959) is a Canadian politician who is the 22nd and current Prime Minister of Canada and the Leader of the Conservative Party. Harper became prime minister in 2006, forming a minority government after the 2006 election. He is the first prime minister to come from the newly reconstituted Conservative Party, which formed after a merger of the Progressive Conservative Party and the Canadian Alliance.','0000-00-00 00:00:00','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `digidemo_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_position`
--

LOCK TABLES `digidemo_position` WRITE;
/*!40000 ALTER TABLE `digidemo_position` DISABLE KEYS */;
REPLACE INTO `digidemo_position` (`id`, `name`, `person_id`, `organization_id`, `salary`, `telephone`, `email`, `mandate_summary`, `creation_date`, `last_modified`) VALUES (1,'Prime minister of Canada',1,1,317574.00,'613-992-4211','stephen.harper@parl.gc.ca','','0000-00-00 00:00:00','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `digidemo_position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_proposal`
--

LOCK TABLES `digidemo_proposal` WRITE;
/*!40000 ALTER TABLE `digidemo_proposal` DISABLE KEYS */;
REPLACE INTO `digidemo_proposal` (`id`, `name`, `title`, `text`, `is_published`, `last_modified`, `creation_date`, `user_id`, `score`, `proposal_image`) VALUES (1,'keystone_xl','Keystone XL Pipeline Extension','The Keystone XL Pipeline is a proposed extension to the existing Keystone Pipeline System, put forward by TransCanada, the corporation that owns the Keystone System. The pipeline would cross the Canada/US border, importing crude oil sourced from the Albertan oil sands, into the United States. The proposal is currently awaiting government approval. The pipeline would be newly constructed, and is similar to existing pipelines in North America.\n\nThe Keystone XL pipeline project is a contentious political issue, owing to probable environmental, economic, and social impacts. Environmentally, the pipeline might present a risk of contaminating groundwater and disturbing sensitive ecosystems, but it might also be a better alternative than ground transport by train or truck. Economically, the pipeline might produce jobs temporarily during its construction, and permanently in additional refinement activities in the US. It would also lead to a redistribution of crude supply, emphasizing export and raising the price of oil in the Midwestern US. Socially, the construction of the pipeline would disturb landowners currently in its path, and would disturb heritage sites of cultural significance.',1,'2014-07-08 00:00:00','2014-06-15 00:00:00',1,2,'/digidemo/proposal-images/'),(2,'test1','no factors','this proposal has no factors',1,'2014-07-08 00:00:00','2014-06-20 00:00:00',1,33,'/digidemo/proposal-images/'),(3,'Quebec','Quebec','a',1,'2014-07-08 00:00:00','2014-02-10 00:00:00',1,-7,'');
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
REPLACE INTO `digidemo_proposalvote` (`id`, `user_id`, `valence`, `creation_date`, `last_modified`, `target_id`) VALUES (1,1,1,'0000-00-00 00:00:00','0000-00-00 00:00:00',1);
/*!40000 ALTER TABLE `digidemo_proposalvote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_reply`
--

LOCK TABLES `digidemo_reply` WRITE;
/*!40000 ALTER TABLE `digidemo_reply` DISABLE KEYS */;
REPLACE INTO `digidemo_reply` (`id`, `discussion_id`, `body`, `user_id`, `score`, `is_open`, `creation_date`, `last_modified`) VALUES (24,2,'A comment.',1,0,0,'2014-07-04 00:00:00','0000-00-00 00:00:00'),(25,2,'Another comment.',1,0,0,'2014-07-04 00:00:00','0000-00-00 00:00:00'),(26,1,'Comment on the first discussion.',1,0,0,'2014-07-04 00:00:00','0000-00-00 00:00:00'),(27,1,'AONETHTNH',1,0,0,'2014-07-05 00:00:00','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `digidemo_reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_replyvote`
--

LOCK TABLES `digidemo_replyvote` WRITE;
/*!40000 ALTER TABLE `digidemo_replyvote` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_replyvote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_sector`
--

LOCK TABLES `digidemo_sector` WRITE;
/*!40000 ALTER TABLE `digidemo_sector` DISABLE KEYS */;
REPLACE INTO `digidemo_sector` (`id`, `short_name`, `name`, `creation_date`, `last_modified`) VALUES (1,'ECO','economy','0000-00-00 00:00:00','0000-00-00 00:00:00'),(2,'ENV','environment','0000-00-00 00:00:00','0000-00-00 00:00:00'),(3,'HEA','health','0000-00-00 00:00:00','0000-00-00 00:00:00'),(4,'EDU','education','0000-00-00 00:00:00','0000-00-00 00:00:00'),(5,'IR','international relations','0000-00-00 00:00:00','0000-00-00 00:00:00'),(6,'SOC','society and culture','0000-00-00 00:00:00','0000-00-00 00:00:00'),(7,'SEC','security and readiness','0000-00-00 00:00:00','0000-00-00 00:00:00'),(8,'DEM','democratic mechanisms','0000-00-00 00:00:00','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `digidemo_sector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_userprofile`
--

LOCK TABLES `digidemo_userprofile` WRITE;
/*!40000 ALTER TABLE `digidemo_userprofile` DISABLE KEYS */;
REPLACE INTO `digidemo_userprofile` (`id`, `user_id`, `email_validated`, `avatar_img`, `rep`, `street`, `zip_code`, `country`, `province`) VALUES (1,1,1,'avatars/superuser.jpg',44,'Somewhere','560072','India','Karnatka'),(2,2,1,'avatars/regularuser.jpg',12,'56 Long Ave.','51515','CAN','QC');
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
REPLACE INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'migration history','south','migrationhistory'),(9,'proposal','digidemo','proposal'),(10,'letter','digidemo','letter'),(11,'comment','digidemo','comment'),(12,'person','digidemo','person'),(13,'organization','digidemo','organization'),(14,'position','digidemo','position'),(15,'capability','digidemo','capability'),(16,'factor','digidemo','factor'),(17,'sector','digidemo','sector'),(18,'proposal vote','digidemo','proposalvote'),(19,'letter vote','digidemo','lettervote'),(20,'user profile','digidemo','userprofile'),(22,'discussion','digidemo','discussion'),(23,'discussion vote','digidemo','discussionvote'),(24,'reply','digidemo','reply'),(25,'reply vote','digidemo','replyvote'),(26,'comment vote','digidemo','commentvote');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-07-09  2:01:15
