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
-- Current Database: `digidemo`
--

/*!40000 DROP DATABASE IF EXISTS `digidemo`*/;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `digidemo` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `digidemo`;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
REPLACE INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add migration history',7,'add_migrationhistory'),(20,'Can change migration history',7,'change_migrationhistory'),(21,'Can delete migration history',7,'delete_migrationhistory'),(22,'Can add user',8,'add_user'),(23,'Can change user',8,'change_user'),(24,'Can delete user',8,'delete_user'),(25,'Can add proposal',9,'add_proposal'),(26,'Can change proposal',9,'change_proposal'),(27,'Can delete proposal',9,'delete_proposal'),(28,'Can add letter',10,'add_letter'),(29,'Can change letter',10,'change_letter'),(30,'Can delete letter',10,'delete_letter'),(31,'Can add comment',11,'add_comment'),(32,'Can change comment',11,'change_comment'),(33,'Can delete comment',11,'delete_comment'),(34,'Can add person',12,'add_person'),(35,'Can change person',12,'change_person'),(36,'Can delete person',12,'delete_person'),(37,'Can add organization',13,'add_organization'),(38,'Can change organization',13,'change_organization'),(39,'Can delete organization',13,'delete_organization'),(40,'Can add position',14,'add_position'),(41,'Can change position',14,'change_position'),(42,'Can delete position',14,'delete_position'),(43,'Can add capability',15,'add_capability'),(44,'Can change capability',15,'change_capability'),(45,'Can delete capability',15,'delete_capability'),(46,'Can add factor',16,'add_factor'),(47,'Can change factor',16,'change_factor'),(48,'Can delete factor',16,'delete_factor'),(49,'Can add sector',17,'add_sector'),(50,'Can change sector',17,'change_sector'),(51,'Can delete sector',17,'delete_sector'),(52,'Can add proposal vote',18,'add_proposalvote'),(53,'Can change proposal vote',18,'change_proposalvote'),(54,'Can delete proposal vote',18,'delete_proposalvote'),(55,'Can add letter vote',19,'add_lettervote'),(56,'Can change letter vote',19,'change_lettervote'),(57,'Can delete letter vote',19,'delete_lettervote'),(58,'Can add user profile',20,'add_userprofile'),(59,'Can change user profile',20,'change_userprofile'),(60,'Can delete user profile',20,'delete_userprofile'),(61,'Can add comment',21,'add_comment'),(62,'Can change comment',21,'change_comment'),(63,'Can delete comment',21,'delete_comment');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
REPLACE INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES (1,'pbkdf2_sha256$12000$vdIKgzqx54r5$J3tT4LmxhxzRu/4YX8kPVNcf7GdGYbCDfBrkbUQ6NaI=','2014-06-15 03:38:24',1,'superuser','super','user','super.user@email.com',1,1,'2014-06-15 03:38:24'),(2,'pbkdf2_sha256$12000$LvEWg7RRIxvY$nK9r1ddB9vUhVIc5ORAzES/+rKZHxMFXJQnwkdyIAt8=','2014-07-01 05:20:13',0,'regularuser','regular','user','regular.user@email.com',0,1,'2014-07-01 05:22:06');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_capability`
--

DROP TABLE IF EXISTS `digidemo_capability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_capability` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `description` varchar(512) NOT NULL,
  `sector_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_capability_663ed8c9` (`sector_id`),
  CONSTRAINT `sector_id_refs_id_84257dfd` FOREIGN KEY (`sector_id`) REFERENCES `digidemo_sector` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_capability`
--

