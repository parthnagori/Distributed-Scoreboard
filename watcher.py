#!/usr/bin/python3
import os
import sys
from kazoo.client import KazooClient
from kazoo.recipe.watchers import ChildrenWatch
from kazoo.recipe.watchers import DataWatch
import pickle

#Establishing connection with the Zookeeper Server
def establish_connection(ip_port):
  zk = KazooClient(hosts=ip_port)
  zk.start()
  return zk

#Creating Base Directories:
#--->online_players for maintaining player online session
#--->score_db to maintain recent and highest scores
def establish_directories(zk):
  children = zk.get_children('/')
  if 'DIC' not in children:
    zk.create('/DIC', ephemeral=False)
    zk.create('/DIC/online_players', ephemeral=False)
    zk.create('/DIC/score_db', ephemeral=False)

#To display a score
def display_score(score):
  global online_players
  if score['name'] in online_players:
    print("{}     {} **".format(score['name'].title(), score['score']))
  else:
    print("{}     {}".format(score['name'].title(), score['score']))

#To display the most recent and highest scores
def update_scoreboard():
  global recent_scores
  global high_scores
  print("\nMost Recent Scores")
  print("-------------------")
  for score in recent_scores:
    display_score(score)

  print("\nHighest Scores")
  print("-------------------")
  for score in high_scores:
    display_score(score)

#Update the scoreboard if any player posts a new score
def scores_updated(data,stat,event=None):
  global recent_scores
  global high_scores
  if data:
    scores = pickle.loads(data)
    recent_scores = scores[0][:n]
    high_scores = scores[1][:n]
    update_scoreboard()

#Update the scoreboard if a player joins/leaves the game
def update_online_status(children):
  global online_players
  if set(children) != set(online_players):
    online_players = children
    update_scoreboard()
    
if __name__ == '__main__':
  online_players = []
  recent_scores = []
  high_scores = []
  n = 25
  default_port = "6000"
  args = sys.argv
  if len(args) == 3:
    ip_port = args[1]
    if ":" not in ip_port:
      ip_port = ip_port+":"+default_port
    if int(args[2]) < n:
      n = int(args[2])
    zk = establish_connection(ip_port)
    establish_directories(zk)
    ChildrenWatch(zk, '/DIC/online_players', func=update_online_status)
    DataWatch(zk, '/DIC/score_db', func=scores_updated)
    while(True):
      pass
  else:
    print("Please provide the correct arguments in the form: $python3 watcher.py <IP:PORT> <Number of records>")



  
