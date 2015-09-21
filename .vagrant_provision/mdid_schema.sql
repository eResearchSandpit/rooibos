-- MySQL dump 10.13  Distrib 5.5.44, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: rooibos
-- ------------------------------------------------------
-- Server version	5.5.44-0ubuntu0.14.04.1

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
-- Table structure for table `access_accesscontrol`
--

DROP TABLE IF EXISTS `access_accesscontrol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `access_accesscontrol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(10) unsigned NOT NULL,
  `read` tinyint(1) DEFAULT NULL,
  `write` tinyint(1) DEFAULT NULL,
  `manage` tinyint(1) DEFAULT NULL,
  `restrictions_repr` longtext NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `usergroup_id` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `access_accesscontrol_content_type_id_71f41e406fa33cb5_uniq` (`content_type_id`,`object_id`,`user_id`,`usergroup_id`),
  KEY `access_accesscontrol_user_id_6856869a80c7ab7_fk_auth_user_id` (`user_id`),
  KEY `access_accesscontrol_af31437c` (`object_id`),
  KEY `access_accesscontrol_50ce08ac` (`usergroup_id`),
  CONSTRAINT `access_accesscont_usergroup_id_2fc40262fdffed4d_fk_auth_group_id` FOREIGN KEY (`usergroup_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `access_accesscontrol_user_id_6856869a80c7ab7_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `acces_content_type_id_22782a5686a502da_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `access_attribute`
--

DROP TABLE IF EXISTS `access_attribute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `access_attribute` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attribute` varchar(255) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `access_attribute_0e939a4f` (`group_id`),
  CONSTRAINT `a_group_id_45772b8872b59061_fk_access_extendedgroup_group_ptr_id` FOREIGN KEY (`group_id`) REFERENCES `access_extendedgroup` (`group_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `access_attributevalue`
--

DROP TABLE IF EXISTS `access_attributevalue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `access_attributevalue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) NOT NULL,
  `attribute_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `access_attr_attribute_id_57d39d8cf3f18cf4_fk_access_attribute_id` (`attribute_id`),
  CONSTRAINT `access_attr_attribute_id_57d39d8cf3f18cf4_fk_access_attribute_id` FOREIGN KEY (`attribute_id`) REFERENCES `access_attribute` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `access_extendedgroup`
--

DROP TABLE IF EXISTS `access_extendedgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `access_extendedgroup` (
  `group_ptr_id` int(11) NOT NULL,
  `type` varchar(1) NOT NULL,
  PRIMARY KEY (`group_ptr_id`),
  CONSTRAINT `access_extendedgr_group_ptr_id_647c31381949fea6_fk_auth_group_id` FOREIGN KEY (`group_ptr_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `access_subnet`
--

DROP TABLE IF EXISTS `access_subnet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `access_subnet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subnet` varchar(80) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `a_group_id_264d71696d6f8767_fk_access_extendedgroup_group_ptr_id` (`group_id`),
  CONSTRAINT `a_group_id_264d71696d6f8767_fk_access_extendedgroup_group_ptr_id` FOREIGN KEY (`group_id`) REFERENCES `access_extendedgroup` (`group_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  KEY `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  KEY `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_collection`
--

DROP TABLE IF EXISTS `data_collection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_collection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `description` longtext NOT NULL,
  `agreement` longtext,
  `password` varchar(32) NOT NULL,
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `data_collection_owner_id_30038080f9b75ada_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `data_collection_owner_id_30038080f9b75ada_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_collection_children`
--

DROP TABLE IF EXISTS `data_collection_children`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_collection_children` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_collection_id` int(11) NOT NULL,
  `to_collection_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `from_collection_id` (`from_collection_id`,`to_collection_id`),
  KEY `data_coll_to_collection_id_fc3fcf1f2dab556_fk_data_collection_id` (`to_collection_id`),
  CONSTRAINT `data_coll_to_collection_id_fc3fcf1f2dab556_fk_data_collection_id` FOREIGN KEY (`to_collection_id`) REFERENCES `data_collection` (`id`),
  CONSTRAINT `data_c_from_collection_id_446e540dcca5004b_fk_data_collection_id` FOREIGN KEY (`from_collection_id`) REFERENCES `data_collection` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_collectionitem`
--

DROP TABLE IF EXISTS `data_collectionitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_collectionitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hidden` tinyint(1) NOT NULL,
  `collection_id` int(11) NOT NULL,
  `record_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `data_collec_collection_id_39e42c26b5d3eaf9_fk_data_collection_id` (`collection_id`),
  KEY `data_collectionitem_5ca316a7` (`record_id`),
  CONSTRAINT `data_collectionitem_record_id_2c52e06c47bf7b0a_fk_data_record_id` FOREIGN KEY (`record_id`) REFERENCES `data_record` (`id`),
  CONSTRAINT `data_collec_collection_id_39e42c26b5d3eaf9_fk_data_collection_id` FOREIGN KEY (`collection_id`) REFERENCES `data_collection` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_displayfieldvalue`
--

DROP TABLE IF EXISTS `data_displayfieldvalue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_displayfieldvalue` (
  `fieldvalue_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`fieldvalue_ptr_id`),
  CONSTRAINT `data_di_fieldvalue_ptr_id_7cd026e128907522_fk_data_fieldvalue_id` FOREIGN KEY (`fieldvalue_ptr_id`) REFERENCES `data_fieldvalue` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_field`
--

DROP TABLE IF EXISTS `data_field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_field` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `old_name` varchar(100) DEFAULT NULL,
  `standard_id` int(11),
  `vocabulary_id` int(11),
  `_order` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `data_field_name_63227624106dee4c_uniq` (`name`,`standard_id`),
  KEY `data_field_b068931c` (`name`),
  KEY `data_field_a5836404` (`standard_id`),
  KEY `data_field_79df6276` (`vocabulary_id`),
  CONSTRAINT `data_field_vocabulary_id_33b163d02639cbb9_fk_data_vocabulary_id` FOREIGN KEY (`vocabulary_id`) REFERENCES `data_vocabulary` (`id`),
  CONSTRAINT `data_fi_standard_id_53d3515c78a75f96_fk_data_metadatastandard_id` FOREIGN KEY (`standard_id`) REFERENCES `data_metadatastandard` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_field_equivalent`
--

DROP TABLE IF EXISTS `data_field_equivalent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_field_equivalent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_field_id` int(11) NOT NULL,
  `to_field_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `from_field_id` (`from_field_id`,`to_field_id`),
  KEY `data_field_equival_to_field_id_53779bed86873697_fk_data_field_id` (`to_field_id`),
  CONSTRAINT `data_field_equival_to_field_id_53779bed86873697_fk_data_field_id` FOREIGN KEY (`to_field_id`) REFERENCES `data_field` (`id`),
  CONSTRAINT `data_field_equiv_from_field_id_2c95be9fb70a0e8c_fk_data_field_id` FOREIGN KEY (`from_field_id`) REFERENCES `data_field` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_fieldsetfield`
--

DROP TABLE IF EXISTS `data_fieldsetfield`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_fieldsetfield` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(100) DEFAULT NULL,
  `order` int(11) NOT NULL,
  `importance` smallint(6) NOT NULL,
  `field_id` int(11) NOT NULL,
  `fieldset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `data_fieldsetfield_field_id_4f547eb336b94738_fk_data_field_id` (`field_id`),
  KEY `data_fieldse_fieldset_id_7cf8a4021a8c2ca3_fk_rooibos_fieldset_id` (`fieldset_id`),
  CONSTRAINT `data_fieldse_fieldset_id_7cf8a4021a8c2ca3_fk_rooibos_fieldset_id` FOREIGN KEY (`fieldset_id`) REFERENCES `rooibos_fieldset` (`id`),
  CONSTRAINT `data_fieldsetfield_field_id_4f547eb336b94738_fk_data_field_id` FOREIGN KEY (`field_id`) REFERENCES `data_field` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_fieldvalue`
--

DROP TABLE IF EXISTS `data_fieldvalue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_fieldvalue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `refinement` varchar(100) DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  `hidden` tinyint(1) NOT NULL,
  `order` int(11) NOT NULL,
  `group` int(11) DEFAULT NULL,
  `value` longtext NOT NULL,
  `index_value` varchar(32) NOT NULL,
  `date_start` decimal(12,0) DEFAULT NULL,
  `date_end` decimal(12,0) DEFAULT NULL,
  `numeric_value` decimal(18,4) DEFAULT NULL,
  `language` varchar(5) DEFAULT NULL,
  `context_id` int(10) unsigned DEFAULT NULL,
  `context_type_id` int(11),
  `field_id` int(11) NOT NULL,
  `owner_id` int(11),
  `record_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `data_fieldvalue_3d84dde3` (`index_value`),
  KEY `data_fieldvalue_e6a04869` (`context_type_id`),
  KEY `data_fieldvalue_3aabf39f` (`field_id`),
  KEY `data_fieldvalue_5e7b1936` (`owner_id`),
  KEY `data_fieldvalue_5ca316a7` (`record_id`),
  CONSTRAINT `data_fieldvalue_record_id_5de644e800500608_fk_data_record_id` FOREIGN KEY (`record_id`) REFERENCES `data_record` (`id`),
  CONSTRAINT `data_fieldvalue_field_id_5a0fb66e05be5234_fk_data_field_id` FOREIGN KEY (`field_id`) REFERENCES `data_field` (`id`),
  CONSTRAINT `data_fieldvalue_owner_id_3de438d7e98e3c67_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `data__context_type_id_3cbdffe7700ead25_fk_django_content_type_id` FOREIGN KEY (`context_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_metadatastandard`
--

DROP TABLE IF EXISTS `data_metadatastandard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_metadatastandard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `prefix` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `prefix` (`prefix`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_record`
--

DROP TABLE IF EXISTS `data_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `name` varchar(50) NOT NULL,
  `source` varchar(1024) DEFAULT NULL,
  `manager` varchar(50) DEFAULT NULL,
  `next_update` datetime DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `data_record_owner_id_44b792df0f263553_fk_auth_user_id` (`owner_id`),
  KEY `data_record_parent_id_7858b066a06fda7f_fk_data_record_id` (`parent_id`),
  CONSTRAINT `data_record_parent_id_7858b066a06fda7f_fk_data_record_id` FOREIGN KEY (`parent_id`) REFERENCES `data_record` (`id`),
  CONSTRAINT `data_record_owner_id_44b792df0f263553_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_vocabulary`
--

DROP TABLE IF EXISTS `data_vocabulary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_vocabulary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` longtext,
  `standard` tinyint(1) DEFAULT NULL,
  `origin` longtext,
  PRIMARY KEY (`id`),
  KEY `data_vocabulary_b068931c` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_vocabularyterm`
--

DROP TABLE IF EXISTS `data_vocabularyterm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_vocabularyterm` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `term` longtext NOT NULL,
  `vocabulary_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `data_vocabu_vocabulary_id_6070066c7a82222e_fk_data_vocabulary_id` (`vocabulary_id`),
  CONSTRAINT `data_vocabu_vocabulary_id_6070066c7a82222e_fk_data_vocabulary_id` FOREIGN KEY (`vocabulary_id`) REFERENCES `data_vocabulary` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_comment_flags`
--

DROP TABLE IF EXISTS `django_comment_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_comment_flags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `flag` varchar(30) NOT NULL,
  `flag_date` datetime NOT NULL,
  `comment_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_comment_flags_user_id_c7a132a641f11c1_uniq` (`user_id`,`comment_id`,`flag`),
  KEY `django_comment__comment_id_26f904a7f2b4c55_fk_django_comments_id` (`comment_id`),
  KEY `django_comment_flags_327a6c43` (`flag`),
  CONSTRAINT `django_comment_flags_user_id_1442753a03512f4c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_comment__comment_id_26f904a7f2b4c55_fk_django_comments_id` FOREIGN KEY (`comment_id`) REFERENCES `django_comments` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_comments`
--

DROP TABLE IF EXISTS `django_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_pk` longtext NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_email` varchar(254) NOT NULL,
  `user_url` varchar(200) NOT NULL,
  `comment` longtext NOT NULL,
  `submit_date` datetime NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `is_public` tinyint(1) NOT NULL,
  `is_removed` tinyint(1) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_39798e235626a505_fk_django_content_type_id` (`content_type_id`),
  KEY `django_comments_site_id_48b7896f6ea83216_fk_django_site_id` (`site_id`),
  KEY `django_comments_user_id_20e3794dfd3a7b1e_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_comments_site_id_48b7896f6ea83216_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`),
  CONSTRAINT `django_comments_user_id_20e3794dfd3a7b1e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `djang_content_type_id_39798e235626a505_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_flatpage`
--

DROP TABLE IF EXISTS `django_flatpage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_flatpage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `enable_comments` tinyint(1) NOT NULL,
  `template_name` varchar(70) NOT NULL,
  `registration_required` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_flatpage_572d4e42` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_flatpage_sites`
--

DROP TABLE IF EXISTS `django_flatpage_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_flatpage_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `flatpage_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `flatpage_id` (`flatpage_id`,`site_id`),
  KEY `django_flatpage_sites_site_id_481dafa7c6e850d9_fk_django_site_id` (`site_id`),
  CONSTRAINT `django_flatpage_sites_site_id_481dafa7c6e850d9_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`),
  CONSTRAINT `django_flatpa_flatpage_id_7b4e76c0a3a9d13a_fk_django_flatpage_id` FOREIGN KEY (`flatpage_id`) REFERENCES `django_flatpage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_redirect`
--

DROP TABLE IF EXISTS `django_redirect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_redirect` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `site_id` int(11) NOT NULL,
  `old_path` varchar(200) NOT NULL,
  `new_path` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `site_id` (`site_id`,`old_path`),
  KEY `django_redirect_91a0b591` (`old_path`),
  CONSTRAINT `django_redirect_site_id_121a4403f653e524_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `federatedsearch_hitcount`
--

DROP TABLE IF EXISTS `federatedsearch_hitcount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `federatedsearch_hitcount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `query` varchar(255) NOT NULL,
  `source` varchar(32) NOT NULL,
  `hits` int(11) NOT NULL,
  `results` longtext,
  `valid_until` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `impersonate_impersonation`
--

DROP TABLE IF EXISTS `impersonate_impersonation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `impersonate_impersonation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `impersonate_impersonation_groups`
--

DROP TABLE IF EXISTS `impersonate_impersonation_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `impersonate_impersonation_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `impersonation_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `impersonation_id` (`impersonation_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `impersonate_impersonation_users`
--

DROP TABLE IF EXISTS `impersonate_impersonation_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `impersonate_impersonation_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `impersonation_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `impersonation_id` (`impersonation_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `migration_objecthistory`
--

DROP TABLE IF EXISTS `migration_objecthistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `migration_objecthistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  `m2m_content_type_id` int(11) DEFAULT NULL,
  `m2m_object_id` int(10) unsigned DEFAULT NULL,
  `type` varchar(8) DEFAULT NULL,
  `original_id` varchar(255) NOT NULL,
  `content_hash` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `presentation_presentation`
--

DROP TABLE IF EXISTS `presentation_presentation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `presentation_presentation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `source` varchar(1024) DEFAULT NULL,
  `description` longtext,
  `password` varchar(32) DEFAULT NULL,
  `fieldset_id` int(11) DEFAULT NULL,
  `hide_default_data` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `presentation_presentationitem`
--

DROP TABLE IF EXISTS `presentation_presentationitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `presentation_presentationitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `presentation_id` int(11) NOT NULL,
  `record_id` int(11) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `type` varchar(16) NOT NULL,
  `order` smallint(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `presentation_presentationiteminfo`
--

DROP TABLE IF EXISTS `presentation_presentationiteminfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `presentation_presentationiteminfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` int(11) NOT NULL,
  `media_id` int(11) NOT NULL,
  `info` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rooibos_fieldset`
--

DROP TABLE IF EXISTS `rooibos_fieldset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rooibos_fieldset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `standard` tinyint(1) NOT NULL,
  `owner_id` int(11),
  PRIMARY KEY (`id`),
  KEY `rooibos_fieldset_b068931c` (`name`),
  KEY `rooibos_fieldset_5e7b1936` (`owner_id`),
  CONSTRAINT `rooibos_fieldset_owner_id_43e0da14734f9d8_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shared_sharedcollection`
--

DROP TABLE IF EXISTS `shared_sharedcollection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shared_sharedcollection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `e_url` longtext NOT NULL,
  `e_username` longtext NOT NULL,
  `e_password` longtext NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `solr_solrindexupdates`
--

DROP TABLE IF EXISTS `solr_solrindexupdates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `solr_solrindexupdates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `record` int(11) NOT NULL,
  `delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statistics_accumulatedactivity`
--

DROP TABLE IF EXISTS `statistics_accumulatedactivity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_accumulatedactivity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(10) unsigned DEFAULT NULL,
  `date` date NOT NULL,
  `event` varchar(64) NOT NULL,
  `final` tinyint(1) NOT NULL,
  `count` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `stati_content_type_id_2c305421ff061787_fk_django_content_type_id` (`content_type_id`),
  KEY `statistics_accumulatedactivity_af31437c` (`object_id`),
  KEY `statistics_accumulatedactivity_5fc73231` (`date`),
  KEY `statistics_accumulatedactivity_41196390` (`event`),
  CONSTRAINT `stati_content_type_id_2c305421ff061787_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statistics_activity`
--

DROP TABLE IF EXISTS `statistics_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(10) unsigned DEFAULT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `event` varchar(64) NOT NULL,
  `data` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `stati_content_type_id_10698f071fe86da4_fk_django_content_type_id` (`content_type_id`),
  KEY `statistics_activity_user_id_7b76db35c95b7f01_fk_auth_user_id` (`user_id`),
  KEY `statistics_activity_af31437c` (`object_id`),
  KEY `statistics_activity_5fc73231` (`date`),
  KEY `statistics_activity_41196390` (`event`),
  CONSTRAINT `statistics_activity_user_id_7b76db35c95b7f01_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `stati_content_type_id_10698f071fe86da4_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `storage_media`
--

DROP TABLE IF EXISTS `storage_media`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `storage_media` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `url` varchar(1024) NOT NULL,
  `mimetype` varchar(128) NOT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `bitrate` int(11) DEFAULT NULL,
  `master_id` int(11) DEFAULT NULL,
  `record_id` int(11) NOT NULL,
  `storage_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `storage_media_record_id_76b7d9dc11ff10dc_uniq` (`record_id`,`name`),
  KEY `storage_media_master_id_6ad6fa0ed478a63d_fk_storage_media_id` (`master_id`),
  KEY `storage_media_b068931c` (`name`),
  KEY `storage_media_5ca316a7` (`record_id`),
  KEY `storage_media_f733a512` (`storage_id`),
  CONSTRAINT `storage_media_storage_id_2537bbd11a6f7249_fk_storage_storage_id` FOREIGN KEY (`storage_id`) REFERENCES `storage_storage` (`id`),
  CONSTRAINT `storage_media_master_id_6ad6fa0ed478a63d_fk_storage_media_id` FOREIGN KEY (`master_id`) REFERENCES `storage_media` (`id`),
  CONSTRAINT `storage_media_record_id_494a718dafd9ee0_fk_data_record_id` FOREIGN KEY (`record_id`) REFERENCES `data_record` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `storage_proxyurl`
--

DROP TABLE IF EXISTS `storage_proxyurl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `storage_proxyurl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(36) NOT NULL,
  `url` varchar(1024) NOT NULL,
  `context` varchar(256) DEFAULT NULL,
  `user_backend` varchar(256) DEFAULT NULL,
  `last_access` datetime DEFAULT NULL,
  `subnet_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `storage_proxyurl_fe866fcb` (`subnet_id`),
  KEY `storage_proxyurl_e8701ad4` (`user_id`),
  CONSTRAINT `storage_proxyurl_user_id_68e7c6ac7fa863b6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `storage_p_subnet_id_153a05b14581f7aa_fk_storage_trustedsubnet_id` FOREIGN KEY (`subnet_id`) REFERENCES `storage_trustedsubnet` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `storage_storage`
--

DROP TABLE IF EXISTS `storage_storage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `storage_storage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `system` varchar(50) NOT NULL,
  `base` varchar(1024) DEFAULT NULL,
  `urlbase` varchar(1024) DEFAULT NULL,
  `serverbase` varchar(1024) DEFAULT NULL,
  `derivative_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `storage_storage_b068931c` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `storage_trustedsubnet`
--

DROP TABLE IF EXISTS `storage_trustedsubnet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `storage_trustedsubnet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subnet` varchar(80) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tagging_tag`
--

DROP TABLE IF EXISTS `tagging_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tagging_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tagging_taggeditem`
--

DROP TABLE IF EXISTS `tagging_taggeditem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tagging_taggeditem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(10) unsigned NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tagging_taggeditem_tag_id_2ccbe9f5fed37043_uniq` (`tag_id`,`content_type_id`,`object_id`),
  KEY `taggi_content_type_id_716a325781ea128d_fk_django_content_type_id` (`content_type_id`),
  KEY `tagging_taggeditem_af31437c` (`object_id`),
  CONSTRAINT `tagging_taggeditem_tag_id_7c6426178988e7e_fk_tagging_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `tagging_tag` (`id`),
  CONSTRAINT `taggi_content_type_id_716a325781ea128d_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userprofile_preference`
--

DROP TABLE IF EXISTS `userprofile_preference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userprofile_preference` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `setting` varchar(128) NOT NULL,
  `value` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userprofile_userprofile`
--

DROP TABLE IF EXISTS `userprofile_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userprofile_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userprofile_userprofile_preferences`
--

DROP TABLE IF EXISTS `userprofile_userprofile_preferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userprofile_userprofile_preferences` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `preference_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `userprofile_id` (`userprofile_id`,`preference_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `util_ownedwrapper`
--

DROP TABLE IF EXISTS `util_ownedwrapper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `util_ownedwrapper` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`object_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workers_jobinfo`
--

DROP TABLE IF EXISTS `workers_jobinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workers_jobinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `func` varchar(128) NOT NULL,
  `arg` longtext NOT NULL,
  `status` longtext,
  `created_time` datetime NOT NULL,
  `status_time` datetime DEFAULT NULL,
  `completed` tinyint(1) NOT NULL,
  `result` longtext NOT NULL,
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `workers_jobinfo_owner_id_6d3fd051fe098690_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `workers_jobinfo_owner_id_6d3fd051fe098690_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-08-03 19:44:54
