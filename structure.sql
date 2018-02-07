-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 07, 2018 at 03:04 PM
-- Server version: 5.5.59-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `initial_sam`
--

-- --------------------------------------------------------

--
-- Table structure for table `deathreason`
--

CREATE TABLE IF NOT EXISTS `deathreason` (
  `id` int(11) NOT NULL,
  `text` varchar(1000) NOT NULL,
  `text_kurz` varchar(255) NOT NULL,
  `inuse` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `extra_types`
--

CREATE TABLE IF NOT EXISTS `extra_types` (
  `id` int(11) NOT NULL,
  `name` varchar(5000) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Beschreibung` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `extra_waypoints`
--

CREATE TABLE IF NOT EXISTS `extra_waypoints` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location` varchar(255) NOT NULL,
  `type` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `chatid` varchar(255) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `waypoint` varchar(255) NOT NULL DEFAULT '1',
  `name` varchar(255) DEFAULT NULL,
  `livestatus` int(11) NOT NULL DEFAULT '0',
  `inventory` varchar(255) DEFAULT NULL,
  `points` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`chatid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `variables`
--

CREATE TABLE IF NOT EXISTS `variables` (
  `name` varchar(255) NOT NULL,
  `value` varchar(2000) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `waypoints`
--

CREATE TABLE IF NOT EXISTS `waypoints` (
  `id` int(11) NOT NULL,
  `location` varchar(255) NOT NULL,
  `text` varchar(255) DEFAULT NULL,
  `bild` varchar(255) DEFAULT NULL,
  `audio` varchar(255) DEFAULT NULL,
  `video` varchar(255) DEFAULT NULL,
  `voice` varchar(255) DEFAULT NULL,
  `samtrigger` varchar(255) DEFAULT NULL,
  `saminfo` varchar(255) DEFAULT NULL,
  `question` varchar(255) DEFAULT NULL,
  `is_wrong` varchar(255) DEFAULT NULL,
  `is_right` varchar(255) DEFAULT NULL,
  `is_wrong2` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

