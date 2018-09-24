#!/usr/bin/python3
# -*- coding: utf-8 -*-

import atexit
import time
import json
import numpy as np
import getopt
import sys


from client import Client

def check_game_status(game_state):
    if game_state['finished']:
        print(game_state['reason'])
        exit(0)


def my_algo(game_state,mat_list,me):
    """This function contains your algorithm for the game"""

    """
    game state looks something like this
    {
        'stones_left': 4,
        'current_max': 3,
        'stones_removed': 3,
        'finished': False,
        'player_0': {'time_taken': 0.003, 'name': 'my name', 'resets_left': 2},
        'player_1': {'time_taken': 13  .149, 'name': 'b2', 'resets_left': 1},
        'reset_used': True
        'init_max': 3
    }

    """

    if not game_state:
        num_stones = client.init_stones
        current_max = 0
        time_taken = 0
        reset_turn = 0
        reset_me = client.init_resets
        reset_opp = client.init_resets

    else:
        num_stones = game_state['stones_left']
        current_max = game_state['current_max']
        if game_state['reset_used']:
            reset_turn = 1
        elif not game_state['reset_used']:
            reset_turn = 0
        reset_me = game_state[me]['resets_left']
        reset_opp = game_state[me]['resets_left']

    max_take = max(3,current_max+1)
    move = mat_list[reset_turn][reset_me][reset_opp][max_take-3][num_stones-1]
    #print move
    if move > 100:
        move -= 100
        r = True
    elif move != 0:
        r = False
    elif move == 0:
        r = False
        move = 1

    return [int(move),r]

def find_win(mat_check,ns,cm,cm_store,i,reset_current):

    cm -= 1
    while cm > 0:
        if mat_check[i,ns-1-cm] == 0:
            return cm
        else:
            cm -= 1

    #If not in the last row and I can increase current max
    if i != 41 and (reset_current !=1 or i == 0):
        if mat_check[i+1,ns - 1 - cm_store] == 0:
            return cm_store

    #If we have a reset we can't increase current max as long as cm > 3 (i>0)
    if reset_current == 1 and i > 0:
        if mat_check[i,ns - 1 - cm_store] == 0:
            return cm_store

    return 0

def get_matrix(reset_current,reset_me,reset_opp,top_stones,mat_list):

    mat_new = np.array([[1,2,3] for i in range(42)])

    ns = 4
    while ns <= top_stones:
        new_col = np.empty([42,1])

        mat_new = np.append(mat_new,new_col,axis=1)

        for i in range(42):
            #print "cmax", i + 3
            win = False

            if reset_current == 1:
                cm = 3
                cm_store = 3
            elif reset_current == 0:
                cm = i + 3
                cm_store = i + 3

            #trivial winning cases
            if cm > ns:
                mat_new[i,ns-1] = ns
                win = True
            elif cm == ns:
                mat_new[i,ns-1] = ns
                win = True

            #non reset cases

            #first case is when I have more resets and I choose not to reset, just the same as if i didn't have the reset
            elif reset_me >= reset_opp and reset_me != 0:

                mat_check = mat_list[0][reset_me-1][reset_opp]
                mat_new[i,ns-1] = mat_check[i,ns-1]
                if mat_new[i,ns-1] != 0:
                    win = True

                #if resets are equal can check same matrix for wins
                if not win and reset_opp == reset_me:
                    mat_opp = np.copy(mat_new)
                    val = find_win(mat_opp,ns,cm,cm_store,i,reset_current)
                    if val != 0:
                        win = True
                        mat_new[i,ns-1] = val


            # if opponent has no resets
            elif reset_opp == 0:
                if reset_me == 0 and reset_current == 0:
                    mat_opp = np.copy(mat_new)
                elif reset_me == 0 and reset_current == 1:
                    mat_opp = mat_list[0][0][0]
                else:
                    mat_opp = mat_list[0][0][reset_me]
                val = find_win(mat_opp,ns,cm,cm_store,i,reset_current)
                if val != 0:
                    win = True
                    mat_new[i,ns-1] = val

            #if opponent has resets
            elif reset_opp > 0:
                #case where I decide not to reset
                mat_opp = mat_list[0][reset_opp][reset_me]
                val = find_win(mat_opp,ns,cm,cm_store,i,reset_current)
                if val != 0:
                    win = True
                    mat_new[i,ns-1] = val

            cm = cm_store

            if not win and reset_me > 0 and reset_opp == 0:
                mat_opp = mat_list[1][0][reset_me - 1]
                val_reset = find_win(mat_opp,ns,cm,cm_store,i,reset_current)
                if val_reset != 0:
                    win = True
                    mat_new[i,ns-1] = 100 + val_reset


            if not win and reset_me > 0 and reset_opp > 0:
                mat_opp = mat_list[1][reset_opp][reset_me - 1]
                val_reset = find_win(mat_opp,ns,cm,cm_store,i,reset_current)
                if val_reset != 0:
                    win = True
                    mat_new[i,ns-1] = 100 + val_reset

            if not win:
                mat_new[i,ns-1] = 0

        ns +=1

    return mat_new

def build_matrix_list():
    mat_list = [[[],[],[],[],[]],[[],[],[],[],[]]]

    index_list = [[0,0,0],[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,1,1],\
              [0,2,0],[1,2,0],[0,2,1],[1,2,1],[0,1,2],[1,1,2],[0,0,2],[1,0,2],[0,2,2],[1,2,2],\
              [0,3,0],[1,3,0],[0,3,1],[1,3,1],[0,3,2],[1,3,2],[0,0,3],[1,0,3],\
              [0,1,3],[1,1,3],[0,2,3],[1,2,3],[0,3,3],[1,3,3],\
              [0,4,0],[1,4,0],[0,4,1],[1,4,1],[0,4,2],[1,4,2],[0,4,3],[1,4,3],\
              [0,0,4],[1,0,4],[0,1,4],[1,1,4],[0,2,4],[1,2,4],[0,3,4],[1,3,4],[0,4,4]]

    for i in index_list:
        print(i)
        mat_list[i[0]][i[1]].append(get_matrix(i[0],i[1],i[2],1000,mat_list))

    return mat_list

if __name__ == '__main__':
    # Read these from stdin to make life easier
    #lines = sys.stdin.readlines()
    #print(lines)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'fn:')
    except getopt.GetoptError:
        sys.stderr.write(__doc__)
        exit(-1)

    goes_first = False
    if len(opts) > 0:
        if '-f' in opts[0]:
            goes_first = True

    if goes_first:
        me = 'player_0'
    else:
        me = 'player_1'
    ip = args[0].split(':')[0]
    port = int(args[0].split(':')[1])

    client = Client('Sam', goes_first, (ip, port))
    atexit.register(client.close)
    stones = client.init_stones
    resets = client.init_resets
    if goes_first:
        mat_list = build_matrix_list()
        num_stones, reset = my_algo(None,mat_list,me)
        check_game_status(client.make_move(num_stones, reset))
    while True:
        game_state = client.receive_move()
        check_game_status(game_state)
        # Some parsing logic to convert game state to algo_inputs
        print('Time Taken: ',game_state[me]['time_taken'])
        if game_state[me]['time_taken'] < 10:
            mat_list = build_matrix_list()
        num_stones, reset = my_algo(game_state,mat_list,me)

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
