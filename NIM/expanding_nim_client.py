#!/usr/bin/python3
# -*- coding: utf-8 -*-

import atexit
import time
import argparse
from client import Client
import random
import sys
import os
import math
import time
import json
import socket

# # -*- coding: utf-8 -*-
# """This file contains the client class used by the Expanding Nim game

# This class can either be instantiated and used in Python or controlled
# via the command line.

# @author: Munir Contractor <mmc691@nyu.edu>
# """

# initial_game_status_displayed = False

# class Client():
#     """The client class for the Expanding Nim game"""

#     DATA_SIZE = 1024

#     def __init__(self, name, goes_first, server_address):
#         """
#         Args:
#             **name:** The name you want to give your player\n
#             **goes_first:** Boolean indicator whether you take the first move
#             or not\n
#             **server_address:** A tuple of the form (address, port) of the
#             server
#         """

#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.socket.connect(server_address)
#         self.__order = 0 if goes_first else 1
#         self.__send_json({'name': name, 'order': self.__order})
#         init_status = self.receive_move()
#         self.init_stones = init_status['init_stones']
#         self.init_resets = init_status['init_resets']
#     def close(self):
#         self.socket.close()

#     def __del__(self):
#         self.close()

#     def __send_json(self, json_object):
#         """Helper method to send an object to the server as JSON"""
#         self.socket.sendall(bytes(json.dumps(json_object), 'utf-8'))

#     def make_move(self, num_stones, reset=False):
#         """Sends your move to the server and waits for the opponent to move

#         The return value is dict containing the keys as follows:
#             ``finished``: Boolean indicator whether the game is over or not\n
#             ``stones_left``: Stones left in the game\n
#             ``current_max``: New current max value\n
#             ``reset_used``: Boolean indicator (should be same as input)\n
#             ``stones_removed``: Number of stones removed (should match
#             the input)\n
#         If  the ``finished`` indicator evaluates to ``True``, two extra keys,
#         ``winner`` and ``reason`` will be included to indicate the winning
#         player and the reason for the win.

#         Args:
#             **num_stones:** The number of stones to remove.\n
#             **reset:** Boolean indicator whether you want to use reset or not.

#         Return:
#             A dict containing the keys described above
#         """
#         self.__send_json({'order': self.__order, 'num_stones': num_stones,
#                           'reset': reset})
#         return self.receive_move()

#     def receive_move(self):
#         """Receives a move and the state of the game after the move

#         The return value is dict containing the keys as follows:
#             ``finished``: Boolean indicator whether the game is over or not\n
#             ``stones_left``: Stones left in the game\n
#             ``current_max``: New current max value\n
#             ``reset_used``: Boolean indicator whether reset was used in the
#             move\n
#             ``stones_removed``: Number of stones removed in the move\n
#         If  the ``finished`` indicator evaluates to ``True``, two extra keys,
#         ``winner`` and ``reason`` will be included to indicate the winning
#         player and the reason for the win.

#         Return:
#             A dict containing the keys described above
#         """
#         # try:
#         message_string = json.loads(self.socket.recv(self.DATA_SIZE).decode('utf-8'))
#         # except:
#             # import pdb; pdb.set_trace()

#         global initial_game_status_displayed

#         if not initial_game_status_displayed:
#             initial_game_status_displayed = True
#             print("Game mode\n%d stones and %d resets\nGood luck have fun!" % (message_string['init_stones'], message_string['init_resets']))

#         return message_string

#     def __read_move(self):
#         try:
#             move = input('Please enter your move: ').split(' ')
#             return int(move[0]), bool(int(move[1]))
#         except Exception:
#             print('Invalid move string')
#             return self.__read_move()

#     def send_move(self):
#         """Reads a move from stdin and sends it to the server

#         The move has to be in the form '%d %d' where the first number
#         is the number of stones to remove and second number is a boolean
#         flag for whether reset should be done. The move and the result
#         are printed out.
#         """
#         move = self.__read_move()
#         status = self.make_move(move[0], move[1])

#         print('You took %d stones%s' % (move[0],
#               ' and used reset.' if move[1] else '.'))
#         print('Current max: %d' % status['current_max'])
#         print('Stones left: %d' % status['stones_left'])
#         print('Player %s has %d resets left' % (status['player_0']['name'], status['player_0']['resets_left']))
#         print('Player %s has %d resets left' % (status['player_1']['name'], status['player_1']['resets_left']))
#         print('---------------------------------------')
#         if status['finished']:
#             print('Game over\n%s' % status['reason'])
#             exit(0)

#     def get_move(self):
#         """Gets the move made by the opponent and prints it out"""
#         status = self.receive_move()
#         print('Opponent took %d stones%s' % (status['stones_removed'],
#               ' and used reset.' if status['reset_used'] else '.'))
#         print('Current max: %d' % status['current_max'])
#         print('Stones left: %d' % status['stones_left'])
#         print('Player %s has %d resets left' % (status['player_0']['name'], status['player_0']['resets_left']))
#         print('Player %s has %d resets left' % (status['player_1']['name'], status['player_1']['resets_left']))
#         print('---------------------------------------')
#         if status['finished']:
#             print('Game over\n%s' % status['reason'])
#             exit(0)

