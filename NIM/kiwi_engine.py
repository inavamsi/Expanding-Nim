#!/usr/bin/python3
# -*- coding: utf-8 -*-

import atexit
import pickle

from client import Client


def check_game_status(game_state):
    if game_state['finished']:
        print(game_state['reason'])
        exit(0)

def my_dp(stones_left, current_max, my_resets, op_resets, reset):

    if reset:
        for j in reversed(range(1, 4)):
            if dp_table[stones_left-j][max(current_max,j+1)][my_resets][op_resets]!=(-1,0):
                my_move = dp_table[stones_left-j][max(current_max,j+1)][my_resets][op_resets]
                break
        if my_resets>0:
            for j in reversed(range(1, 4)):
                if dp_table[stones_left - j][max(current_max, j + 1)][my_resets-1][op_resets] != (-1, 0):
                    my_move = dp_table[stones_left - j][max(current_max, j + 1)][my_resets-1][op_resets]
                    break
    else:
        my_move = dp_table[stones_left][current_max][my_resets][op_resets]

    if my_move == (-1,0):
        return (1,0)
    else:
        return my_move


def my_algo(game_state):
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

    if(game_state):
        num_stones = game_state['stones_left']
        current_max = game_state['current_max']
        my_resets = game_state['player_0']['resets_left']
        op_resets = game_state['player_1']['resets_left']

        if(game_state['reset_used']):
            my_move = my_dp(num_stones, current_max, my_resets, op_resets, True)
        else:
            my_move = my_dp(num_stones, current_max, my_resets, op_resets, False)

        final_move = min(my_move[0], current_max, num_stones), my_move[1]

    else:
        final_move = my_dp(stones, 3, 4, 4, False)

    print(game_state)

    return final_move[0], final_move[1]

if __name__ == '__main__':
    # Read these from stdin to make life easier
    goes_first = True
    ip = '127.0.0.1'
    port = 9000
    client = Client('KiwiEngine', goes_first, (ip, port))
    atexit.register(client.close)
    stones = client.init_stones
    resets = client.init_resets
    pkl_file = open('data.pkl', 'rb')
    dp_table = pickle.load(pkl_file)
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
