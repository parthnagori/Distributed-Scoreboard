# CSC_591_DIC_HW1
Distributed Scoreboard


## Cloning the repo

    $ git clone https://github.ncsu.edu/pnagori/CSC_591_DIC_HW1.git

and then cd to the repo:

    $ cd CSC_591_DIC_HW1

## Dependency installation

    $ bash install.sh

## To Run

### Player
    
    $ python3 player.py <IP[:PORT]> <name> [count] [delay] [score]
    
### Watcher

    $ python3 watcher.py <IP[:PORT]> <list_size>

Note: Ephemeral nodes have been used to maintain online status. After player exit, there's a slight delay of (5-10 seconds) in deletion of the znodes by zookeeper server, which might show the player still online for the next 5-10 seconds.
