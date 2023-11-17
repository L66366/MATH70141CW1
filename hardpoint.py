import numpy as np
import matplotlib.pyplot as plt
# AA Strategies
aa_possible_moves = np.array([[0, 0], [0, 1], [1, 1]])
aa_strategies = np.zeros((27, 4, 2))
count = 0
for response1 in aa_possible_moves:
    for response2 in aa_possible_moves:
        for response3 in aa_possible_moves:
            aa_strategies[count] = [[0, 0], response1, response2, response3]
            count += 1

# AB Strategies
ab_possible_moves = np.array([[0, 0], [0, 1], [0, 2], [1, 1], [1, 2]])
ab_strategies = np.zeros((125, 4, 2))
count = 0
for response1 in ab_possible_moves:
    for response2 in ab_possible_moves:
        for response3 in ab_possible_moves:
            ab_strategies[count] = [[0, 1], response1, response2, response3]
            count += 1

# BB Strategies
bb_possible_moves = np.array([[0, 0], [0, 1], [0, 2], [1, 1], [1, 2], [2, 2]])
bb_strategies = np.zeros((216, 4, 2))
count = 0
for response1 in bb_possible_moves:
    for response2 in bb_possible_moves:
        for response3 in bb_possible_moves:
            bb_strategies[count] = [[1, 1], response1, response2, response3]
            count += 1

strategies = np.concatenate((aa_strategies, ab_strategies, bb_strategies), axis=0)

def payoff_calculator(blue_strategy, red_strategy):
    blue_total = 0
    red_total = 0
    # adjusting numbers so that they match with red
    blue_first_move = list(blue_strategy[0])
    red_first_move = list(red_strategy[0])
    if blue_first_move == [0, 0]:
        red_second_move = red_strategy[1]
    if blue_first_move == [0, 1]:
        red_second_move = red_strategy[2]
    if blue_first_move == [1, 1]:
        red_second_move = red_strategy[3]
    if red_first_move == [0, 0]:
        blue_second_move = blue_strategy[1]
    if red_first_move == [0, 1]:
        blue_second_move = blue_strategy[2]
    if red_first_move == [1, 1]:
        blue_second_move = blue_strategy[3]
    red_first_move = list(np.array([2, 2]) - np.array(red_first_move))
    red_second_move = np.array([2, 2]) - red_second_move
    blue_second_move = list(blue_second_move)
    red_second_move = list(red_second_move)
    # Running through all possible hill combinations
    for hill1 in [0, 1, 2]:
        for hill2 in [0,1,2]:
            if blue_first_move.count(hill1) > red_first_move.count(hill1):
                blue_total += 1
            if red_first_move.count(hill1) > blue_first_move.count(hill1):
                red_total += 1
            if blue_second_move.count(hill2) > red_second_move.count(hill2):
                blue_total += 1
            if red_second_move.count(hill2) > blue_second_move.count(hill2):
                red_total += 1
    return [blue_total, red_total]

def best_response(strategy):
    best_responses = []
    best_payoffs = [-1, []]
    for i in range(368):
        opponent_strategy = strategies[i]
        if payoff_calculator(opponent_strategy, strategy)[0] == best_payoffs[0]:
            best_responses.append(i)
            best_payoffs[1].append(payoff_calculator(opponent_strategy, strategy)[1])
        if payoff_calculator(opponent_strategy, strategy)[0] > best_payoffs[0]:
            best_responses = [i]
            best_payoffs[0] = payoff_calculator(opponent_strategy, strategy)[0]
            best_payoffs[1] = [payoff_calculator(opponent_strategy, strategy)[1]]
    return best_responses, best_payoffs

all_best_responses = [best_response(strategies[i])[0] for i in range(368)]
eq_points = []
for i in range(368):
    if i in all_best_responses[i]:
        eq_points.append(i)
def times_best_response(strategy_number):
    count = 0
    for i in range(368):
        if strategy_number in all_best_responses[i]:
            count += 1
    return count
br_times = [[j, times_best_response(j)] for j in range(368)]
br_nums = []
av_brs = []
av_others = []
av_anys = []
def eq_stats(strategy_num):
    br = (best_response(strategies[strategy_num]))
    br_num = (len(br[0]))
    av_br = (sum(br[1][1]))/br_num
    br_nums.append(br_num)
    av_brs.append(av_br)
    x = [payoff_calculator(strategies[strategy_num], strategies[j])[0] for j in range(368)]
    av_others.append((sum(x) - sum(br[1][1])) / (368 - br_num))
    av_anys.append(sum(x)/368)
for eq in eq_points:
    eq_stats(eq)
print('Number of Equilibrium Points: ', len(eq_points))
plt.plot(eq_points, av_anys, marker='o', linestyle='-', color='purple')
plt.xlabel('Strategy Number')
plt.ylabel('Average Payoff vs All Strategies')
plt.grid(True) 
plt.show()