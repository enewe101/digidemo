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
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
REPLACE INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add sector',7,'add_sector'),(20,'Can change sector',7,'change_sector'),(21,'Can delete sector',7,'delete_sector'),(22,'Can add user profile',8,'add_userprofile'),(23,'Can change user profile',8,'change_userprofile'),(24,'Can delete user profile',8,'delete_userprofile'),(25,'Can add tag',9,'add_tag'),(26,'Can change tag',9,'change_tag'),(27,'Can delete tag',9,'delete_tag'),(28,'Can add proposal',10,'add_proposal'),(29,'Can change proposal',10,'change_proposal'),(30,'Can delete proposal',10,'delete_proposal'),(31,'Can add proposal version',11,'add_proposalversion'),(32,'Can change proposal version',11,'change_proposalversion'),(33,'Can delete proposal version',11,'delete_proposalversion'),(34,'Can add discussion',12,'add_discussion'),(35,'Can change discussion',12,'change_discussion'),(36,'Can delete discussion',12,'delete_discussion'),(37,'Can add reply',13,'add_reply'),(38,'Can change reply',13,'change_reply'),(39,'Can delete reply',13,'delete_reply'),(40,'Can add question',14,'add_question'),(41,'Can change question',14,'change_question'),(42,'Can delete question',14,'delete_question'),(43,'Can add question comment',15,'add_questioncomment'),(44,'Can change question comment',15,'change_questioncomment'),(45,'Can delete question comment',15,'delete_questioncomment'),(46,'Can add answer',16,'add_answer'),(47,'Can change answer',16,'change_answer'),(48,'Can delete answer',16,'delete_answer'),(49,'Can add answer comment',17,'add_answercomment'),(50,'Can change answer comment',17,'change_answercomment'),(51,'Can delete answer comment',17,'delete_answercomment'),(52,'Can add factor',18,'add_factor'),(53,'Can change factor',18,'change_factor'),(54,'Can delete factor',18,'delete_factor'),(55,'Can add factor version',19,'add_factorversion'),(56,'Can change factor version',19,'change_factorversion'),(57,'Can delete factor version',19,'delete_factorversion'),(58,'Can add person',20,'add_person'),(59,'Can change person',20,'change_person'),(60,'Can delete person',20,'delete_person'),(61,'Can add organization',21,'add_organization'),(62,'Can change organization',21,'change_organization'),(63,'Can delete organization',21,'delete_organization'),(64,'Can add position',22,'add_position'),(65,'Can change position',22,'change_position'),(66,'Can delete position',22,'delete_position'),(67,'Can add letter',23,'add_letter'),(68,'Can change letter',23,'change_letter'),(69,'Can delete letter',23,'delete_letter'),(70,'Can add comment',24,'add_comment'),(71,'Can change comment',24,'change_comment'),(72,'Can delete comment',24,'delete_comment'),(73,'Can add discussion vote',25,'add_discussionvote'),(74,'Can change discussion vote',25,'change_discussionvote'),(75,'Can delete discussion vote',25,'delete_discussionvote'),(76,'Can add proposal vote',26,'add_proposalvote'),(77,'Can change proposal vote',26,'change_proposalvote'),(78,'Can delete proposal vote',26,'delete_proposalvote'),(79,'Can add letter vote',27,'add_lettervote'),(80,'Can change letter vote',27,'change_lettervote'),(81,'Can delete letter vote',27,'delete_lettervote'),(82,'Can add reply vote',28,'add_replyvote'),(83,'Can change reply vote',28,'change_replyvote'),(84,'Can delete reply vote',28,'delete_replyvote'),(85,'Can add question vote',29,'add_questionvote'),(86,'Can change question vote',29,'change_questionvote'),(87,'Can delete question vote',29,'delete_questionvote'),(88,'Can add answer vote',30,'add_answervote'),(89,'Can change answer vote',30,'change_answervote'),(90,'Can delete answer vote',30,'delete_answervote'),(91,'Can add comment vote',31,'add_commentvote'),(92,'Can change comment vote',31,'change_commentvote'),(93,'Can delete comment vote',31,'delete_commentvote');
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
-- Table structure for table `digidemo_answer`
--

DROP TABLE IF EXISTS `digidemo_answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_answer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `score` smallint(6) NOT NULL,
  `text` longtext NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_answer_6340c63c` (`user_id`),
  KEY `digidemo_answer_70bfdfd1` (`target_id`),
  CONSTRAINT `user_id_refs_id_daa77108` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `target_id_refs_id_e84baa74` FOREIGN KEY (`target_id`) REFERENCES `digidemo_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_answer`
--

