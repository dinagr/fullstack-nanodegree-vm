#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import math

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect();
    c = DB.cursor();
    c.execute("delete from match");
    DB.commit()
    DB.close();

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect();
    c = DB.cursor();
    c.execute("delete from players");
    DB.commit()
    DB.close();

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect();
    c = DB.cursor();
    c.execute("select count(*) from players");
    result = c.fetchone()[0];
    print (result);
    DB.close();
    return result;

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect();
    c = DB.cursor();
    c.execute("insert into players(name) values(%s)", (name,));
    DB.commit()
    DB.close();

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect();
    c = DB.cursor();
    # Get the matches where the player won and all the matches he participated
    # Order by the number of wins descending
    c.execute("select p.ID, p.name,"
              "(select count(*) from match where winner  = p.id) \"wins\","
              "(select count(*) from match where p.id in (loser,winner)) \"matches\""
              "from players p "
              "order by 3 desc");
    resultList = c.fetchall();
    DB.close();
    return resultList;

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect();
    c = DB.cursor();
    c.execute("insert into match(winner, loser) values(%s, %s)", (winner, loser,));
    DB.commit()
    DB.close();
    

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """         
    DB = connect();
    c = DB.cursor();
    # Join between all the players that had the same amount of wins
    # Create pairs from these players
    c.execute("select p1.ID, p1.name, p2.ID, p2.name "
              "from (select ID, name, (select count(*) "
              "from match where ID = winner) \"wins\" " 
              "from players) p1 "
              "inner join (select ID, name, (select count(*) "
              "from match where ID = winner) \"wins\" " 
              "from players) p2 on p1.wins = p2.wins "
              "where p1.ID < p2.ID");
    pairs = c.fetchall();
    DB.close();
    return pairs;

    

