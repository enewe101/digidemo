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
REPLACE INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add sector',7,'add_sector'),(20,'Can change sector',7,'change_sector'),(21,'Can delete sector',7,'delete_sector'),(22,'Can add user profile',8,'add_userprofile'),(23,'Can change user profile',8,'change_userprofile'),(24,'Can delete user profile',8,'delete_userprofile'),(25,'Can add tag',9,'add_tag'),(26,'Can change tag',9,'change_tag'),(27,'Can delete tag',9,'delete_tag'),(28,'Can add proposal',10,'add_proposal'),(29,'Can change proposal',10,'change_proposal'),(30,'Can delete proposal',10,'delete_proposal'),(31,'Can add proposal version',11,'add_proposalversion'),(32,'Can change proposal version',11,'change_proposalversion'),(33,'Can delete proposal version',11,'delete_proposalversion'),(34,'Can add discussion',12,'add_discussion'),(35,'Can change discussion',12,'change_discussion'),(36,'Can delete discussion',12,'delete_discussion'),(37,'Can add reply',13,'add_reply'),(38,'Can change reply',13,'change_reply'),(39,'Can delete reply',13,'delete_reply'),(40,'Can add question',14,'add_question'),(41,'Can change question',14,'change_question'),(42,'Can delete question',14,'delete_question'),(43,'Can add question comment',15,'add_questioncomment'),(44,'Can change question comment',15,'change_questioncomment'),(45,'Can delete question comment',15,'delete_questioncomment'),(46,'Can add answer',16,'add_answer'),(47,'Can change answer',16,'change_answer'),(48,'Can delete answer',16,'delete_answer'),(49,'Can add answer comment',17,'add_answercomment'),(50,'Can change answer comment',17,'change_answercomment'),(51,'Can delete answer comment',17,'delete_answercomment'),(52,'Can add factor',18,'add_factor'),(53,'Can change factor',18,'change_factor'),(54,'Can delete factor',18,'delete_factor'),(55,'Can add factor version',19,'add_factorversion'),(56,'Can change factor version',19,'change_factorversion'),(57,'Can delete factor version',19,'delete_factorversion'),(58,'Can add person',20,'add_person'),(59,'Can change person',20,'change_person'),(60,'Can delete person',20,'delete_person'),(61,'Can add organization',21,'add_organization'),(62,'Can change organization',21,'change_organization'),(63,'Can delete organization',21,'delete_organization'),(64,'Can add position',22,'add_position'),(65,'Can change position',22,'change_position'),(66,'Can delete position',22,'delete_position'),(67,'Can add letter',23,'add_letter'),(68,'Can change letter',23,'change_letter'),(69,'Can delete letter',23,'delete_letter'),(70,'Can add comment',24,'add_comment'),(71,'Can change comment',24,'change_comment'),(72,'Can delete comment',24,'delete_comment'),(73,'Can add discussion vote',25,'add_discussionvote'),(74,'Can change discussion vote',25,'change_discussionvote'),(75,'Can delete discussion vote',25,'delete_discussionvote'),(76,'Can add proposal vote',26,'add_proposalvote'),(77,'Can change proposal vote',26,'change_proposalvote'),(78,'Can delete proposal vote',26,'delete_proposalvote'),(79,'Can add letter vote',27,'add_lettervote'),(80,'Can change letter vote',27,'change_lettervote'),(81,'Can delete letter vote',27,'delete_lettervote'),(82,'Can add reply vote',28,'add_replyvote'),(83,'Can change reply vote',28,'change_replyvote'),(84,'Can delete reply vote',28,'delete_replyvote'),(85,'Can add question vote',29,'add_questionvote'),(86,'Can change question vote',29,'change_questionvote'),(87,'Can delete question vote',29,'delete_questionvote'),(88,'Can add answer vote',30,'add_answervote'),(89,'Can change answer vote',30,'change_answervote'),(90,'Can delete answer vote',30,'delete_answervote'),(91,'Can add comment vote',31,'add_commentvote'),(92,'Can change comment vote',31,'change_commentvote'),(93,'Can delete comment vote',31,'delete_commentvote');
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
-- Dumping data for table `digidemo_answer`
--