LOCK TABLES `digidemo_answer` WRITE;
/*!40000 ALTER TABLE `digidemo_answer` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_answercomment`
--

DROP TABLE IF EXISTS `digidemo_answercomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_answercomment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `score` smallint(6) NOT NULL,
  `text` varchar(512) NOT NULL,
  `answer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_answercomment_6340c63c` (`user_id`),
  KEY `digidemo_answercomment_5b4ce3ea` (`answer_id`),
  CONSTRAINT `user_id_refs_id_bf3a0f99` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `answer_id_refs_id_5979b3a6` FOREIGN KEY (`answer_id`) REFERENCES `digidemo_answer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_answercomment`
--

LOCK TABLES `digidemo_answercomment` WRITE;
/*!40000 ALTER TABLE `digidemo_answercomment` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_answercomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_answervote`
--

DROP TABLE IF EXISTS `digidemo_answervote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_answervote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`target_id`),
  KEY `digidemo_answervote_6340c63c` (`user_id`),
  KEY `digidemo_answervote_70bfdfd1` (`target_id`),
  CONSTRAINT `user_id_refs_id_c58dd99d` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `target_id_refs_id_b2d5d960` FOREIGN KEY (`target_id`) REFERENCES `digidemo_answer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_answervote`
--

LOCK TABLES `digidemo_answervote` WRITE;
/*!40000 ALTER TABLE `digidemo_answervote` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_answervote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_comment`
--

DROP TABLE IF EXISTS `digidemo_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `target_id` int(11) NOT NULL,
  `letter_id` int(11) DEFAULT NULL,
  `body` varchar(512) DEFAULT NULL,
  `text` varchar(512) NOT NULL,
  `score` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_comment_6340c63c` (`user_id`),
  KEY `digidemo_comment_70bfdfd1` (`target_id`),
  KEY `digidemo_comment_45f341a0` (`letter_id`),
  CONSTRAINT `user_id_refs_id_b202d78c` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `letter_id_refs_id_549c5f06` FOREIGN KEY (`letter_id`) REFERENCES `digidemo_letter` (`id`),
  CONSTRAINT `target_id_refs_id_549c5f06` FOREIGN KEY (`target_id`) REFERENCES `digidemo_letter` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_comment`
--

LOCK TABLES `digidemo_comment` WRITE;
/*!40000 ALTER TABLE `digidemo_comment` DISABLE KEYS */;
REPLACE INTO `digidemo_comment` (`id`, `creation_date`, `last_modified`, `user_id`, `target_id`, `letter_id`, `body`, `text`, `score`) VALUES (1,'2014-07-13 17:00:32','2014-07-28 03:56:58',1,1,NULL,NULL,'@normaluser I agree with you but I think that you should consider offering some concrete evidence for what you are saying -- back up how the environmental losses will arise and why they are certain.  There\'s plenty of facts in the issue \nwiki to choose from.',1),(2,'2014-07-13 17:00:32','2014-07-28 03:56:58',1,1,NULL,NULL,'ll',0),(3,'2014-07-13 17:00:32','2014-07-28 03:56:58',1,1,NULL,NULL,'lll\r\n',0),(4,'2014-07-13 17:00:32','2014-07-28 03:56:58',1,1,NULL,NULL,'bic!',0),(5,'2014-07-13 17:00:32','2014-07-28 03:56:58',1,1,NULL,NULL,'super',0),(6,'2014-07-13 17:00:32','2014-07-28 03:56:58',1,14,NULL,NULL,'lame!',0),(7,'2014-07-13 17:00:32','2014-07-28 03:56:58',1,1,NULL,NULL,'kilp',0),(8,'2014-07-13 17:00:32','2014-07-28 03:56:58',1,1,NULL,NULL,'froze',0),(9,'2014-07-13 17:00:32','2014-07-28 03:56:58',1,1,NULL,NULL,'Blip',0),(10,'2014-07-13 17:00:32','2014-07-28 03:56:58',1,40,NULL,NULL,'Jimmi',0),(11,'2014-07-13 17:00:32','2014-07-28 03:56:58',1,1,NULL,NULL,'james',0),(12,'2014-07-13 17:00:32','2014-07-28 03:56:58',1,14,NULL,NULL,'blatant comment.',0),(13,'2014-07-13 17:00:32','2014-07-28 03:56:58',1,1,NULL,NULL,'pequifi',0),(14,'2014-07-15 01:51:53','2014-07-28 03:56:58',1,1,NULL,NULL,'hdkujehhie',0);
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `proposal_id` int(11) NOT NULL,
  `title` varchar(256) NOT NULL,
  `body` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  `score` smallint(6) NOT NULL,
  `is_open` tinyint(1) NOT NULL,
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
REPLACE INTO `digidemo_discussion` (`id`, `creation_date`, `last_modified`, `proposal_id`, `title`, `body`, `user_id`, `score`, `is_open`) VALUES (1,'2014-07-13 17:01:56','2014-07-17 05:54:52',1,'Social Factors','I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w',1,1,1),(2,'2014-07-13 17:01:56','2014-07-13 17:01:56',1,'Social Factors','I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w I think that we need more material covering the social factors of this proposal.  There is only a brief mention of the displacement of people.  It would be better to get some statistics together on how many people are likely to be displaced, and how this w',1,1,1);
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
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
REPLACE INTO `digidemo_discussionvote` (`id`, `creation_date`, `last_modified`, `user_id`, `valence`, `target_id`) VALUES (1,'2014-07-13 17:02:03','2014-07-17 05:54:52',1,0,1),(2,'2014-07-13 17:02:03','2014-07-13 17:02:03',1,-1,2);
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `proposal_id` int(11) NOT NULL,
  `description` varchar(256) NOT NULL,
  `valence` smallint(6) NOT NULL,
  `sector_id` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_factor_ad574d3c` (`proposal_id`),
  KEY `digidemo_factor_663ed8c9` (`sector_id`),
  CONSTRAINT `sector_id_refs_id_7ab86ae0` FOREIGN KEY (`sector_id`) REFERENCES `digidemo_sector` (`id`),
  CONSTRAINT `proposal_id_refs_id_34acf33f` FOREIGN KEY (`proposal_id`) REFERENCES `digidemo_proposal` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_factor`
--

