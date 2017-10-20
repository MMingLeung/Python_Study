-- MySQL dump 10.13  Distrib 5.7.19, for Win64 (x86_64)
--
-- Host: localhost    Database: project_1
-- ------------------------------------------------------
-- Server version	5.7.19

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
-- Current Database: `project_1`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `project_1` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `project_1`;

--
-- Table structure for table `app01_article`
--

DROP TABLE IF EXISTS `app01_article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_article` (
  `nid` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `summary` varchar(255) NOT NULL,
  `read_count` int(11) NOT NULL,
  `comment_count` int(11) NOT NULL,
  `up_count` int(11) NOT NULL,
  `down_count` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `article_type_id` int(11) NOT NULL,
  `blog_id` bigint(20) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`nid`),
  KEY `app01_article_blog_id_8dd74ae6_fk_app01_blog_nid` (`blog_id`),
  KEY `app01_article_category_id_acb2c466_fk_app01_category_nid` (`category_id`),
  CONSTRAINT `app01_article_blog_id_8dd74ae6_fk_app01_blog_nid` FOREIGN KEY (`blog_id`) REFERENCES `app01_blog` (`nid`),
  CONSTRAINT `app01_article_category_id_acb2c466_fk_app01_category_nid` FOREIGN KEY (`category_id`) REFERENCES `app01_category` (`nid`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_article`
--

LOCK TABLES `app01_article` WRITE;
/*!40000 ALTER TABLE `app01_article` DISABLE KEYS */;
INSERT INTO `app01_article` VALUES (1,'first/back_stage','python/back_stage',12,12,22,12,'2017-09-11 17:12:54.000000',1,1,1),(2,'first223','first summary23',12,7,16,12,'2017-08-01 17:12:54.000000',1,1,2),(3,'first3','python3',12,123,16,12,'2017-09-03 17:12:54.000000',3,1,1),(4,'first4','first 4',12,128,16,12,'2017-06-14 17:12:54.000000',3,1,2),(17,'123123','ewqeqw',0,0,1,0,'2017-09-27 06:29:31.146686',2,1,1),(18,'6666666666','666666666',0,0,0,0,'2017-09-27 09:06:53.845777',1,1,1);
/*!40000 ALTER TABLE `app01_article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_article2tag`
--

DROP TABLE IF EXISTS `app01_article2tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_article2tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` bigint(20) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app01_article2tag_article_id_tag_id_feac10bd_uniq` (`article_id`,`tag_id`),
  KEY `app01_article2tag_tag_id_d24dfcf8_fk_app01_tag_nid` (`tag_id`),
  CONSTRAINT `app01_article2tag_article_id_35c1561c_fk_app01_article_nid` FOREIGN KEY (`article_id`) REFERENCES `app01_article` (`nid`),
  CONSTRAINT `app01_article2tag_tag_id_d24dfcf8_fk_app01_tag_nid` FOREIGN KEY (`tag_id`) REFERENCES `app01_tag` (`nid`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_article2tag`
--

LOCK TABLES `app01_article2tag` WRITE;
/*!40000 ALTER TABLE `app01_article2tag` DISABLE KEYS */;
INSERT INTO `app01_article2tag` VALUES (15,1,1),(16,1,2),(17,2,1),(3,3,1),(4,4,2),(14,17,1),(18,18,2);
/*!40000 ALTER TABLE `app01_article2tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_articledetail`
--

DROP TABLE IF EXISTS `app01_articledetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_articledetail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `article_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `article_id` (`article_id`),
  CONSTRAINT `app01_articledetail_article_id_4d7e27f6_fk_app01_article_nid` FOREIGN KEY (`article_id`) REFERENCES `app01_article` (`nid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_articledetail`
--

LOCK TABLES `app01_articledetail` WRITE;
/*!40000 ALTER TABLE `app01_articledetail` DISABLE KEYS */;
INSERT INTO `app01_articledetail` VALUES (1,'详细内容',1),(2,'详细内容223',2),(4,'weqqwesdfdf',17),(5,'12312312',18);
/*!40000 ALTER TABLE `app01_articledetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_blog`
--

DROP TABLE IF EXISTS `app01_blog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_blog` (
  `nid` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `site` varchar(32) NOT NULL,
  `theme` varchar(32) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`nid`),
  UNIQUE KEY `site` (`site`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `app01_blog_user_id_f5778399_fk_app01_userinfo_nid` FOREIGN KEY (`user_id`) REFERENCES `app01_userinfo` (`nid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_blog`
--

LOCK TABLES `app01_blog` WRITE;
/*!40000 ALTER TABLE `app01_blog` DISABLE KEYS */;
INSERT INTO `app01_blog` VALUES (1,'blog_title','noah','default',1);
/*!40000 ALTER TABLE `app01_blog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_category`
--

DROP TABLE IF EXISTS `app01_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_category` (
  `nid` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  `blog_id` bigint(20) NOT NULL,
  PRIMARY KEY (`nid`),
  KEY `app01_category_blog_id_5f26cf92_fk_app01_blog_nid` (`blog_id`),
  CONSTRAINT `app01_category_blog_id_5f26cf92_fk_app01_blog_nid` FOREIGN KEY (`blog_id`) REFERENCES `app01_blog` (`nid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_category`
--

LOCK TABLES `app01_category` WRITE;
/*!40000 ALTER TABLE `app01_category` DISABLE KEYS */;
INSERT INTO `app01_category` VALUES (1,'category1',1),(2,'cate2',1);
/*!40000 ALTER TABLE `app01_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_comment`
--

DROP TABLE IF EXISTS `app01_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_comment` (
  `nid` bigint(20) NOT NULL AUTO_INCREMENT,
  `content` varchar(255) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `article_id` bigint(20) NOT NULL,
  `reply_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`nid`),
  KEY `app01_comment_article_id_2bf4f73b_fk_app01_article_nid` (`article_id`),
  KEY `app01_comment_reply_id_82e2dc98_fk_app01_comment_nid` (`reply_id`),
  KEY `app01_comment_user_id_7f913f03_fk_app01_userinfo_nid` (`user_id`),
  CONSTRAINT `app01_comment_article_id_2bf4f73b_fk_app01_article_nid` FOREIGN KEY (`article_id`) REFERENCES `app01_article` (`nid`),
  CONSTRAINT `app01_comment_reply_id_82e2dc98_fk_app01_comment_nid` FOREIGN KEY (`reply_id`) REFERENCES `app01_comment` (`nid`),
  CONSTRAINT `app01_comment_user_id_7f913f03_fk_app01_userinfo_nid` FOREIGN KEY (`user_id`) REFERENCES `app01_userinfo` (`nid`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_comment`
--

LOCK TABLES `app01_comment` WRITE;
/*!40000 ALTER TABLE `app01_comment` DISABLE KEYS */;
INSERT INTO `app01_comment` VALUES (1,'好文章','2017-09-18 21:41:21.000000',1,NULL,1),(2,'非常好','2017-09-18 21:41:46.000000',1,1,2),(3,'超级好','2017-09-18 21:42:06.000000',1,2,2),(4,'不好','2017-09-18 21:42:20.000000',1,NULL,2),(5,'为什么','2017-09-18 21:42:43.000000',1,4,1),(21,'  好111','2017-09-26 04:37:30.246267',1,NULL,1),(23,'66666666','2017-09-26 04:38:40.460283',1,3,1),(24,'没有为什么','2017-09-26 04:48:23.317621',1,5,1),(25,'666666666','2017-09-27 08:04:55.117078',1,NULL,1),(26,'ewqeqw','2017-09-27 08:05:15.637252',1,24,1),(27,'哈哈哈哈','2017-10-20 00:30:06.582004',4,NULL,1),(28,'666666666','2017-10-20 00:30:10.900251',4,27,1),(29,'77777777','2017-10-20 00:30:14.746471',4,NULL,1);
/*!40000 ALTER TABLE `app01_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_tag`
--

DROP TABLE IF EXISTS `app01_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_tag` (
  `nid` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  `blog_id` bigint(20) NOT NULL,
  PRIMARY KEY (`nid`),
  KEY `app01_tag_blog_id_ce05dc18_fk_app01_blog_nid` (`blog_id`),
  CONSTRAINT `app01_tag_blog_id_ce05dc18_fk_app01_blog_nid` FOREIGN KEY (`blog_id`) REFERENCES `app01_blog` (`nid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_tag`
--

LOCK TABLES `app01_tag` WRITE;
/*!40000 ALTER TABLE `app01_tag` DISABLE KEYS */;
INSERT INTO `app01_tag` VALUES (1,'python',1),(2,'django',1);
/*!40000 ALTER TABLE `app01_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_updown`
--

DROP TABLE IF EXISTS `app01_updown`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_updown` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `up` tinyint(1) NOT NULL,
  `article_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app01_updown_article_id_user_id_2e2043f4_uniq` (`article_id`,`user_id`),
  KEY `app01_updown_user_id_42027cf5_fk_app01_userinfo_nid` (`user_id`),
  CONSTRAINT `app01_updown_article_id_8c38d6c9_fk_app01_article_nid` FOREIGN KEY (`article_id`) REFERENCES `app01_article` (`nid`),
  CONSTRAINT `app01_updown_user_id_42027cf5_fk_app01_userinfo_nid` FOREIGN KEY (`user_id`) REFERENCES `app01_userinfo` (`nid`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_updown`
--

LOCK TABLES `app01_updown` WRITE;
/*!40000 ALTER TABLE `app01_updown` DISABLE KEYS */;
INSERT INTO `app01_updown` VALUES (8,1,1,2),(9,1,2,2),(10,1,3,2),(13,1,4,2),(14,1,1,1),(15,1,2,1),(16,1,3,1),(17,1,4,1),(27,1,1,4),(28,1,2,4),(29,1,3,4),(30,1,4,4),(31,1,17,1);
/*!40000 ALTER TABLE `app01_updown` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_userfans`
--

DROP TABLE IF EXISTS `app01_userfans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_userfans` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `follower_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app01_userfans_user_id_follower_id_e51e3214_uniq` (`user_id`,`follower_id`),
  KEY `app01_userfans_follower_id_2aab5fe5_fk_app01_userinfo_nid` (`follower_id`),
  CONSTRAINT `app01_userfans_follower_id_2aab5fe5_fk_app01_userinfo_nid` FOREIGN KEY (`follower_id`) REFERENCES `app01_userinfo` (`nid`),
  CONSTRAINT `app01_userfans_user_id_f4c29059_fk_app01_userinfo_nid` FOREIGN KEY (`user_id`) REFERENCES `app01_userinfo` (`nid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_userfans`
--

LOCK TABLES `app01_userfans` WRITE;
/*!40000 ALTER TABLE `app01_userfans` DISABLE KEYS */;
INSERT INTO `app01_userfans` VALUES (1,2,1),(2,3,1),(3,1,2),(4,1,3);
/*!40000 ALTER TABLE `app01_userfans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_userinfo`
--

DROP TABLE IF EXISTS `app01_userinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_userinfo` (
  `nid` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) NOT NULL,
  `password` varchar(64) NOT NULL,
  `nickname` varchar(32) NOT NULL,
  `email` varchar(254) NOT NULL,
  `avatar` varchar(100) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  PRIMARY KEY (`nid`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_userinfo`
--

LOCK TABLES `app01_userinfo` WRITE;
/*!40000 ALTER TABLE `app01_userinfo` DISABLE KEYS */;
INSERT INTO `app01_userinfo` VALUES (1,'Noah','123','Noah','Noah@gmail.com','/static/img/default_img.jpg','2017-09-15 15:40:42.000000'),(2,'Mia','123','Mia','Mia@gmail.com','/static/img/default_img.jpg','2017-09-13 14:07:29.076813'),(3,'Isabella','123','Isabella','Isabella@gmail.com','/static/img/default_img.jpg','2017-09-25 19:11:19.000000'),(4,'Cooper','123','Cooper','Cooper@gmail.com','/static/img/default_img.jpg','2017-09-26 09:30:17.207040'),(5,'ken','123','ken','ken@gmail.com','/static/img/default_img.jpg','2017-09-27 08:28:15.835195'),(6,'asdsadasd','12345','asdsadasd','wqeqwdqw@gmail.com','QQ图片20170827210306_副本.jpg','2017-10-19 09:14:35.775194'),(7,'bbbbbbbbbbbbb','12345','bbbbbbbbbbbbb','bbbbbbbbbbbbb@gmail.com','QQ图片20170827210306_副本_nhSbcQO.jpg','2017-10-19 09:18:32.277721'),(8,'bbbbbbbbbbbbbb','12345','qwewqe','wdqdqw@gmail.com','2.jpg','2017-10-19 11:57:50.339932');
/*!40000 ALTER TABLE `app01_userinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app02_action`
--

DROP TABLE IF EXISTS `app02_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app02_action` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `caption` varchar(32) NOT NULL,
  `code` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app02_action`
--

LOCK TABLES `app02_action` WRITE;
/*!40000 ALTER TABLE `app02_action` DISABLE KEYS */;
INSERT INTO `app02_action` VALUES (1,' 查看','get'),(2,'添加','post'),(3,'删除','del'),(4,'修改','edit');
/*!40000 ALTER TABLE `app02_action` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app02_menu`
--

DROP TABLE IF EXISTS `app02_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app02_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `caption` varchar(32) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app02_menu_parent_id_ed0f1419_fk_app02_menu_id` (`parent_id`),
  CONSTRAINT `app02_menu_parent_id_ed0f1419_fk_app02_menu_id` FOREIGN KEY (`parent_id`) REFERENCES `app02_menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app02_menu`
--

LOCK TABLES `app02_menu` WRITE;
/*!40000 ALTER TABLE `app02_menu` DISABLE KEYS */;
INSERT INTO `app02_menu` VALUES (1,'菜单1',NULL),(2,'菜单2',NULL),(3,'菜单3',NULL),(4,'菜单1-1',1),(5,'菜单1-2',1),(6,'菜单2-1',2),(7,'菜单1-1-1',4);
/*!40000 ALTER TABLE `app02_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app02_permission`
--

DROP TABLE IF EXISTS `app02_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app02_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `caption` varchar(32) NOT NULL,
  `url` varchar(128) NOT NULL,
  `menu_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app02_permission_menu_id_0346ab16_fk_app02_menu_id` (`menu_id`),
  CONSTRAINT `app02_permission_menu_id_0346ab16_fk_app02_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `app02_menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app02_permission`
--

LOCK TABLES `app02_permission` WRITE;
/*!40000 ALTER TABLE `app02_permission` DISABLE KEYS */;
INSERT INTO `app02_permission` VALUES (1,'用户管理','/users.html',3),(2,'订单管理','/orders.html',3),(3,'博客管理','/blogs.html',1),(4,'人员管理','/staff.html',7);
/*!40000 ALTER TABLE `app02_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app02_permission2action2role`
--

DROP TABLE IF EXISTS `app02_permission2action2role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app02_permission2action2role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app02_permission2action2_permission_id_action_id__23462ae3_uniq` (`permission_id`,`action_id`,`role_id`),
  KEY `app02_permission2act_action_id_423019b2_fk_app02_act` (`action_id`),
  KEY `app02_permission2action2role_role_id_02075621_fk_app02_role_id` (`role_id`),
  CONSTRAINT `app02_permission2act_action_id_423019b2_fk_app02_act` FOREIGN KEY (`action_id`) REFERENCES `app02_action` (`id`),
  CONSTRAINT `app02_permission2act_permission_id_7855b749_fk_app02_per` FOREIGN KEY (`permission_id`) REFERENCES `app02_permission` (`id`),
  CONSTRAINT `app02_permission2action2role_role_id_02075621_fk_app02_role_id` FOREIGN KEY (`role_id`) REFERENCES `app02_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app02_permission2action2role`
--

LOCK TABLES `app02_permission2action2role` WRITE;
/*!40000 ALTER TABLE `app02_permission2action2role` DISABLE KEYS */;
INSERT INTO `app02_permission2action2role` VALUES (8,1,1,2),(1,1,1,3),(9,2,1,2),(2,2,1,3),(4,3,1,4),(3,4,1,4),(7,1,2,3),(5,1,3,3),(6,1,4,4);
/*!40000 ALTER TABLE `app02_permission2action2role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app02_role`
--

DROP TABLE IF EXISTS `app02_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app02_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `caption` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app02_role`
--

LOCK TABLES `app02_role` WRITE;
/*!40000 ALTER TABLE `app02_role` DISABLE KEYS */;
INSERT INTO `app02_role` VALUES (1,'R & D department'),(2,'Marketing Department'),(3,'sales department'),(4,'Sales Manager');
/*!40000 ALTER TABLE `app02_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app02_user`
--

DROP TABLE IF EXISTS `app02_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app02_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) NOT NULL,
  `password` varchar(64) NOT NULL,
  `email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app02_user`
--

LOCK TABLES `app02_user` WRITE;
/*!40000 ALTER TABLE `app02_user` DISABLE KEYS */;
INSERT INTO `app02_user` VALUES (1,'Noah','123','noah@gmail'),(2,'Liam','123','liam@gmail.com'),(3,'William','123','william@gmail.com'),(4,'Mia','123','mia@gmail.com');
/*!40000 ALTER TABLE `app02_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app02_user2role`
--

DROP TABLE IF EXISTS `app02_user2role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app02_user2role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app02_user2role_role_id_73906b0b_fk_app02_role_id` (`role_id`),
  KEY `app02_user2role_user_id_4d256310_fk_app02_user_id` (`user_id`),
  CONSTRAINT `app02_user2role_role_id_73906b0b_fk_app02_role_id` FOREIGN KEY (`role_id`) REFERENCES `app02_role` (`id`),
  CONSTRAINT `app02_user2role_user_id_4d256310_fk_app02_user_id` FOREIGN KEY (`user_id`) REFERENCES `app02_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app02_user2role`
--

LOCK TABLES `app02_user2role` WRITE;
/*!40000 ALTER TABLE `app02_user2role` DISABLE KEYS */;
INSERT INTO `app02_user2role` VALUES (1,1,1),(2,2,2),(3,3,3),(4,4,4),(5,3,4);
/*!40000 ALTER TABLE `app02_user2role` ENABLE KEYS */;
UNLOCK TABLES;

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
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
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
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add permission',4,'add_permission'),(11,'Can change permission',4,'change_permission'),(12,'Can delete permission',4,'delete_permission'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add user fans',7,'add_userfans'),(20,'Can change user fans',7,'change_userfans'),(21,'Can delete user fans',7,'delete_userfans'),(22,'Can add article',8,'add_article'),(23,'Can change article',8,'change_article'),(24,'Can delete article',8,'delete_article'),(25,'Can add category',9,'add_category'),(26,'Can change category',9,'change_category'),(27,'Can delete category',9,'delete_category'),(28,'Can add article detail',10,'add_articledetail'),(29,'Can change article detail',10,'change_articledetail'),(30,'Can delete article detail',10,'delete_articledetail'),(31,'Can add article2 tag',11,'add_article2tag'),(32,'Can change article2 tag',11,'change_article2tag'),(33,'Can delete article2 tag',11,'delete_article2tag'),(34,'Can add comment',12,'add_comment'),(35,'Can change comment',12,'change_comment'),(36,'Can delete comment',12,'delete_comment'),(37,'Can add user info',13,'add_userinfo'),(38,'Can change user info',13,'change_userinfo'),(39,'Can delete user info',13,'delete_userinfo'),(40,'Can add blog',14,'add_blog'),(41,'Can change blog',14,'change_blog'),(42,'Can delete blog',14,'delete_blog'),(43,'Can add tag',15,'add_tag'),(44,'Can change tag',15,'change_tag'),(45,'Can delete tag',15,'delete_tag'),(46,'Can add up down',16,'add_updown'),(47,'Can change up down',16,'change_updown'),(48,'Can delete up down',16,'delete_updown'),(49,'Can add user',17,'add_user'),(50,'Can change user',17,'change_user'),(51,'Can delete user',17,'delete_user'),(52,'Can add role',18,'add_role'),(53,'Can change role',18,'change_role'),(54,'Can delete role',18,'delete_role'),(55,'Can add user2 role',19,'add_user2role'),(56,'Can change user2 role',19,'change_user2role'),(57,'Can delete user2 role',19,'delete_user2role'),(58,'Can add menu',20,'add_menu'),(59,'Can change menu',20,'change_menu'),(60,'Can delete menu',20,'delete_menu'),(61,'Can add permission',21,'add_permission'),(62,'Can change permission',21,'change_permission'),(63,'Can delete permission',21,'delete_permission'),(64,'Can add action',22,'add_action'),(65,'Can change action',22,'change_action'),(66,'Can delete action',22,'delete_action'),(67,'Can add permission2 action2 role',23,'add_permission2action2role'),(68,'Can change permission2 action2 role',23,'change_permission2action2role'),(69,'Can delete permission2 action2 role',23,'delete_permission2action2role');
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
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$36000$eNzhyKr2GRrl$i1GDvIts29cCQl3K9ksUCHdqq9tD/M8cmz5P6C/sQGg=','2017-09-18 06:11:19.657073',1,'root','','','',1,1,'2017-09-18 06:11:01.574073');
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
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
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
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
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
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
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
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(8,'app01','article'),(11,'app01','article2tag'),(10,'app01','articledetail'),(14,'app01','blog'),(9,'app01','category'),(12,'app01','comment'),(15,'app01','tag'),(16,'app01','updown'),(7,'app01','userfans'),(13,'app01','userinfo'),(22,'app02','action'),(20,'app02','menu'),(21,'app02','permission'),(23,'app02','permission2action2role'),(18,'app02','role'),(17,'app02','user'),(19,'app02','user2role'),(2,'auth','group'),(4,'auth','permission'),(3,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-09-12 02:17:37.508438'),(2,'auth','0001_initial','2017-09-12 02:17:56.299112'),(3,'admin','0001_initial','2017-09-12 02:18:00.954378'),(4,'admin','0002_logentry_remove_auto_add','2017-09-12 02:18:01.066384'),(5,'app01','0001_initial','2017-09-12 02:18:45.932951'),(6,'contenttypes','0002_remove_content_type_name','2017-09-12 02:18:48.349089'),(7,'auth','0002_alter_permission_name_max_length','2017-09-12 02:18:50.203195'),(8,'auth','0003_alter_user_email_max_length','2017-09-12 02:18:52.015298'),(9,'auth','0004_alter_user_username_opts','2017-09-12 02:18:52.088303'),(10,'auth','0005_alter_user_last_login_null','2017-09-12 02:18:53.258370'),(11,'auth','0006_require_contenttypes_0002','2017-09-12 02:18:53.417379'),(12,'auth','0007_alter_validators_add_error_messages','2017-09-12 02:18:53.490383'),(13,'auth','0008_alter_user_username_max_length','2017-09-12 02:18:55.120476'),(14,'sessions','0001_initial','2017-09-12 02:18:56.270542'),(15,'app02','0001_initial','2017-09-20 03:51:36.509893');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
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
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1ia8esybugsoetpgb2db859ha5oxskwz','ODgxMjk5MmU4NzI1YjJlNWQzZjJiNTE2MjAyM2Q2MGFkZmI4MmY3Mzp7InVzZXJfaW5mbyI6Ik5vYWgiLCJ1c2VyX2lkIjoxLCJjb2RlIjoiUyJ9','2017-10-09 09:35:49.035779'),('3pbkl27kdvjkxjddsvo5lp5euxslhxzz','NWY4MjNjZWQ1NTgzNjRhMDYwN2FjOWJiYzg2NmIxMjBhNzMwZjRhYzp7ImxvZ2luX3VzZXJfaW5mb19zZXNzaW9uX2tleSI6eyJ1c2VyX2lkX3Nlc3Npb24iOjEsInVzZXJfbmFtZV9zZXNzaW9uIjoiTm9haCJ9LCJjb2RlIjoiSSJ9','2017-10-23 14:22:59.784688'),('3pnurp64n0mgelo1v8bpmvhlhgt7z3dh','YWVlMGI3ZTc5YTEwOTQ3MDk1ZWIwZDg2NzIzZmQ5YWI4YWY1OTdiNTp7ImNvZGUiOiJLIiwidXNlcl9pZCI6MSwidXNlcl9pbmZvIjoiTm9haCJ9','2017-10-10 01:49:19.823745'),('4ey63z7k2hxyjwetmclwbxw9889pd1ci','NmI0ZDcxNjIxZTYzZjJiZDkwZDNlODUzYmM1NTkyZTBlOWJmY2NiMzp7ImNvZGUiOiJFIiwibG9naW5fdXNlcl9pbmZvX3Nlc3Npb25fa2V5Ijp7InVzZXJfbmFtZV9zZXNzaW9uIjoiTm9haCIsInVzZXJfaWRfc2Vzc2lvbiI6MX19','2017-10-11 03:26:39.437140'),('6w53gsztiekh0sk6xmkbtd4pnlp19hfw','ZTc1NDg3NWM1ZDZlN2MzMjgxMGIyZjBmODYzZTFkYTNmYjlkMTEwNzp7ImNvZGUiOiJNIn0=','2017-11-02 11:57:23.025370'),('71dhbjwkwb5f33au3tgienfosj1oalsp','OWVmZWVhODk2MzQ1MjM2M2QwMGFmYTUzMzllNDVmNDExMWUwZDRlNjp7ImNvZGUiOiJMIn0=','2017-11-01 14:28:48.812178'),('928i78r3zjbwop3hcc287yu310xgdx86','ZGJlY2ViNDllNmQyNjRiZjY3MTBkOTdlM2NhYTJjMWQ4YTI5NWQzNTp7ImxvZ2luX3VzZXJfaW5mb19zZXNzaW9uX2tleSI6eyJ1c2VyX25hbWVfc2Vzc2lvbiI6Ik5vYWgiLCJ1c2VyX2lkX3Nlc3Npb24iOjF9LCJjb2RlIjoiRSJ9','2017-10-11 02:13:04.142599'),('a273ogbo6ojf61iuth4nzq36565u23hk','NDAyYzYzZThkNTRlYmQ3YjJjOWMxMTQ4YWQ1MDg1ZTg0OWQ4ZGFmNzp7ImNvZGUiOiJHIn0=','2017-11-02 09:18:06.060221'),('a2hur30ihjav90h6bb1nim0guc0zzk9y','ZjVmODc3MzMzNjkzNjcxOWZjZWZlOTYyZDRkMmRlYTc1MTUzY2JhODp7ImxvZ2luX3VzZXJfaW5mb19zZXNzaW9uX2tleSI6eyJ1c2VyX2lkX3Nlc3Npb24iOjEsInVzZXJfbmFtZV9zZXNzaW9uIjoiTm9haCJ9LCJjb2RlIjoiTiJ9','2017-11-01 12:56:50.544250'),('dz9okc0fqvzfyahnxihsk90b2j64zg0q','YTEzOTk5N2NjYTg1MTVlYzQ4OWRkOWZmMjI1N2NkNWU4ZmQ0NDUzOTp7ImNvZGUiOiJaIiwibG9naW5fdXNlcl9pbmZvX3Nlc3Npb25fa2V5Ijp7InVzZXJfbmFtZV9zZXNzaW9uIjoiTm9haCIsInVzZXJfaWRfc2Vzc2lvbiI6MX19','2017-11-01 10:01:55.130667'),('elw5vgym4571emz0sov9hrlwsotwb7t8','MDBhMTBmNTVhYzA2ZDYwYTc4NTI1YzQ1ZGU0NjVkMmM1YmI1MWFhMDp7InVzZXJfaW5mbyI6Ik5vYWgiLCJ1c2VyX2lkIjoxLCJjb2RlIjoiRCJ9','2017-10-09 01:18:56.457868'),('forsh7k95k8xslqj4jd4c7akidtxjwop','NGY1NzlkZDQ4MTNjNDFmZjUxODE1OWQ1ODI5Mjg1OWE5YWQ3ODY4OTp7ImxvZ2luX3VzZXJfaW5mb19zZXNzaW9uX2tleSI6eyJ1c2VyX2lkX3Nlc3Npb24iOjEsInVzZXJfbmFtZV9zZXNzaW9uIjoiTm9haCJ9LCJjb2RlIjoiUyJ9','2017-11-01 10:41:27.399314'),('gvmfc6636l8h5z2br9324nvy4bii4022','YzE5Y2QzZGE4ZTAzY2ZmYWE2NzIyNjM1NmU5ZTQxZmQ0ZjYxOTU5ZDp7ImNvZGUiOiJCIiwibG9naW5fdXNlcl9pbmZvX3Nlc3Npb25fa2V5Ijp7InVzZXJfbmFtZV9zZXNzaW9uIjoiTm9haCIsInVzZXJfaWRfc2Vzc2lvbiI6MX19','2017-10-10 14:26:01.023928'),('h73h0gsz5cu2uz8lls81l2fdq12ih6av','ODgxMjk5MmU4NzI1YjJlNWQzZjJiNTE2MjAyM2Q2MGFkZmI4MmY3Mzp7InVzZXJfaW5mbyI6Ik5vYWgiLCJ1c2VyX2lkIjoxLCJjb2RlIjoiUyJ9','2017-10-09 10:59:53.067000'),('jicsyvd9tjopzlh5xrjffrrdc5cn2gim','MTBmMTQ1ZDAxM2MzZWZmNDJjZTdhMjFlMzAyYzFmYmEwODg3MjhkYTp7ImNvZGUiOiJWIiwibG9naW5fdXNlcl9pbmZvX3Nlc3Npb25fa2V5Ijp7InVzZXJfbmFtZV9zZXNzaW9uIjoiTm9haCIsInVzZXJfaWRfc2Vzc2lvbiI6MX19','2017-10-11 01:57:38.001627'),('jn51jcjzluun7omubp6b858zwo3qmv2y','NDM2MjNjNjI4ZTk5NDM1OTJkNDZjMjgxZjRlMzRlNDYwYTMzOWU4Njp7InVzZXJfaW5mbyI6Ik5vYWgiLCJ1c2VyX2lkIjoxLCJjb2RlIjoiUSJ9','2017-10-09 14:08:41.286735'),('jwxphk1m2a8wfkyr4lz2n8cuv6w0yhx4','NDJiZjllYjg2M2EyMjAyMTI3ZTRkY2ZlOTYwMDczYWVmOTc2MjA1Yjp7ImxvZ2luX3VzZXJfaW5mb19zZXNzaW9uX2tleSI6eyJ1c2VyX25hbWVfc2Vzc2lvbiI6Ik5vYWgiLCJ1c2VyX2lkX3Nlc3Npb24iOjF9LCJjb2RlIjoiUyJ9','2017-10-10 12:37:08.669299'),('kfhsyispdcgfxq5u1tbqjhawx6scueai','ODVmM2VmODRiZjNjYTdhNDM5YWFmNjMyMGY2NTNiMGFjZDkzM2I4ZDp7InVzZXJfaW5mbyI6Ik5vYWgiLCJ1c2VyX2lkIjoxLCJjb2RlIjoiRSJ9','2017-10-04 16:11:31.571943'),('lkjlrh7aatehggeo4vcy2c0rjgphuh0w','NGY1NzlkZDQ4MTNjNDFmZjUxODE1OWQ1ODI5Mjg1OWE5YWQ3ODY4OTp7ImxvZ2luX3VzZXJfaW5mb19zZXNzaW9uX2tleSI6eyJ1c2VyX2lkX3Nlc3Npb24iOjEsInVzZXJfbmFtZV9zZXNzaW9uIjoiTm9haCJ9LCJjb2RlIjoiUyJ9','2017-11-01 13:54:53.220999'),('m74vnc158mns5sqa008ckrwmuk6h5ull','ZTc1NDg3NWM1ZDZlN2MzMjgxMGIyZjBmODYzZTFkYTNmYjlkMTEwNzp7ImNvZGUiOiJNIn0=','2017-11-02 11:57:26.097545'),('n95cxm0b5lpipfbpiac7fsqq4iqmtesc','YjcwMjZiZWJmNDkyMTIzMTllMTdiMTFlYTg4NjQwOTBjMDY3MDBjMzp7ImNvZGUiOiJHIiwibG9naW5fdXNlcl9pbmZvX3Nlc3Npb25fa2V5Ijp7InVzZXJfaWRfc2Vzc2lvbiI6MSwidXNlcl9uYW1lX3Nlc3Npb24iOiJOb2FoIn19','2017-11-03 00:29:46.417851'),('ojux9aukfsg7652qy435c4qm06o2k0vc','ZGYzM2ZlZGYzYWEzZTNjMGNmODliYzE0YTM1YmRjYmNkOGM0OWIzNTp7InVzZXJfaWQiOjIsImNvZGUiOiJCIiwidXNlcl9pbmZvIjoiTWlhIiwidXNlcl9wZXJtaXNzaW9uX2RpY3QiOnsiL2Jsb2dzLmh0bWwiOlsiZ2V0Il0sIi9pbmRleC5odG1sIjpbImdldCJdLCIvdXNlcnMuaHRtbCI6WyJnZXQiLCJwb3N0IiwiZGVsIiwiZWRpdCJdLCIvYXV0aC1pbmRleC5odG1sIjpbImdldCJdfX0=','2017-10-04 07:20:37.404989'),('pgcpqt1lzabhph6kd3a8jc7ge6a7pof2','MjQ3YmZjNzFhNTY4ZmJmYjA3Y2JkNjM3Mjg1ZmVkYWI0ZDI2M2YwMDp7ImNvZGUiOiJaIn0=','2017-10-29 07:13:11.961124'),('pomzlujzcudx6ji107dt36yehzozarcu','YTJkYjZhYzM4MDZkYTNmMGRlMjczZjhjNWRlMGZhNzc1ZjJhYjRkYTp7ImNvZGUiOiJCIn0=','2017-11-02 09:37:28.133873'),('qia5lx2c5qg4r5gmwrywuvh5c19oh92m','ZWZjMjIzNjVjOWQ5YTcwNjcyZDE3MTBmYjcwZGJkYjAzMDg3ODM5Njp7ImxvZ2luX3VzZXJfaW5mb19zZXNzaW9uX2tleSI6eyJ1c2VyX2lkX3Nlc3Npb24iOjEsInVzZXJfbmFtZV9zZXNzaW9uIjoiTm9haCJ9LCJjb2RlIjoiRyJ9','2017-10-23 14:09:59.877812'),('t2tvtsfdfv00nwl7lrugvxi53lkxl89p','YzUyM2Q5ZTU1Y2QzMTBiOTY2MjAxNTY3OTdjNzJhNjRjNTJhZjU3Njp7ImNvZGUiOiJEIn0=','2017-11-02 09:14:15.290022'),('tqjh4bqbjhsxpc4uxkf0pz7qd8u8hq82','OGQwOWJmNDllMzE5MDcyZjQ3NWY5YTQ1ZTU2OTk2NjJmNDZhNjBiZTp7ImxvZ2luX3VzZXJfaW5mb19zZXNzaW9uX2tleSI6eyJ1c2VyX25hbWVfc2Vzc2lvbiI6Ik5vYWgiLCJ1c2VyX2lkX3Nlc3Npb24iOjF9LCJjb2RlIjoiWCJ9','2017-10-10 11:57:54.820667'),('uj1i2vb1rn6erbxreyevuj1j0w8a3tpt','OGMxMmM1NmJlMDJkZjAxZTU3NTEwMGIwYTE3YWU5ZDkwM2I5MDZlMDp7ImxvZ2luX3VzZXJfaW5mb19zZXNzaW9uX2tleSI6eyJ1c2VyX25hbWVfc2Vzc2lvbiI6Ik5vYWgiLCJ1c2VyX2lkX3Nlc3Npb24iOjF9LCJjb2RlIjoiUiJ9','2017-10-22 11:47:15.298723'),('vmn8bsd1rfd85uq1bld3apaebvy9nri8','ODM0MzllYjkzYWUyM2E1YmRiZTNjMjNlYzkwMWYxMGViYjJhOWQzNTp7InVzZXJfcGVybWlzc2lvbl9kaWN0Ijp7Ii9hdXRoLWluZGV4Lmh0bWwiOlsiZ2V0Il0sIi9ibG9ncy5odG1sIjpbImdldCJdLCIvaW5kZXguaHRtbCI6WyJnZXQiXSwiL3VzZXJzLmh0bWwiOlsiZ2V0IiwicG9zdCIsImRlbCIsImVkaXQiXX0sImNvZGUiOiJVIn0=','2017-10-06 08:43:10.790414'),('y8zl4lpub5decvxpn5rz5bp0g3fc9aw9','YTI5NzFiYjczMGYzYzRkYmYwZjU3OWNhNGIzYzhjNTAxMTEzNTMxMTp7ImxvZ2luX3VzZXJfaW5mb19zZXNzaW9uX2tleSI6eyJ1c2VyX25hbWVfc2Vzc2lvbiI6Ik5vYWgiLCJ1c2VyX2lkX3Nlc3Npb24iOjF9LCJjb2RlIjoiRiJ9','2017-10-27 10:15:39.920010');
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

-- Dump completed on 2017-10-20  9:12:00