#0: reset; 1: not rest
#mem denote the result state of after playing 1 means after move wins; -1 means after move lose
class DecisionMaker():
    def __init__(self):
           pass
           #self.mem = [[[[1/2 for _ in range(2)] for _ in range(4)] for _ in range(4)]for _ in range(1001)]
           #init
           #for i in range(2):
           #       for x in range(4):
           #           for y in range(4):
           #               self.mem[0][x][y][i] = 1
           #               self.mem[1][x][y][i] = 0
           #               self.mem[2][x][y][i] = 0
           #               self.mem[3][x][y][i] = 0
           #               self.mem[4][x][y][1] = 1
           #               self.mem[4][x][y][0] = 0 if curmax>=3 else 1 

    def makeDecision(self, game_state, falseArg):
        curmax = game_state['current_max']
        stones = game_state['stones_left']
        reset = game_state['reset_used']
        leftreset = game_state['player_0']['resets_left']
        otherreset = game_state['player_1']['resets_left']
        left_time = float(120.00) - float(game_state['player_0']['time_taken'])
        time_broken = 0.0001

        if reset or curmax < 3:
            maxstep = 3
        else:
            maxstep = curmax +1

        threshhold = 3*curmax + 1

        if maxstep >= stones:
            return stones, False

        if stones-4 <= maxstep and leftreset>0:
            print('maxstep')
            return stones-4, True

        if stones <= threshhold and left_time >= time_broken:
            print("begin calculate")
            self.mem = [[[[float(0.5) for x in range(2)] for _ in range(leftreset + 1)] for _ in range(otherreset + 1)] for _ in range(max(stones+1, 5))]
            # import pdb; pdb.set_trace()
            for i in range(2):
                for x in range(leftreset):
                    for y in range(otherreset):
                        self.mem[0][x][y][i] = float(1)
                        self.mem[1][x][y][i] = float(0)
                        self.mem[2][x][y][i] = float(0)
                        self.mem[3][x][y][i] = float(0)
                        self.mem[4][x][y][1] = float(1)
                        self.mem[4][x][y][0] = float(0) if curmax >= 3 else float(1) 
               #if curmax >= 3:
               #    self.mem[4][leftreset][otherreset][0] = 0
               #else
               #    self.mem[4][leftreset][otherreset][0] = 1
            for i in range(1, leftreset+1):
                if 4*i<stones+1:
                    self.mem[4*i][leftreset][otherreset][1] = float(1)

            for i in range(5, min(4*otherreset+3, stones+1)):
                if (i%4)!=0:
                    self.mem[i][leftreset][otherreset][1] = float(0)

            #if leftreset > otherreset & 4*leftreset + maxstep <= stones:
                #for i in range(4*leftreset, max(4*leftreset, stones)):
                    #self.mem[i][leftreset][otherreset][1] = 1

            #True is my turn
            #start_time = time.time()
            score, state, reset = self.lookahead(stones, maxstep, leftreset, otherreset, True)
            #end_time = time.time()
            move = stones - state
            #print(end_time-start_time)
            #print("judge %r" % (end_time-start_time < 1))

            print('Score: %f, State: %d, Reset: %r' % (score, state, reset))
            # something to prevent corner case.... Algorithm maybe wrong...
            if move == 0:
                move = random.randint(1, maxstep)

            if(stones > (leftreset+1)*(curmax+1)):
                reset = False

            if state <= max(move, curmax, 3)+1 or (state - 4 <= max(move, curmax, 3)+1 and otherreset>0):
                reset = True
            if leftreset<=0:
                reset = False
            
            return move, reset

        elif left_time < time_broken:
            if leftreset > 0:
                return random.randint(math.floor(maxstep/2), maxstep), True
            else:
                return random.randint(math.floor(maxstep/2), maxstep), False

        elif stones > threshhold: #do something here
            if not reset:
                return random.randint(math.floor(maxstep/2), maxstep), False

            if reset and leftreset > 0:
                return random.randint(1, maxstep), True
            else:
                return random.randint(1, maxstep), False

    def lookahead(self, stone, maxstep, leftreset, otherreset, turn):
           #check whether we could win by reset
        if stone <= 0:    
            return 1, 0, False

        # Small Mitigation due to last minute bugs related to out of index look up
        try:
            if self.mem[stone][leftreset][otherreset][0] != float(0.5): #back to some where let other lose
                #print("root!!!")
                return self.mem[stone][leftreset][otherreset][0], stone, False

            if self.mem[stone][leftreset][otherreset][1] != float(0.5): #back to some where let other lose
                #print("root!!")
                return self.mem[stone][leftreset][otherreset][1], stone, True
        except:
            print("Did not look up old value correctly")
            return float(0.5), stone, False
            # import pdb; pdb.set_trace()
       
        s1 =float(0)
        move1 = stone
        reset1 = False
        s2 = float(0)
        move2 = stone
        reset2 = True
        count1 = float(0)
        count2 = float(0)
        score1 = float(0)
        score2 = float(0)

        for i in range(maxstep, 0, -1):
            if turn:
                score1, state1, resetchoice1 = self.lookahead(stone-i, maxstep, leftreset, otherreset, not turn)
                count1 += score1
                if leftreset>=1:
                    score2, state2, resetchoice2 = self.lookahead(stone-i, 3, leftreset-1, otherreset, not turn)
                count2 += score2
                s1 = score1 if score1>=s1 else s1
                move1 = stone-i if score1>=s1 else move1
                #reset1 = resetchoice1 if score1>s1 else False
                s2 = score2 if score2>=s2 else s2
                move2 = stone-i if score2>=s2 else move2
                #reset = False if s1>s2 else True


            else:
                score1, state1, resetchoice1 = self.lookahead(stone-i, maxstep, leftreset, otherreset, not turn)
                count1 += 1-score1
                if otherreset>=1:
                    score2, state2, resetchoice2 = self.lookahead(stone-i, 3, leftreset, otherreset-1, not turn)
                count2 += 1-score2
                s1 = 1-score1 if 1-score1>=s1 else s1
                move1 = stone-i if 1-score1>=s1 else move1
                #reset1 = resetchoice1 if 1-score1>s1 else False
                s2 = 1-score2 if 1-score2>=s2 else s2
                move2 = stone-i if 1-score2>=s2 else move2
                #reset = False if s1>s2 else True
                
            

        self.mem[stone][leftreset][otherreset][0] = float(count1)/float(maxstep)
        self.mem[stone][leftreset][otherreset][1] = float(count2)/float(maxstep)
        #print("not reset", self.mem[stone][leftreset][otherreset][0])
        #print("reset", self.mem[stone][leftreset][otherreset][1])
        if s1>s2:
            finalstate = move1
        else:
            finalstate = move2

        if self.mem[stone][leftreset][otherreset][0]>self.mem[stone][leftreset][otherreset][1]:
            finalscore = self.mem[stone][leftreset][otherreset][0]
            finalreset = False
        else:
            finalscore = self.mem[stone][leftreset][otherreset][1]
            finalreset = True
        
        return finalscore, finalstate, finalreset
        