LOCK TABLES `digidemo_factor` WRITE;
/*!40000 ALTER TABLE `digidemo_factor` DISABLE KEYS */;
REPLACE INTO `digidemo_factor` (`id`, `creation_date`, `last_modified`, `proposal_id`, `description`, `valence`, `sector_id`, `deleted`) VALUES (1,'2014-07-13 17:02:11','2014-07-22 05:12:38',1,'Transport of crude oil by pipeline is safer than by truck and train, which are the current alternatives',1,7,0),(2,'2014-07-13 17:02:11','2014-07-22 05:12:38',1,'The operation of pipelines for the transport of crude oil poses environmental risks due to the eventuality of leaks',-1,2,0),(3,'2014-07-13 17:02:11','2014-07-22 05:12:38',1,'Canada\'s readiness to make use of its natural resources will be increased',1,7,0),(4,'2014-07-13 17:02:11','2014-07-22 05:12:38',1,'Facilitating the development of the tarsands will create additional wealth and income in Canada.',1,1,0),(7,'2014-07-22 14:29:18','2014-07-22 14:29:18',2,'Test pos Eco factor.',1,1,0),(8,'2014-07-22 14:29:18','2014-07-22 14:29:18',2,'Test neg Env factor.',-1,2,0),(9,'2014-07-22 14:53:28','2014-07-22 14:53:28',3,'test2',1,1,0),(10,'2014-07-22 14:53:28','2014-07-22 14:53:28',3,'test2',-1,1,0);
/*!40000 ALTER TABLE `digidemo_factor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_factorversion`
--

DROP TABLE IF EXISTS `digidemo_factorversion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_factorversion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `factor_id` int(11) DEFAULT NULL,
  `proposal_version_id` int(11) DEFAULT NULL,
  `description` varchar(256) NOT NULL,
  `valence` smallint(6) NOT NULL,
  `sector_id` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_factorversion_ebe94448` (`factor_id`),
  KEY `digidemo_factorversion_145c8dbd` (`proposal_version_id`),
  KEY `digidemo_factorversion_663ed8c9` (`sector_id`),
  CONSTRAINT `sector_id_refs_id_b806429c` FOREIGN KEY (`sector_id`) REFERENCES `digidemo_sector` (`id`),
  CONSTRAINT `factor_id_refs_id_475a336f` FOREIGN KEY (`factor_id`) REFERENCES `digidemo_factor` (`id`),
  CONSTRAINT `proposal_version_id_refs_id_2e779041` FOREIGN KEY (`proposal_version_id`) REFERENCES `digidemo_proposalversion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_factorversion`
--

LOCK TABLES `digidemo_factorversion` WRITE;
/*!40000 ALTER TABLE `digidemo_factorversion` DISABLE KEYS */;
REPLACE INTO `digidemo_factorversion` (`id`, `creation_date`, `last_modified`, `factor_id`, `proposal_version_id`, `description`, `valence`, `sector_id`, `deleted`) VALUES (1,'2014-07-14 18:34:25','2014-07-17 20:56:41',1,1,'Transport of crude oil by pipeline is safer than by truck and train, which are the current alternatives',1,7,0),(2,'2014-07-14 18:34:25','2014-07-17 20:56:41',2,1,'The operation of pipelines for the transport of crude oil poses environmental risks due to the eventuality of leaks',-1,2,0),(3,'2014-07-14 18:34:25','2014-07-17 20:56:41',3,1,'Canada\'s readiness to make use of its natural resources will be increased',1,7,0),(4,'2014-07-14 18:34:25','2014-07-17 20:56:41',4,1,'Facilitating the development of the tarsands will create additional wealth and income in Canada.',1,1,0),(7,'2014-07-14 18:34:25','2014-07-22 12:56:20',4,1,'Facilitating the development of the tarsands will create additional wealth and income in Canada.',1,1,1),(72,'2014-07-22 14:29:18','2014-07-22 14:29:18',7,22,'Test pos Eco factor.',1,1,0),(73,'2014-07-22 14:29:18','2014-07-22 14:29:18',8,22,'Test neg Env factor.',-1,2,0),(74,'2014-07-22 14:53:28','2014-07-22 14:53:28',9,23,'test2',1,1,0),(75,'2014-07-22 14:53:28','2014-07-22 14:53:28',10,23,'test2',-1,1,0);
/*!40000 ALTER TABLE `digidemo_factorversion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_letter`
--

DROP TABLE IF EXISTS `digidemo_letter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_letter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `parent_letter_id` int(11) DEFAULT NULL,
  `proposal_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  `body` longtext NOT NULL,
  `score` smallint(6) NOT NULL,
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
REPLACE INTO `digidemo_letter` (`id`, `creation_date`, `last_modified`, `parent_letter_id`, `proposal_id`, `valence`, `user_id`, `body`, `score`) VALUES (1,'2014-07-13 17:02:17','2014-07-15 01:06:09',NULL,1,-1,2,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',3),(14,'2014-07-13 17:02:17','2014-07-15 01:52:09',NULL,1,0,2,'A new letter!',1),(16,'2014-07-13 17:02:17','2014-07-13 17:02:17',NULL,1,1,2,'aoeu',0),(38,'2014-07-13 17:02:17','2014-07-13 17:02:17',14,1,0,1,'A new letter!',0),(39,'2014-07-13 17:02:17','2014-07-13 17:02:17',1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0),(40,'2014-07-13 17:02:17','2014-07-13 17:02:17',NULL,1,1,1,'Wadatay',0),(41,'2014-07-13 17:02:17','2014-07-13 17:02:17',1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0),(42,'2014-07-13 17:02:17','2014-07-13 17:02:17',1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0),(43,'2014-07-13 17:02:17','2014-07-13 17:02:17',1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0),(44,'2014-07-13 17:02:17','2014-07-13 17:02:17',16,1,1,1,'aoeu',0),(45,'2014-07-13 17:02:17','2014-07-13 17:02:17',1,1,-1,1,'I do not support the project to expand the Keystone Pipeline System.  This proposal generates serious and certain  environmental losses, which do not justify the economic gains.  Furthermore, the development will bring wealth mainly to foreign shareholders, so that the actual economic gains will be much less than they should  be.',0);
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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_letter_recipients`
--

LOCK TABLES `digidemo_letter_recipients` WRITE;
/*!40000 ALTER TABLE `digidemo_letter_recipients` DISABLE KEYS */;
REPLACE INTO `digidemo_letter_recipients` (`id`, `letter_id`, `position_id`) VALUES (1,1,1),(2,14,1),(3,16,1),(4,38,1),(5,39,1),(6,40,1),(7,41,1),(8,42,1),(9,43,1),(10,44,1),(11,45,1);
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`target_id`),
  KEY `digidemo_lettervote_6340c63c` (`user_id`),
  KEY `digidemo_lettervote_70bfdfd1` (`target_id`),
  CONSTRAINT `user_id_refs_id_955f482c` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `target_id_refs_id_2b6488e6` FOREIGN KEY (`target_id`) REFERENCES `digidemo_letter` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_lettervote`
--

LOCK TABLES `digidemo_lettervote` WRITE;
/*!40000 ALTER TABLE `digidemo_lettervote` DISABLE KEYS */;
REPLACE INTO `digidemo_lettervote` (`id`, `creation_date`, `last_modified`, `user_id`, `valence`, `target_id`) VALUES (1,'2014-07-13 17:03:06','2014-07-15 01:06:09',1,1,1),(2,'2014-07-13 17:03:06','2014-07-13 17:03:06',1,0,16),(3,'2014-07-15 01:52:09','2014-07-15 01:52:09',1,1,14);
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
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
REPLACE INTO `digidemo_organization` (`id`, `creation_date`, `last_modified`, `short_name`, `legal_name`, `legal_classification`, `revenue`, `operations_summary`) VALUES (1,'2014-07-13 17:03:14','2014-07-13 17:03:14','The Conservative Party of Canada','The Conservative Party of Canada','NPT',-1,'Stephen Harper’s Conservative Government is focused on the priorities of Canadians – job creation and economic growth.\nWith the support of our Economic Action Plan, the Canadian economy has created approximately one million net new jobs since the depths of the global economic recession.  While the job isn’t done yet, this job creation record is the best in the G7 and shows that Canada is on the right track.');
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
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
REPLACE INTO `digidemo_person` (`id`, `creation_date`, `last_modified`, `fname`, `lname`, `portrait_url`, `wikipedia_url`, `bio_summary`) VALUES (1,'2014-07-13 17:03:26','2014-07-13 17:03:26','stephen','harper','http://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Stephen_Harper_by_Remy_Steinegger.jpg/800px-Stephen_Harper_by_Remy_Steinegger.jpg','http://en.wikipedia.org/wiki/Stephen_Harper','Stephen Joseph Harper (born April 30, 1959) is a Canadian politician who is the 22nd and current Prime Minister of Canada and the Leader of the Conservative Party. Harper became prime minister in 2006, forming a minority government after the 2006 election. He is the first prime minister to come from the newly reconstituted Conservative Party, which formed after a merger of the Progressive Conservative Party and the Canadian Alliance.');
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
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
  CONSTRAINT `person_id_refs_id_791b385c` FOREIGN KEY (`person_id`) REFERENCES `digidemo_person` (`id`),
  CONSTRAINT `organization_id_refs_id_e8072702` FOREIGN KEY (`organization_id`) REFERENCES `digidemo_organization` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_position`
