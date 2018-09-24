#!/usr/local/bin/python3
#  -*- coding: utf-8 -*-

import pickle
import os
import atexit
import sys

from client import Client

bounds = {'max_stones': 1000, 'max_cm': 45, 'max_resets': 4, 'reset_conditions': 1}
lookup = []


def fill_lookup():
    """
    :return: void, but fills global lookup table (either from pickle file or manually, iteratively)
    """

    # Using global variable
    global lookup

    # Load pickle file
    if os.path.isfile("lookup_file.pickle"):
        lookup = pickle.load(open("lookup_file.pickle", "rb"))
    # Or fill it manually
    else:
        for n_iter in range(bounds['max_stones'] + 1):
            for cm_iter in range(bounds['max_cm'] + 1):
                for r_iter in range(bounds['max_resets'] + 1):
                    for s_iter in range(bounds['max_resets'] + 1):
                        for limited_iter in range(bounds['reset_conditions'] + 1):
                            fill_entry(n_iter, cm_iter, r_iter, s_iter, limited_iter)
        pickle.dump(lookup, open("lookup_file.pickle", "wb"))


def fill_entry(n, cm, r, s, limited):
    """
    :param n: number of stones (int)
    :param cm: current max (int)
    :param r: number of my resets left (int)
    :param s: number of resets opponent has left (int)
    :param limited: whether or not we're under reset conditions (bool)
    :return: void, but fills lookup table entries
    """

    # Using global variable
    global lookup

    # Base case: 0 stones left, already lost
    if n == 0:
        lookup[n][cm][r][s][limited] = (0, False)
        return

    # Maximum number of stones we can take
    upper = 3 if limited else cm + 1

    # Base case: we will win just by taking remainder, no reset necessary
    if n <= upper:
        lookup[n][cm][r][s][limited] = (n, False)
        return

    # Try all possibilities without resets
    for i in range(1, upper + 1):
        # If this puts other player in a bad position...
        if lookup[n - i][min(45, max(i, cm))][s][r][False][0] == 0:
            lookup[n][cm][r][s][limited] = (i, False)
            return

    # Ty all possibilities with resets
    if r > 0:
        for i in range(1, upper + 1):
            if max(i, cm) > 2:
                # If this puts other player in a bad position...
                if lookup[n - i][min(45, max(i, cm))][s][r - 1][True][0] == 0:
                    lookup[n][cm][r][s][limited] = (i, True)
                    return

    # Going to lose with or without resets, so just take 1 and save resets just in case
    lookup[n][cm][r][s][limited] = (0, False)
    return


def my_algo(game_state):
    """
    :param game_state: looks as follows
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
    :return: number of stones to take, whether or not to do reset (int, int)
    """

    # Using global variable
    global lookup

    # TODO is printing necessary?
    print(game_state)

    # Parameters for lookup table
    n = game_state['stones_left']
    cm = max(2, game_state['current_max'])
    if game_state['player_0']['name'] == 'Stephiroth':
        r = game_state['player_0']['resets_left']
        s = game_state['player_1']['resets_left']
    else:
        r = game_state['player_1']['resets_left']
        s = game_state['player_0']['resets_left']
    limited = game_state['reset_used']

    # Try to use lookup table
    try:
        (num_take, use_reset) = lookup[n][cm][r][s][limited]
        num_take = 1 if num_take == 0 else num_take
        use_reset = 1 if use_reset else 0
    except IndexError:
        (num_take, use_reset) = (1, False)  # there was an error; we will probably lose

    # Return move
    return num_take, use_reset


def check_game_status(game_state):
    if game_state['finished']:
        print(game_state['reason'])
        exit(0)


def main():

    # Using global variable
    global lookup

    # Default
    goes_first = False
    ip = '127.0.01'
    port = 9000

    # Read from command line
    if len(sys.argv) != 4:
        print("Argument format: goes_first, ip, port   please re-enter")
        exit(1)
    else:
        goes_first = True if (sys.argv[1] == "True") else False
        ip = sys.argv[2]
        port = int(sys.argv[3])

    # Make client
    client = Client('Stephiroth', goes_first, (ip, port))
    atexit.register(client.close)
    stones = client.init_stones
    resets = client.init_resets

    # Fill lookup table
    lookup = [[[[[(-1, False)
                  for _ in range(bounds['reset_conditions'] + 1)]
                 for _ in range(bounds['max_resets'] + 1)]
                for _ in range(bounds['max_resets'] + 1)]
               for _ in range(bounds['max_cm'] + 1)]
              for _ in range(bounds['max_stones'] + 1)]
    fill_lookup()

    # Create game state for first move
    game_state = {'stones_left': stones,
                  'current_max': 0,
                  'stones_removed': 0,
                  'finished': False,
                  'player_0': {'time_taken': 0.0, 'name': 'Stephiroth', 'resets_left': resets},
                  'player_1': {'time_taken': 0.0, 'name': 'Stephiroth', 'resets_left': resets},
                  'reset_used': False,
                  'init_max': 0}

    # First turn
    if goes_first:
        num_stones, reset = my_algo(game_state)
        check_game_status(client.make_move(num_stones, reset))

    # Game play
    while True:

        game_state = client.receive_move()
        check_game_status(game_state)

        num_stones, reset = my_algo(game_state)

        # TODO is printing necessary?
        print('You took %d stones%s' % (num_stones, ' and used reset.' if reset else '.'))
        print('Current max: %d' % game_state['current_max'])
        print('Stones left: %d' % game_state['stones_left'])
        print('Player %s has %d resets left' % (game_state['player_0']['name'], game_state['player_0']['resets_left']))
        print('Player %s has %d resets left' % (game_state['player_1']['name'], game_state['player_1']['resets_left']))
        print('---------------------------------------')
        if game_state['finished']:
            print('Game over\n%s' % game_state['reason'])
            exit(0)

        check_game_status(client.make_move(num_stones, reset))


main()
