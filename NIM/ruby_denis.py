#!/usr/bin/python3
# -*- coding: utf-8 -*-

import atexit
from getopt import getopt
from client import Client
import sys
import json

sys.setrecursionlimit(1500)

def check_game_status(game_state):    
    if game_state['finished']:
        print(game_state['reason'])
        exit(0)


def my_algo(game_state):
    """This function contains your algorithm for the game"""

    print("in my algo", game_state)

    """
    game state looks something like this
    {
        'stones_left': 4, 
        'current_max': 3, 
        'stones_removed': 3, 
        'finished': False,
        'player_0': {'time_taken': 0.003, 'name': 'my name', 'resets_left': 2},
        'player_1': {'time_taken': 13.149, 'name': 'b2', 'resets_left': 1}, 
        'reset_used': True,
        'init_max': 3
    }
        
    """
    if game_state:
        if(game_state['reset_used'] == True): 
            max_allowed = game_state['init_max']
        else:
            max_allowed = max(game_state['init_max'], game_state['current_max'])
        if goes_first:
            print("A going first")
            result = get_move_A(game_state['current_max'], max_allowed, game_state['player_0']['resets_left'], 
            game_state['player_1']['resets_left'], game_state['stones_left'])
        else: 
            print("A going second")
            result = get_move_B(game_state['current_max'], max_allowed, game_state['player_0']['resets_left'], 
            game_state['player_1']['resets_left'], game_state['stones_left'])
        return (result[1],result[2])
    # goes first 
    else:
        result = get_move_A(0, 3, resets, resets, stones)
        return (result[1],result[2])


def get_move_A(curr_max, max_allowed, reset_A, reset_B, stones_left):
    key = '%s-%s-%s-%s-%s' % (curr_max, max_allowed, reset_A, reset_B, stones_left)
    if memoA.get(key):
        return memoA.get(key)
    if (max_allowed >= stones_left):
        memoA[key] = (1, stones_left, 0)
        return memoA[key]
    else:
        ## i is for number of stones possible
        for i in range (1, max_allowed+1):
            next_curr_max = max(i+1, curr_max)
            next_max_allowed = max(3, next_curr_max)
            ## j is for using reset or not
            if (reset_A > 0):
                for j in range (0, 2):
                    if (j == 0):
                        next_max_allowed = max(3, next_curr_max)
                    if (j == 1):   
                        next_max_allowed = 3
                    result = get_move_B(next_curr_max, next_max_allowed, reset_A-j, reset_B, stones_left-i)
                    if (result[0] == 0):
                        memoA[key] = (1, i, j)
                        return memoA[key]
            else:
                result = get_move_B(next_curr_max, next_max_allowed, reset_A, reset_B, stones_left-i)
                if (result[0] == 0):
                    memoA[key] = (1, i, 0)
                    return memoA[key]

        # what move to return no optimal move
        memoA[key] = (0, 1, 0)
        return memoA[key]

def get_move_B(curr_max, max_allowed, reset_A, reset_B, stones_left):
    key = '%s-%s-%s-%s-%s' % (curr_max, max_allowed, reset_A, reset_B, stones_left)
    if memoB.get(key):
        return memoB.get(key)
    if (max_allowed >= stones_left):
        memoB[key] = (1, stones_left, 0)
        return memoB[key]
    else:
        ## i is for number of stones possible
        for i in range (1, max_allowed+1):
            next_curr_max = max(i+1, curr_max)
            next_max_allowed = max(3, next_curr_max)
            ## j is for using reset or not
            if (reset_B > 0):
                for j in range (0, 2):
                    if (j == 0):
                        next_max_allowed = max(3, next_curr_max)
                    if (j == 1):   
                        next_max_allowed = 3
                    result = get_move_A(next_curr_max, next_max_allowed, reset_A, reset_B-j, stones_left-i)
                    if (result[0] == 0):
                        memoB[key] = (1, i, j)
                        return memoB[key]
            else:
                result = get_move_A(next_curr_max, next_max_allowed, reset_A, reset_B, stones_left-i)
                if (result[0] == 0):
                    memoB[key] = (1, i, 0)
                    return memoB[key]
                
        # what move to return no optimal move
        memoB[key] = (0, 1, 0)
        return memoB[key]

if __name__ == '__main__':
    # Read these from stdin to make life easier
    try:
        opts, args = getopt(sys.argv[1:], 'fn:')
    except GetoptError:
        sys.stderr.write('Error parsing options\n')
        sys.stderr.write(__doc__)
        exit(-1)
	
    global goes_first
    goes_first = False
    ip = '127.0.0.1'
    port = 9000
    name = None

    for o, a in opts:
        if o == '-f':
            goes_first = True
        elif o == '-n':
            name = a

    print(goes_first)

    if ip is None:
        ip = '127.0.0.1'
    if port is None:
        port = 9000
    if name is None:
        name = 'Ruby/Denis'

    client = Client(name, goes_first, (ip, port))
    atexit.register(client.close)
    global stones, resets, memoA, memoB
    stones = client.init_stones
    resets = client.init_resets
    memoA = {}
    memoB = {}

    if goes_first:
        num_stones, reset = my_algo(None)
        check_game_status(client.make_move(num_stones, reset))
    while True:
        game_state = client.receive_move()
        check_game_status(game_state)
        # Some parsing logic to convert game state to algo_inputs
        num_stones, reset = my_algo(game_state)
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