--

LOCK TABLES `digidemo_position` WRITE;
/*!40000 ALTER TABLE `digidemo_position` DISABLE KEYS */;
REPLACE INTO `digidemo_position` (`id`, `creation_date`, `last_modified`, `name`, `person_id`, `organization_id`, `salary`, `telephone`, `email`, `mandate_summary`) VALUES (1,'2014-07-13 17:03:36','2014-07-13 17:03:36','Prime minister of Canada',1,1,317574.00,'613-992-4211','stephen.harper@parl.gc.ca','');
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `is_published` tinyint(1) NOT NULL,
  `score` smallint(6) NOT NULL,
  `title` varchar(256) NOT NULL,
  `summary` longtext NOT NULL,
  `text` longtext NOT NULL,
  `original_user_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `proposal_image` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_proposal_24741952` (`original_user_id`),
  KEY `digidemo_proposal_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_1f8c5260` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `original_user_id_refs_id_1f8c5260` FOREIGN KEY (`original_user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_proposal`
--

LOCK TABLES `digidemo_proposal` WRITE;
/*!40000 ALTER TABLE `digidemo_proposal` DISABLE KEYS */;
REPLACE INTO `digidemo_proposal` (`id`, `creation_date`, `last_modified`, `is_published`, `score`, `title`, `summary`, `text`, `original_user_id`, `user_id`, `proposal_image`) VALUES (1,'2014-07-13 17:03:48','2014-07-24 05:47:35',1,0,'Keystone XL Pipeline Extension','The Keystone XL Pipeline is a proposed extension to the existing Keystone Pipeline System, put forward by TransCanada, the corporation that owns the Keystone System. The pipeline would cross the Canada/US border, importing crude oil sourced from the Albertan oil sands, into the United States. The proposal is currently awaiting government approval. The pipeline would be newly constructed, and is similar to existing pipelines in North America.\r\n\r\nThe Keystone XL pipeline project is a contentious political issue, owing to probable environmental, economic, and social impacts. Environmentally, the pipeline might present a risk of contaminating groundwater and disturbing sensitive ecosystems, but it might also be a better alternative than ground transport by train or truck. Economically, the pipeline might produce jobs temporarily during its construction, and permanently in additional refinement activities in the US. It would also lead to a redistribution of crude supply, emphasizing export and raising the price of oil in the Midwestern US. Socially, the construction of the pipeline would disturb landowners currently in its path, and would disturb heritage sites of cultural significance.','# Actors #\r\n - **TransCanada**: Corporation that owns the existing Keysone Pipeline System, and which has put forward the proposal to state and federal authorities for the Keystone XL extension.\r\n - **ConocoPhillips**: Corporation that was part-owner of the Keystone Pipeline System, bought out by TransCanada.\r\n - **Cardno Entrix**: Environmental Assessment Consultancy, contracted by TransCanada to produce an environmental assessment of the Keystone XL proposal.\r\n- **US Government**:\r\n        - **President Obama**: Can approve or reject the application for a Presidential Permit, legally needed to proceed with the construction project. \r\n         - **Environmental Protection Agency**: Oversees the environmental assessment of the project, and approves or rejects the application for an environmental permit, legally needed to proceed with the construction project.\r\n         - **US State Governments**: Each US state through which the proposed pipeline would pass can approve or reject the construction activities within its borders.\r\n     - **Canadian Government**:\r\n             - **National Energy Board of Canada** (NEB): Responsible for approving or rejecting the construction activities within Canada.\r\n         - WorleyParsons: Corporation acting as the general contractor for the pipeline construction.\r\n        \r\n        # Impacts #\r\n        ## Environmental Impacts ##\r\n        **Hazards relating to oil spills**. The originally proposed route traversed the Sand Hills region and the Ogallala aquifer.  The Sand Hills region is a sensitive wetland ecosystem in Nebraska.  The Ogallala aquifer is one of the largest reserves of fresh water in the world, spans eight states, provides drinking water for two million people, and supports a US$20 billion worth of agricultural activity.\r\n        \r\n        The path of the pipeline has been revised by TransCanada to avoid the Sand Hills region, and reduce the length\r\n        of piping running over the Ogallala aquifer.  The actual risks of a spill in the region of the aquifer are unclear, and the severity of impact is debated.  The pipeline, with a normal depth of 4 feet would be separated from the aquifer by a layer of fine clay, which might drastically reduce the actual effects on drinking water.  Thousands of miles of existing pipelines carrying crude oil and refined liquid hydrocarbons have crossed over the Ogallala Aquifer for years, so the severity of risk could be evaluated empirically.  The pipeline will be newly constructed, which should be considered when comparing to existing pipelines which do not benefit from technological advances or were converted from natural gas pipelines.\r\n        \r\n        **Greenhouse Gas Emissions**.  The Keystone XL pipeline would carry crude oil to refineries for conversion into fuels, among other products.  The activities of extracting, refining, and burning petroleum-derived fuels is a major contributor to CO2 accumulation in the atmosphere and climate change.  By providing access to US and global markets, the Keystone XL pipeline would facilitate further extraction in the oilsands of Alberta.  \r\n        If the Keystone XL pipeline is not built, crude from the Albertan tarsands might be refined and exported from\r\n        Canada, based on alternative Canadian pipeline  construction projects which would bring the crude to tidewater.  Additionally, ground transport of crude, by train and tanker, might be used instead, which adds to greenhouse gas emissions and poses its own safety hazards.\r\n        \r\n        ## Economic Impacts ##\r\n        **Employment**.  Construction of the pipeline would provide temporary employment for about 2 years.  Estimates of the amount of employment vary widely.  A report by Perryman Group, a financial analysis firm that was hired by TransCanada, estimates construction would employ 20,000 US workers and spend US$7 billion.  A study conducted by Cornell ILR Global Labor Institute estimated construction would employ 2500 to 4650 US workers.  The US State Department estimated 5000 to 6000 temporary construction jobs.  It\'s Supplemenntal Environmental Impact Statement estimated 3900 US workers directly employed and 42000 US workers indirectly employed by construction activities. \r\n        \r\n        **Risk of impact due to spills**.  The original route proposed for the Keystone XL pipeline passed over the Ogallala aquifer.  The aquifer supports about US$20 billion in agricultural activity.  If a spill contaminated the water, it could have serious economic impact.  The amended proposal has reduced the length of piping that crosses the aquifer.  The 2010 Enbridge oil spill along the Kalamazoo river in Michigan showed that spills can result in significant economic costs beyond environmental ones.\r\n        \r\n        # Social Impacts #\r\n        **Displacement of people**.  Land owners in the path of the pipeline would be displaced.  Landowners have already complained about threats by TransCanada to confiscate private land and some have faced lawsuits.  As of October 17, 2011 Transcanada had 34 eminent domain actions against landowners in Texas and 22 in South Dakota.\r\n        \r\n        **Damage to public goods (excluding the environment)**.  Various sacred sites, and prehistoric or historic archeological sites, and sites with traditional cultural value to Native Americans and other groups might be disturbed, removed or demolished.  TransCanada made a major donation to the University of Toronto to promote education and research in the health of the Aboriginal population.\r\n        \r\n        **Safety**.  Ground transport by tanker truck and rail is less safe.  As an example, the derailment of a train transporting crude oil at Lac-Mégantic in 2013 kiled 50 people.  Increased production in North Dakota has exceeded pipeline capacity since 2010, leading to increasing volumes of crude being shipped by truck or rail to refineries.  Alberta is expected to running up against a pipeline capacity limit around 2016.\r\n        \r\n        # In Perspective #\r\n         - The Alberta oil sands account for a quantity of GHG emissions equal to \r\n             - the coal-fired power plants in the State of Wisconsin \r\n             - 2.5% of total GHG emissions from the coal-fired power plants of the US\r\n             - 0.1% of global GHG emissions from all sources\r\n         - The Enbridge \"Alberta Clipper\" expansion has continued during late 2013, adding approximately the same cross-border capacity.\r\n         - The Keystone XL expansion is Phase 4 in the Keystone Pipeline system.\r\n             - it corresponds to between 1897 km, later revised to 1408 km of piping or 28% revised to 23% of the Keystone system by length.\r\n             - it will account for about 40% of the Keystone system\'s capacity if built.\r\n         - There are currently about 320,000 km of similar oil pipelines in the US.\r\n         - Alternative projects are being considered:\r\n                 - An all-Canadian pipeline north to the Arctic coast for shipping to markets in Europe and Asia\r\n                 - An all-Canadian pipeline (\"Energy East\") that would extend to Saint John, New Brunswick for export, while also supplying Montreal, Quebec City, and Saint John refineries.',1,1,'/digidemo/proposal-images/'),(2,'2014-07-22 14:29:18','2014-07-22 14:29:18',0,0,'Test Proposal','Test proposal summary.','Test proposal text.',1,1,'/digidemo/proposal-images/'),(3,'2014-07-22 14:53:28','2014-07-22 14:53:28',0,0,'Test 2','test2','eaeua',1,1,'/digidemo/proposal-images/');
/*!40000 ALTER TABLE `digidemo_proposal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_proposal_tags`
--

DROP TABLE IF EXISTS `digidemo_proposal_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_proposal_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proposal_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `proposal_id` (`proposal_id`,`tag_id`),
  KEY `digidemo_proposal_tags_ad574d3c` (`proposal_id`),
  KEY `digidemo_proposal_tags_5659cca2` (`tag_id`),
  CONSTRAINT `proposal_id_refs_id_b71410b6` FOREIGN KEY (`proposal_id`) REFERENCES `digidemo_proposal` (`id`),
  CONSTRAINT `tag_id_refs_id_e1334569` FOREIGN KEY (`tag_id`) REFERENCES `digidemo_tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_proposal_tags`
--

LOCK TABLES `digidemo_proposal_tags` WRITE;
/*!40000 ALTER TABLE `digidemo_proposal_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_proposal_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_proposalversion`
--

DROP TABLE IF EXISTS `digidemo_proposalversion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_proposalversion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `proposal_id` int(11) DEFAULT NULL,
  `title` varchar(256) NOT NULL,
  `summary` longtext NOT NULL,
  `text` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_proposalversion_ad574d3c` (`proposal_id`),
  KEY `digidemo_proposalversion_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_947246bb` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `proposal_id_refs_id_5991915b` FOREIGN KEY (`proposal_id`) REFERENCES `digidemo_proposal` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_proposalversion`
--

LOCK TABLES `digidemo_proposalversion` WRITE;
/*!40000 ALTER TABLE `digidemo_proposalversion` DISABLE KEYS */;
REPLACE INTO `digidemo_proposalversion` (`id`, `creation_date`, `last_modified`, `proposal_id`, `title`, `summary`, `text`, `user_id`) VALUES (1,'2014-07-13 17:04:17','2014-07-13 17:04:17',1,'Keystone XL Pipeline Extension','The Keystone XL Pipeline is a proposed extension to the existing Keystone Pipeline System, put forward by TransCanada, the corporation that owns the Keystone System. The pipeline would cross the Canada/US border, importing crude oil sourced from the Albertan oil sands, into the United States. The proposal is currently awaiting government approval. The pipeline would be newly constructed, and is similar to existing pipelines in North America.\n\nThe Keystone XL pipeline project is a contentious political issue, owing to probable environmental, economic, and social impacts. Environmentally, the pipeline might present a risk of contaminating groundwater and disturbing sensitive ecosystems, but it might also be a better alternative than ground transport by train or truck. Economically, the pipeline might produce jobs temporarily during its construction, and permanently in additional refinement activities in the US. It would also lead to a redistribution of crude supply, emphasizing export and raising the price of oil in the Midwestern US. Socially, the construction of the pipeline would disturb landowners currently in its path, and would disturb heritage sites of cultural significance.','# Actors #\n - **TransCanada**: Corporation that owns the existing Keysone Pipeline System, and which has put forward the proposal to state and federal authorities for the Keystone XL extension.\n - **ConocoPhillips**: Corporation that was part-owner of the Keystone Pipeline System, bought out by TransCanada.\n - **Cardno Entrix**: Environmental Assessment Consultancy, contracted by TransCanada to produce an environmental assessment of the Keystone XL proposal.\n- **US Government**:\n        - **President Obama**: Can approve or reject the application for a Presidential Permit, legally needed to proceed with the construction project. \n         - **Environmental Protection Agency**: Oversees the environmental assessment of the project, and approves or rejects the application for an environmental permit, legally needed to proceed with the construction project.\n         - **US State Governments**: Each US state through which the proposed pipeline would pass can approve or reject the construction activities within its borders.\n     - **Canadian Government**:\n             - **National Energy Board of Canada** (NEB): Responsible for approving or rejecting the construction activities within Canada.\n         - WorleyParsons: Corporation acting as the general contractor for the pipeline construction.\n        \n        # Impacts #\n        ## Environmental Impacts ##\n        **Hazards relating to oil spills**. The originally proposed route traversed the Sand Hills region and the Ogallala aquifer.  The Sand Hills region is a sensitive wetland ecosystem in Nebraska.  The Ogallala aquifer is one of the largest reserves of fresh water in the world, spans eight states, provides drinking water for two million people, and supports a US$20 billion worth of agricultural activity.\n        \n        The path of the pipeline has been revised by TransCanada to avoid the Sand Hills region, and reduce the length\n        of piping running over the Ogallala aquifer.  The actual risks of a spill in the region of the aquifer are unclear, and the severity of impact is debated.  The pipeline, with a normal depth of 4 feet would be separated from the aquifer by a layer of fine clay, which might drastically reduce the actual effects on drinking water.  Thousands of miles of existing pipelines carrying crude oil and refined liquid hydrocarbons have crossed over the Ogallala Aquifer for years, so the severity of risk could be evaluated empirically.  The pipeline will be newly constructed, which should be considered when comparing to existing pipelines which do not benefit from technological advances or were converted from natural gas pipelines.\n        \n        **Greenhouse Gas Emissions**.  The Keystone XL pipeline would carry crude oil to refineries for conversion into fuels, among other products.  The activities of extracting, refining, and burning petroleum-derived fuels is a major contributor to CO2 accumulation in the atmosphere and climate change.  By providing access to US and global markets, the Keystone XL pipeline would facilitate further extraction in the oilsands of Alberta.  \n        If the Keystone XL pipeline is not built, crude from the Albertan tarsands might be refined and exported from\n        Canada, based on alternative Canadian pipeline  construction projects which would bring the crude to tidewater.  Additionally, ground transport of crude, by train and tanker, might be used instead, which adds to greenhouse gas emissions and poses its own safety hazards.\n        \n        ## Economic Impacts ##\n        **Employment**.  Construction of the pipeline would provide temporary employment for about 2 years.  Estimates of the amount of employment vary widely.  A report by Perryman Group, a financial analysis firm that was hired by TransCanada, estimates construction would employ 20,000 US workers and spend US$7 billion.  A study conducted by Cornell ILR Global Labor Institute estimated construction would employ 2500 to 4650 US workers.  The US State Department estimated 5000 to 6000 temporary construction jobs.  It\'s Supplemenntal Environmental Impact Statement estimated 3900 US workers directly employed and 42000 US workers indirectly employed by construction activities. \n        \n        **Risk of impact due to spills**.  The original route proposed for the Keystone XL pipeline passed over the Ogallala aquifer.  The aquifer supports about US$20 billion in agricultural activity.  If a spill contaminated the water, it could have serious economic impact.  The amended proposal has reduced the length of piping that crosses the aquifer.  The 2010 Enbridge oil spill along the Kalamazoo river in Michigan showed that spills can result in significant economic costs beyond environmental ones.\n        \n        # Social Impacts #\n        **Displacement of people**.  Land owners in the path of the pipeline would be displaced.  Landowners have already complained about threats by TransCanada to confiscate private land and some have faced lawsuits.  As of October 17, 2011 Transcanada had 34 eminent domain actions against landowners in Texas and 22 in South Dakota.\n        \n        **Damage to public goods (excluding the environment)**.  Various sacred sites, and prehistoric or historic archeological sites, and sites with traditional cultural value to Native Americans and other groups might be disturbed, removed or demolished.  TransCanada made a major donation to the University of Toronto to promote education and research in the health of the Aboriginal population.\n        \n        **Safety**.  Ground transport by tanker truck and rail is less safe.  As an example, the derailment of a train transporting crude oil at Lac-Mégantic in 2013 kiled 50 people.  Increased production in North Dakota has exceeded pipeline capacity since 2010, leading to increasing volumes of crude being shipped by truck or rail to refineries.  Alberta is expected to running up against a pipeline capacity limit around 2016.\n        \n        # In Perspective #\n         - The Alberta oil sands account for a quantity of GHG emissions equal to \n             - the coal-fired power plants in the State of Wisconsin \n             - 2.5% of total GHG emissions from the coal-fired power plants of the US\n             - 0.1% of global GHG emissions from all sources\n         - The Enbridge \"Alberta Clipper\" expansion has continued during late 2013, adding approximately the same cross-border capacity.\n         - The Keystone XL expansion is Phase 4 in the Keystone Pipeline system.\n             - it corresponds to between 1897 km, later revised to 1408 km of piping or 28% revised to 23% of the Keystone system by length.\n             - it will account for about 40% of the Keystone system\'s capacity if built.\n         - There are currently about 320,000 km of similar oil pipelines in the US.\n         - Alternative projects are being considered:\n                 - An all-Canadian pipeline north to the Arctic coast for shipping to markets in Europe and Asia\n                 - An all-Canadian pipeline (\"Energy East\") that would extend to Saint John, New Brunswick for export, while also supplying Montreal, Quebec City, and Saint John refineries.',1),(22,'2014-07-22 14:29:18','2014-07-22 14:29:18',2,'Test Proposal','Test proposal summary.','Test proposal text.',1),(23,'2014-07-22 14:53:28','2014-07-22 14:53:28',3,'Test 2','test2','eaeua',1);
/*!40000 ALTER TABLE `digidemo_proposalversion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_proposalversion_tags`
--

DROP TABLE IF EXISTS `digidemo_proposalversion_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_proposalversion_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proposalversion_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `proposalversion_id` (`proposalversion_id`,`tag_id`),
  KEY `digidemo_proposalversion_tags_19f2c095` (`proposalversion_id`),
  KEY `digidemo_proposalversion_tags_5659cca2` (`tag_id`),
  CONSTRAINT `proposalversion_id_refs_id_55181f50` FOREIGN KEY (`proposalversion_id`) REFERENCES `digidemo_proposalversion` (`id`),
  CONSTRAINT `tag_id_refs_id_8710c93d` FOREIGN KEY (`tag_id`) REFERENCES `digidemo_tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_proposalversion_tags`
--

LOCK TABLES `digidemo_proposalversion_tags` WRITE;
/*!40000 ALTER TABLE `digidemo_proposalversion_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_proposalversion_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_proposalvote`
--

DROP TABLE IF EXISTS `digidemo_proposalvote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_proposalvote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
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
REPLACE INTO `digidemo_proposalvote` (`id`, `creation_date`, `last_modified`, `user_id`, `valence`, `target_id`) VALUES (1,'2014-07-13 17:04:25','2014-07-15 01:50:31',1,1,1);
/*!40000 ALTER TABLE `digidemo_proposalvote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_question`
--

DROP TABLE IF EXISTS `digidemo_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `score` smallint(6) NOT NULL,
  `title` varchar(256) NOT NULL,
  `text` longtext NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_question_6340c63c` (`user_id`),
  KEY `digidemo_question_70bfdfd1` (`target_id`),
  CONSTRAINT `user_id_refs_id_b7595eaf` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `target_id_refs_id_246dc8e3` FOREIGN KEY (`target_id`) REFERENCES `digidemo_proposal` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_question`
--

LOCK TABLES `digidemo_question` WRITE;
/*!40000 ALTER TABLE `digidemo_question` DISABLE KEYS */;
REPLACE INTO `digidemo_question` (`id`, `creation_date`, `last_modified`, `user_id`, `score`, `title`, `text`, `target_id`) VALUES (1,'2014-07-25 21:25:57','2014-07-25 21:25:57',1,0,'How likely (or frequent) can we expect spills along the pipeline extension to be?','I would like to know how likely spills are, based on the rate of previous incidents. It will probably be important to take into account the kind of piping technology used, and the kind of service. For example, repurposed piping originally for the transport of natural gas is likely to be different from newly built piping. Or, (and I\'m not sure), there may be a difference due to the fact that this is crude derived from tarsands, rather than conventional crude.',1);
/*!40000 ALTER TABLE `digidemo_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_questioncomment`
--

DROP TABLE IF EXISTS `digidemo_questioncomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_questioncomment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `score` smallint(6) NOT NULL,
  `text` varchar(512) NOT NULL,
  `question_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digidemo_questioncomment_6340c63c` (`user_id`),
  KEY `digidemo_questioncomment_25110688` (`question_id`),
  CONSTRAINT `user_id_refs_id_89b69e62` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `question_id_refs_id_91b3fcca` FOREIGN KEY (`question_id`) REFERENCES `digidemo_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_questioncomment`
--

LOCK TABLES `digidemo_questioncomment` WRITE;
/*!40000 ALTER TABLE `digidemo_questioncomment` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_questioncomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_questionvote`
--

DROP TABLE IF EXISTS `digidemo_questionvote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_questionvote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`target_id`),
  KEY `digidemo_questionvote_6340c63c` (`user_id`),
  KEY `digidemo_questionvote_70bfdfd1` (`target_id`),
  CONSTRAINT `user_id_refs_id_71f545ab` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `target_id_refs_id_5f95e94d` FOREIGN KEY (`target_id`) REFERENCES `digidemo_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_questionvote`
--

LOCK TABLES `digidemo_questionvote` WRITE;
/*!40000 ALTER TABLE `digidemo_questionvote` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_questionvote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_reply`
--

DROP TABLE IF EXISTS `digidemo_reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_reply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `discussion_id` int(11) NOT NULL,
  `body` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  `score` smallint(6) NOT NULL,
  `is_open` tinyint(1) NOT NULL,
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
REPLACE INTO `digidemo_reply` (`id`, `creation_date`, `last_modified`, `discussion_id`, `body`, `user_id`, `score`, `is_open`) VALUES (24,'2014-07-13 17:04:31','2014-07-13 17:04:31',2,'A comment.',1,0,0),(25,'2014-07-13 17:04:31','2014-07-13 17:04:31',2,'Another comment.',1,0,0),(26,'2014-07-13 17:04:31','2014-07-13 17:04:31',1,'Comment on the first discussion.',1,0,0),(27,'2014-07-13 17:04:31','2014-07-13 17:04:31',1,'AONETHTNH',1,0,0);
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `valence` smallint(6) NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`target_id`),
  KEY `digidemo_replyvote_6340c63c` (`user_id`),
  KEY `digidemo_replyvote_70bfdfd1` (`target_id`),
  CONSTRAINT `user_id_refs_id_d659ef00` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `target_id_refs_id_9f87ff39` FOREIGN KEY (`target_id`) REFERENCES `digidemo_reply` (`id`)
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
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
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
REPLACE INTO `digidemo_sector` (`id`, `creation_date`, `last_modified`, `short_name`, `name`) VALUES (1,'2014-07-13 17:04:46','2014-07-13 17:04:46','ECO','economy'),(2,'2014-07-13 17:04:46','2014-07-13 17:04:46','ENV','environment'),(3,'2014-07-13 17:04:46','2014-07-13 17:04:46','HEA','health'),(4,'2014-07-13 17:04:46','2014-07-13 17:04:46','EDU','education'),(5,'2014-07-13 17:04:46','2014-07-13 17:04:46','IR','international relations'),(6,'2014-07-13 17:04:46','2014-07-13 17:04:46','SOC','society and culture'),(7,'2014-07-13 17:04:46','2014-07-13 17:04:46','SEC','security and readiness'),(8,'2014-07-13 17:04:46','2014-07-13 17:04:46','DEM','democratic mechanisms');
/*!40000 ALTER TABLE `digidemo_sector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_tag`
--

DROP TABLE IF EXISTS `digidemo_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `name` varchar(48) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digidemo_tag`
--

LOCK TABLES `digidemo_tag` WRITE;
/*!40000 ALTER TABLE `digidemo_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `digidemo_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digidemo_userprofile`
--

DROP TABLE IF EXISTS `digidemo_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `digidemo_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
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
REPLACE INTO `digidemo_userprofile` (`id`, `creation_date`, `last_modified`, `user_id`, `email_validated`, `avatar_img`, `rep`, `street`, `zip_code`, `country`, `province`) VALUES (1,'2014-07-13 17:04:58','2014-07-17 05:54:52',1,1,'avatars/superuser.jpg',34,'Somewhere','560072','India','Karnatka'),(2,'2014-07-13 17:04:58','2014-07-15 01:52:09',2,1,'avatars/regularuser.jpg',34,'56 Long Ave.','51515','CAN','QC');
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
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
REPLACE INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'sector','digidemo','sector'),(8,'user profile','digidemo','userprofile'),(9,'tag','digidemo','tag'),(10,'proposal','digidemo','proposal'),(11,'proposal version','digidemo','proposalversion'),(12,'discussion','digidemo','discussion'),(13,'reply','digidemo','reply'),(14,'question','digidemo','question'),(15,'question comment','digidemo','questioncomment'),(16,'answer','digidemo','answer'),(17,'answer comment','digidemo','answercomment'),(18,'factor','digidemo','factor'),(19,'factor version','digidemo','factorversion'),(20,'person','digidemo','person'),(21,'organization','digidemo','organization'),(22,'position','digidemo','position'),(23,'letter','digidemo','letter'),(24,'comment','digidemo','comment'),(25,'discussion vote','digidemo','discussionvote'),(26,'proposal vote','digidemo','proposalvote'),(27,'letter vote','digidemo','lettervote'),(28,'reply vote','digidemo','replyvote'),(29,'question vote','digidemo','questionvote'),(30,'answer vote','digidemo','answervote'),(31,'comment vote','digidemo','commentvote');
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

-- Dump completed on 2014-07-27 23:57:10
