-- phpMyAdmin SQL Dump
-- version 4.7.9
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 10, 2018 at 07:39 AM
-- Server version: 5.7.21
-- PHP Version: 5.6.35

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pricosha`
--

-- --------------------------------------------------------

--
-- Table structure for table `contentitem`
--

DROP TABLE IF EXISTS `contentitem`;
CREATE TABLE IF NOT EXISTS `contentitem` (
  `item_id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(20) DEFAULT NULL,
  `post_time` timestamp NULL DEFAULT NULL,
  `file_path` varchar(100) DEFAULT NULL,
  `item_name` tinytext,
  `is_pub` tinyint(1) DEFAULT NULL,
  `tot_votes` tinyint(4) DEFAULT '0',
  `comment_on_item` int(11) DEFAULT NULL,
  PRIMARY KEY (`item_id`),
  KEY `email_post` (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `emoji`
--

DROP TABLE IF EXISTS `emoji`;
CREATE TABLE IF NOT EXISTS `emoji` (
  `post_id` int(11) NOT NULL,
  `emoji` varchar(25) DEFAULT NULL,
  `email` varchar(20) NOT NULL,
  PRIMARY KEY (`email`,`post_id`),
  KEY `post_id` (`post_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `friendgroup`
--

DROP TABLE IF EXISTS `friendgroup`;
CREATE TABLE IF NOT EXISTS `friendgroup` (
  `owner_email` varchar(20) NOT NULL,
  `fg_name` varchar(20) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`owner_email`,`fg_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
CREATE TABLE IF NOT EXISTS `member` (
  `owner_email` varchar(50) NOT NULL,
  `fg_name` varchar(50) NOT NULL,
  `email_creator` varchar(50) NOT NULL,
  PRIMARY KEY (`owner_email`,`fg_name`,`email_creator`),
  KEY `fg_name` (`fg_name`,`email_creator`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
CREATE TABLE IF NOT EXISTS `person` (
  `email` varchar(20) NOT NULL,
  `password` char(64) DEFAULT NULL,
  `fname` varchar(20) DEFAULT NULL,
  `lname` varchar(20) DEFAULT NULL,
  `about_me` text,
  PRIMARY KEY (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `rate`
--

DROP TABLE IF EXISTS `rate`;
CREATE TABLE IF NOT EXISTS `rate` (
  `email` varchar(20) NOT NULL,
  `item_id` int(11) NOT NULL,
  `rate_time` timestamp NULL DEFAULT NULL,
  `emoji` varchar(20) CHARACTER SET utf8mb4 DEFAULT NULL,
  `vote` tinyint(2) DEFAULT '0',
  PRIMARY KEY (`email`,`item_id`),
  KEY `item_id` (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `share`
--

DROP TABLE IF EXISTS `share`;
CREATE TABLE IF NOT EXISTS `share` (
  `owner_email` varchar(20) NOT NULL,
  `fg_name` varchar(20) NOT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`owner_email`,`fg_name`,`item_id`),
  KEY `item_id` (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
CREATE TABLE IF NOT EXISTS `tag` (
  `email_tagged` varchar(20) NOT NULL,
  `email_tagger` varchar(20) NOT NULL,
  `item_id` int(11) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `tagtime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`email_tagged`,`email_tagger`,`item_id`),
  KEY `email_tagger` (`email_tagger`),
  KEY `item_id` (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `grouptag`
--

DROP TABLE IF EXISTS `grouptag`;
CREATE TABLE IF NOT EXISTS `grouptag` (
  `email_tagger` varchar(20) NOT NULL,
  `fg_name` varchar(50) NOT NULL,
  `item_id` int(11) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `tagtime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`fg_name`,`email_tagger`,`item_id`),
  KEY `email_tagger` (`email_tagger`),
  KEY `item_id` (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;



COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
