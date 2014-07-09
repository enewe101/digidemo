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
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
REPLACE INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add migration history',7,'add_migrationhistory'),(20,'Can change migration history',7,'change_migrationhistory'),(21,'Can delete migration history',7,'delete_migrationhistory'),(22,'Can add sector',8,'add_sector'),(23,'Can change sector',8,'change_sector'),(24,'Can delete sector',8,'delete_sector'),(25,'Can add proposal',9,'add_proposal'),(26,'Can change proposal',9,'change_proposal'),(27,'Can delete proposal',9,'delete_proposal'),(28,'Can add letter',10,'add_letter'),(29,'Can change letter',10,'change_letter'),(30,'Can delete letter',10,'delete_letter'),(31,'Can add comment',11,'add_comment'),(32,'Can change comment',11,'change_comment'),(33,'Can delete comment',11,'delete_comment'),(34,'Can add person',12,'add_person'),(35,'Can change person',12,'change_person'),(36,'Can delete person',12,'delete_person'),(37,'Can add organization',13,'add_organization'),(38,'Can change organization',13,'change_organization'),(39,'Can delete organization',13,'delete_organization'),(40,'Can add position',14,'add_position'),(41,'Can change position',14,'change_position'),(42,'Can delete position',14,'delete_position'),(43,'Can add position',15,'add_position'),(44,'Can change position',15,'change_position'),(45,'Can delete position',15,'delete_position'),(46,'Can add factor',16,'add_factor'),(47,'Can change factor',16,'change_factor'),(48,'Can delete factor',16,'delete_factor'),(49,'Can add sector',17,'add_sector'),(50,'Can change sector',17,'change_sector'),(51,'Can delete sector',17,'delete_sector'),(52,'Can add proposal vote',18,'add_proposalvote'),(53,'Can change proposal vote',18,'change_proposalvote'),(54,'Can delete proposal vote',18,'delete_proposalvote'),(55,'Can add letter vote',19,'add_lettervote'),(56,'Can change letter vote',19,'change_lettervote'),(57,'Can delete letter vote',19,'delete_lettervote'),(58,'Can add user profile',20,'add_userprofile'),(59,'Can change user profile',20,'change_userprofile'),(60,'Can delete user profile',20,'delete_userprofile'),(61,'Can add comment',21,'add_comment'),(62,'Can change comment',21,'change_comment'),(63,'Can delete comment',21,'delete_comment'),(64,'Can add discussion',22,'add_discussion'),(65,'Can change discussion',22,'change_discussion'),(66,'Can delete discussion',22,'delete_discussion'),(67,'Can add discussion vote',23,'add_discussionvote'),(68,'Can change discussion vote',23,'change_discussionvote'),(69,'Can delete discussion vote',23,'delete_discussionvote'),(70,'Can add reply',24,'add_reply'),(71,'Can change reply',24,'change_reply'),(72,'Can delete reply',24,'delete_reply'),(73,'Can add reply vote',25,'add_replyvote'),(74,'Can change reply vote',25,'change_replyvote'),(75,'Can delete reply vote',25,'delete_replyvote'),(76,'Can add comment vote',26,'add_commentvote'),(77,'Can change comment vote',26,'change_commentvote'),(78,'Can delete comment vote',26,'delete_commentvote');
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
-- Table structure for table `digidemo_comment`
--

DROP TABLE IF EXISTS `digidemo_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `letter_id` int(11) NOT NULL,
  `body` varchar(512) NOT NULL,
  `score` smallint(6) NOT NULL,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_comment_6340c63c` (`user_id`),
  KEY `digidemo_comment_45f341a0` (`letter_id`),
  CONSTRAINT `user_id_refs_id_b202d78c` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `letter_id_refs_id_549c5f06` FOREIGN KEY (`letter_id`) REFERENCES `digidemo_letter` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_comment`
--

LOCK TABLES `digidemo_comment` WRITE;
/*!40000 ALTER TABLE `digidemo_comment` DISABLE KEYS */;
REPLACE INTO `digidemo_comment` (`id`, `user_id`, `letter_id`, `body`, `score`, `creation_date`, `last_modified`) VALUES (1,1,1,'@normaluser I agree with you but I think that you should consider offering some concrete evidence for what you are saying -- back up how the environmental losses will arise and why they are certain.  There\'s plenty of facts in the issue \nwiki to choose from.',1,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(2,1,1,'ll',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(3,1,1,'lll\r\n',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(4,1,1,'bic!',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(5,1,1,'super',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(6,1,14,'lame!',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(7,1,1,'kilp',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(8,1,1,'froze',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(9,1,1,'Blip',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(10,1,40,'Jimmi',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(11,1,1,'james',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(12,1,14,'blatant comment.',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(13,1,1,'pequifi',0,'0000-00-00 00:00:00','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `digidemo_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_commentvote`
--

DROP TABLE IF EXISTS `digidemo_commentvote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_commentvote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`target_id`),
  KEY `digidemo_commentvote_6340c63c` (`user_id`),
  KEY `digidemo_commentvote_70bfdfd1` (`target_id`),
  CONSTRAINT `user_id_refs_id_5b5404b8` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `target_id_refs_id_29c7728e` FOREIGN KEY (`target_id`) REFERENCES `digidemo_comment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_commentvote`
