-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Dec 10, 2018 at 06:43 AM
-- Server version: 5.7.23
-- PHP Version: 7.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
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

CREATE TABLE `contentitem` (
  `item_id` int(11) NOT NULL,
  `email` varchar(20) DEFAULT NULL,
  `post_time` timestamp NULL DEFAULT NULL,
  `file_path` varchar(100) DEFAULT NULL,
  `item_name` tinytext,
  `is_pub` tinyint(1) DEFAULT NULL,
  `tot_votes` tinyint(4) DEFAULT '0',
  `comment_on_item` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `contentitem`
--

INSERT INTO `contentitem` (`item_id`, `email`, `post_time`, `file_path`, `item_name`, `is_pub`, `tot_votes`, `comment_on_item`) VALUES
(5, 'Ash', '2018-11-20 16:32:33', NULL, 'Pub Post', 1, 1, NULL),
(9, 'Person', '2018-11-30 20:23:10', NULL, 'Private', 0, 2, NULL),
(6, 'Ash', '2018-11-20 16:33:45', NULL, 'Private Post', 0, 1, NULL),
(7, 'Person', '2018-11-27 17:49:27', NULL, 'posting', 0, 0, NULL),
(8, 'Person', '2018-11-27 18:05:39', NULL, 'Pub post', 1, 0, NULL),
(10, 'Ash', '2018-11-30 20:54:47', NULL, 'post', 0, 1, NULL),
(11, 'Ash', '2018-11-30 20:54:51', NULL, 'another', 0, 1, NULL),
(12, 'Ash', '2018-12-03 20:49:20', NULL, ' A VEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRYYYYYYY LOOOOOOOOOOOOOOONNNNNNNG POST', 1, 0, NULL),
(13, 'Ash', '2018-12-05 22:35:35', NULL, 'aaaaaaaaaahhhhhhhhhhhhh!!!!!!!!!!!!!!!!!', 1, -1, NULL),
(14, 'Ash', '2018-12-06 00:46:47', NULL, 'nnnnnnnnnnnnoooooooooo.........', 1, 2, 13),
(15, 'Ash', '2018-12-06 01:17:08', NULL, 'another comment', 0, NULL, 13),
(16, 'Ash', '2018-12-06 01:17:33', NULL, 'another comment', 0, NULL, 13),
(17, 'Ash', '2018-12-06 01:17:47', NULL, 'another comment', 0, NULL, 13),
(18, 'Ash', '2018-12-06 01:19:58', NULL, 'comment 2', 0, -1, 13),
(19, 'Ash', '2018-12-06 01:23:10', NULL, 'comment 2', 0, 1, 13),
(20, 'Ash', '2018-12-06 01:23:23', NULL, 'comment 2', 0, -1, 13),
(21, 'Ash', '2018-12-06 14:45:53', NULL, 'post', 0, 1, NULL),
(22, 'amehovic13@gmail.com', '2018-12-06 20:17:50', NULL, 'ahh', 0, NULL, 14),
(23, 'amehovic13@gmail.com', '2018-12-08 00:33:00', NULL, 'rwefs', 0, NULL, 22),
(24, 'amehovic13@gmail.com', '2018-12-10 01:20:54', NULL, 'jd', 0, NULL, 23),
(25, 'amehovic13@gmail.com', '2018-12-10 06:03:23', NULL, 'fsd', 0, 1, 24);

-- --------------------------------------------------------

--
-- Table structure for table `emoji`
--

CREATE TABLE `emoji` (
  `post_id` int(11) DEFAULT NULL,
  `emoji` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `emoji`
--

INSERT INTO `emoji` (`post_id`, `emoji`) VALUES
(24, ':)'),
(24, ':)'),
(24, ':|'),
(23, ':|'),
(13, ':)'),
(25, ':)'),
(25, ':)'),
(25, ':)');

-- --------------------------------------------------------

--
-- Table structure for table `friendgroup`
--

CREATE TABLE `friendgroup` (
  `owner_email` varchar(20) NOT NULL,
  `fg_name` varchar(20) NOT NULL,
  `description` varchar(1000) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `member`
--

CREATE TABLE `member` (
  `owner_email` varchar(50) NOT NULL,
  `fg_name` varchar(50) NOT NULL,
  `email_creator` varchar(50) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `person`
--

CREATE TABLE `person` (
  `email` varchar(20) NOT NULL,
  `password` char(64) DEFAULT NULL,
  `fname` varchar(20) DEFAULT NULL,
  `lname` varchar(20) DEFAULT NULL,
  `about_me` text
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `person`
--

INSERT INTO `person` (`email`, `password`, `fname`, `lname`, `about_me`) VALUES
('Person', '8b0a44048f58988b486bdd0d245b22a8', 'Peron', 'Pers', NULL),
('Ash', '2852f697a9f8581725c6fc6a5472a2e5', 'ASD', 'sdfgh', 'something about me'),
('amehovic13@gmail.com', '9cfefed8fb9497baa5cd519d7d2bb5d7', 'Enisa', 'Mehovic', 'hi im aida and i love balogny');

-- --------------------------------------------------------

--
-- Table structure for table `rate`
--

CREATE TABLE `rate` (
  `email` varchar(20) NOT NULL,
  `item_id` int(11) NOT NULL,
  `rate_time` timestamp NULL DEFAULT NULL,
  `emoji` varchar(20) CHARACTER SET utf8mb4 DEFAULT NULL,
  `vote` tinyint(2) DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rate`
--

INSERT INTO `rate` (`email`, `item_id`, `rate_time`, `emoji`, `vote`) VALUES
('Ash', 21, '2018-12-06 15:14:00', NULL, 1),
('Ash', 12, '2018-12-04 17:05:12', NULL, 1),
('Ash', 11, '2018-12-04 00:27:47', NULL, 1),
('Ash', 10, '2018-12-04 00:27:50', NULL, 1),
('person', 12, '2018-12-04 02:16:02', NULL, -1),
('person', 9, '2018-12-04 02:22:27', NULL, 1),
('person', 8, '2018-12-04 02:22:30', NULL, -1),
('person', 7, '2018-12-04 02:22:32', NULL, -1),
('person', 5, '2018-12-04 02:22:36', NULL, 1),
('Ash', 6, '2018-12-04 17:32:30', NULL, 1),
('Ash', 20, '2018-12-06 14:46:06', NULL, -1),
('Ash', 13, '2018-12-06 15:49:38', NULL, -1),
('Ash', 9, '2018-12-06 15:28:11', NULL, 1),
('Ash', 8, '2018-12-06 15:28:00', NULL, 1),
('Ash', 7, '2018-12-06 15:28:03', NULL, 1),
('Ash', 19, '2018-12-06 15:32:44', NULL, 1),
('Ash', 18, '2018-12-06 15:32:47', NULL, -1),
('Ash', 14, '2018-12-06 15:45:07', NULL, 1),
('amehovic13@gmail.com', 14, '2018-12-06 20:17:39', NULL, 1),
('amehovic13@gmail.com', 25, '2018-12-10 06:19:32', NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `share`
--

CREATE TABLE `share` (
  `owner_email` varchar(20) NOT NULL,
  `fg_name` varchar(20) NOT NULL,
  `item_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--

CREATE TABLE `tag` (
  `email_tagged` varchar(20) NOT NULL,
  `email_tagger` varchar(20) NOT NULL,
  `item_id` int(11) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `tagtime` timestamp NULL DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contentitem`
--
ALTER TABLE `contentitem`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `email_post` (`email`);

--
-- Indexes for table `friendgroup`
--
ALTER TABLE `friendgroup`
  ADD PRIMARY KEY (`owner_email`,`fg_name`);

--
-- Indexes for table `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`owner_email`,`fg_name`,`email_creator`),
  ADD KEY `fg_name` (`fg_name`,`email_creator`);

--
-- Indexes for table `person`
--
ALTER TABLE `person`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `rate`
--
ALTER TABLE `rate`
  ADD PRIMARY KEY (`email`,`item_id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `share`
--
ALTER TABLE `share`
  ADD PRIMARY KEY (`owner_email`,`fg_name`,`item_id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `tag`
--
ALTER TABLE `tag`
  ADD PRIMARY KEY (`email_tagged`,`email_tagger`,`item_id`),
  ADD KEY `email_tagger` (`email_tagger`),
  ADD KEY `item_id` (`item_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contentitem`
--
ALTER TABLE `contentitem`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
