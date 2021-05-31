import random
import copy
 
def legalMoves (state):
    return [0, 1]
 
def play (state, move):
    state.append (move)
    return state
 
def terminal (state):
    return len (state) >= 60
 
def score (state):
    s = 0
    for i in state:
        if i == 0:
            s = s + 1
    return s
    
def playout (state):
    while not terminal (state):
        moves = legalMoves (state)
        move = moves [int(random.random () * len (moves))]
        state = play (state, move)
    return state

def nested (state, n):
    if (n == 0):
        s1 = copy.deepcopy (state)
        return playout (s1)
    bestSequence = []
    while not terminal (state):
        moves = legalMoves (state)
        for m in moves:
            s1 = copy.deepcopy (state)
            s1 = play (s1, m)
            s1 = nested (s1, n - 1)
            if score (s1) > score (bestSequence):
                bestSequence = s1
        state = play (state, bestSequence [len (state)])
    return state


print(nested([],10))