--

LOCK TABLES `digidemo_commentvote` WRITE;
/*!40000 ALTER TABLE `digidemo_commentvote` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_commentvote` ENABLE KEYS */;
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
  `creation_date` datetime NOT NULL,
  `last_activity_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_discussion_ad574d3c` (`proposal_id`),
  KEY `digidemo_discussion_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_dc56e1ff` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `proposal_id_refs_id_67b12962` FOREIGN KEY (`proposal_id`) REFERENCES `digidemo_proposal` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_discussion`
--

LOCK TABLES `digidemo_discussion` WRITE;
/*!40000 ALTER TABLE `digidemo_discussion` DISABLE KEYS */;
REPLACE INTO `digidemo_discussion` (`id`, `proposal_id`, `title`, `body`, `user_id`, `score`, `is_open`, `creation_date`, `last_activity_date`) VALUES (1,1,'Social Factors','I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w',1,2,1,'2014-06-30 00:00:00','2014-07-08 00:00:00'),(2,1,'Social Factors','I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w',1,1,1,'2014-07-04 00:00:00','2014-07-04 00:00:00');
/*!40000 ALTER TABLE `digidemo_discussion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_discussionvote`
--

DROP TABLE IF EXISTS `digidemo_discussionvote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_discussionvote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`target_id`),
  KEY `digidemo_discussionvote_6340c63c` (`user_id`),
  KEY `digidemo_discussionvote_70bfdfd1` (`target_id`),
  CONSTRAINT `user_id_refs_id_ae8336d4` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `target_id_refs_id_4355b2d1` FOREIGN KEY (`target_id`) REFERENCES `digidemo_discussion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_discussionvote`
--

