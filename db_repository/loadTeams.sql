BEGIN TRANSACTION;

INSERT INTO 'team' ('id', 'city', 'name') VALUES ('ARI','Arizona','Cardinals');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('ATL','Atlanta','Falcons');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('BAL','Baltimore','Ravens');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('BUF','Buffalo','Bills');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('CAR','Carolina','Panthers');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('CHI','Chicago','Bears');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('CIN','Cincinnati','Bengals');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('CLE','Cleveland','Browns');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('DAL','Dallas','Cowboys');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('DEN','Denver','Broncos');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('DET','Detroit','Lions');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('GB','Green Bay','Packers');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('HOU','Houston','Texans');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('IND','Indianapolis','Colts');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('JAX','Jacksonville','Jaguars');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('KC','Kansas City','Chiefs');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('LA','Los Angeles','Rams');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('MIA','Miami','Dolphins');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('MIN','Minnesota','Vikings');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('NE','New England','Patriots');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('NO','New Orleans','Saints');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('NYG','New York','Giants');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('NYJ','New York','Jets');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('OAK','Oakland','Raiders');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('PHI','Philadelphia','Eagles');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('PIT','Pittsburgh','Steelers');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('SD','San Diego','Chargers');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('SEA','Seattle','Seahawks');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('SF','San Francisco','49ers');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('TB','Tampa Bay','Buccaneers');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('TEN','Tennessee','Titans');
INSERT INTO 'team' ('id', 'city', 'name') VALUES ('WAS','Washington','Redskins');

UPDATE team set losses = 0, wins = 0, ties = 0;

COMMIT;
