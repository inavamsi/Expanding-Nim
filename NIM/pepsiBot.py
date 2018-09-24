#!/usr/bin/python3
# -*- coding: utf-8 -*-

import atexit
import time
import json
import getopt
import sys
sys.setrecursionlimit(1500)

from client import Client

def check_game_status(game_state):
    if game_state['finished']:
        print(game_state['reason'])
        exit(0)

        
class nimBot():
    def __init__(self, stones):
        self.winDict = {}
        self.buildWinDict(self.winDict, stones, 2, 0, 4, 4)
        self.reset_avail = 4
        self.opp_reset_avail = 4
        self.c_max = 2
        return
            
    def buildWinDict(self, winDict, stones, c_max, prev_reset, reset_avail, opp_reset_avail):  
    
        key = (stones, c_max, prev_reset, reset_avail, opp_reset_avail)

        #Auto-win
        if stones <= (c_max+1):
            winDict[key] = 1
            return 1

        loss = 0

        #If opp used reset
        if prev_reset == 1:
            for i in range(1, 4):

            #Check if available else find it
                t_key = (stones-i, c_max, 0, opp_reset_avail, reset_avail)
                loss |= not winDict[t_key] if t_key in winDict else not self.buildWinDict(winDict, stones-i, c_max, 0, opp_reset_avail, reset_avail)

                if reset_avail:
                    t_key = (stones-i, c_max, 1, opp_reset_avail, reset_avail-1)
                    loss |= not winDict[t_key] if t_key in winDict else not self.buildWinDict(winDict, stones-i, c_max, 1, opp_reset_avail, reset_avail-1)

        else:
            for i in range(1, c_max+2):
                t_max = c_max + 1 if i == (c_max + 1) else c_max

                t_key = (stones-i, t_max, 0, opp_reset_avail, reset_avail)
                loss |= not winDict[t_key] if t_key in winDict else not self.buildWinDict(winDict, stones-i, t_max, 0, opp_reset_avail, reset_avail)

                if reset_avail:
                    t_key = (stones-i, t_max, 1, opp_reset_avail, reset_avail-1)
                    loss |= not winDict[t_key] if t_key in winDict else not self.buildWinDict(winDict, stones-i, t_max, 1, opp_reset_avail, reset_avail-1)

        if loss > 0:
            winDict[key] = 1
        else:
            winDict[key] = 0

        return loss
    
    def nextMove(self, stones, c_max, prev_reset):
        bestMove, next_reset = 1, 0

        if prev_reset:
            t_range = 4
            c_max = self.c_max
            self.opp_reset_avail -= 1
        else:
            t_range = c_max + 2

        for i in range(1, t_range):
            if (stones-i <= 0):
                    bestMove = i
                    break

            r_range = 2 if self.reset_avail else 1

            for j in range(r_range):
                if j == 0:
                    t_max = c_max+1 if i == (c_max+1) else c_max  
                else:
                    t_max = 2

                t_key = (stones-i, t_max, j, self.reset_avail, self.opp_reset_avail)
                if t_key not in self.winDict:
                    self.buildWinDict(self.winDict, stones-i, t_max, j, self.reset_avail, self.opp_reset_avail)
                if not self.winDict[t_key]:
                        bestMove = i
                        next_reset = j
                        
        if next_reset:
            self.reset_avail -= 1
        if bestMove == (c_max + 1):
            self.c_max += 1
            
        return bestMove, next_reset
    

if __name__ == '__main__':
    # Read these from stdin to make life easier
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'fn:')
    except getopt.GetoptError:
        sys.stderr.write(__doc__)
        exit(-1)
        
    goes_first = False
        
    for o, a in opts:
        if o == '-f':
            goes_first = True
            print("-f true")
    
    ip = '127.0.0.1'
    port = 9000
    client = Client('Pepsi', goes_first, (ip, port))
    atexit.register(client.close)
    stones = client.init_stones
    resets = client.init_resets
    bot = nimBot(stones)
    print(goes_first)
    
    if goes_first:
        move, use_reset = bot.nextMove(stones, 2, 0)
        check_game_status(client.make_move(move, use_reset))
    while True:
        game_state = client.receive_move()
        check_game_status(game_state)
        move, use_reset = bot.nextMove(game_state['stones_left'], game_state['current_max'], game_state['reset_used'])
        check_game_status(client.make_move(move, use_reset))
        
        print('Move: ({}, {})'.format(move, use_reset))
        print('Stones Left, Current Max: ({}, {})'.format(game_state['stones_left'], bot.c_max))
        
        if game_state['player_0']['name'] == 'Pepsi':
            print('Resets Left: ({}, {})'.format(game_state['player_0']['resets_left']-use_reset, game_state['player_1']['resets_left']))
            print('Time used: ({}, {})'.format(round(game_state['player_0']['time_taken'], 3), round(game_state['player_1']['time_taken'], 3)))
        else:
            print('Resets Left: ({}, {})'.format(game_state['player_1']['resets_left']-use_reset, game_state['player_0']['resets_left']))
            print('Time used: ({}, {})'.format(round(game_state['player_1']['time_taken'], 3), round(game_state['player_0']['time_taken'], 3)))
        print('---------------------------------------')
        if game_state['finished']:
            print('Game over\n%s' % game_state['reason'])
            exit(0)
