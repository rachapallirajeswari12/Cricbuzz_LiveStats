-- Cricbuzz LiveStats Sample Data

-- Teams
INSERT INTO teams (team_name, country) VALUES
('India', 'India'),
('Australia', 'Australia'),
('England', 'England'),
('South Africa', 'South Africa'),
('New Zealand', 'New Zealand'),
('Pakistan', 'Pakistan'),
('Sri Lanka', 'Sri Lanka'),
('West Indies', 'West Indies');

-- Players
INSERT INTO players
(player_name, team_id, playing_role, batting_style, bowling_style)
VALUES
('Virat Kohli', 1, 'Batsman', 'Right-hand bat', 'Right-arm medium'),
('Rohit Sharma', 1, 'Batsman', 'Right-hand bat', 'Right-arm off break'),
('Jasprit Bumrah', 1, 'Bowler', 'Right-hand bat', 'Right-arm fast'),
('Ravindra Jadeja', 1, 'All-rounder', 'Left-hand bat', 'Slow left-arm orthodox'),
('Pat Cummins', 2, 'Bowler', 'Right-hand bat', 'Right-arm fast'),
('Steve Smith', 2, 'Batsman', 'Right-hand bat', 'Right-arm leg break'),
('Jos Buttler', 3, 'Wicket-keeper', 'Right-hand bat', 'Right-arm medium'),
('Joe Root', 3, 'Batsman', 'Right-hand bat', 'Right-arm off break'),
('Kagiso Rabada', 4, 'Bowler', 'Right-hand bat', 'Right-arm fast'),
('Kane Williamson', 5, 'Batsman', 'Right-hand bat', 'Right-arm off break'),
('Babar Azam', 6, 'Batsman', 'Right-hand bat', 'Right-arm off break'),
('Wanindu Hasaranga', 7, 'All-rounder', 'Right-hand bat', 'Right-arm leg break');

-- Venues
INSERT INTO venues
(venue_name, city, country, capacity)
VALUES
('Narendra Modi Stadium', 'Ahmedabad', 'India', 132000),
('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
('Eden Gardens', 'Kolkata', 'India', 68000),
('Lord''s Cricket Ground', 'London', 'England', 31100),
('Newlands Cricket Ground', 'Cape Town', 'South Africa', 25000),
('Wankhede Stadium', 'Mumbai', 'India', 33000);

-- Series
INSERT INTO series
(series_name, host_country, match_type, start_date, total_matches)
VALUES
('India vs Australia Series', 'India', 'ODI', '2024-01-01', 5),
('England vs New Zealand Series', 'England', 'Test', '2024-02-01', 3),
('South Africa vs India Series', 'South Africa', 'T20I', '2024-03-01', 4);