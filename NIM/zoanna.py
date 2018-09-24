#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" The most beautiful algorithm """

import argparse
import atexit
from random import randint
import sys
from client import Client


def check_game_status(game_state):
    """
    Checks if game done.
    """
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
    stones = game_state['stones_left']
    curr_max = game_state['current_max']
    reset = game_state['reset_used']

    if not game_state:
        print('Something wrong with game_state, we politely refuse to play.')
        sys.exit(0)

    if stones <= 3:
        return stones, False

    if stones <= curr_max + 1 and not reset:
        return stones, False

    if reset:
        # If reset, get to target (up to 3)
        for i in [4, 8, 12, 16]:
            diff = stones - i
            if 0 < diff <= 3:
                return diff, True

    else:
        # If no reset, get to target (if poss)
        for i in [4, 8, 12, 16]:
            diff = stones - i
            if 0 < diff <= curr_max + 1:
                return diff, True

    # Go to current max + 2 from 16 if possible
    dist_from_16 = stones - 16
    move = dist_from_16 % (curr_max + 1)
    if not reset and 0 < move <= (curr_max + 1):
        return move, False
    if 0 < move <= 3:
        return move, False

    # No logic, mess up opponent... if possible
    return randint(1, 3), False


def main():
    """
    Maine?
    """
    parser = argparse.ArgumentParser(description='Zoanna Algorithm')
    parser.add_argument('-f', '--first', action='store_true')
    parser.add_argument('-i', '--host', nargs='?', default='127.0.0.1', type=str)
    parser.add_argument('-p', '--port', nargs='?', default=9000, type=int)
    args = parser.parse_args()

    client = Client('Zoanna', args.first, (args.host, args.port))
    atexit.register(client.close)
    stones = client.init_stones

    if args.first:
        num_stones, reset = my_algo({
            'current_max': 0,
            'stones_left': stones,
            'reset_used': False,
        })
        check_game_status(client.make_move(num_stones, reset))

    while True:
        game_state = client.receive_move()
        check_game_status(game_state)
        num_stones, reset = my_algo(game_state)
        print('You took %d stones%s' % (num_stones, ' and used reset.' if reset else '.'))
        print('Current max: %d' % game_state['current_max'])
        print('Stones left: %d' % game_state['stones_left'])
        print('Player %s has %d resets left' %
              (game_state['player_0']['name'], game_state['player_0']['resets_left']))
        print('Player %s has %d resets left' %
              (game_state['player_1']['name'], game_state['player_1']['resets_left']))
        print('---------------------------------------')
        if game_state['finished']:
            print('Game over\n%s' % game_state['reason'])
            exit(0)

        check_game_status(client.make_move(num_stones, reset))
        print(args.first)


if __name__ == '__main__':
    main()
