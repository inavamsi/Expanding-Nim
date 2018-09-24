#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import atexit
import time
import json
import random
import csv
import pickle
import sys
from getopt import getopt

from client import Client

def check_game_status(game_state):
    if game_state['finished']:
        print(game_state['reason'])
        exit(0)

memo = {}
thisapi = False
def parseMemo(line):
    row = [int(x) for x in line]
    key, value  = row[:5], row[5:]
    value[1] = bool(value[1])
    memo[tuple(key)] = value

def init(filename):
    print("init ... start")
    #with open(filename) as csv_file:
    #    csv_reader = csv.reader(csv_file, delimiter=',')
    #    for line in csv_reader:
    #        parseMemo(line)
    #with open('memo.pickle', 'wb') as handle:
    #    pickle.dump(memo, handle, protocol=pickle.HIGHEST_PROTOCOL)
    global memo
    with open('memo.pickle', 'rb') as handle:
        memo = pickle.load(handle)
    #for key in memo:
    #    print(key, memo[key])
    print("init ... done")

def randMove(currMax, resetPossible):
    reset = False
    if resetPossible:
       reset = bool(random.getrandbits(1))
    numCoins = random.randint(1, max(3, currMax+1))
    print((numCoins, reset))
    return [numCoins, reset]

def memoPlayer(game_state):
    move = [0, False]
    currMax = 0
    myresets, otherresets = 0,0
    if thisapi:
        myresets = game_state['player_0']['resets_left']
        otherresets = game_state['player_1']['resets_left']
    else:
        myresets = game_state['player_1']['resets_left']
        otherresets = game_state['player_0']['resets_left']

    # fill move from table
    key = tuple([game_state['stones_left'], max(game_state['current_max'], 2), myresets, otherresets, int(game_state['reset_used'] == True)])
    #print("key is")
    #print(key)
    #print("value is")
    #print(memo[key])
    if key in memo:
        move = memo[key]
        currMax = game_state['current_max']
        #print("played from table")
    #else:
        #print("played from bla")
    ##
    if move[0] == 0:
        move = randMove(currMax, myresets > 0)
    return move

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
    time.sleep(0.01)
    return memoPlayer(game_state)

if __name__ == '__main__':
    opts, args = getopt(sys.argv[1:], 'i:p:g:')
    goes_first = True
    ip = 0
    port = 0
    for o, a in opts:
        if o == '-i':
            ip = a
        elif o == '-p':
            port = int(a)
        elif o == '-g':
            goes_first = (int(a) > 0)
    # Read these from stdin to make life easier
    #goes_first = True
    thisapi = goes_first
    #ip = '172.22.49.59'
    #port = 9000
    #print(ip)
    #print(port)
    #print(goes_first)
    client = Client('win', goes_first, (ip, port))
    atexit.register(client.close)
    stones = client.init_stones
    resets = client.init_resets
    init('StrategyTable.csv')
    initGameState = {'stones_left': stones, 'current_max': 2, 'player_0': {'resets_left': resets}, 'player_1': {'resets_left': resets}, 'reset_used': False}

    if goes_first:
        num_stones, reset = my_algo(initGameState)
        check_game_status(client.make_move(num_stones, reset))
    while True:
        game_state = client.receive_move()
        print('Current max: %d' % game_state['current_max'])
        print('Stones left: %d' % game_state['stones_left'])
        print('Player %s has %d resets left' % (game_state['player_0']['name'], game_state['player_0']['resets_left']))
        print('Player %s has %d resets left' % (game_state['player_1']['name'], game_state['player_1']['resets_left']))

        check_game_status(game_state)
        # Some parsing logic to convert game state to algo_inputs
        num_stones, reset = my_algo(game_state)

        print('You took %d stones%s' % (num_stones,
                                        ' and used reset.' if reset else '.'))
        print('---------------------------------------')
        if game_state['finished']:
            print('Game over\n%s' % game_state['reason'])
            exit(0)

        check_game_status(client.make_move(num_stones, reset))
