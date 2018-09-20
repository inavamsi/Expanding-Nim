In class, we will kick up the server and everyone may run their python scripts to compete. As of now, the only option is localhost since I could not get access to crunchy5. If professor Shasha permits, I will keep trying to make crunchy5 work.

In the meantime, everyone can start brainstorming their strategy. Below are the instructions on how to start testing.

Start up the server by running start-game.py

Ex: ./start-game.py -m 3 -p 9000 -t 120 -a '127.0.0.1' 130 4

-m is the current max -p is the port -a is the IP address -t is time per turn 130 is the starting number of stones 4 is the number of resets available per player

You can use the sample Algorithms noob_raid_boss.py and raid_boss_who_goes_second to see how the very basic algorithms work.

Also, if you want to test manually picking out stones (via for both players or for yourself vs 1 AI), you can run exp-nim with the following parameters after the server is up and running.

./exp-nim [-f] -n (name) IP:PORT

-f is if going first -n is name is IP address is PORT number

To enter a move, you provide 2 integers in the following format.

%d %d

The first integer must be a positive integer that is either within the range of the init_max or current_max + 1.
The second integer represents if a reset will be used. 0 = false, any other integer = true.

Don't forget the following conditions will cause the opponent to automatically win:
- invalid integer input (greater than reset)
- trying to use a reset when you do not have one left
- time runs out
- trying to go out of turn

Note: 
Due to the confusion with current max, this is what the class page states:

*******************************************************************************************
currentmax starts at 0. In the course of play, currentmax = max value anyone has used.

The first player can take up to three (1, 2, or 3).

At any later point in play,

call the maximum that any previous player has taken <i> currentmax </i>.

Initially currentmax has the value 0.

At any later turn, a player may take (i) 1, 2, or 3 if a reset

has been imposed by the other player in the immediately preceding

turn

(ii) up to a maximum of 3 and 1 + currentmax, otherwise.
*******************************************************************************************

Here is an example:

Player 1 takes 1 stone : current_max = 1
Player 2 takes 3 stones: current_max = 3
This is legal because the player may take a maximum of 3 stones

Player 1 takes 1 stone: current_max = 1
Player 2 takes 4 stones: illegal
This is illegal because the previous current_max is 1. The input 4 breaks both the conditions (i) and (ii).

The reset specifiction is the following:
*******************************************************************************************
The reset option permits a team after making its move to force the maximum number of stones that can be removed in the next turn for the other team (and in the next turn only) to be three again.
*******************************************************************************************

When a reset is used, the current_max will be set to (init_max - 1), which is because players are allowed to take 1 more than the current max. That means you will see for the turn that the reset was used, the current_max as 2. !!!Don't let this confuse you!!!

For instance: let's say current_max = 42 at this point in the game

Player 1 takes 43 stones: current_max = 43
Player 2 takes 44 stones uses reset: current_max = 2, tmp_current_max = 44
Player 1 takes 3 stones: current_max = 44 (it goes back to the non-reset value)
This is legal

Player 1 takes 43 stones: current_max = 43
Player 2 takes 44 stones uses reset: current_max = 2, tmp_current_max = 44
Player 1 takes 4 stones: current_max = 44 (it goes back to the non-reset value)
This is illegal because the user broke rule (ii)



