SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;


CREATE TABLE IF NOT EXISTS `deathreason` (
  `id` int(11) NOT NULL,
  `text` varchar(1000) NOT NULL,
  `text_kurz` varchar(255) NOT NULL,
  `inuse` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `extra_types` (
  `id` int(11) NOT NULL,
  `name` varchar(5000) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Beschreibung` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `extra_waypoints` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location` varchar(255) NOT NULL,
  `type` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=610 ;

CREATE TABLE IF NOT EXISTS `trigger_clients` (
  `name` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `trigger` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `battery` int(11) NOT NULL,
  `last_seen` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `count` int(255) NOT NULL DEFAULT '0',
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

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

CREATE TABLE IF NOT EXISTS `variables` (
  `name` varchar(255) NOT NULL,
  `value` varchar(2000) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
