-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournaments;
CREATE TABLE players(ID int Primary Key, name varchar(40));
CREATE TABLE match(matchID int Primary Key, player1 int REFERENCES players(ID), player2 int REFERENCES players(ID), winner int REFERENCES players(ID));
CREATE TABLE tournaments(tournamentID int Primat Key, name varchar(40));
CREATE TABLE tourMatch(tournamentID int REFERENCES tournaments,matchID int REFERENCES int match); 
CREATE TABLE matchWins(matchID int REFERENCES int match);

--id, name, wins, matches

select p.ID, p.name, (select count(*) from match where m.winner  = p.id or m.loaser = p.id ) as 'Matches', 
(select count(*) from match where m.winner  = p.id) as 'Wins'
from players p

create PROCEDURE swissPairings     
AS
DECLARE @playerStandings(
	ID  serial,
	name varchar(40),
	wins int
)
insert into @playerStandings(ID, name, wins)
select ID, name, (select count(*) from match where ID = winner) 'wins' 
from players

select p1.ID, p1.name, p2.ID, p2,name
from (select ID, name, (select count(*) from match where ID = winner) 'wins' 
from players) p1
inner join (select ID, name, (select count(*) from match where ID = winner) 'wins' 
from players) p2 on p1.wins = p2.wins
where p1.ID < p2.ID







