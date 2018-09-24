In class, we will kick up the server and everyone may run their python scripts to compete. As of now, the only option is localhost since I could not get access to crunchy5. If professor Shasha permits, I will keep trying to make crunchy5 work.

In the meantime, everyone can start brainstorming their strategy. Below are the instructions on how to start testing.

Start up the server by running start-game.py

Ex: ./start-game.py -m 3 -p 9000 -t 120 -a '127.0.0.1' 130 4

-m is the current max -p is the port -a is the IP address -t is time per turn 130 is the starting number of stones 4 is the number of resets available per player

You can use the sample Algorithms noob_raid_boss.py and raid_boss_who_goes_second to see how the very basic algorithms work.

Also, if you want to test manually picking out stones (via for both players or for yourself vs 1 AI), you can run exp-nim with the following parameters after the server is up and running.

./exp-nim [-f] -n (name) IP:PORT

-f is if going first -n is name is IP address is PORT number
