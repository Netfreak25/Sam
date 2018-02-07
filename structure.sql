-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 07, 2018 at 08:14 PM
-- Server version: 5.5.59-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `sam_initial`
--
CREATE DATABASE IF NOT EXISTS `sam_initial` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
USE `sam_initial`;

-- --------------------------------------------------------

--
-- Table structure for table `deathreason`
--

DROP TABLE IF EXISTS `deathreason`;
CREATE TABLE IF NOT EXISTS `deathreason` (
  `id` int(11) NOT NULL,
  `text` varchar(1000) NOT NULL,
  `text_kurz` varchar(255) NOT NULL,
  `inuse` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Truncate table before insert `deathreason`
--

TRUNCATE TABLE `deathreason`;
--
-- Dumping data for table `deathreason`
--

INSERT INTO `deathreason` (`id`, `text`, `text_kurz`, `inuse`) VALUES
(0, 'Am Leben', 'Am Leben', -1),
(1, 'Samsquetch hat dich beim Cheaten erwischt und dir einen Nackenklatscher verteilt!\nDu bist tot!', 'Tot durch Cheaten', -1),
(2, 'Samsquetch schnappt dich und haut dich um!', 'Tot durch umhauen', 0);

-- --------------------------------------------------------

--
-- Table structure for table `extra_types`
--

DROP TABLE IF EXISTS `extra_types`;
CREATE TABLE IF NOT EXISTS `extra_types` (
  `id` int(11) NOT NULL,
  `name` varchar(5000) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Beschreibung` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Truncate table before insert `extra_types`
--

TRUNCATE TABLE `extra_types`;
--
-- Dumping data for table `extra_types`
--

INSERT INTO `extra_types` (`id`, `name`, `Beschreibung`) VALUES
(1, 'MedKit', 'Zum Wiederbeleben'),
(2, 'Schluessel', 'Verwendungszweck nicht bekannt'),
(3, 'Pistole', 'Ob die noch funktioniert?'),
(4, 'Bier', 'Zum trinken?!?!'),
(5, 'Buch', 'Was da wohl drinne steht?'),
(6, 'Taschenlampe', 'Ist ziemlich dunkel hier!'),
(7, 'Geld', 'Cash ist immer gut!'),
(8, 'Stift', 'Zum Schreiben!'),
(9, 'Pillen', 'Zum Schlucken!'),
(10, 'Schild', 'Zum Schutz vor was auch immer!'),
(11, 'Kerze', 'Zum erleuchten!'),
(12, 'Schleife', 'Ist wohl von Mrs. Samsquetch?!'),
(13, 'Messer', 'Zur Verteidigung!'),
(14, 'Falle', 'Du bist in einen Hinterhalt geraten!'),
(15, 'Tennisball', 'WTF?'),
(16, 'Apfel', 'Bio ist für mich Abfall!'),
(17, 'Fliegenpilz', 'Bitte nicht essen!'),
(18, 'Taco', 'Samsquetch seine lieblings Nahrung!'),
(19, 'Burito', 'Sams zweit liebings Essen!'),
(20, 'Keks', 'Kekse gehen immer!'),
(21, 'Whisky', 'Zum warm halten!'),
(22, 'Nebelhorn', 'Mache auf dich aufmerksam!');

-- --------------------------------------------------------

--
-- Table structure for table `extra_waypoints`
--

DROP TABLE IF EXISTS `extra_waypoints`;
CREATE TABLE IF NOT EXISTS `extra_waypoints` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location` varchar(255) NOT NULL,
  `type` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=424 ;

--
-- Truncate table before insert `extra_waypoints`
--

TRUNCATE TABLE `extra_waypoints`;
--
-- Dumping data for table `extra_waypoints`
--

INSERT INTO `extra_waypoints` (`id`, `location`, `type`, `amount`) VALUES
(2, '50.143467, 8.738169', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
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

--
-- Truncate table before insert `user`
--

TRUNCATE TABLE `user`;
-- --------------------------------------------------------

--
-- Table structure for table `variables`
--

DROP TABLE IF EXISTS `variables`;
CREATE TABLE IF NOT EXISTS `variables` (
  `name` varchar(255) NOT NULL,
  `value` varchar(2000) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Truncate table before insert `variables`
--

TRUNCATE TABLE `variables`;
--
-- Dumping data for table `variables`
--

INSERT INTO `variables` (`name`, `value`) VALUES
('cheat_text', 'Benutze bitte den Positions Knopf!'),
('finished_text', 'Du hast den Trail überlebt! Gratulation!\n\nJetzt erstmal ein Bierchen!'),
('help_text', 'Dieser Bot begleitet Sie auf der Suche nach dem sagenumwobenen Samsquetch welcher zuletzt im Elsass in der Gegend des Schwarzbachs gesichtet wurde!\r\n\r\nFalls Sie dem Samsquetch begegnen machen Sie so viel Tohuwabohu wie möglich um seinen Angriff zu vermeiden und Samsquetch in seine Schranken zu verweisen!'),
('reset_text', 'Todesursachen wurden wieder freigegeben!'),
('revive_text', 'Admin hat dir ein Med-Pack gegeben!'),
('rightanswer_text', 'Richtige Antwort! Es geht weiter!'),
('start_error', 'Leider ist etwas mit der Aktivierung schief gegangen. Kontaktiere bitte Moritz oder versuche es später noch einmal.'),
('start_image', 'data/sam.jpg'),
('start_text', 'Du bist also bereit für Samsquetch? Es kann gefährlich werden! Richtig Beängstigend!\n\nKlicke dann auf ''Position aktualisieren'' um zum ersten Wegpunkt zu gelangen!'),
('stop_error', 'Leider ist etwas mit der Deaktivierung schief gegangen. Kontaktiere bitte Moritz oder versuche es später noch einmal. Sorry!'),
('stop_text', 'Dein Abenteuer ist nun zu Ende!'),
('unknown_text', 'Rooooooaaaaaarrrrrrrr'),
('wronganswer_text', 'Das war leider Falsch! Weiter gehts!');

-- --------------------------------------------------------

--
-- Table structure for table `waypoints`
--

DROP TABLE IF EXISTS `waypoints`;
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

--
-- Truncate table before insert `waypoints`
--

TRUNCATE TABLE `waypoints`;
--
-- Dumping data for table `waypoints`
--

INSERT INTO `waypoints` (`id`, `location`, `text`, `bild`, `audio`, `video`, `voice`, `samtrigger`, `saminfo`, `question`, `is_wrong`, `is_right`, `is_wrong2`) VALUES
(0, '50.143443, 8.738051', 'Das ist der Text des ersten Wegpunktes, den man bei erreichen des Wegpunktes gesendet bekommt', 'data/sam.jpg', 'data/music.mp3', 'data/josh.mp4', '/data/death.ogg', 'trigger1', NULL, 'Wie hoch war damals das Kopfgeld auf das es Josh abgesehen hat?', '100€', '10000 Deutsche Mark', '10 Dukaten');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

