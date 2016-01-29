-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournaments;
CREATE TABLE players(ID serial Primary Key, name varchar(40));
CREATE TABLE match(matchID serial Primary Key, winner int REFERENCES players(ID), loser int REFERENCES players(ID));
CREATE TABLE tournaments(tournamentID serial Primat Key, name varchar(40));
CREATE TABLE tourMatch(tournamentID int REFERENCES tournaments,matchID int REFERENCES int match); 