LOCK TABLES `digidemo_answer` WRITE;
/*!40000 ALTER TABLE `digidemo_answer` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_answercomment`
--

LOCK TABLES `digidemo_answercomment` WRITE;
/*!40000 ALTER TABLE `digidemo_answercomment` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_answercomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_answervote`
--

LOCK TABLES `digidemo_answervote` WRITE;
/*!40000 ALTER TABLE `digidemo_answervote` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_answervote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_comment`
--

LOCK TABLES `digidemo_comment` WRITE;
/*!40000 ALTER TABLE `digidemo_comment` DISABLE KEYS */;
REPLACE INTO `digidemo_comment` (`id`, `creation_date`, `last_modified`, `user_id`, `letter_id`, `body`, `score`) VALUES (1,'2014-07-13 17:00:32','2014-07-13 17:00:32',1,1,'@normaluser I agree with you but I think that you should consider offering some concrete evidence for what you are saying -- back up how the environmental losses will arise and why they are certain.  There\'s plenty of facts in the issue \nwiki to choose from.',1),(2,'2014-07-13 17:00:32','2014-07-13 17:00:32',1,1,'ll',0),(3,'2014-07-13 17:00:32','2014-07-13 17:00:32',1,1,'lll\r\n',0),(4,'2014-07-13 17:00:32','2014-07-13 17:00:32',1,1,'bic!',0),(5,'2014-07-13 17:00:32','2014-07-13 17:00:32',1,1,'super',0),(6,'2014-07-13 17:00:32','2014-07-13 17:00:32',1,14,'lame!',0),(7,'2014-07-13 17:00:32','2014-07-13 17:00:32',1,1,'kilp',0),(8,'2014-07-13 17:00:32','2014-07-13 17:00:32',1,1,'froze',0),(9,'2014-07-13 17:00:32','2014-07-13 17:00:32',1,1,'Blip',0),(10,'2014-07-13 17:00:32','2014-07-13 17:00:32',1,40,'Jimmi',0),(11,'2014-07-13 17:00:32','2014-07-13 17:00:32',1,1,'james',0),(12,'2014-07-13 17:00:32','2014-07-13 17:00:32',1,14,'blatant comment.',0),(13,'2014-07-13 17:00:32','2014-07-13 17:00:32',1,1,'pequifi',0),(14,'2014-07-15 01:51:53','2014-07-15 01:51:53',1,1,'hdkujehhie',0);
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
REPLACE INTO `digidemo_discussion` (`id`, `creation_date`, `last_modified`, `proposal_id`, `title`, `body`, `user_id`, `score`, `is_open`) VALUES (1,'2014-07-13 17:01:56','2014-07-17 05:54:52',1,'Social Factors','I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w',1,1,1),(2,'2014-07-13 17:01:56','2014-07-13 17:01:56',1,'Social Factors','I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w',1,1,1);
/*!40000 ALTER TABLE `digidemo_discussion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_discussionvote`
--

LOCK TABLES `digidemo_discussionvote` WRITE;
/*!40000 ALTER TABLE `digidemo_discussionvote` DISABLE KEYS */;
REPLACE INTO `digidemo_discussionvote` (`id`, `creation_date`, `last_modified`, `user_id`, `valence`, `target_id`) VALUES (1,'2014-07-13 17:02:03','2014-07-17 05:54:52',1,0,1),(2,'2014-07-13 17:02:03','2014-07-13 17:02:03',1,-1,2);
/*!40000 ALTER TABLE `digidemo_discussionvote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_factor`
--

LOCK TABLES `digidemo_factor` WRITE;
/*!40000 ALTER TABLE `digidemo_factor` DISABLE KEYS */;
REPLACE INTO `digidemo_factor` (`id`, `creation_date`, `last_modified`, `proposal_id`, `description`, `valence`, `sector_id`, `deleted`) VALUES (1,'2014-07-13 17:02:11','2014-07-22 05:12:38',1,'Transport of crude oil by pipeline is safer than by truck and train, which are the current alternatives',1,7,0),(2,'2014-07-13 17:02:11','2014-07-22 05:12:38',1,'The operation of pipelines for the transport of crude oil poses environmental risks due to the eventuality of leaks',-1,2,0),(3,'2014-07-13 17:02:11','2014-07-22 05:12:38',1,'Canada\'s readiness to make use of its natural resources will be increased',1,7,0),(4,'2014-07-13 17:02:11','2014-07-22 05:12:38',1,'Facilitating the development of the tarsands will create additional wealth and income in Canada.',1,1,0),(7,'2014-07-22 14:29:18','2014-07-22 14:29:18',2,'Test pos Eco factor.',1,1,0),(8,'2014-07-22 14:29:18','2014-07-22 14:29:18',2,'Test neg Env factor.',-1,2,0),(9,'2014-07-22 14:53:28','2014-07-22 14:53:28',3,'test2',1,1,0),(10,'2014-07-22 14:53:28','2014-07-22 14:53:28',3,'test2',-1,1,0);
/*!40000 ALTER TABLE `digidemo_factor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_factorversion`
--

LOCK TABLES `digidemo_factorversion` WRITE;
/*!40000 ALTER TABLE `digidemo_factorversion` DISABLE KEYS */;
REPLACE INTO `digidemo_factorversion` (`id`, `creation_date`, `last_modified`, `factor_id`, `proposal_version_id`, `description`, `valence`, `sector_id`, `deleted`) VALUES (1,'2014-07-14 18:34:25','2014-07-17 20:56:41',1,1,'Transport of crude oil by pipeline is safer than by truck and train, which are the current alternatives',1,7,0),(2,'2014-07-14 18:34:25','2014-07-17 20:56:41',2,1,'The operation of pipelines for the transport of crude oil poses environmental risks due to the eventuality of leaks',-1,2,0),(3,'2014-07-14 18:34:25','2014-07-17 20:56:41',3,1,'Canada\'s readiness to make use of its natural resources will be increased',1,7,0),(4,'2014-07-14 18:34:25','2014-07-17 20:56:41',4,1,'Facilitating the development of the tarsands will create additional wealth and income in Canada.',1,1,0),(7,'2014-07-14 18:34:25','2014-07-22 12:56:20',4,1,'Facilitating the development of the tarsands will create additional wealth and income in Canada.',1,1,1),(72,'2014-07-22 14:29:18','2014-07-22 14:29:18',7,22,'Test pos Eco factor.',1,1,0),(73,'2014-07-22 14:29:18','2014-07-22 14:29:18',8,22,'Test neg Env factor.',-1,2,0),(74,'2014-07-22 14:53:28','2014-07-22 14:53:28',9,23,'test2',1,1,0),(75,'2014-07-22 14:53:28','2014-07-22 14:53:28',10,23,'test2',-1,1,0);
/*!40000 ALTER TABLE `digidemo_factorversion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_letter`
--

LOCK TABLES `digidemo_letter` WRITE;
/*!40000 ALTER TABLE `digidemo_letter` DISABLE KEYS */;
REPLACE INTO `digidemo_letter` (`id`, `creation_date`, `last_modified`, `parent_letter_id`, `proposal_id`, `valence`, `user_id`, `body`, `score`) VALUES (1,'2014-07-13 17:02:17','2014-07-15 01:06:09',NULL,1,-1,2,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',3),(14,'2014-07-13 17:02:17','2014-07-15 01:52:09',NULL,1,0,2,'A new letter!',1),(16,'2014-07-13 17:02:17','2014-07-13 17:02:17',NULL,1,1,2,'aoeu',0),(38,'2014-07-13 17:02:17','2014-07-13 17:02:17',14,1,0,1,'A new letter!',0),(39,'2014-07-13 17:02:17','2014-07-13 17:02:17',1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0),(40,'2014-07-13 17:02:17','2014-07-13 17:02:17',NULL,1,1,1,'Wadatay',0),(41,'2014-07-13 17:02:17','2014-07-13 17:02:17',1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0),(42,'2014-07-13 17:02:17','2014-07-13 17:02:17',1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0),(43,'2014-07-13 17:02:17','2014-07-13 17:02:17',1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0),(44,'2014-07-13 17:02:17','2014-07-13 17:02:17',16,1,1,1,'aoeu',0),(45,'2014-07-13 17:02:17','2014-07-13 17:02:17',1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0);
/*!40000 ALTER TABLE `digidemo_letter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_letter_recipients`
--

LOCK TABLES `digidemo_letter_recipients` WRITE;
/*!40000 ALTER TABLE `digidemo_letter_recipients` DISABLE KEYS */;
REPLACE INTO `digidemo_letter_recipients` (`id`, `letter_id`, `position_id`) VALUES (1,1,1),(2,14,1),(3,16,1),(4,38,1),(5,39,1),(6,40,1),(7,41,1),(8,42,1),(9,43,1),(10,44,1),(11,45,1);
/*!40000 ALTER TABLE `digidemo_letter_recipients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_lettervote`
--

LOCK TABLES `digidemo_lettervote` WRITE;
/*!40000 ALTER TABLE `digidemo_lettervote` DISABLE KEYS */;
REPLACE INTO `digidemo_lettervote` (`id`, `creation_date`, `last_modified`, `user_id`, `valence`, `target_id`) VALUES (1,'2014-07-13 17:03:06','2014-07-15 01:06:09',1,1,1),(2,'2014-07-13 17:03:06','2014-07-13 17:03:06',1,0,16),(3,'2014-07-15 01:52:09','2014-07-15 01:52:09',1,1,14);
/*!40000 ALTER TABLE `digidemo_lettervote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_organization`
--

LOCK TABLES `digidemo_organization` WRITE;
/*!40000 ALTER TABLE `digidemo_organization` DISABLE KEYS */;
REPLACE INTO `digidemo_organization` (`id`, `creation_date`, `last_modified`, `short_name`, `legal_name`, `legal_classification`, `revenue`, `operations_summary`) VALUES (1,'2014-07-13 17:03:14','2014-07-13 17:03:14','The Conservative Party of Canada','The Conservative Party of Canada','NPT',-1,'Stephen Harper’s Conservative Government is focused on the priorities of Canadians – job creation and economic growth.\nWith the support of our Economic Action Plan, the Canadian economy has created approximately one million net new jobs since the depths of the global economic recession.  While the job isn’t done yet, this job creation record is the best in the G7 and shows that Canada is on the right track.');
/*!40000 ALTER TABLE `digidemo_organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_person`
--

LOCK TABLES `digidemo_person` WRITE;
/*!40000 ALTER TABLE `digidemo_person` DISABLE KEYS */;
REPLACE INTO `digidemo_person` (`id`, `creation_date`, `last_modified`, `fname`, `lname`, `portrait_url`, `wikipedia_url`, `bio_summary`) VALUES (1,'2014-07-13 17:03:26','2014-07-13 17:03:26','stephen','harper','http://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Stephen_Harper_by_Remy_Steinegger.jpg/800px-Stephen_Harper_by_Remy_Steinegger.jpg','http://en.wikipedia.org/wiki/Stephen_Harper','Stephen Joseph Harper (born April 30, 1959) is a Canadian politician who is the 22nd and current Prime Minister of Canada and the Leader of the Conservative Party. Harper became prime minister in 2006, forming a minority government after the 2006 election. He is the first prime minister to come from the newly reconstituted Conservative Party, which formed after a merger of the Progressive Conservative Party and the Canadian Alliance.');
/*!40000 ALTER TABLE `digidemo_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_position`
--

LOCK TABLES `digidemo_position` WRITE;
/*!40000 ALTER TABLE `digidemo_position` DISABLE KEYS */;
REPLACE INTO `digidemo_position` (`id`, `creation_date`, `last_modified`, `name`, `person_id`, `organization_id`, `salary`, `telephone`, `email`, `mandate_summary`) VALUES (1,'2014-07-13 17:03:36','2014-07-13 17:03:36','Prime minister of Canada',1,1,317574.00,'613-992-4211','stephen.harper@parl.gc.ca','');
/*!40000 ALTER TABLE `digidemo_position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_proposal`
--

LOCK TABLES `digidemo_proposal` WRITE;
/*!40000 ALTER TABLE `digidemo_proposal` DISABLE KEYS */;
REPLACE INTO `digidemo_proposal` (`id`, `creation_date`, `last_modified`, `is_published`, `score`, `title`, `summary`, `text`, `original_user_id`, `user_id`, `proposal_image`) VALUES (1,'2014-07-13 17:03:48','2014-07-24 05:47:35',1,0,'Keystone XL Pipeline Extension','The Keystone XL Pipeline is a proposed extension to the existing Keystone Pipeline System, put forward by TransCanada, the corporation that owns the Keystone System. The pipeline would cross the Canada/US border, importing crude oil sourced from the Albertan oil sands, into the United States. The proposal is currently awaiting government approval. The pipeline would be newly constructed, and is similar to existing pipelines in North America.\r\n\r\nThe Keystone XL pipeline project is a contentious political issue, owing to probable environmental, economic, and social impacts. Environmentally, the pipeline might present a risk of contaminating groundwater and disturbing sensitive ecosystems, but it might also be a better alternative than ground transport by train or truck. Economically, the pipeline might produce jobs temporarily during its construction, and permanently in additional refinement activities in the US. It would also lead to a redistribution of crude supply, emphasizing export and raising the price of oil in the Midwestern US. Socially, the construction of the pipeline would disturb landowners currently in its path, and would disturb heritage sites of cultural significance.','# Actors #\r\n - **TransCanada**: Corporation that owns the existing Keysone Pipeline System, and which has put forward the proposal to state and federal authorities for the Keystone XL extension.\r\n - **ConocoPhillips**: Corporation that was part-owner of the Keystone Pipeline System, bought out by TransCanada.\r\n - **Cardno Entrix**: Environmental Assessment Consultancy, contracted by TransCanada to produce an environmental assessment of the Keystone XL proposal.\r\n- **US Government**:\r\n        - **President Obama**: Can approve or reject the application for a Presidential Permit, legally needed to proceed with the construction project. \r\n         - **Environmental Protection Agency**: Oversees the environmental assessment of the project, and approves or rejects the application for an environmental permit, legally needed to proceed with the construction project.\r\n         - **US State Governments**: Each US state through which the proposed pipeline would pass can approve or reject the construction activities within its borders.\r\n     - **Canadian Government**:\r\n             - **National Energy Board of Canada** (NEB): Responsible for approving or rejecting the construction activities within Canada.\r\n         - WorleyParsons: Corporation acting as the general contractor for the pipeline construction.\r\n        \r\n        # Impacts #\r\n        ## Environmental Impacts ##\r\n        **Hazards relating to oil spills**. The originally proposed route traversed the Sand Hills region and the Ogallala aquifer.  The Sand Hills region is a sensitive wetland ecosystem in Nebraska.  The Ogallala aquifer is one of the largest reserves of fresh water in the world, spans eight states, provides drinking water for two million people, and supports a US$20 billion worth of agricultural activity.\r\n        \r\n        The path of the pipeline has been revised by TransCanada to avoid the Sand Hills region, and reduce the length\r\n        of piping running over the Ogallala aquifer.  The actual risks of a spill in the region of the aquifer are unclear, and the severity of impact is debated.  The pipeline, with a normal depth of 4 feet would be separated from the aquifer by a layer of fine clay, which might drastically reduce the actual effects on drinking water.  Thousands of miles of existing pipelines carrying crude oil and refined liquid hydrocarbons have crossed over the Ogallala Aquifer for years, so the severity of risk could be evaluated empirically.  The pipeline will be newly constructed, which should be considered when comparing to existing pipelines which do not benefit from technological advances or were converted from natural gas pipelines.\r\n        \r\n        **Greenhouse Gas Emissions**.  The Keystone XL pipeline would carry crude oil to refineries for conversion into fuels, among other products.  The activities of extracting, refining, and burning petroleum-derived fuels is a major contributor to CO2 accumulation in the atmosphere and climate change.  By providing access to US and global markets, the Keystone XL pipeline would facilitate further extraction in the oilsands of Alberta.  \r\n        If the Keystone XL pipeline is not built, crude from the Albertan tarsands might be refined and exported from\r\n        Canada, based on alternative Canadian pipeline  construction projects which would bring the crude to tidewater.  Additionally, ground transport of crude, by train and tanker, might be used instead, which adds to greenhouse gas emissions and poses its own safety hazards.\r\n        \r\n        ## Economic Impacts ##\r\n        **Employment**.  Construction of the pipeline would provide temporary employment for about 2 years.  Estimates of the amount of employment vary widely.  A report by Perryman Group, a financial analysis firm that was hired by TransCanada, estimates construction would employ 20,000 US workers and spend US$7 billion.  A study conducted by Cornell ILR Global Labor Institute estimated construction would employ 2500 to 4650 US workers.  The US State Department estimated 5000 to 6000 temporary construction jobs.  It\'s Supplemenntal Environmental Impact Statement estimated 3900 US workers directly employed and 42000 US workers indirectly employed by construction activities. \r\n        \r\n        **Risk of impact due to spills**.  The original route proposed for the Keystone XL pipeline passed over the Ogallala aquifer.  The aquifer supports about US$20 billion in agricultural activity.  If a spill contaminated the water, it could have serious economic impact.  The amended proposal has reduced the length of piping that crosses the aquifer.  The 2010 Enbridge oil spill along the Kalamazoo river in Michigan showed that spills can result in significant economic costs beyond environmental ones.\r\n        \r\n        # Social Impacts #\r\n        **Displacement of people**.  Land owners in the path of the pipeline would be displaced.  Landowners have already complained about threats by TransCanada to confiscate private land and some have faced lawsuits.  As of October 17, 2011 Transcanada had 34 eminent domain actions against landowners in Texas and 22 in South Dakota.\r\n        \r\n        **Damage to public goods (excluding the environment)**.  Various sacred sites, and prehistoric or historic archeological sites, and sites with traditional cultural value to Native Americans and other groups might be disturbed, removed or demolished.  TransCanada made a major donation to the University of Toronto to promote education and research in the health of the Aboriginal population.\r\n        \r\n        **Safety**.  Ground transport by tanker truck and rail is less safe.  As an example, the derailment of a train transporting crude oil at Lac-Mégantic in 2013 kiled 50 people.  Increased production in North Dakota has exceeded pipeline capacity since 2010, leading to increasing volumes of crude being shipped by truck or rail to refineries.  Alberta is expected to running up against a pipeline capacity limit around 2016.\r\n        \r\n        # In Perspective #\r\n         - The Alberta oil sands account for a quantity of GHG emissions equal to \r\n             - the coal-fired power plants in the State of Wisconsin \r\n             - 2.5% of total GHG emissions from the coal-fired power plants of the US\r\n             - 0.1% of global GHG emissions from all sources\r\n         - The Enbridge \"Alberta Clipper\" expansion has continued during late 2013, adding approximately the same cross-border capacity.\r\n         - The Keystone XL expansion is Phase 4 in the Keystone Pipeline system.\r\n             - it corresponds to between 1897 km, later revised to 1408 km of piping or 28% revised to 23% of the Keystone system by length.\r\n             - it will account for about 40% of the Keystone system\'s capacity if built.\r\n         - There are currently about 320,000 km of similar oil pipelines in the US.\r\n         - Alternative projects are being considered:\r\n                 - An all-Canadian pipeline north to the Arctic coast for shipping to markets in Europe and Asia\r\n                 - An all-Canadian pipeline (\"Energy East\") that would extend to Saint John, New Brunswick for export, while also supplying Montreal, Quebec City, and Saint John refineries.',1,1,'/digidemo/proposal-images/'),(2,'2014-07-22 14:29:18','2014-07-22 14:29:18',0,0,'Test Proposal','Test proposal summary.','Test proposal text.',1,1,'/digidemo/proposal-images/'),(3,'2014-07-22 14:53:28','2014-07-22 14:53:28',0,0,'Test 2','test2','eaeua',1,1,'/digidemo/proposal-images/');
/*!40000 ALTER TABLE `digidemo_proposal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_proposal_tags`
--

LOCK TABLES `digidemo_proposal_tags` WRITE;
/*!40000 ALTER TABLE `digidemo_proposal_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_proposal_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_proposalversion`
--

LOCK TABLES `digidemo_proposalversion` WRITE;
/*!40000 ALTER TABLE `digidemo_proposalversion` DISABLE KEYS */;
REPLACE INTO `digidemo_proposalversion` (`id`, `creation_date`, `last_modified`, `proposal_id`, `title`, `summary`, `text`, `user_id`) VALUES (1,'2014-07-13 17:04:17','2014-07-13 17:04:17',1,'Keystone XL Pipeline Extension','The Keystone XL Pipeline is a proposed extension to the existing Keystone Pipeline System, put forward by TransCanada, the corporation that owns the Keystone System. The pipeline would cross the Canada/US border, importing crude oil sourced from the Albertan oil sands, into the United States. The proposal is currently awaiting government approval. The pipeline would be newly constructed, and is similar to existing pipelines in North America.\n\nThe Keystone XL pipeline project is a contentious political issue, owing to probable environmental, economic, and social impacts. Environmentally, the pipeline might present a risk of contaminating groundwater and disturbing sensitive ecosystems, but it might also be a better alternative than ground transport by train or truck. Economically, the pipeline might produce jobs temporarily during its construction, and permanently in additional refinement activities in the US. It would also lead to a redistribution of crude supply, emphasizing export and raising the price of oil in the Midwestern US. Socially, the construction of the pipeline would disturb landowners currently in its path, and would disturb heritage sites of cultural significance.','# Actors #\n - **TransCanada**: Corporation that owns the existing Keysone Pipeline System, and which has put forward the proposal to state and federal authorities for the Keystone XL extension.\n - **ConocoPhillips**: Corporation that was part-owner of the Keystone Pipeline System, bought out by TransCanada.\n - **Cardno Entrix**: Environmental Assessment Consultancy, contracted by TransCanada to produce an environmental assessment of the Keystone XL proposal.\n- **US Government**:\n        - **President Obama**: Can approve or reject the application for a Presidential Permit, legally needed to proceed with the construction project. \n         - **Environmental Protection Agency**: Oversees the environmental assessment of the project, and approves or rejects the application for an environmental permit, legally needed to proceed with the construction project.\n         - **US State Governments**: Each US state through which the proposed pipeline would pass can approve or reject the construction activities within its borders.\n     - **Canadian Government**:\n             - **National Energy Board of Canada** (NEB): Responsible for approving or rejecting the construction activities within Canada.\n         - WorleyParsons: Corporation acting as the general contractor for the pipeline construction.\n        \n        # Impacts #\n        ## Environmental Impacts ##\n        **Hazards relating to oil spills**. The originally proposed route traversed the Sand Hills region and the Ogallala aquifer.  The Sand Hills region is a sensitive wetland ecosystem in Nebraska.  The Ogallala aquifer is one of the largest reserves of fresh water in the world, spans eight states, provides drinking water for two million people, and supports a US$20 billion worth of agricultural activity.\n        \n        The path of the pipeline has been revised by TransCanada to avoid the Sand Hills region, and reduce the length\n        of piping running over the Ogallala aquifer.  The actual risks of a spill in the region of the aquifer are unclear, and the severity of impact is debated.  The pipeline, with a normal depth of 4 feet would be separated from the aquifer by a layer of fine clay, which might drastically reduce the actual effects on drinking water.  Thousands of miles of existing pipelines carrying crude oil and refined liquid hydrocarbons have crossed over the Ogallala Aquifer for years, so the severity of risk could be evaluated empirically.  The pipeline will be newly constructed, which should be considered when comparing to existing pipelines which do not benefit from technological advances or were converted from natural gas pipelines.\n        \n        **Greenhouse Gas Emissions**.  The Keystone XL pipeline would carry crude oil to refineries for conversion into fuels, among other products.  The activities of extracting, refining, and burning petroleum-derived fuels is a major contributor to CO2 accumulation in the atmosphere and climate change.  By providing access to US and global markets, the Keystone XL pipeline would facilitate further extraction in the oilsands of Alberta.  \n        If the Keystone XL pipeline is not built, crude from the Albertan tarsands might be refined and exported from\n        Canada, based on alternative Canadian pipeline  construction projects which would bring the crude to tidewater.  Additionally, ground transport of crude, by train and tanker, might be used instead, which adds to greenhouse gas emissions and poses its own safety hazards.\n        \n        ## Economic Impacts ##\n        **Employment**.  Construction of the pipeline would provide temporary employment for about 2 years.  Estimates of the amount of employment vary widely.  A report by Perryman Group, a financial analysis firm that was hired by TransCanada, estimates construction would employ 20,000 US workers and spend US$7 billion.  A study conducted by Cornell ILR Global Labor Institute estimated construction would employ 2500 to 4650 US workers.  The US State Department estimated 5000 to 6000 temporary construction jobs.  It\'s Supplemenntal Environmental Impact Statement estimated 3900 US workers directly employed and 42000 US workers indirectly employed by construction activities. \n        \n        **Risk of impact due to spills**.  The original route proposed for the Keystone XL pipeline passed over the Ogallala aquifer.  The aquifer supports about US$20 billion in agricultural activity.  If a spill contaminated the water, it could have serious economic impact.  The amended proposal has reduced the length of piping that crosses the aquifer.  The 2010 Enbridge oil spill along the Kalamazoo river in Michigan showed that spills can result in significant economic costs beyond environmental ones.\n        \n        # Social Impacts #\n        **Displacement of people**.  Land owners in the path of the pipeline would be displaced.  Landowners have already complained about threats by TransCanada to confiscate private land and some have faced lawsuits.  As of October 17, 2011 Transcanada had 34 eminent domain actions against landowners in Texas and 22 in South Dakota.\n        \n        **Damage to public goods (excluding the environment)**.  Various sacred sites, and prehistoric or historic archeological sites, and sites with traditional cultural value to Native Americans and other groups might be disturbed, removed or demolished.  TransCanada made a major donation to the University of Toronto to promote education and research in the health of the Aboriginal population.\n        \n        **Safety**.  Ground transport by tanker truck and rail is less safe.  As an example, the derailment of a train transporting crude oil at Lac-Mégantic in 2013 kiled 50 people.  Increased production in North Dakota has exceeded pipeline capacity since 2010, leading to increasing volumes of crude being shipped by truck or rail to refineries.  Alberta is expected to running up against a pipeline capacity limit around 2016.\n        \n        # In Perspective #\n         - The Alberta oil sands account for a quantity of GHG emissions equal to \n             - the coal-fired power plants in the State of Wisconsin \n             - 2.5% of total GHG emissions from the coal-fired power plants of the US\n             - 0.1% of global GHG emissions from all sources\n         - The Enbridge \"Alberta Clipper\" expansion has continued during late 2013, adding approximately the same cross-border capacity.\n         - The Keystone XL expansion is Phase 4 in the Keystone Pipeline system.\n             - it corresponds to between 1897 km, later revised to 1408 km of piping or 28% revised to 23% of the Keystone system by length.\n             - it will account for about 40% of the Keystone system\'s capacity if built.\n         - There are currently about 320,000 km of similar oil pipelines in the US.\n         - Alternative projects are being considered:\n                 - An all-Canadian pipeline north to the Arctic coast for shipping to markets in Europe and Asia\n                 - An all-Canadian pipeline (\"Energy East\") that would extend to Saint John, New Brunswick for export, while also supplying Montreal, Quebec City, and Saint John refineries.',1),(22,'2014-07-22 14:29:18','2014-07-22 14:29:18',2,'Test Proposal','Test proposal summary.','Test proposal text.',1),(23,'2014-07-22 14:53:28','2014-07-22 14:53:28',3,'Test 2','test2','eaeua',1);
/*!40000 ALTER TABLE `digidemo_proposalversion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_proposalversion_tags`
--

LOCK TABLES `digidemo_proposalversion_tags` WRITE;
/*!40000 ALTER TABLE `digidemo_proposalversion_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_proposalversion_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_proposalvote`
--

LOCK TABLES `digidemo_proposalvote` WRITE;
/*!40000 ALTER TABLE `digidemo_proposalvote` DISABLE KEYS */;
REPLACE INTO `digidemo_proposalvote` (`id`, `creation_date`, `last_modified`, `user_id`, `valence`, `target_id`) VALUES (1,'2014-07-13 17:04:25','2014-07-15 01:50:31',1,1,1);
/*!40000 ALTER TABLE `digidemo_proposalvote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_question`
--

LOCK TABLES `digidemo_question` WRITE;
/*!40000 ALTER TABLE `digidemo_question` DISABLE KEYS */;
REPLACE INTO `digidemo_question` (`id`, `creation_date`, `last_modified`, `user_id`, `score`, `title`, `text`, `target_id`) VALUES (1,'2014-07-25 21:25:57','2014-07-25 21:25:57',1,0,'How likely (or frequent) can we expect spills along the pipeline extension to be?','I would like to know how likely spills are, based on the rate of previous incidents. It will probably be important to take into account the kind of piping technology used, and the kind of service. For example, repurposed piping originally for the transport of natural gas is likely to be different from newly built piping. Or, (and I\'m not sure), there may be a difference due to the fact that this is crude derived from tarsands, rather than conventional crude.',1);
/*!40000 ALTER TABLE `digidemo_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_questioncomment`
--

LOCK TABLES `digidemo_questioncomment` WRITE;
/*!40000 ALTER TABLE `digidemo_questioncomment` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_questioncomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_questionvote`
--

LOCK TABLES `digidemo_questionvote` WRITE;
/*!40000 ALTER TABLE `digidemo_questionvote` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_questionvote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_reply`
--

LOCK TABLES `digidemo_reply` WRITE;
/*!40000 ALTER TABLE `digidemo_reply` DISABLE KEYS */;
REPLACE INTO `digidemo_reply` (`id`, `creation_date`, `last_modified`, `discussion_id`, `body`, `user_id`, `score`, `is_open`) VALUES (24,'2014-07-13 17:04:31','2014-07-13 17:04:31',2,'A comment.',1,0,0),(25,'2014-07-13 17:04:31','2014-07-13 17:04:31',2,'Another comment.',1,0,0),(26,'2014-07-13 17:04:31','2014-07-13 17:04:31',1,'Comment on the first discussion.',1,0,0),(27,'2014-07-13 17:04:31','2014-07-13 17:04:31',1,'AONETHTNH',1,0,0);
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
REPLACE INTO `digidemo_sector` (`id`, `creation_date`, `last_modified`, `short_name`, `name`) VALUES (1,'2014-07-13 17:04:46','2014-07-13 17:04:46','ECO','economy'),(2,'2014-07-13 17:04:46','2014-07-13 17:04:46','ENV','environment'),(3,'2014-07-13 17:04:46','2014-07-13 17:04:46','HEA','health'),(4,'2014-07-13 17:04:46','2014-07-13 17:04:46','EDU','education'),(5,'2014-07-13 17:04:46','2014-07-13 17:04:46','IR','international relations'),(6,'2014-07-13 17:04:46','2014-07-13 17:04:46','SOC','society and culture'),(7,'2014-07-13 17:04:46','2014-07-13 17:04:46','SEC','security and readiness'),(8,'2014-07-13 17:04:46','2014-07-13 17:04:46','DEM','democratic mechanisms');
/*!40000 ALTER TABLE `digidemo_sector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_tag`
--

LOCK TABLES `digidemo_tag` WRITE;
/*!40000 ALTER TABLE `digidemo_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `digidemo_userprofile`
--

LOCK TABLES `digidemo_userprofile` WRITE;
/*!40000 ALTER TABLE `digidemo_userprofile` DISABLE KEYS */;
REPLACE INTO `digidemo_userprofile` (`id`, `creation_date`, `last_modified`, `user_id`, `email_validated`, `avatar_img`, `rep`, `street`, `zip_code`, `country`, `province`) VALUES (1,'2014-07-13 17:04:58','2014-07-17 05:54:52',1,1,'avatars/superuser.jpg',34,'Somewhere','560072','India','Karnatka'),(2,'2014-07-13 17:04:58','2014-07-15 01:52:09',2,1,'avatars/regularuser.jpg',34,'56 Long Ave.','51515','CAN','QC');
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
REPLACE INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'sector','digidemo','sector'),(8,'user profile','digidemo','userprofile'),(9,'tag','digidemo','tag'),(10,'proposal','digidemo','proposal'),(11,'proposal version','digidemo','proposalversion'),(12,'discussion','digidemo','discussion'),(13,'reply','digidemo','reply'),(14,'question','digidemo','question'),(15,'question comment','digidemo','questioncomment'),(16,'answer','digidemo','answer'),(17,'answer comment','digidemo','answercomment'),(18,'factor','digidemo','factor'),(19,'factor version','digidemo','factorversion'),(20,'person','digidemo','person'),(21,'organization','digidemo','organization'),(22,'position','digidemo','position'),(23,'letter','digidemo','letter'),(24,'comment','digidemo','comment'),(25,'discussion vote','digidemo','discussionvote'),(26,'proposal vote','digidemo','proposalvote'),(27,'letter vote','digidemo','lettervote'),(28,'reply vote','digidemo','replyvote'),(29,'question vote','digidemo','questionvote'),(30,'answer vote','digidemo','answervote'),(31,'comment vote','digidemo','commentvote');
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

-- Dump completed on 2014-07-25 17:26:11
