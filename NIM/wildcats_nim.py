#!/usr/bin/python3

import time
import atexit
from client import Client
'''
dynamic programming is a good idea, but you must keep track of which players
turn it is, how many stones are left, and what the currentmax is, and
who has used the reset option and how often."
'''

def check_game_status(game_state):
    if game_state['finished']:
        print(game_state['reason'])
        exit(0)

    print(game_state)


d = {}
def Check(x, y, bar):   ## x------stones,      y------moves
    cell = (x, y, bar)
    # print("Check ", cell)
    try:
        return d[cell]['Basic_Al']
    except:
        try:
            temp = d[cell]
        except:
            d[cell] = {}
        if y >= x:    ## you can remove all the stones
            d[cell]['Basic_Al'] = 1   ## Win
            # print(cell, '=', d[cell])
            return d[cell]['Basic_Al']
        left_stones = x - y    ## left_stones = stones - moves
        if y == bar:
            bar += 1    ## update cur_max for the next round
        # print("bar = ", bar)
        ## check out my opponent
        op_win_count = 0
        for i in range(min(left_stones, bar), 0, -1):
            if ( Check(left_stones, i, bar) ):
                op_win_count += 1
                # d[cell]['Basic_Al'] = 0     ### One win for next round, then you will lose
                # # print(cell, '=', d[cell])
                # return 0
        if left_stones:
            p_win = 1 - op_win_count / min(left_stones, bar)
        else:
            p_win = 1.0
        d[cell]['Basic_Al'] = p_win
        return d[cell]['Basic_Al']


def Check_with_reset(x, y, bar):
    cell = (x, y, bar)
    left_stones = x - y
    try:
        return d[cell]['Reset_Al']
    except:
        try:
            temp = d[cell]
        except:
            d[cell] = {}

        if y >= x:    ## you can remove all the stones
            d[cell]['Reset_Al'] = 1   ## Win
            # print(cell, '=', d[cell])
            return d[cell]['Reset_Al']
        # print("left stones = ", left_stones)
        if y == bar:
            bar += 1

        ## check out my opponent
        op_win_count = 0
        for i in range(3, 1, -1):
            left_stones = left_stones - i

            if( Check_under_reset(min(left_stones, 3), i, bar - 1)):
                op_win_count += 1
        if left_stones:
            p_win = 1 - op_win_count / min(left_stones, bar)
        else:
            p_win = 1.0
        d[cell]['Reset_Al'] = p_win
        return d[cell]['Reset_Al']

def Check_under_reset(x, y, cur_max = 2):
    cell = (x, y, cur_max + 1)
    upper_bound = 3  ## Since this the a reset round

    try:
        return d[cell]['under_reset']
    except:
        try:
            temp = d[cell]
        except:
            d[cell] = {}

        if y >= x:    ## you can remove all the stones
            d[cell]['under_reset'] = 1   ## Win
            # print(cell, '=', d[cell])
            return d[cell]['under_reset']

        left_stones = x - y   ## y = [1, 3]
        op_win_count = 0
        for i in range(min(left_stones, 3), 0 , -1):
            if(Check(left_stones, i, cur_max + 1)):       ## one win, you will lose
                op_win_count += 1

        if left_stones:
            p_win = 1 - op_win_count / min(left_stones, 3)
        else:
            p_win = 1.0
        d[cell]['under_reset'] = p_win
        return d[cell]['under_reset']


def Check_under_reset_with_reset(x, y, cur_max = 2):
    cell = (x, y, cur_max + 1)
    upper_bound = 3  ## Since this the a reset round

    try:
        return d[cell]['under_reset_with_reset']
    except:
        try:
            temp = d[cell]
        except:
            d[cell] = {}

        if y >= x:    ## you can remove all the stones
            d[cell]['under_reset_with_reset'] = 1   ## Win
            print(cell, '=', d[cell])
            return d[cell]['under_reset_with_reset']

        left_stones = x - y   ## y = [1, 3]
        op_win_count = 0
        for i in range(min(left_stones, 3), 0 , -1):
            if(Check_under_reset(left_stones, i, cur_max)):       ## one win, you will lose
                op_win_count += 1
        if left_stones:
            p_win = 1 - op_win_count / min(left_stones, 3)
        else:
            p_win = 1.0
        d[cell]['under_reset_with_reset'] = p_win
        return d[cell]['under_reset_with_reset']


# total_stones = 100
# cur_max = 3
# upper_bound = 3   ## bar = 3
#
# reset_times = 4
# reset_flag = 0
#
# op_reset = 1


def Decision_making(total_stones, cur_max, reset_times, reset_flag):
    max_p = 0
    move_choice = cur_max + 1
    reset_choice = 0  ## by default, we do not set reset for the next round
    if reset_flag:
        for i in range(3, 0, -1):
            temp1 = Check_under_reset(total_stones, i, cur_max)
            temp2 = 0
            if reset_times:
                temp2 = Check_under_reset_with_reset(total_stones, i, cur_max)
            if (max(temp1, temp2) > max_p):
                max_p = max(temp1, temp2)
                move_choice = i
                if temp1 < temp2:
                    reset_choice = 1
                else:
                    reset_choice = 0
    else:
        for i in range(cur_max + 1, 0, -1):
            temp1 = Check(total_stones, i, cur_max + 1)
            temp2 = 0
            if reset_times:
                temp2 = Check_with_reset(total_stones, i, cur_max + 1)
            if (max(temp1, temp2) > max_p):
                max_p = max(temp1, temp2)
                move_choice = i
                if temp1 < temp2:
                    reset_choice = 0
                else:
                    reset_choice = 1
    return move_choice, reset_choice


def my_algo(game_state):
    '''
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
    '''

    if game_state:
        curMax = max(2, game_state['current_max'])
        reset_times = game_state['player_1']['resets_left']
        if game_state['current_max'] + 1 >= game_state['stones_left']:
            return game_state['stones_left'], False
        if game_state['stones_left'] == game_state['current_max'] + 2:
            return 1, True
        if game_state['stones_left'] < (game_state['current_max'] + 1) + 4:
            return (game_state['stones_left'] - 4), True
        #under reset
        if game_state['reset_used'] == True:
            #opponent has no resets left
            return Decision_making(game_state['stones_left'], curMax, reset_times, 1)
        else:
            return Decision_making(game_state['stones_left'], curMax, reset_times, 0)



if __name__ == '__main__':
    # Read these from stdin to make life easier
    goes_first = True
    ip = '127.0.0.1'
    port = 9000
    client = Client('my name', goes_first, (ip, port))
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
        check_game_status(client.make_move(num_stones, reset))
