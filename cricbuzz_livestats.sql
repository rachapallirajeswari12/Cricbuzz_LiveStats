-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: cricbuzz_livestats
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `batting_performance`
--

DROP TABLE IF EXISTS `batting_performance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `batting_performance` (
  `innings_id` int NOT NULL,
  `player_id` int NOT NULL,
  `batting_position` int NOT NULL,
  `runs` int NOT NULL DEFAULT '0',
  `balls_faced` int NOT NULL DEFAULT '0',
  `fours` int NOT NULL DEFAULT '0',
  `sixes` int NOT NULL DEFAULT '0',
  `dismissed` tinyint(1) NOT NULL DEFAULT '0',
  `dismissal_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`innings_id`,`player_id`),
  KEY `fk_batting_player` (`player_id`),
  CONSTRAINT `fk_batting_innings` FOREIGN KEY (`innings_id`) REFERENCES `innings` (`innings_id`),
  CONSTRAINT `fk_batting_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `batting_performance`
--

LOCK TABLES `batting_performance` WRITE;
/*!40000 ALTER TABLE `batting_performance` DISABLE KEYS */;
INSERT INTO `batting_performance` VALUES (1,1,1,120,180,14,2,1,'Caught'),(1,2,2,95,140,10,1,1,'LBW'),(2,5,1,1,1,0,0,1,'Bowled'),(3,1,1,110,120,9,3,1,'Caught'),(4,5,1,105,115,8,2,0,NULL),(5,5,1,85,55,7,4,1,'Caught'),(6,1,1,90,60,8,3,1,'Caught'),(7,6,1,108,99,13,1,0,NULL),(7,7,2,71,81,7,1,0,NULL);
/*!40000 ALTER TABLE `batting_performance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bowling_performance`
--

DROP TABLE IF EXISTS `bowling_performance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bowling_performance` (
  `innings_id` int NOT NULL,
  `player_id` int NOT NULL,
  `balls_bowled` int NOT NULL DEFAULT '0',
  `runs_conceded` int NOT NULL DEFAULT '0',
  `wickets` int NOT NULL DEFAULT '0',
  `maidens` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`innings_id`,`player_id`),
  KEY `fk_bowling_player` (`player_id`),
  CONSTRAINT `fk_bowling_innings` FOREIGN KEY (`innings_id`) REFERENCES `innings` (`innings_id`),
  CONSTRAINT `fk_bowling_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bowling_performance`
--

LOCK TABLES `bowling_performance` WRITE;
/*!40000 ALTER TABLE `bowling_performance` DISABLE KEYS */;
INSERT INTO `bowling_performance` VALUES (1,3,120,70,3,2),(2,4,144,80,4,1),(3,3,60,45,2,0),(4,4,60,50,2,0),(5,3,24,35,1,0),(6,4,24,30,2,0),(7,8,36,37,1,0),(7,9,24,31,0,0);
/*!40000 ALTER TABLE `bowling_performance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commentary`
--

DROP TABLE IF EXISTS `commentary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `commentary` (
  `commentary_id` bigint NOT NULL AUTO_INCREMENT,
  `match_id` int NOT NULL,
  `innings_id` int DEFAULT NULL,
  `comm_type` varchar(30) DEFAULT NULL,
  `commentary_text` text,
  `team_name` varchar(100) DEFAULT NULL,
  `event_type` varchar(50) DEFAULT NULL,
  `timestamp_ms` bigint DEFAULT NULL,
  `batsman_api_id` varchar(50) DEFAULT NULL,
  `batsman_name` varchar(150) DEFAULT NULL,
  `bowler_api_id` varchar(50) DEFAULT NULL,
  `bowler_name` varchar(150) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`commentary_id`),
  KEY `fk_commentary_match` (`match_id`),
  CONSTRAINT `fk_commentary_match` FOREIGN KEY (`match_id`) REFERENCES `matches` (`match_id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commentary`
--

LOCK TABLES `commentary` WRITE;
/*!40000 ALTER TABLE `commentary` DISABLE KEYS */;
INSERT INTO `commentary` VALUES (1,4,3,'commentary','For its first Test match, the pitch played pretty good. Runs in it for the able batters and enough in it to keep the bowlers interested as well. The players will take a much deserved break after having toiled in 40+ degrees heat. Mind you it would have been even high inside the ground. On that note, we sign off from this game. There\'s lot of cricket around the globe. We will seen you again soon. Take care!','AFG',NULL,1780915583727,NULL,'',NULL,'','2026-09-09 09:03:22'),(2,4,3,'commentary','The Indian team had Manav in their plans for a while and they will be absolutely delighted that he\'s come good in his very first game. Impressed everyone with the technical aspects of his bowling - the revs, drift, length, line etc. Who next after Jadeja/Axar? Manav has made a strong case here, although this is just his first international game. The next Test assignment for India is in Sri Lanka in an away-tour where they will play two Tests. Few boxes ticked here in Mullanpur.','AFG',NULL,1780915580748,NULL,'',NULL,'','2026-09-09 09:03:22'),(3,4,3,'commentary','Gill collects the trophy and gives it to his teammates. They pose in front of the winners board. Manav lifts the trophy high and has his moment. Sports a lovely smile as well.','AFG',NULL,1780914999409,NULL,'',NULL,'','2026-09-09 09:03:22'),(4,4,3,'commentary','<b>Shubman Gill:</b> I think a complete win from us, ticked all the boxes. So very happy with that. (Thought process to enforce the follow-on?) It was very hot. We decided that if we get them before lunch or just after the first drinks, we\'ll see if the bowlers are fresh we\'ll give them a follow-on. If not, we\'ll bat a couple of sessions and maybe at the end of the day, we\'ll give them the ball again. But we got quick wickets, we came back. And also the way our fast bowlers bowled, Siraj got us that crucial wicket when we gave them a follow-on and Prasidh got three important wickets. (Thoughts on the spin-trio?) The kind of quality, I think, Manav, Washi and Kuldeep has, all three of them, there was never any doubt. It\'s all about getting the experience and getting a number of overs and seeing, on wickets like these how to set the batsman up, keep varying the pace, keep testing the batsman in different areas. (Young side in transition. What does India as a team and you as a captain need to do to take this team forward?) I\'d say pretty simple. When you\'re batting first innings, try to post 350 on the board every time you get into bat, no matter where we are playing, what kind of conditions it is. I think there\'s enough trust in our bowling group that we can take 20 wickets anywhere. Whenever there\'s a transition, we feel the batting group is under more pressure and we are trying to get experience. We\'re trying to build here to see what kind of game can work for us as a batting group and in different conditions and different situations. How we can keep posting regularly 350-400 totals on the board.','AFG',NULL,1780914829680,NULL,'',NULL,'','2026-09-09 09:03:22'),(5,4,3,'commentary','<b>Manav Suthar | PoTM</b>: (Test cricket is easy, right?) No sir, it\'s not really like that. (His feeling on receiving the India cap) It was a very unreal feeling. It has been my dream from the very beginning to play for India and to play Test cricket. So it was an incredible moment for me and honestly felt quite unreal. (Did batting before bowling help settle his nerves?) No. Even when I went out to bat, I felt quite comfortable. As I settled in and faced a few deliveries, I realized there was a bit of assistance for the spinners on the wicket. Then, when I came on to bowl and delivered my first over, I got the same feeling. After that, my only focus was to keep using the right line, length and pace. (Relying on his stock ball primarily and then experimenting) Yes, initially my focus was on understanding how the wicket was playing. That\'s why I wanted to rely on my stock delivery as much as possible. Once I understood that the wicket was a little slow and required some variation in pace, I started making those adjustments. But the main idea was always to make my stock ball as effective as possible. (How did it feel getting the second new ball?) It\'s a matter of great pride. Being trusted with that responsibility means a lot. (The review he wanted to take and was denied) It was more of a heat-of-the-moment decision. From where I was standing, it looked absolutely plumb, so I felt it was worth taking the review. (What\'s the biggest lesson you\'ve learned from this match?) The biggest lesson is that consistency is everything. You have to keep bowling in the same area over and over again. I think that\'s the most important thing in Test cricket. It\'s a format that demands a lot of patience. That\'s what I\'ve learned - keep being patient, stick to your plans and keep hitting the right areas consistently.','AFG',NULL,1780914661795,NULL,'',NULL,'','2026-09-09 09:03:22'),(6,4,3,'commentary','<b>Hashmatullah Shahidi</b>: Congratulations to the India team on their performance. I think it was a tough day, a tough game for us, and right from the start, from the beginning, our discipline in the bowling was not that good. So I think they played really well right from the start. (What lessons have you learnt?) Well, the reality is that we don\'t have that experience in this format. I think we learned a lot from this game because we don\'t get enough opportunities to play this format, but everybody knows that India is a tough team playing in their own conditions. But a lot of lessons to us and hopefully that we learn from this and hopefully that we play and we learn to play under pressure because as we win the things get tougher. (What about the positives?) Yeah, we had positives, especially Saleem. Saleem was part of the team before this, but he got injured in the middle of tours. I think he did a brilliant comeback the way he was bowling. I am very happy for him and in the batting also Rahmat played really well in the first innings and in the second innings I think Sediq was also good. (On Manav Suthar) I think he bowled really well. He bowled stump to stump and he was really disciplined in his bowling. That\'s why we struggled against him because if you look at the pitch, the pitch behavior was also keep changing session by session. I think the scoreboard pressure was there and also with that the pitch condition was changing and I think he bowled very disciplined.','AFG',NULL,1780914402395,NULL,'',NULL,'','2026-09-09 09:03:22'),(7,4,3,'commentary','You can now see the players coming out, so the presentation should start very shortly.','AFG',NULL,1780914130554,NULL,'',NULL,'','2026-09-09 09:03:22'),(8,4,3,'commentary','We are waiting for the presentation ceremony to begin. Hang tight!','AFG',NULL,1780913057057,NULL,'',NULL,'','2026-09-09 09:03:22'),(9,4,3,'commentary','<i>Stats by Shashikant Singh</i><br><br><b>Biggest innings wins for India </b><br>Inns & 300 runs vs AFG, Mullanpur, 2026*<br>Inns & 272 runs vs WI, Rajkot, 2018<br>Inns & 262 runs vs AFG, Bengaluru, 2018<br>Inns & 239 runs vs BAN, Mirpur, 2007<br>Inns & 239 runs vs SL, Nagpur, 2017<br><br>The only bigger innings wins on Indian soil are by <b>WI vs IND at Eden Gardens in 1958 (Inns & 336 runs).</b> <br><br>The only other biggest innings wins by an Asian team than this are by <b>PAK vs NZ in Lahore in 2002 (Inns & 324 runs).</b> <br><br><b>Innings defeats for AFG in Tests</b> <br>Inns & 300 runs vs IND, Mullanpur, 2026*<br>Inns & 262 runs vs IND, Bengaluru, 2018<br>Inns & 73 runs vs ZIM, Harare, 2025 <br><br><b>Lowest totals for AFG in Tests</b> <br>103 vs IND, Bengaluru, 2018<br>109 vs IND, Bengaluru, 2018<br>112 vs IND, Mullanpur, 2026*<br>115 vs BAN, Mirpur, 2023 <br>120 vs WI, Lucknow, 2019','AFG',NULL,1780911794684,NULL,'',NULL,'','2026-09-09 09:03:22'),(10,4,3,'commentary','<b>Washington Sundar </b>- (How good did you feel this morning, the way you bowled?) I felt really good, especially to play this format after a while. Yeah, I just wanted to get a lot of volume coming into the game and obviously I felt like I was getting the rhythm right from the scratch, from ball one. And that was definitely a very good feeling. (Did you try to bowl a little slower today?) I mean, nothing of that sort. I didn\'t really think about the pace as such. I was just working on getting my rhythm right. And especially yesterday I was bowling really well. The way the ball was coming out of my hand, I was really pleased with it. And obviously this morning I got to keep the consistency and the rest of the wickets did have something for us. (Stuck to your basics) Yes, towards the end I sort of wanted to bowl a little wide, but apart from that, I wanted to be as close to the stumps as possible. And obviously get those lengths really right because this wicket is a little slow. And I mean, if you\'re going to bowl a good length or a little back of length, the batsmen just did have a little bit of time to actually go in the back foot and sort of manoeuvre. So I had to really get lengths really right in this wicket. (On getting a few reviews wrong) I mean, it\'s part and parcel of the game, obviously. And we just try and go with our experiences in the past and obviously what our gut says at that point of time. And you\'ve got to use the technology to the best. We try and use it to the best. It doesn\'t happen every time, but it\'s just an experience. (On getting a fifty as well) Definitely, it felt really good, both with the bat and the ball. I wanted to show good discipline with the bat and glad the way I sort of approached the entire innings and God was kind.','AFG',NULL,1780911696722,NULL,'',NULL,'','2026-09-09 09:03:22'),(11,4,3,'commentary','Afghanistan showed a bit of promise through Rahmat in their first effort. They didn\'t play rash shots and made the Indian bowlers work for their wickets. Some felt they should have played more shots. On the contrary, they played too many shots and lacked patience in the second innings.','AFG',NULL,1780911344844,NULL,'',NULL,'','2026-09-09 09:03:22'),(12,4,3,'commentary','<b>15:03 Local Time, 09:33 GMT, 15:03 IST:</b> Handshakes between both sides. Satisfied look on Gill\'s face. Pant has some fun with Jurel. Sai puts his arm around Washi as they walk off. He then has some banter with Nitish. Supportstaff happy as well. A thumping win for India. They needed only 35.5 overs to bowl out Afghanistan after enforcing the follow-on. They win by an innings and 300 runs - their biggest victory in Tests. The visitors actually got off to a good start in their second innings as the openers put on 42. The Indian bowlers were a bit frustrated that the wickets weren\'t coming but an inspired Siraj opened the door. He was their best bowler early on. But the spinners soon joined the party. If Manav led from the front in the first innings, Washi took the baton in the second. Suddenly Afghanistan lost 4 wickets for 24 runs in the post-lunch session and lost their way. India wanted to wrap it up quickly and they wasted no time, taking the next 4 wickets for just 14 runs as Kuldeep too chipped in. Injured Sharafuddin Ashraf did not come out to bat.','AFG',NULL,1780911344834,NULL,'',NULL,'','2026-09-09 09:03:22'),(13,4,3,'commentary','Kuldeep Yadav to Saleem Safi, <b>out</b> Caught by Sai Sudharsan!! <b>Ashraf is not coming out to bat</b>. Handshake between the players. <b>India win by an innings and 300 runs.</b> Safi was never going to hang around. Kuldeep knew that and smartly floated up the googly around leg, Safi slogs to the leg-side and gets a leading edge towards cover. Sai settles under and hangs on to a simple catch. <b>Saleem Safi c Sai Sudharsan b Kuldeep Yadav 0(1)</b>','AFG',NULL,1780911177489,'19267','Mohammad Saleem Safi','8292','Kuldeep Yadav','2026-09-09 09:03:22'),(14,4,3,'commentary','Kuldeep Yadav to Saleem Safi, <b>THATS OUT!!</b> Caught!!','AFG',NULL,1780911176878,'19267','Saleem Safi','8292','Kuldeep Yadav','2026-09-09 09:03:22'),(15,4,3,'commentary','<b>Mohammad Saleem Safi, right handed bat, comes to the crease</b>','AFG',NULL,1780911122914,'19267','Saleem Safi','8292','Kuldeep Yadav','2026-09-09 09:03:22'),(16,4,3,'commentary','Kuldeep Yadav to Nangeyalia Kharote, <b>out</b> Caught by Manav Suthar!! This time Kuldeep has his man. Manav once again into the thick of things. Short and spinning away, bit of extra bounce and Kharote cannot control it, hits it uppishly towards point and Manav moves to his left to take the catch. Second wicket for Kuldeep and India are almost there. <b>Nangeyalia Kharote c Manav Suthar b Kuldeep Yadav 6(11) [6s-1]</b>','AFG',NULL,1780911078693,'22956','Nangeyalia Kharote','8292','Kuldeep Yadav','2026-09-09 09:03:22'),(17,4,3,'commentary','Kuldeep Yadav to Nangeyalia Kharote, <b>THATS OUT!!</b> Caught!!','AFG',NULL,1780911077778,'22956','Nangeyalia Kharote','8292','Kuldeep Yadav','2026-09-09 09:03:22'),(18,4,3,'commentary','Kuldeep Yadav to Nangeyalia Kharote, no run, that was poor from Richard Illingworth. He\'s had a good match till this point. But got this wrong. Tossed up around off, Kharote crouches low and plays the reverse sweep, he hits it into the ground and the ball flies to Jaiswal at gully. He holds on and Indians appeal for the catch, Illingworth raises his finger only for it to be overturned','AFG',NULL,1780911039064,'22956','Nangeyalia Kharote','8292','Kuldeep Yadav','2026-09-09 09:03:22'),(19,4,3,'commentary','<b>Afghanistan review!</b> Kharote is caught at gully. But he decides to challenge the onfield call. It is a bump ball. Not Out','AFG',NULL,1780911017593,NULL,'',NULL,'','2026-09-09 09:03:22'),(20,4,3,'commentary','Kuldeep Yadav to Nangeyalia Kharote, no run, flighted outside off, Kharote now attempts the sweep and misses. The impact is outside off','AFG',NULL,1780910963122,'22956','Nangeyalia Kharote','8292','Kuldeep Yadav','2026-09-09 09:03:22'),(21,5,1,'commentary','Gerhard Erasmus to Jordan Hermann, no run','RSA',NULL,1788948470521,'21386','Jordan Hermann','7973','Gerhard Erasmus','2026-09-09 10:08:14'),(22,5,1,'commentary','Gerhard Erasmus to Jordan Hermann, no run','RSA',NULL,1788948456098,'21386','Jordan Hermann','7973','Gerhard Erasmus','2026-09-09 10:08:14'),(23,5,1,'commentary','Gerhard Erasmus to Jordan Hermann, no run','RSA',NULL,1788948434018,'21386','Jordan Hermann','7973','Gerhard Erasmus','2026-09-09 10:08:14'),(24,5,1,'commentary','Gerhard Erasmus to Dewald Brevis, 1 run, drives a tossed up delivery down to deep cover for a single','RSA',NULL,1788948431846,'20538','Dewald Brevis','7973','Gerhard Erasmus','2026-09-09 10:08:14'),(25,5,1,'commentary','<b>Dewald Brevis, right handed bat, comes to the crease</b>','RSA',NULL,1788948374731,'20538','Dewald Brevis','7973','Gerhard Erasmus','2026-09-09 10:08:14'),(26,5,1,'commentary','Gerhard Erasmus to de Zorzi, <b>out</b> Lbw!! Was fired in fuller, at the sticks, Tony de Zorzi looks to reverse sweep and misses. That was quicker and Tony de Zorzi missed the line to be given out. Tony de Zorzi has missed out on a 100. <b>de Zorzi lbw b Gerhard Erasmus 72(84) [4s-7 6s-1]</b>','RSA',NULL,1788948316148,'11196','Tony de Zorzi','7973','Gerhard Erasmus','2026-09-09 10:08:14'),(27,5,1,'commentary','Gerhard Erasmus to de Zorzi, <b>THATS OUT!!</b> Lbw!!','RSA',NULL,1788948314375,'11196','Tony de Zorzi','7973','Gerhard Erasmus','2026-09-09 10:08:14'),(28,5,1,'commentary','Gerhard Erasmus to de Zorzi, no run, short ball, outside off, Tony de Zorzi looks to slash it and misses','RSA',NULL,1788948303306,'11196','Tony de Zorzi','7973','Gerhard Erasmus','2026-09-09 10:08:14'),(29,5,1,'commentary','Ruben Trumpelmann to Jordan Hermann, <b>SIX</b>, straight down the ground for a sixer! Was a length delivery, outside off, Jordan Hermann got under the ball and slammed it over the ropes. That was hit hard and long','RSA',NULL,1788948207205,'21386','Jordan Hermann','14431','Ruben Trumpelmann','2026-09-09 10:08:14'),(30,5,1,'commentary','Ruben Trumpelmann to Jordan Hermann, <b>wide</b>, full toss, down leg, Jordan Hermann looks to heave it and misses. Has been wided as that was well down leg','RSA',NULL,1788948172700,'21386','Jordan Hermann','14431','Ruben Trumpelmann','2026-09-09 10:08:14'),(31,5,1,'commentary','Ruben Trumpelmann to Jordan Hermann, <b>FOUR</b>, slower one, on the sticks, Jordan Hermann walks across, gets under the ball and scoops it over the keeper','RSA',NULL,1788948130988,'21386','Jordan Hermann','14431','Ruben Trumpelmann','2026-09-09 10:08:14'),(32,5,1,'commentary','Ruben Trumpelmann to Jordan Hermann, no run, slower one, outside off, Jordan Hermann looks to slash it and misses','RSA',NULL,1788948091255,'21386','Jordan Hermann','14431','Ruben Trumpelmann','2026-09-09 10:08:14'),(33,5,1,'commentary','Ruben Trumpelmann to Jordan Hermann, <b>wide</b>, down leg, left alone and has been wided','RSA',NULL,1788948053948,'21386','Jordan Hermann','14431','Ruben Trumpelmann','2026-09-09 10:08:14'),(34,5,1,'commentary','Ruben Trumpelmann to de Zorzi, 1 run, short ball, at the body, pulled down to deep mid for a single','RSA',NULL,1788948019360,'11196','Tony de Zorzi','14431','Ruben Trumpelmann','2026-09-09 10:08:14'),(35,5,1,'commentary','Ruben Trumpelmann to de Zorzi, <b>wide</b>, wided again! Short ball, down leg, left alone and has been wided','RSA',NULL,1788947989858,'11196','Tony de Zorzi','14431','Ruben Trumpelmann','2026-09-09 10:08:14'),(36,5,1,'commentary','Ruben Trumpelmann to Jordan Hermann, 1 run, angled down leg, pulled down to fine leg for a single','RSA',NULL,1788947957023,'21386','Jordan Hermann','14431','Ruben Trumpelmann','2026-09-09 10:08:14'),(37,5,1,'commentary','Ruben Trumpelmann to Jordan Hermann, <b>wide</b>, angled across, outside off, left alone and has been wided. That went over the batter','RSA',NULL,1788947925881,'21386','Jordan Hermann','14431','Ruben Trumpelmann','2026-09-09 10:08:14'),(38,5,1,'commentary','Ruben Trumpelmann to Jordan Hermann, no run, banged in short, angled across, Jordan Hermann looks to pull and gets an under-edge down to the keeper','RSA',NULL,1788947884943,'21386','Jordan Hermann','14431','Ruben Trumpelmann','2026-09-09 10:08:14'),(39,5,1,'commentary','Gerhard Erasmus to de Zorzi, no run, full on off, Zorzi drives it straight to extra cover','RSA',NULL,1788947801891,'11196','Tony de Zorzi','7973','Gerhard Erasmus','2026-09-09 10:08:14'),(40,5,1,'commentary','Gerhard Erasmus to Jordan Hermann, 1 run, full around off, Hermann strokes it down to long-off','RSA',NULL,1788947789188,'21386','Jordan Hermann','7973','Gerhard Erasmus','2026-09-09 10:08:14'),(41,5,1,'commentary','Bernard Scholtz to Jordan Hermann, 1 run, to long-off','RSA',NULL,1788948727622,'21386','Jordan Hermann','10769','Bernard Scholtz','2026-09-09 10:12:27'),(42,5,1,'commentary','Bernard Scholtz to Jordan Hermann, no run','RSA',NULL,1788948686241,'21386','Jordan Hermann','10769','Bernard Scholtz','2026-09-09 10:12:27'),(43,5,1,'commentary','Bernard Scholtz to Dewald Brevis, 1 run, tossed up delivery, outside off, patted down into the off-side for a single','RSA',NULL,1788948650335,'20538','Dewald Brevis','10769','Bernard Scholtz','2026-09-09 10:12:27'),(44,5,1,'commentary','Bernard Scholtz to Dewald Brevis, no run, angled in, arm ball, Dewald Brevis punches it down to cover','RSA',NULL,1788948624389,'20538','Dewald Brevis','10769','Bernard Scholtz','2026-09-09 10:12:27'),(45,5,1,'commentary','Bernard Scholtz to Dewald Brevis, no run, on the sticks, Dewald Brevis defends it back to the bowler','RSA',NULL,1788948607211,'20538','Dewald Brevis','10769','Bernard Scholtz','2026-09-09 10:12:27'),(46,5,1,'commentary','Bernard Scholtz to Dewald Brevis, <b>SIX</b>, straight down the ground for a sixer. That was a tossed up delivery, Dewald Brevis got under the ball and lofted it over the ropes','RSA',NULL,1788948584415,'20538','Dewald Brevis','10769','Bernard Scholtz','2026-09-09 10:12:27'),(47,5,1,'commentary','<b>Bernard Scholtz [4.0-0-30-0] is back into the attack</b>','RSA',NULL,1788948581463,'20538','Dewald Brevis','10769','Bernard Scholtz','2026-09-09 10:12:27');
/*!40000 ALTER TABLE `commentary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `countries`
--

DROP TABLE IF EXISTS `countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `countries` (
  `country_id` int NOT NULL AUTO_INCREMENT,
  `country_name` varchar(100) NOT NULL,
  `iso_code` varchar(3) NOT NULL,
  PRIMARY KEY (`country_id`),
  UNIQUE KEY `country_name` (`country_name`),
  UNIQUE KEY `iso_code` (`iso_code`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `countries`
--

LOCK TABLES `countries` WRITE;
/*!40000 ALTER TABLE `countries` DISABLE KEYS */;
INSERT INTO `countries` VALUES (1,'India','IND'),(2,'Australia','AUS'),(3,'England','ENG'),(4,'New Zealand','NZL'),(5,'South Africa','SA'),(6,'Pakistan','PAK'),(7,'Sri Lanka','SL'),(8,'Bangladesh','BAN'),(9,'West Indies','WI'),(10,'Afghanistan','AFG'),(11,'Namibia','NAM');
/*!40000 ALTER TABLE `countries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fielding_performance`
--

DROP TABLE IF EXISTS `fielding_performance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fielding_performance` (
  `innings_id` int NOT NULL,
  `player_id` int NOT NULL,
  `catches` int NOT NULL DEFAULT '0',
  `stumpings` int NOT NULL DEFAULT '0',
  `runouts` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`innings_id`,`player_id`),
  KEY `fk_fielding_player` (`player_id`),
  CONSTRAINT `fk_fielding_innings` FOREIGN KEY (`innings_id`) REFERENCES `innings` (`innings_id`),
  CONSTRAINT `fk_fielding_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fielding_performance`
--

LOCK TABLES `fielding_performance` WRITE;
/*!40000 ALTER TABLE `fielding_performance` DISABLE KEYS */;
INSERT INTO `fielding_performance` VALUES (1,2,1,0,0),(1,3,2,0,1),(2,4,1,0,0),(3,2,2,0,0),(4,5,1,0,1),(5,3,1,0,0),(6,2,1,0,1);
/*!40000 ALTER TABLE `fielding_performance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `formats`
--

DROP TABLE IF EXISTS `formats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `formats` (
  `format_id` int NOT NULL AUTO_INCREMENT,
  `format_name` varchar(20) NOT NULL,
  PRIMARY KEY (`format_id`),
  UNIQUE KEY `format_name` (`format_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `formats`
--

LOCK TABLES `formats` WRITE;
/*!40000 ALTER TABLE `formats` DISABLE KEYS */;
INSERT INTO `formats` VALUES (2,'ODI'),(3,'T20I'),(1,'Test');
/*!40000 ALTER TABLE `formats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `innings`
--

DROP TABLE IF EXISTS `innings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `innings` (
  `innings_id` int NOT NULL AUTO_INCREMENT,
  `match_id` int NOT NULL,
  `innings_number` int NOT NULL,
  `batting_team_id` int NOT NULL,
  `bowling_team_id` int NOT NULL,
  `total_runs` int NOT NULL DEFAULT '0',
  `total_wickets` int NOT NULL DEFAULT '0',
  `total_balls` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`innings_id`),
  UNIQUE KEY `uq_innings_match_number` (`match_id`,`innings_number`),
  KEY `fk_innings_batting_team` (`batting_team_id`),
  KEY `fk_innings_bowling_team` (`bowling_team_id`),
  CONSTRAINT `fk_innings_batting_team` FOREIGN KEY (`batting_team_id`) REFERENCES `teams` (`team_id`),
  CONSTRAINT `fk_innings_bowling_team` FOREIGN KEY (`bowling_team_id`) REFERENCES `teams` (`team_id`),
  CONSTRAINT `fk_innings_match` FOREIGN KEY (`match_id`) REFERENCES `matches` (`match_id`),
  CONSTRAINT `chk_different_innings_teams` CHECK ((`batting_team_id` <> `bowling_team_id`))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `innings`
--

LOCK TABLES `innings` WRITE;
/*!40000 ALTER TABLE `innings` DISABLE KEYS */;
INSERT INTO `innings` VALUES (1,1,1,1,2,450,8,540),(2,1,2,2,1,300,10,480),(3,2,1,1,2,280,6,300),(4,2,2,2,1,281,5,276),(5,3,1,2,1,181,3,120),(6,3,2,1,2,180,7,120),(7,5,1,5,11,226,2,216);
/*!40000 ALTER TABLE `innings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `match_teams`
--

DROP TABLE IF EXISTS `match_teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `match_teams` (
  `match_id` int NOT NULL,
  `team_id` int NOT NULL,
  `batting_first` tinyint(1) NOT NULL DEFAULT '0',
  `team_score` int DEFAULT NULL,
  `team_wickets` int DEFAULT NULL,
  PRIMARY KEY (`match_id`,`team_id`),
  KEY `fk_match_teams_team` (`team_id`),
  CONSTRAINT `fk_match_teams_match` FOREIGN KEY (`match_id`) REFERENCES `matches` (`match_id`),
  CONSTRAINT `fk_match_teams_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `match_teams`
--

LOCK TABLES `match_teams` WRITE;
/*!40000 ALTER TABLE `match_teams` DISABLE KEYS */;
INSERT INTO `match_teams` VALUES (1,1,1,450,8),(1,2,0,300,10),(2,1,1,280,6),(2,2,0,281,5),(3,1,0,180,7),(3,2,1,181,3),(4,1,1,587,6),(4,10,0,133,10),(5,5,1,226,2),(5,11,0,NULL,NULL);
/*!40000 ALTER TABLE `match_teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matches`
--

DROP TABLE IF EXISTS `matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matches` (
  `match_id` int NOT NULL AUTO_INCREMENT,
  `series_id` int DEFAULT NULL,
  `format_id` int NOT NULL,
  `venue_id` int DEFAULT NULL,
  `description` varchar(255) NOT NULL,
  `match_date` datetime NOT NULL,
  `status` varchar(20) NOT NULL,
  `toss_winner_team_id` int DEFAULT NULL,
  `toss_decision` varchar(10) DEFAULT NULL,
  `winner_team_id` int DEFAULT NULL,
  `win_margin_value` decimal(10,2) DEFAULT NULL,
  `win_margin_type` varchar(20) DEFAULT NULL,
  `api_match_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`match_id`),
  UNIQUE KEY `api_match_id` (`api_match_id`),
  KEY `fk_matches_series` (`series_id`),
  KEY `fk_matches_format` (`format_id`),
  KEY `fk_matches_venue` (`venue_id`),
  KEY `fk_matches_toss_winner` (`toss_winner_team_id`),
  KEY `fk_matches_winner` (`winner_team_id`),
  CONSTRAINT `fk_matches_format` FOREIGN KEY (`format_id`) REFERENCES `formats` (`format_id`),
  CONSTRAINT `fk_matches_series` FOREIGN KEY (`series_id`) REFERENCES `series` (`series_id`),
  CONSTRAINT `fk_matches_toss_winner` FOREIGN KEY (`toss_winner_team_id`) REFERENCES `teams` (`team_id`),
  CONSTRAINT `fk_matches_venue` FOREIGN KEY (`venue_id`) REFERENCES `venues` (`venue_id`),
  CONSTRAINT `fk_matches_winner` FOREIGN KEY (`winner_team_id`) REFERENCES `teams` (`team_id`),
  CONSTRAINT `chk_margin_type` CHECK (((`win_margin_type` in (_cp850'Runs',_cp850'Wickets')) or (`win_margin_type` is null))),
  CONSTRAINT `chk_match_status` CHECK ((`status` in (_cp850'Scheduled',_cp850'Live',_cp850'Completed',_cp850'Abandoned'))),
  CONSTRAINT `chk_toss_decision` CHECK (((`toss_decision` in (_cp850'Bat',_cp850'Field')) or (`toss_decision` is null)))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matches`
--

LOCK TABLES `matches` WRITE;
/*!40000 ALTER TABLE `matches` DISABLE KEYS */;
INSERT INTO `matches` VALUES (1,1,1,3,'India vs Australia, 1st Test','2026-01-02 09:30:00','Completed',1,'Bat',1,150.00,'Runs','match_001'),(2,2,2,2,'India vs Australia, 1st ODI','2026-02-02 14:00:00','Completed',2,'Field',1,5.00,'Wickets','match_002'),(3,3,3,1,'India vs Australia, 1st T20I','2026-03-02 19:00:00','Completed',1,'Field',2,7.00,'Wickets','match_003'),(4,4,1,NULL,'One-off Test - India vs Afghanistan - India won by an innings and 300 runs','2026-06-05 09:30:00','Completed',1,'Bat',1,300.00,'Runs','148382'),(5,5,2,NULL,'1st ODI - South Africa vs Namibia','2026-09-09 13:00:00','Live',11,'Field',NULL,NULL,NULL,'169980');
/*!40000 ALTER TABLE `matches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partnerships`
--

DROP TABLE IF EXISTS `partnerships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partnerships` (
  `innings_id` int NOT NULL,
  `partnership_number` int NOT NULL,
  `player1_id` int NOT NULL,
  `player2_id` int NOT NULL,
  `player1_position` int NOT NULL,
  `player2_position` int NOT NULL,
  `partnership_runs` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`innings_id`,`partnership_number`),
  KEY `fk_partnership_player1` (`player1_id`),
  KEY `fk_partnership_player2` (`player2_id`),
  CONSTRAINT `fk_partnership_innings` FOREIGN KEY (`innings_id`) REFERENCES `innings` (`innings_id`),
  CONSTRAINT `fk_partnership_player1` FOREIGN KEY (`player1_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `fk_partnership_player2` FOREIGN KEY (`player2_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `chk_partnership_players` CHECK ((`player1_id` <> `player2_id`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partnerships`
--

LOCK TABLES `partnerships` WRITE;
/*!40000 ALTER TABLE `partnerships` DISABLE KEYS */;
INSERT INTO `partnerships` VALUES (1,1,1,2,1,2,180),(2,1,5,4,1,2,95),(3,1,1,2,1,2,150),(4,1,5,4,1,2,140),(5,1,5,4,1,2,110),(6,1,1,2,1,2,125);
/*!40000 ALTER TABLE `partnerships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `players` (
  `player_id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(150) NOT NULL,
  `role_id` int NOT NULL,
  `national_team_id` int NOT NULL,
  `batting_style` varchar(50) DEFAULT NULL,
  `bowling_style` varchar(50) DEFAULT NULL,
  `api_player_id` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`player_id`),
  UNIQUE KEY `api_player_id` (`api_player_id`),
  KEY `fk_players_role` (`role_id`),
  KEY `fk_players_team` (`national_team_id`),
  CONSTRAINT `fk_players_role` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`),
  CONSTRAINT `fk_players_team` FOREIGN KEY (`national_team_id`) REFERENCES `teams` (`team_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
INSERT INTO `players` VALUES (1,'Virat Kohli',1,1,'Right-hand Bat',NULL,'sample_001',1),(2,'Rohit Sharma',1,1,'Right-hand Bat',NULL,'sample_002',1),(3,'Jasprit Bumrah',2,1,'Right-hand Bat','Right-arm Fast','sample_003',1),(4,'Pat Cummins',2,2,'Right-hand Bat','Right-arm Fast','sample_004',1),(5,'Steve Smith',1,2,'Right-hand Bat','Right-arm Leg Break','sample_005',1),(6,'Jordan Hermann',1,5,NULL,NULL,'21386',1),(7,'Tony de Zorzi',1,5,NULL,NULL,'11196',1),(8,'Ruben Trumpelmann',2,11,NULL,NULL,'14431',1),(9,'Gerhard Erasmus',3,11,NULL,NULL,'7973',1);
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(30) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (3,'All-rounder'),(1,'Batsman'),(2,'Bowler'),(4,'Wicketkeeper');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `series`
--

DROP TABLE IF EXISTS `series`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `series` (
  `series_id` int NOT NULL AUTO_INCREMENT,
  `series_name` varchar(200) NOT NULL,
  `host_country_id` int NOT NULL,
  `format_id` int NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `total_matches_planned` int DEFAULT NULL,
  `api_series_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`series_id`),
  UNIQUE KEY `api_series_id` (`api_series_id`),
  KEY `fk_series_country` (`host_country_id`),
  KEY `fk_series_format` (`format_id`),
  CONSTRAINT `fk_series_country` FOREIGN KEY (`host_country_id`) REFERENCES `countries` (`country_id`),
  CONSTRAINT `fk_series_format` FOREIGN KEY (`format_id`) REFERENCES `formats` (`format_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `series`
--

LOCK TABLES `series` WRITE;
/*!40000 ALTER TABLE `series` DISABLE KEYS */;
INSERT INTO `series` VALUES (1,'India vs Australia Test Series',1,1,'2026-01-01','2026-01-15',3,'series_001'),(2,'India vs Australia ODI Series',1,2,'2026-02-01','2026-02-10',3,'series_002'),(3,'India vs Australia T20I Series',1,3,'2026-03-01','2026-03-08',5,'series_003'),(4,'Afghanistan tour of India 2026',1,1,'2026-06-05','2026-06-08',1,'11641'),(5,'South Africa tour of Namibia, 2026',11,2,'2026-09-09','2026-09-30',3,'12943');
/*!40000 ALTER TABLE `series` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teams` (
  `team_id` int NOT NULL AUTO_INCREMENT,
  `team_name` varchar(100) NOT NULL,
  `country_id` int NOT NULL,
  `team_type` varchar(20) NOT NULL,
  PRIMARY KEY (`team_id`),
  UNIQUE KEY `team_name` (`team_name`),
  KEY `fk_teams_country` (`country_id`),
  CONSTRAINT `fk_teams_country` FOREIGN KEY (`country_id`) REFERENCES `countries` (`country_id`),
  CONSTRAINT `chk_team_type` CHECK ((`team_type` in (_cp850'International',_cp850'Domestic')))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams`
--

LOCK TABLES `teams` WRITE;
/*!40000 ALTER TABLE `teams` DISABLE KEYS */;
INSERT INTO `teams` VALUES (1,'India',1,'International'),(2,'Australia',2,'International'),(3,'England',3,'International'),(4,'New Zealand',4,'International'),(5,'South Africa',5,'International'),(6,'Pakistan',6,'International'),(7,'Sri Lanka',7,'International'),(8,'Bangladesh',8,'International'),(9,'West Indies',9,'International'),(10,'Afghanistan',10,'International'),(11,'Namibia',11,'International');
/*!40000 ALTER TABLE `teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venues`
--

DROP TABLE IF EXISTS `venues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venues` (
  `venue_id` int NOT NULL AUTO_INCREMENT,
  `venue_name` varchar(150) NOT NULL,
  `city` varchar(100) DEFAULT NULL,
  `country_id` int NOT NULL,
  `capacity` int DEFAULT NULL,
  `api_venue_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`venue_id`),
  UNIQUE KEY `api_venue_id` (`api_venue_id`),
  KEY `fk_venues_country` (`country_id`),
  CONSTRAINT `fk_venues_country` FOREIGN KEY (`country_id`) REFERENCES `countries` (`country_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venues`
--

LOCK TABLES `venues` WRITE;
/*!40000 ALTER TABLE `venues` DISABLE KEYS */;
INSERT INTO `venues` VALUES (1,'M. Chinnaswamy Stadium','Bengaluru',1,40000,'venue_001'),(2,'Wankhede Stadium','Mumbai',1,33000,'venue_002'),(3,'Narendra Modi Stadium','Ahmedabad',1,132000,'venue_003'),(4,'Melbourne Cricket Ground','Melbourne',2,100024,'venue_004'),(5,'Sydney Cricket Ground','Sydney',2,48000,'venue_005');
/*!40000 ALTER TABLE `venues` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-09 15:55:02
