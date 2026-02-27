CREATE DATABASE IPL_database

CREATE TABLE Teams (
    team_id INT IDENTITY(1,1) PRIMARY KEY,
    team_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Players (
    player_id INT IDENTITY(1,1) PRIMARY KEY,
    player_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Venues (
    venue_id INT IDENTITY(1,1) PRIMARY KEY,
    venue_name VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE Matches (
    match_id VARCHAR(50) PRIMARY KEY,
    season INT NOT NULL,
    match_date DATE NOT NULL,
    team1_id INT FOREIGN KEY REFERENCES Teams(team_id),
    team2_id INT FOREIGN KEY REFERENCES Teams(team_id),
    venue_id INT FOREIGN KEY REFERENCES Venues(venue_id),
    toss_winner_id INT,
    toss_decision VARCHAR(10),
    winner_id INT
);

CREATE TABLE Deliveries (
    delivery_id BIGINT IDENTITY(1,1) PRIMARY KEY,

    match_id VARCHAR(50) NOT NULL,
    inning INT NOT NULL,
    over_number INT NOT NULL,
    ball_number INT NOT NULL,

    batting_team_id INT NOT NULL,

    batter_id INT NOT NULL,
    bowler_id INT NOT NULL,

    runs_batter INT DEFAULT 0,
    runs_extras INT DEFAULT 0,
    total_runs INT DEFAULT 0,

    wides INT DEFAULT 0,
    noballs INT DEFAULT 0,
    byes INT DEFAULT 0,
    legbyes INT DEFAULT 0,

    is_wicket BIT DEFAULT 0,
    dismissal_type VARCHAR(50),
    player_out_id INT,
    fielder_id INT,

    FOREIGN KEY (match_id) REFERENCES Matches(match_id),
    FOREIGN KEY (batting_team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (batter_id) REFERENCES Players(player_id),
    FOREIGN KEY (bowler_id) REFERENCES Players(player_id),
    FOREIGN KEY (player_out_id) REFERENCES Players(player_id),
    FOREIGN KEY (fielder_id) REFERENCES Players(player_id)
);

CREATE INDEX idx_match ON Deliveries(match_id);
CREATE INDEX idx_batter ON Deliveries(batter_id);
CREATE INDEX idx_bowler ON Deliveries(bowler_id);
CREATE INDEX idx_batting_team ON Deliveries(batting_team_id);

CREATE TABLE Player_Match_Summary (
    player_id INT NOT NULL,
    match_id VARCHAR(50) NOT NULL,
    team_id INT NOT NULL,

    runs INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    fours INT DEFAULT 0,
    sixes INT DEFAULT 0,
    strike_rate FLOAT DEFAULT 0,

    wickets INT DEFAULT 0,
    legal_balls INT DEFAULT 0,
    runs_conceded INT DEFAULT 0,
    economy FLOAT DEFAULT 0,

    catches INT DEFAULT 0,

    PRIMARY KEY (player_id, match_id),

    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (match_id) REFERENCES Matches(match_id),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
);