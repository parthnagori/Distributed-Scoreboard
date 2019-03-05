# Distributed Scoreboard
## Overview

A distributed scoreboard application to keep track of player scores as well as their online status. The application uses zookeeper as a co-ordination service. The online status is maintained by ephemeral Znodes and scores are maintained in regular nodes. Player program can be used to insert/post scores to zookeeper server. Watchers display the scoreboards by implementing watches on player Znodes. The scoreboard displays n (count parameter -> default = 25) most recent scores as well as n top scores since the server has been up. 

The program expects a zookeeper service running on some IP and port that will be passed as parameters in the form IP:PORT or just IP (defualt port = 2181).


## Cloning the repo

    $ git clone https://github.ncsu.edu/pnagori/CSC_591_DIC_HW1.git

and then cd to the repo:

    $ cd CSC_591_DIC_HW1

## Dependency installation

    $ bash install.sh

## Setting up aliases

    $ source custom_bashrc

## To Run

### Player
    
    $ player <IP[:PORT]> <name> [count] [delay] [score]
   
    or
   
    $ python3 player.py <IP[:PORT]> <name> [count] [delay] [score]
    
### Watcher

    $ watcher <IP[:PORT]> <list_size>
    
    or
    
    $ python3 watcher.py <IP[:PORT]> <list_size>

Note: Ephemeral nodes have been used to maintain online status. After player exit, there's a slight delay of (5-10 seconds) in deletion of the znodes by zookeeper server, which might show the player still online for the next 5-10 seconds.
