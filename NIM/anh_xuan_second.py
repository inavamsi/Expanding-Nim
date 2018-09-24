#!/usr/bin/python3
# -*- coding: utf-8 -*-
import atexit
import time
import json
import random
from client import Client

def check_game_status(game_state):
    if game_state['finished']:
        print(game_state['reason'])
        exit(0)


win_dic = {}
move_dic = {}

def find_move(my_reset, opponent_reset, being_reset, stones_left, possible_move):
    # if possible_move<3:
    #   possible_move = 2
    if  stones_left<=3:
        ## 0 for we win
        ## 1 for the opponent wins
        ## if there are less or equal to 3 stones left, then it is a win regardless
        win_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = 0
        move_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = (stones_left, 0)
        # print(stones_left, 0)
        return 0
    elif stones_left<=possible_move+1 and being_reset==0:
        ## if we are not being reset, and we can possible_move+1 is >=the stones left, then we can just 
        ## make that move
        win_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = 0
        move_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = (stones_left, 0)
        # print(stones_left, 0)
        return 0
    if (my_reset, opponent_reset, being_reset, stones_left, possible_move) in win_dic:
        ## if it is already recorded, then just return it
        # print(move_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)])
        return win_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)]
    else:
        if being_reset==0:
            ## if we are not being reset
            if_won = False
            for i in range(1, max(3, possible_move)+1):
                ## if we are using less than possible move steps
                if find_move(opponent_reset, my_reset, 0, stones_left-i, max(i, possible_move))==1:
                    ## if removing i stones will make the other player lose
                    ## here ==1 means at the opponent's turn, their opponent will win, aka us
                    if_won = True
                    move_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = (i, 0)
                    break
            if not if_won and possible_move>=3:
                ## if that did not work
                ## we move the possible_move+1 stones
                if find_move(opponent_reset, my_reset, 0, stones_left-possible_move-1, possible_move+1)==1:
                    ## if that will make them lose, then we win
                    if_won = True
                    move_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)]= (possible_move+1, 0)
                    
            if not if_won and my_reset>0:
                ## if the regular moves dont work, then we use the reset
                for i in range(1, max(3, possible_move)+1):
                    if find_move(opponent_reset, my_reset-1, 1, stones_left-i, max(i, possible_move))==1:
                        if_won = True
                        move_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = (i, 1)
                        break
                if not if_won and possible_move>=3:
                    if find_move(opponent_reset, my_reset-1, 1, stones_left-i-1, possible_move+1)==1:
                        if_won = True
                        move_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)]= (possible_move+1, 1)
            if not if_won:
                win_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = 1
                move_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = (-1, -1)
                # print(-1, -1)
                return 1
            else:
                win_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = 0
                # print(move_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)])
                return 0

        else:
            ## if we got reset
            if_won = False
            for i in range(1, 4):
                # first we go over 1, 2, 3, and dont reset the opponent
                if find_move(opponent_reset, my_reset, 0, stones_left-i, possible_move)==1:
                    if_won = True
                    move_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = (i, 0)
                    break
            if not if_won and my_reset>0:
                ## now we try to reset
                for i in range(1, 4):
                    if find_move(opponent_reset, my_reset-1, 1, stones_left-i, possible_move)==1:
                        if_won = True
                        move_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = (i, 1)
                        break
            if not if_won:
                win_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = 1
                move_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = (-1, -1)
                # print(-1, -1)
                return 1
            else:
                win_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)] = 0
                # print(move_dic[(my_reset, opponent_reset, being_reset, stones_left, possible_move)])
                return 0



if __name__ == '__main__':
    # Read these from stdin to make life easier
    goes_first = False
    ip = '127.0.0.1'
    port = 9000
    client = Client('second noob', goes_first, (ip, port))
    atexit.register(client.close)
    stones = client.init_stones
    resets = client.init_resets
    my_reset = 4
    opponent_reset = 4
    current_max = 0

    while True:
        game_state = client.receive_move()
        # print(game_state)
        check_game_status(game_state)
        stones = game_state['stones_left']
        opponent_use_reset = game_state['reset_used']
        if opponent_use_reset:
            opponent_reset = opponent_reset-1
            print("Being reset this turn")

        ## find a move
        current_max_this_turn = max(game_state['current_max'], game_state['stones_removed'])
        if current_max_this_turn>current_max:
            current_max =current_max_this_turn


        if ((my_reset, opponent_reset, opponent_use_reset, stones, current_max)) in move_dic:
            num_stones, reset = move_dic[(my_reset, opponent_reset, opponent_use_reset, stones, current_max)]
        else:
            find_move(my_reset, opponent_reset, opponent_use_reset, stones, current_max)
            num_stones, reset = move_dic[(my_reset, opponent_reset, opponent_use_reset, stones, current_max)]

        ## if we use a reset, -1
        if reset==1:
            my_reset = my_reset - 1


        if num_stones == -1:
            print("dead game\n------------------------------------------------------------------------------")
            ## if it is a dead game, we jam them by doing random moves
            # print(current_max)
            num_stones, reset = (random.randint(1, max(3, current_max+1))) if not opponent_use_reset else (random.randint(1, 3)), 0

        
        # Some parsing logic to convert game state to algo_inputs
        # num_stones, reset = my_algo(game_state)

        print('Current max: %d' % game_state['current_max'])
        print('Stones left: %d' % game_state['stones_left'])

        print('You took %d stones%s' % (num_stones,
                                        ' and used reset.' if reset else '.'))
        # print('Player %s has %d resets left' % (game_state['player_0']['name'], game_state['player_0']['resets_left']))
        # print('Player %s has %d resets left' % (game_state['player_1']['name'], game_state['player_1']['resets_left']))
        print('---------------------------------------')
        if game_state['finished']:
            print('Game over\n%s' % game_state['reason'])
            exit(0)

        check_game_status(client.make_move(num_stones, reset))