LOCK TABLES `digidemo_discussionvote` WRITE;
/*!40000 ALTER TABLE `digidemo_discussionvote` DISABLE KEYS */;
REPLACE INTO `digidemo_discussionvote` (`id`, `user_id`, `valence`, `creation_date`, `last_modified`, `target_id`) VALUES (1,1,1,'0000-00-00 00:00:00','0000-00-00 00:00:00',1),(2,1,-1,'0000-00-00 00:00:00','0000-00-00 00:00:00',2);
/*!40000 ALTER TABLE `digidemo_discussionvote` ENABLE KEYS */;
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
  `valence` smallint(6) NOT NULL,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `sector_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_factor_ad574d3c` (`proposal_id`),
  KEY `digidemo_factor_663ed8c9` (`sector_id`),
  CONSTRAINT `proposal_id_refs_id_34acf33f` FOREIGN KEY (`proposal_id`) REFERENCES `digidemo_proposal` (`id`),
  CONSTRAINT `sector_id_refs_id_7ab86ae0` FOREIGN KEY (`sector_id`) REFERENCES `digidemo_sector` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_factor`
--

LOCK TABLES `digidemo_factor` WRITE;
/*!40000 ALTER TABLE `digidemo_factor` DISABLE KEYS */;
REPLACE INTO `digidemo_factor` (`id`, `proposal_id`, `description`, `valence`, `creation_date`, `last_modified`, `sector_id`) VALUES (1,1,'Transport of crude oil by pipeline is safer than by truck and train, which are the current alternatives',1,'2014-07-09 05:57:04','2014-07-09 05:57:04',7),(2,1,'The operation of pipelines for the transport of crude oil poses environmental risks due to the eventuality of leaks',-1,'2014-07-09 05:57:04','2014-07-09 05:57:04',2),(3,1,'Canada\'s readiness to make use of its natural resources will be increased',1,'2014-07-09 05:57:04','2014-07-09 05:57:04',7),(4,1,'Facilitating the development of the tarsands will create additional wealth and income in Canada.',1,'2014-07-09 05:57:04','2014-07-09 05:57:04',1);
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
  `user_id` int(11) NOT NULL,
  `body` longtext NOT NULL,
  `score` smallint(6) NOT NULL,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_letter_b0eaace7` (`parent_letter_id`),
  KEY `digidemo_letter_ad574d3c` (`proposal_id`),
  KEY `digidemo_letter_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_747eea8b` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `parent_letter_id_refs_id_5234e149` FOREIGN KEY (`parent_letter_id`) REFERENCES `digidemo_letter` (`id`),
  CONSTRAINT `proposal_id_refs_id_a3d9d864` FOREIGN KEY (`proposal_id`) REFERENCES `digidemo_proposal` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_letter`
--

LOCK TABLES `digidemo_letter` WRITE;
/*!40000 ALTER TABLE `digidemo_letter` DISABLE KEYS */;
REPLACE INTO `digidemo_letter` (`id`, `parent_letter_id`, `proposal_id`, `valence`, `user_id`, `body`, `score`, `creation_date`, `last_modified`) VALUES (1,NULL,1,-1,2,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',1,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(14,NULL,1,0,2,'A new letter!',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(16,NULL,1,1,2,'aoeu',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(38,14,1,0,1,'A new letter!',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(39,1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(40,NULL,1,1,1,'Wadatay',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(41,1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(42,1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(43,1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(44,16,1,1,1,'aoeu',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(45,1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0,'0000-00-00 00:00:00','0000-00-00 00:00:00');
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
  UNIQUE KEY `letter_id` (`letter_id`,`position_id`),
  KEY `digidemo_letter_recipients_45f341a0` (`letter_id`),
  KEY `digidemo_letter_recipients_1f456125` (`position_id`),
  CONSTRAINT `letter_id_refs_id_72f69299` FOREIGN KEY (`letter_id`) REFERENCES `digidemo_letter` (`id`),
  CONSTRAINT `position_id_refs_id_0e734fb2` FOREIGN KEY (`position_id`) REFERENCES `digidemo_position` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_letter_recipients`
--

LOCK TABLES `digidemo_letter_recipients` WRITE;
/*!40000 ALTER TABLE `digidemo_letter_recipients` DISABLE KEYS */;
REPLACE INTO `digidemo_letter_recipients` (`id`, `letter_id`, `position_id`) VALUES (1,1,1),(14,14,1),(16,16,1),(38,38,1),(39,39,1),(40,40,1),(41,41,1),(42,42,1),(43,43,1),(44,44,1),(45,45,1);
/*!40000 ALTER TABLE `digidemo_letter_recipients` ENABLE KEYS */;
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
  `valence` smallint(6) NOT NULL,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`target_id`),
  KEY `digidemo_lettervote_6340c63c` (`user_id`),
  KEY `digidemo_lettervote_70bfdfd1` (`target_id`),
  CONSTRAINT `user_id_refs_id_955f482c` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `target_id_refs_id_2b6488e6` FOREIGN KEY (`target_id`) REFERENCES `digidemo_letter` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_lettervote`
--

LOCK TABLES `digidemo_lettervote` WRITE;
/*!40000 ALTER TABLE `digidemo_lettervote` DISABLE KEYS */;
REPLACE INTO `digidemo_lettervote` (`id`, `user_id`, `valence`, `creation_date`, `last_modified`, `target_id`) VALUES (1,1,-1,'0000-00-00 00:00:00','0000-00-00 00:00:00',1),(2,1,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',16);
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_organization`
--

