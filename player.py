import os
import sys
from kazoo.client import KazooClient
import random
import pickle
import time

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

#To get list of currently online players
def get_online_players(zk):
  return zk.get_children('/DIC/online_players')

#Post a score to the server for the current player
def post_score(zk, name, curr_score):
  data, stat = zk.get('DIC/score_db')
  scores = [[],[]]
  if data:
    scores = pickle.loads(data)
  scores[0].insert(0, {'name': name, 'score': curr_score})
  scores[0] = scores[0][:25]
  scores[1].insert(0, {'name': name, 'score': curr_score})
  scores[1] = sorted(scores[1], key=lambda k: k['score'], reverse=True)[:25]

  zk.set('DIC/score_db', pickle.dumps(scores))

#Create online session for current player
def go_online(zk, name):
  zk.create('DIC/online_players/'+name, ephemeral=True)

#Join and start playing the game with current player
def join(zk,name,count=None,delay=None,score=None):
  if name in get_online_players(zk):
    print("Player already online")
    exit(0)
  else:
    go_online(zk, name)
  if count:
    delays = [int(abs(random.normalvariate(delay,2))) for i in range(count)]
    scores = [int(abs(random.normalvariate(score,5))) for i in range(count)]
    i=0
    while (i < count):
      post_score(zk, name, scores[i])
      time.sleep(delays[i])
      i+=1
  else:
    while(True):
      print("Please enter a score for {}".format(name))
      try:
        curr_score = int(input())
        if curr_score < 0:
          continue
        post_score(zk, name, curr_score)
      except ValueError:
        print("Score is not a valid integer.")
      
if __name__ == '__main__':
  count=None
  delay=None
  score=None
  default_port = "6000"

  args = sys.argv
  # print(args)
  if len(args) < 3:
    print("Please provide atleast the IP:Port and Player Name")
    exit(0)
  elif len(args) >= 3:
    ip_port = args[1]
    if ":" not in ip_port:
      ip_port = ip_port+":"+default_port
    name = args[2].lower()
    if len(args) == 6:
      count = int(args[3])
      delay = int(args[4])
      score = int(args[5])
    zk = establish_connection(ip_port)
    establish_directories(zk)
    join(zk,name,count,delay,score)
  else:
    print("Invalid input format.")
    exit(0)     
 
  