decision_maker = DecisionMaker()

def check_game_status(game_state):
    if game_state['finished']:
        print(game_state['reason'])
        exit(0)


def my_algo(game_state, goes_first):
    """This function contains your algorithm for the game"""

    """
    game state looks something like this
    {
        'stones_left': 4, 
        'current_max': 3, 
        'stones_removed': 3, 
        'finished': False,
        'player_0': {'time_taken': 0.003, 'name': 'my name', 'resets_left': 2},
        'player_1': {'time_taken': 13.149, 'name': 'b2', 'resets_left': 1}, 
        'reset_used': True
        'init_max': 3
    }

    """

    print(game_state)

    return decision_maker.makeDecision(game_state, False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--first', action='store_true', default=False,
                    help='Indicates whether client should go first')
    parser.add_argument('--ip', type=str, default= '127.0.0.1')
    parser.add_argument('--port', type=int, default= 9000)
    parser.add_argument('--name', type=str, default= "Lily")


    args = parser.parse_args()
    # Read these from stdin to make life easier
    goes_first = args.first
    ip = args.ip
    port = args.port
    name = args.name if args.first else 'Lily2'
    client = Client(name, goes_first, (ip, port))
    atexit.register(client.close)
    stones = client.init_stones
    resets = client.init_resets

    if goes_first:
        num_stones = random.randint(1, 3) if client.init_stones > 3 else 3
        num_stones = num_stones if client.init_stones - 4 > 3 else client.init_stones - 4
        shouldReset = True if client.init_stones - num_stones == 4 else False
        check_game_status(client.make_move(num_stones, shouldReset))
    while True:
        game_state = client.receive_move()
        check_game_status(game_state)
        # Some parsing logic to convert game state to algo_inputs
        num_stones, reset = my_algo(game_state, goes_first)
        num_stones = max(1, num_stones)
        ourPlayerGameState = game_state['player_0'] if args.first else game_state['player_1']
        reset = reset if ourPlayerGameState['resets_left'] > 0 else False
        print('You took %d stones%s' % (num_stones,
                                        ' and used reset.' if reset else '.'))
        print('Current max: %d' % game_state['current_max'])
        print('Stones left: %d' % game_state['stones_left'])
        print('Player %s has %d resets left' % (game_state['player_0']['name'], game_state['player_0']['resets_left']))
        print('Player %s has %d resets left' % (game_state['player_1']['name'], game_state['player_1']['resets_left']))
        print('---------------------------------------')
        if game_state['finished']:
            print('Game over\n%s' % game_state['reason'])
            exit(0)
        check_game_status(client.make_move(num_stones, reset))