LOCK TABLES `digidemo_organization` WRITE;
/*!40000 ALTER TABLE `digidemo_organization` DISABLE KEYS */;
REPLACE INTO `digidemo_organization` (`id`, `short_name`, `legal_name`, `legal_classification`, `revenue`, `operations_summary`, `creation_date`, `last_modified`) VALUES (1,'The Conservative Party of Canada','The Conservative Party of Canada','NPT',-1,'Stephen Harper’s Conservative Government is focused on the priorities of Canadians – job creation and economic growth.\nWith the support of our Economic Action Plan, the Canadian economy has created approximately one million net new jobs since the depths of the global economic recession.  While the job isn’t done yet, this job creation record is the best in the G7 and shows that Canada is on the right track.','0000-00-00 00:00:00','0000-00-00 00:00:00');
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_person`
--

LOCK TABLES `digidemo_person` WRITE;
/*!40000 ALTER TABLE `digidemo_person` DISABLE KEYS */;
REPLACE INTO `digidemo_person` (`id`, `fname`, `lname`, `portrait_url`, `wikipedia_url`, `bio_summary`, `creation_date`, `last_modified`) VALUES (1,'stephen','harper','http://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Stephen_Harper_by_Remy_Steinegger.jpg/800px-Stephen_Harper_by_Remy_Steinegger.jpg','http://en.wikipedia.org/wiki/Stephen_Harper','Stephen Joseph Harper (born April 30, 1959) is a Canadian politician who is the 22nd and current Prime Minister of Canada and the Leader of the Conservative Party. Harper became prime minister in 2006, forming a minority government after the 2006 election. He is the first prime minister to come from the newly reconstituted Conservative Party, which formed after a merger of the Progressive Conservative Party and the Canadian Alliance.','0000-00-00 00:00:00','0000-00-00 00:00:00');
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
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
REPLACE INTO `digidemo_position` (`id`, `name`, `person_id`, `organization_id`, `salary`, `telephone`, `email`, `mandate_summary`, `creation_date`, `last_modified`) VALUES (1,'Prime minister of Canada',1,1,317574.00,'613-992-4211','stephen.harper@parl.gc.ca','','0000-00-00 00:00:00','0000-00-00 00:00:00');
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
  `title` varchar(256) NOT NULL,
  `text` longtext NOT NULL,
  `is_published` tinyint(1) NOT NULL,
  `last_modified` datetime NOT NULL,
  `creation_date` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `score` smallint(6) NOT NULL,
  `proposal_image` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_proposal_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_1f8c5260` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_proposal`
--

LOCK TABLES `digidemo_proposal` WRITE;
/*!40000 ALTER TABLE `digidemo_proposal` DISABLE KEYS */;
REPLACE INTO `digidemo_proposal` (`id`, `title`, `text`, `is_published`, `last_modified`, `creation_date`, `user_id`, `score`, `proposal_image`) VALUES (1,'Keystone XL Pipeline Extension','The Keystone XL Pipeline is a proposed extension to the existing Keystone Pipeline System, put forward by TransCanada, the corporation that owns the Keystone System. The pipeline would cross the Canada/US border, importing crude oil sourced from the Albertan oil sands, into the United States. The proposal is currently awaiting government approval. The pipeline would be newly constructed, and is similar to existing pipelines in North America.\n\nThe Keystone XL pipeline project is a contentious political issue, owing to probable environmental, economic, and social impacts. Environmentally, the pipeline might present a risk of contaminating groundwater and disturbing sensitive ecosystems, but it might also be a better alternative than ground transport by train or truck. Economically, the pipeline might produce jobs temporarily during its construction, and permanently in additional refinement activities in the US. It would also lead to a redistribution of crude supply, emphasizing export and raising the price of oil in the Midwestern US. Socially, the construction of the pipeline would disturb landowners currently in its path, and would disturb heritage sites of cultural significance.',1,'2014-07-08 00:00:00','2014-06-15 00:00:00',1,2,'/digidemo/proposal-images/'),(2,'no factors','this proposal has no factors',1,'2014-07-08 00:00:00','2014-06-20 00:00:00',1,33,'/digidemo/proposal-images/'),(3,'Quebec','a',1,'2014-07-08 00:00:00','2014-02-10 00:00:00',1,-7,'');
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
  UNIQUE KEY `proposal_id` (`proposal_id`,`sector_id`),
  KEY `digidemo_proposal_sector_ad574d3c` (`proposal_id`),
  KEY `digidemo_proposal_sector_663ed8c9` (`sector_id`),
  CONSTRAINT `proposal_id_refs_id_f31a0883` FOREIGN KEY (`proposal_id`) REFERENCES `digidemo_proposal` (`id`),
  CONSTRAINT `sector_id_refs_id_85342870` FOREIGN KEY (`sector_id`) REFERENCES `digidemo_sector` (`id`)
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
  `valence` smallint(6) NOT NULL,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`target_id`),
  KEY `digidemo_proposalvote_6340c63c` (`user_id`),
  KEY `digidemo_proposalvote_70bfdfd1` (`target_id`),
  CONSTRAINT `user_id_refs_id_baf64dae` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `target_id_refs_id_2722b1c2` FOREIGN KEY (`target_id`) REFERENCES `digidemo_proposal` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_proposalvote`
--

