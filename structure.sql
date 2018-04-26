SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;


CREATE TABLE IF NOT EXISTS `config` (
  `name` varchar(255) NOT NULL,
  `value` varchar(2000) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `config` (`name`, `value`) VALUES
('advanced', '0'),
('botname', 'SchnitzelBot'),
('cheat_detection', '0'),
('extra_distance_m', '20'),
('invincible', '1'),
('pagename', 'Schnitzeljagdt'),
('reset_minutes', '1'),
('trigger_distance_m', '30'),
('zoom_koordinaten', '50.110504,8.682120'),
('zoom_level', '16');

CREATE TABLE IF NOT EXISTS `deathreason` (
  `id` int(11) NOT NULL,
  `text` varchar(1000) NOT NULL,
  `text_kurz` varchar(255) NOT NULL,
  `inuse` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `deathreason` (`id`, `text`, `text_kurz`, `inuse`) VALUES
(0, 'Am Leben', 'Am Leben', -1),
(1, 'Du wurdest beim Cheaten erwischt und hast einen Nackenklatscher erhalten!\nDu bist tot!', 'Tot durch Cheaten', -1),
(3, 'Ein Tier springt aus dem Baum neben dir und hat dir den Schädel mit einem Ast eingeschlagen!\nDu bist tot!', 'Tot durch Ast', 0);

CREATE TABLE IF NOT EXISTS `extra_types` (
  `id` int(11) NOT NULL,
  `name` varchar(5000) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Beschreibung` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
(19, 'Burrito', 'Sams zweit liebings Essen!'),
(20, 'Keks', 'Kekse gehen immer!'),
(21, 'Whisky', 'Zum warm halten!'),
(22, 'Nebelhorn', 'Mache auf dich aufmerksam!'),
(23, 'Karte', 'Jetzt weißt du in welche Richtung du gehen musst!');

CREATE TABLE IF NOT EXISTS `extra_waypoints` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location` varchar(255) NOT NULL,
  `type` int(11) NOT NULL,
  `amount` int(11) unsigned NOT NULL DEFAULT '1',
  `chance` int(11) unsigned NOT NULL DEFAULT '100',
  `item_distance_m` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

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

INSERT INTO `variables` (`name`, `value`) VALUES
('cheat_text', 'Benutze bitte den Positions Knopf!'),
('finished_text', 'Du hast den Trail überlebt! Gratulation!\n\nJetzt erstmal ein Bierchen!'),
('help_text', 'Dieser Bot begleitet Sie auf der Suche nach dem sagenumwobenen Samsquetch welcher zuletzt im Elsass in der Gegend des Schwarzbachs gesichtet wurde!\r\n\r\nFalls Sie dem Samsquetch begegnen machen Sie so viel Tohuwabohu wie möglich um seinen Angriff zu vermeiden und Samsquetch in seine Schranken zu verweisen!'),
('reset_text', 'Todesursachen wurden wieder freigegeben!'),
('revive_text', 'Moritz hat dir ein Med-Pack gegeben!'),
('rightanswer_text', 'Richtige Antwort! Es geht weiter!'),
('start_error', 'Leider ist etwas mit der Aktivierung schief gegangen. Kontaktiere bitte Moritz oder versuche es später noch einmal.'),
('start_image', 'data/sam.jpg'),
('start_text', 'Du bist also bereit für Samsquetch? Es kann gefährlich werden! Richtig Beängstigend! Klicke dann auf ''Position aktualisieren'' um zum ersten Wegpunkt zu gelangen!'),
('stop_error', 'Leider ist etwas mit der Deaktivierung schief gegangen. Kontaktiere bitte Moritz oder versuche es später noch einmal. Sorry!'),
('stop_text', 'Dein Abenteuer ist nun zu Ende!'),
('unknown_text', 'Rooooooaaaaaarrrrrrrr'),
('wronganswer_text', 'Das war leider Falsch! Weiter gehts!');

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
  `name` varchar(255) NOT NULL,
  `trigger_distance_m` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