LOCK TABLES `digidemo_capability` WRITE;
/*!40000 ALTER TABLE `digidemo_capability` DISABLE KEYS */;
REPLACE INTO `digidemo_capability` (`id`, `name`, `description`, `sector_id`) VALUES (3,'~ obtain quality education','Universal access to quality education, including: literacy, numeracy, computer skills; history, human rights, political rights and process; self esteem, morality, automomy; natural sciences, cosmological and ecological origins; life skills, practical arts, expressive arts.',4),(4,'~ live in harmony with the natural world','A lifestyle that, without unusual inconvenience, does not pollute the environment in a way that renders it unfit or unpleasant, nor brings hopeless struggle or devastation to other life, and which provides access to nature and tranquility, and extracts resources from nature only at a rate that is either replenished, or exausted in a timeframe that allows our adaptation to alternatives',2),(5,'~ be represented politically','The capability to have one\'s interests and stakes in society considered, guarded, and improved by a political process that reconciles these stakes with those of others in a way that is fair, proportionate, efficient, and transparent',8),(6,'~ have meaningful political participation','The ability to participate in collective decisionmaking regarding matters with one holds stake, and for that participation to have substancial effect, in proportion to one\'s stake and that of others, and to be safe from harm, discrimination, or retribution for one\'s participation.',8),(8,'safeguarding capabilities with good international relations','Diplomatic cooperation and coordination which fosters amicable relations, through demands on and compromises with other nations, which are compatible with the longterm flourishing of human capabilities.',5),(9,'~ live a healthy life to its natural end','The ability to live a healthy life, to have full use of one\'s body, to be free of suffering and disease, and to live a long life to its natural end.',3),(10,'~ be free from undue descrimination','The ability to embrace one\'s nature, including for example body form and appearance, language, sexality, and so on, insofar as it does no harm to others, without being arbitrarily descriminated against.',6),(11,'safeguarding capabilities with security and readiness','Collective readiness to make use of natural resources, in a way that is sustainable, or consistent with reasonable expectations for adaptive exit, and exact gains in the national wealth by such usage',7),(12,'safeguarding capabilities with security','Collective readiness to defend the security of the nation, for example, defending sovereign territory from invasion and exploit, to protect against excessive foreign economic claim, to protect the integrity of computer systems and networks, and exert reasonable and proportionate pressure in the maintenance of treaty agreements.',7),(13,'~ to live free from harm and hazards','The ability to live without the fear or risk of hazards from reasonably forseable sources, including protection against natural disaster, economic disaster, and negligence in business and professional practice.',7),(14,'~ obtain the material necessities of life','The ability to obtain the basics of food, shelter, clothing, transportation, access to hygiene facilities, transportation, and communication which are necessary to live most lifestyles.',1),(15,'~ do meaningful work','The ability to earn the basic necessities of life through meaninful activities that contribute to society and make effecient use of ones talents, without putting oneself or others at risk.',1),(16,'~ enjoy freedom of choice in lifestyle','The capability to gain a sufficiency of income such that, after securing ones basic necessities, one still has some time and income to dispose of, in the ways of ones choosing, such as for entertainment, relaxation, intellectual or cultural enrichment, artistic expression, political engagement, human relationships, and so on.',1);
/*!40000 ALTER TABLE `digidemo_capability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_comment`
--

DROP TABLE IF EXISTS `digidemo_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author_id` int(11) NOT NULL,
  `letter_id` int(11) NOT NULL,
  `body` varchar(512) NOT NULL,
  `score` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_comment_e969df21` (`author_id`),
  KEY `digidemo_comment_45f341a0` (`letter_id`),
  CONSTRAINT `letter_id_refs_id_549c5f06` FOREIGN KEY (`letter_id`) REFERENCES `digidemo_letter` (`id`),
  CONSTRAINT `author_id_refs_id_b202d78c` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_comment`
--

LOCK TABLES `digidemo_comment` WRITE;
/*!40000 ALTER TABLE `digidemo_comment` DISABLE KEYS */;
REPLACE INTO `digidemo_comment` (`id`, `author_id`, `letter_id`, `body`, `score`) VALUES (1,1,1,'@normaluser I agree with you but I think that you should consider offering some concrete evidence for what you are saying -- back up how the environmental losses will arise and why they are certain.  There\'s plenty of facts in the issue \nwiki to choose from.',1),(2,1,1,'ll',0),(3,1,1,'lll\r\n',0);
/*!40000 ALTER TABLE `digidemo_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_discussion`
--

DROP TABLE IF EXISTS `digidemo_discussion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_discussion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proposal_id` int(11) NOT NULL,
  `title` varchar(256) NOT NULL,
  `body` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  `score` smallint(6) NOT NULL,
  `is_open` tinyint(1) NOT NULL,
  `creation_date` date NOT NULL,
  `last_activity_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_discussion_ad574d3c` (`proposal_id`),
  KEY `digidemo_discussion_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_dc56e1ff` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `proposal_id_refs_id_67b12962` FOREIGN KEY (`proposal_id`) REFERENCES `digidemo_proposal` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_discussion`
--

LOCK TABLES `digidemo_discussion` WRITE;
/*!40000 ALTER TABLE `digidemo_discussion` DISABLE KEYS */;
REPLACE INTO `digidemo_discussion` (`id`, `proposal_id`, `title`, `body`, `user_id`, `score`, `is_open`, `creation_date`, `last_activity_date`) VALUES (1,1,'Social Factors','I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w',3,1,127,'2014-06-30','0000-00-00');
/*!40000 ALTER TABLE `digidemo_discussion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_factor`
--

DROP TABLE IF EXISTS `digidemo_factor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_factor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proposal_id` int(11) NOT NULL,
  `description` varchar(256) NOT NULL,
  `capability_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_factor_ad574d3c` (`proposal_id`),
  KEY `digidemo_factor_567242ae` (`capability_id`),
  CONSTRAINT `capability_id_refs_id_7b69deb5` FOREIGN KEY (`capability_id`) REFERENCES `digidemo_capability` (`id`),
  CONSTRAINT `proposal_id_refs_id_34acf33f` FOREIGN KEY (`proposal_id`) REFERENCES `digidemo_proposal` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_factor`
--

LOCK TABLES `digidemo_factor` WRITE;
/*!40000 ALTER TABLE `digidemo_factor` DISABLE KEYS */;
REPLACE INTO `digidemo_factor` (`id`, `proposal_id`, `description`, `capability_id`, `valence`) VALUES (1,1,'Transport of crude oil by pipeline is safer than by truck and train, which are the current alternatives',13,1),(2,1,'The operation of pipelines for the transport of crude oil poses environmental risks due to the eventuality of leaks',4,-1),(3,1,'Canada\'s readiness to make use of its natural resources will be increased',11,1),(4,1,'Facilitating the development of the tarsands will create additional wealth and income in Canada.',15,1);
/*!40000 ALTER TABLE `digidemo_factor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_letter`
--

DROP TABLE IF EXISTS `digidemo_letter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_letter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_letter_id` int(11) DEFAULT NULL,
  `proposal_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `body` longtext NOT NULL,
  `score` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_letter_b0eaace7` (`parent_letter_id`),
  KEY `digidemo_letter_ad574d3c` (`proposal_id`),
  KEY `digidemo_letter_0a681a64` (`sender_id`),
  CONSTRAINT `sender_id_refs_id_747eea8b` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `parent_letter_id_refs_id_5234e149` FOREIGN KEY (`parent_letter_id`) REFERENCES `digidemo_letter` (`id`),
  CONSTRAINT `proposal_id_refs_id_a3d9d864` FOREIGN KEY (`proposal_id`) REFERENCES `digidemo_proposal` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_letter`
--

LOCK TABLES `digidemo_letter` WRITE;
/*!40000 ALTER TABLE `digidemo_letter` DISABLE KEYS */;
REPLACE INTO `digidemo_letter` (`id`, `parent_letter_id`, `proposal_id`, `valence`, `sender_id`, `body`, `score`) VALUES (1,NULL,1,-1,2,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',2);
/*!40000 ALTER TABLE `digidemo_letter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_letter_recipients`
--

DROP TABLE IF EXISTS `digidemo_letter_recipients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_letter_recipients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `letter_id` int(11) NOT NULL,
  `position_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `digidemo_letter_recipients_letter_id_7632fb1660808629_uniq` (`letter_id`,`position_id`),
  KEY `digidemo_letter_recipients_45f341a0` (`letter_id`),
  KEY `digidemo_letter_recipients_1f456125` (`position_id`),
  CONSTRAINT `position_id_refs_id_0e734fb2` FOREIGN KEY (`position_id`) REFERENCES `digidemo_position` (`id`),
  CONSTRAINT `letter_id_refs_id_72f69299` FOREIGN KEY (`letter_id`) REFERENCES `digidemo_letter` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_letter_recipients`
--

LOCK TABLES `digidemo_letter_recipients` WRITE;
/*!40000 ALTER TABLE `digidemo_letter_recipients` DISABLE KEYS */;
REPLACE INTO `digidemo_letter_recipients` (`id`, `letter_id`, `position_id`) VALUES (1,1,1);
/*!40000 ALTER TABLE `digidemo_letter_recipients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_letter_resenders`
--

DROP TABLE IF EXISTS `digidemo_letter_resenders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_letter_resenders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `letter_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `digidemo_letter_resenders_letter_id_382bd8e9b6d83aa3_uniq` (`letter_id`,`user_id`),
  KEY `digidemo_letter_resenders_45f341a0` (`letter_id`),
  KEY `digidemo_letter_resenders_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_99a14ef7` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `letter_id_refs_id_4cfb61f4` FOREIGN KEY (`letter_id`) REFERENCES `digidemo_letter` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_letter_resenders`
--

LOCK TABLES `digidemo_letter_resenders` WRITE;
/*!40000 ALTER TABLE `digidemo_letter_resenders` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_letter_resenders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_lettervote`
--

DROP TABLE IF EXISTS `digidemo_lettervote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_lettervote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `letter_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `digidemo_lettervote_user_id_114de14f34d25fb7_uniq` (`user_id`,`letter_id`),
  KEY `digidemo_lettervote_6340c63c` (`user_id`),
  KEY `digidemo_lettervote_45f341a0` (`letter_id`),
  CONSTRAINT `letter_id_refs_id_2b6488e6` FOREIGN KEY (`letter_id`) REFERENCES `digidemo_letter` (`id`),
  CONSTRAINT `user_id_refs_id_955f482c` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_lettervote`
--

LOCK TABLES `digidemo_lettervote` WRITE;
/*!40000 ALTER TABLE `digidemo_lettervote` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_lettervote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_organization`
--

DROP TABLE IF EXISTS `digidemo_organization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_organization` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `short_name` varchar(64) NOT NULL,
  `legal_name` varchar(128) NOT NULL,
  `legal_classification` varchar(48) NOT NULL,
  `revenue` bigint(20) NOT NULL,
  `operations_summary` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_organization`
--

LOCK TABLES `digidemo_organization` WRITE;
/*!40000 ALTER TABLE `digidemo_organization` DISABLE KEYS */;
REPLACE INTO `digidemo_organization` (`id`, `short_name`, `legal_name`, `legal_classification`, `revenue`, `operations_summary`) VALUES (1,'The Conservative Party of Canada','The Conservative Party of Canada','NPT',-1,'Stephen Harper’s Conservative Government is focused on the priorities of Canadians – job creation and economic growth.\nWith the support of our Economic Action Plan, the Canadian economy has created approximately one million net new jobs since the depths of the global economic recession.  While the job isn’t done yet, this job creation record is the best in the G7 and shows that Canada is on the right track.');
/*!40000 ALTER TABLE `digidemo_organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_person`
--

DROP TABLE IF EXISTS `digidemo_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(48) NOT NULL,
  `lname` varchar(48) NOT NULL,
  `portrait_url` varchar(256) NOT NULL,
  `wikipedia_url` varchar(256) NOT NULL,
  `bio_summary` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_person`
--

LOCK TABLES `digidemo_person` WRITE;
/*!40000 ALTER TABLE `digidemo_person` DISABLE KEYS */;
REPLACE INTO `digidemo_person` (`id`, `fname`, `lname`, `portrait_url`, `wikipedia_url`, `bio_summary`) VALUES (1,'stephen','harper','http://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Stephen_Harper_by_Remy_Steinegger.jpg/800px-Stephen_Harper_by_Remy_Steinegger.jpg','http://en.wikipedia.org/wiki/Stephen_Harper','Stephen Joseph Harper (born April 30, 1959) is a Canadian politician who is the 22nd and current Prime Minister of Canada and the Leader of the Conservative Party. Harper became prime minister in 2006, forming a minority government after the 2006 election. He is the first prime minister to come from the newly reconstituted Conservative Party, which formed after a merger of the Progressive Conservative Party and the Canadian Alliance.');
/*!40000 ALTER TABLE `digidemo_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_position`
--

DROP TABLE IF EXISTS `digidemo_position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_position` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `person_id` int(11) NOT NULL,
  `organization_id` int(11) NOT NULL,
  `salary` decimal(11,2) NOT NULL,
  `telephone` varchar(14) NOT NULL,
  `email` varchar(254) NOT NULL,
  `mandate_summary` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_position_16f39487` (`person_id`),
  KEY `digidemo_position_de772da3` (`organization_id`),
  CONSTRAINT `organization_id_refs_id_e8072702` FOREIGN KEY (`organization_id`) REFERENCES `digidemo_organization` (`id`),
  CONSTRAINT `person_id_refs_id_791b385c` FOREIGN KEY (`person_id`) REFERENCES `digidemo_person` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_position`
--

LOCK TABLES `digidemo_position` WRITE;
/*!40000 ALTER TABLE `digidemo_position` DISABLE KEYS */;
REPLACE INTO `digidemo_position` (`id`, `name`, `person_id`, `organization_id`, `salary`, `telephone`, `email`, `mandate_summary`) VALUES (1,'Prime minister of Canada',1,1,317574.00,'613-992-4211','stephen.harper@parl.gc.ca','');
/*!40000 ALTER TABLE `digidemo_position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_proposal`
--

DROP TABLE IF EXISTS `digidemo_proposal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_proposal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `title` varchar(256) NOT NULL,
  `text` longtext NOT NULL,
  `is_published` tinyint(1) NOT NULL,
  `last_modified` date NOT NULL,
  `creation_date` date NOT NULL,
  `author_id` int(11) NOT NULL,
  `score` smallint(6) NOT NULL,
  `proposal_image` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_proposal_e969df21` (`author_id`),
  CONSTRAINT `author_id_refs_id_1f8c5260` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_proposal`
--

LOCK TABLES `digidemo_proposal` WRITE;
/*!40000 ALTER TABLE `digidemo_proposal` DISABLE KEYS */;
REPLACE INTO `digidemo_proposal` (`id`, `name`, `title`, `text`, `is_published`, `last_modified`, `creation_date`, `author_id`, `score`, `proposal_image`) VALUES (1,'keystone_xl','Keystone XL Pipeline Extension','<p>The Keystone XL Pipeline is a proposed extension to the existing Keystone Pipeline System, put forward by TransCanada, the corporation that owns the Keystone System. The pipeline would cross the Canada/US border, importing crude oil sourced from the Albertan oil sands, into the United States. The proposal is currently awaiting government approval. The pipeline would be newly constructed, and is similar to existing pipelines in North America.</p><p>The Keystone XL pipeline project is a contentious political issue, owing to probable environmental, economic, and social impacts. Environmentally, the pipeline might present a risk of contaminating groundwater and disturbing sensitive ecosystems, but it might also be a better alternative than ground transport by train or truck. Economically, the pipeline might produce jobs temporarily during its construction, and permanently in additional refinement activities in the US. It would also lead to a redistribution of crude supply, emphasizing export and raising the price of oil in the Midwestern US. Socially, the construction of the pipeline would disturb landowners currently in its path, and would disturb heritage sites of cultural significance.</p>',1,'2014-06-27','2014-06-15',1,0,'/digidemo/proposal-images/'),(2,'test1','no factors','this proposal has no factors',1,'2014-06-20','2014-06-20',1,33,'/digidemo/proposal-images/'),(3,'Quebec','Quebec','a',1,'2014-03-10','2014-02-10',1,-7,'');
/*!40000 ALTER TABLE `digidemo_proposal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_proposal_sector`
--

DROP TABLE IF EXISTS `digidemo_proposal_sector`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_proposal_sector` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proposal_id` int(11) NOT NULL,
  `sector_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `digidemo_proposal_sector_proposal_id_7b9ae77beabec166_uniq` (`proposal_id`,`sector_id`),
  KEY `digidemo_proposal_sector_ad574d3c` (`proposal_id`),
  KEY `digidemo_proposal_sector_663ed8c9` (`sector_id`),
  CONSTRAINT `sector_id_refs_id_85342870` FOREIGN KEY (`sector_id`) REFERENCES `digidemo_sector` (`id`),
  CONSTRAINT `proposal_id_refs_id_f31a0883` FOREIGN KEY (`proposal_id`) REFERENCES `digidemo_proposal` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_proposal_sector`
--

LOCK TABLES `digidemo_proposal_sector` WRITE;
/*!40000 ALTER TABLE `digidemo_proposal_sector` DISABLE KEYS */;
REPLACE INTO `digidemo_proposal_sector` (`id`, `proposal_id`, `sector_id`) VALUES (1,1,1),(2,1,2);
/*!40000 ALTER TABLE `digidemo_proposal_sector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_proposalvote`
--

DROP TABLE IF EXISTS `digidemo_proposalvote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_proposalvote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `proposal_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `digidemo_proposalvote_user_id_ceb6b116ffcd231_uniq` (`user_id`,`proposal_id`),
  KEY `digidemo_proposalvote_6340c63c` (`user_id`),
  KEY `digidemo_proposalvote_ad574d3c` (`proposal_id`),
  CONSTRAINT `proposal_id_refs_id_2722b1c2` FOREIGN KEY (`proposal_id`) REFERENCES `digidemo_proposal` (`id`),
  CONSTRAINT `user_id_refs_id_baf64dae` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_proposalvote`
--

LOCK TABLES `digidemo_proposalvote` WRITE;
/*!40000 ALTER TABLE `digidemo_proposalvote` DISABLE KEYS */;
REPLACE INTO `digidemo_proposalvote` (`id`, `user_id`, `proposal_id`, `valence`) VALUES (1,1,1,0);
/*!40000 ALTER TABLE `digidemo_proposalvote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_reply`
--

DROP TABLE IF EXISTS `digidemo_reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_reply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `discussion_id` int(11) NOT NULL,
  `body` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  `score` smallint(6) NOT NULL,
  `is_open` tinyint(1) NOT NULL,
  `creation_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_reply_acd02281` (`discussion_id`),
  KEY `digidemo_reply_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_9950cae7` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `discussion_id_refs_id_0f0a157b` FOREIGN KEY (`discussion_id`) REFERENCES `digidemo_discussion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_reply`
--

LOCK TABLES `digidemo_reply` WRITE;
/*!40000 ALTER TABLE `digidemo_reply` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_sector`
--

DROP TABLE IF EXISTS `digidemo_sector`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_sector` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `short_name` varchar(3) NOT NULL,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_sector`
--

LOCK TABLES `digidemo_sector` WRITE;
/*!40000 ALTER TABLE `digidemo_sector` DISABLE KEYS */;
REPLACE INTO `digidemo_sector` (`id`, `short_name`, `name`) VALUES (1,'ECO','economy'),(2,'ENV','environment'),(3,'HEA','health'),(4,'EDU','education'),(5,'IR','international relations'),(6,'SOC','society and culture'),(7,'SEC','security and readiness'),(8,'DEM','democratic mechanisms');
/*!40000 ALTER TABLE `digidemo_sector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_userprofile`
--

DROP TABLE IF EXISTS `digidemo_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `email_validated` tinyint(1) NOT NULL,
  `avatar_img` varchar(100) NOT NULL,
  `rep` int(11) NOT NULL,
  `street` varchar(128) NOT NULL,
  `zip_code` varchar(10) NOT NULL,
  `country` varchar(64) NOT NULL,
  `province` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_7d86ea27` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_userprofile`
--

LOCK TABLES `digidemo_userprofile` WRITE;
/*!40000 ALTER TABLE `digidemo_userprofile` DISABLE KEYS */;
REPLACE INTO `digidemo_userprofile` (`id`, `user_id`, `email_validated`, `avatar_img`, `rep`, `street`, `zip_code`, `country`, `province`) VALUES (1,1,1,'avatars/superuser.jpg',4,'Somewhere','560072','India','Karnatka'),(2,2,1,'avatars/regularuser.jpg',12,'56 Long Ave.','51515','CAN','QC');
/*!40000 ALTER TABLE `digidemo_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
REPLACE INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'migration history','south','migrationhistory'),(8,'user','digidemo','user'),(9,'proposal','digidemo','proposal'),(10,'letter','digidemo','letter'),(11,'comment','digidemo','comment'),(12,'person','digidemo','person'),(13,'organization','digidemo','organization'),(14,'position','digidemo','position'),(15,'capability','digidemo','capability'),(16,'factor','digidemo','factor'),(17,'sector','digidemo','sector'),(18,'proposal vote','digidemo','proposalvote'),(19,'letter vote','digidemo','lettervote'),(20,'user profile','digidemo','userprofile');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `south_migrationhistory`
--

DROP TABLE IF EXISTS `south_migrationhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) NOT NULL,
  `migration` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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

-- Dump completed on 2014-07-02 22:22:04