LOCK TABLES `digidemo_proposalvote` WRITE;
/*!40000 ALTER TABLE `digidemo_proposalvote` DISABLE KEYS */;
REPLACE INTO `digidemo_proposalvote` (`id`, `user_id`, `valence`, `creation_date`, `last_modified`, `target_id`) VALUES (1,1,1,'0000-00-00 00:00:00','0000-00-00 00:00:00',1);
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_reply_acd02281` (`discussion_id`),
  KEY `digidemo_reply_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_9950cae7` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `discussion_id_refs_id_0f0a157b` FOREIGN KEY (`discussion_id`) REFERENCES `digidemo_discussion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_reply`
--

LOCK TABLES `digidemo_reply` WRITE;
/*!40000 ALTER TABLE `digidemo_reply` DISABLE KEYS */;
REPLACE INTO `digidemo_reply` (`id`, `discussion_id`, `body`, `user_id`, `score`, `is_open`, `creation_date`, `last_modified`) VALUES (24,2,'A comment.',1,0,0,'2014-07-04 00:00:00','0000-00-00 00:00:00'),(25,2,'Another comment.',1,0,0,'2014-07-04 00:00:00','0000-00-00 00:00:00'),(26,1,'Comment on the first discussion.',1,0,0,'2014-07-04 00:00:00','0000-00-00 00:00:00'),(27,1,'AONETHTNH',1,0,0,'2014-07-05 00:00:00','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `digidemo_reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_replyvote`
--

DROP TABLE IF EXISTS `digidemo_replyvote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_replyvote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`target_id`),
  KEY `digidemo_replyvote_6340c63c` (`user_id`),
  KEY `digidemo_replyvote_70bfdfd1` (`target_id`),
  CONSTRAINT `target_id_refs_id_9f87ff39` FOREIGN KEY (`target_id`) REFERENCES `digidemo_reply` (`id`),
  CONSTRAINT `user_id_refs_id_d659ef00` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_replyvote`
--

LOCK TABLES `digidemo_replyvote` WRITE;
/*!40000 ALTER TABLE `digidemo_replyvote` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_replyvote` ENABLE KEYS */;
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_sector`
--

LOCK TABLES `digidemo_sector` WRITE;
/*!40000 ALTER TABLE `digidemo_sector` DISABLE KEYS */;
REPLACE INTO `digidemo_sector` (`id`, `short_name`, `name`, `creation_date`, `last_modified`) VALUES (1,'ECO','economy','0000-00-00 00:00:00','0000-00-00 00:00:00'),(2,'ENV','environment','0000-00-00 00:00:00','0000-00-00 00:00:00'),(3,'HEA','health','0000-00-00 00:00:00','0000-00-00 00:00:00'),(4,'EDU','education','0000-00-00 00:00:00','0000-00-00 00:00:00'),(5,'IR','international relations','0000-00-00 00:00:00','0000-00-00 00:00:00'),(6,'SOC','society and culture','0000-00-00 00:00:00','0000-00-00 00:00:00'),(7,'SEC','security and readiness','0000-00-00 00:00:00','0000-00-00 00:00:00'),(8,'DEM','democratic mechanisms','0000-00-00 00:00:00','0000-00-00 00:00:00');
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
REPLACE INTO `digidemo_userprofile` (`id`, `user_id`, `email_validated`, `avatar_img`, `rep`, `street`, `zip_code`, `country`, `province`) VALUES (1,1,1,'avatars/superuser.jpg',44,'Somewhere','560072','India','Karnatka'),(2,2,1,'avatars/regularuser.jpg',12,'56 Long Ave.','51515','CAN','QC');
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
REPLACE INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'migration history','south','migrationhistory'),(9,'proposal','digidemo','proposal'),(10,'letter','digidemo','letter'),(11,'comment','digidemo','comment'),(12,'person','digidemo','person'),(13,'organization','digidemo','organization'),(14,'position','digidemo','position'),(15,'capability','digidemo','capability'),(16,'factor','digidemo','factor'),(17,'sector','digidemo','sector'),(18,'proposal vote','digidemo','proposalvote'),(19,'letter vote','digidemo','lettervote'),(20,'user profile','digidemo','userprofile'),(22,'discussion','digidemo','discussion'),(23,'discussion vote','digidemo','discussionvote'),(24,'reply','digidemo','reply'),(25,'reply vote','digidemo','replyvote'),(26,'comment vote','digidemo','commentvote');
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-07-09  2:44:01
