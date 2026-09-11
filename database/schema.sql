-- Cricbuzz LiveStats Database Schema

CREATE TABLE teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(100)
);

CREATE TABLE players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name VARCHAR(100) NOT NULL,
    team_id INTEGER,
    playing_role VARCHAR(50),
    batting_style VARCHAR(50),
    bowling_style VARCHAR(100),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE venues (
    venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INTEGER
);

CREATE TABLE series (
    series_id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name VARCHAR(200) NOT NULL,
    host_country VARCHAR(100),
    match_type VARCHAR(50),
    start_date DATE,
    total_matches INTEGER
);

CREATE TABLE matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_description VARCHAR(250),
    team1_id INTEGER,
    team2_id INTEGER,
    winning_team_id INTEGER,
    venue_id INTEGER,
    match_date DATE,
    match_type VARCHAR(50),
    toss_winner_id INTEGER,
    toss_decision VARCHAR(20),
    victory_margin INTEGER,
    victory_type VARCHAR(20),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (winning_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id)
);

CREATE TABLE batting_stats (
    batting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    player_id INTEGER,
    runs INTEGER DEFAULT 0,
    balls_faced INTEGER DEFAULT 0,
    fours INTEGER DEFAULT 0,
    sixes INTEGER DEFAULT 0,
    strike_rate DECIMAL(6,2),
    batting_position INTEGER,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

CREATE TABLE bowling_stats (
    bowling_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    player_id INTEGER,
    overs DECIMAL(5,1) DEFAULT 0,
    runs_conceded INTEGER DEFAULT 0,
    wickets INTEGER DEFAULT 0,
    economy_rate DECIMAL(6,2),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

CREATE TABLE fielding_stats (
    fielding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    player_id INTEGER,
    catches INTEGER DEFAULT 0,
    stumpings INTEGER DEFAULT 0,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);