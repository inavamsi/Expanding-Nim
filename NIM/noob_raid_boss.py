#!/usr/bin/python3
# -*- coding: utf-8 -*-

import atexit
import time
import json

from client import Client

def check_game_status(game_state):
    if game_state['finished']:
        print(game_state['reason'])
        exit(0)


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

    print(game_state)

    time.sleep(0.1)

    if game_state:
        if game_state['stones_left'] < 10:
            return 1, False
        if game_state['stones_left'] < 20:
            return 1, True

    return 1, False

if __name__ == '__main__':
    # Read these from stdin to make life easier
    goes_first = True
    ip = '127.0.0.1'
    port = 9000
    client = Client('Sephiroth', goes_first, (ip, port))
    atexit.register(client.close)
    stones = client.init_stones
    resets = client.init_resets

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
