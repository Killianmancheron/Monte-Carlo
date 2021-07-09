import math
import numpy as np
from TP.Left_Move_Problem import *



weights = {0 : .5, 1:.5}
# def playout(state, policy):
#     sequence = []
#     while True :
#         if terminal(state):
#             return (score(state), sequence)
#         z = 0.0
#         for m in legalMoves(state):
#             z+=exp(policy[m]) #code(m)
#         move = np.random.choice(2, 1, p=[exp(policy[m])/z for m in legalMoves(state)])
#         state = play(state, move)
#         sequence+= [move]
    
def randomMove (state, policy):
    moves = legalMoves (state)
    sum = 0.0
    for m in moves:
        if policy.get (m) == None:
            policy [m] = 0.0
        sum = sum + math.exp (policy [m])
    stop = random.random () * sum
    sum = 0.0
    for m in moves:
        sum = sum + math.exp (policy [m])
        if (sum >= stop):
            return m

def playout (state, policy):
    while not terminal (state):
        move = randomMove (state, policy)
        state = play (state, move)
    return state


# def Adapt(policy, sequence):
#     polp = copy.deepcopy (policy)
#     state = root
#     for move in sequence :
#         polp[move] = polp[move] + alpha
#         z=0.0
#         for m in legalMoves(state):
#             z+=exp(policy[m])
#         for m in legalMoves(state):
#             polp[m]=polp[m]-alpha*exp(policy[m])/z
#         state = play(state, move)
#     policy = polp
#     return policy

def adapt (policy, sequence):
    s = []
    polp = copy.deepcopy (policy)
    for best in sequence:
        moves = legalMoves (s)
        sum = 0.0
        for m in moves:
            if policy.get (m) == None:
                policy [m] = 0.0
            sum = sum + math.exp (policy [m])
        for m in moves:
            if polp.get (m) == None:
                polp [m] = 0.0
            polp [m] -= math.exp (policy [m]) / sum
        polp [best] += 1.0
        s = play (s, best)
    return polp

    
def NRPA (level, policy):
    seq = []
    if level == 0:
        return playout (seq, policy)
    for i in range (100):
        pol = copy.deepcopy (policy)
        s = NRPA (level - 1, pol)
        if score (s) > score (seq):
            seq = s
        policy = adapt (policy, seq)
    return seq


def NRPA(level, policy):
    if level==0:
        return playout([], policy)
    bestScore = -100
    for i in range(100):
        (result, new) = NRPA(level-1, policy)
        if result >= bestScore:
            bestScore = result
            seq = new
        policy = adapt(policy, seq)
    return (bestScore, seq)