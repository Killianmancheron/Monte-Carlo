import random
import copy

 

atoms = [1, 2, 3, '+', '-']
children = [0, 0, 0, 2, 2]
MaxLength = 11

def legalMoves (state, leaves):
    l = []
    for a in range (len (atoms)):
        if len (state) + leaves + children [a] <= MaxLength:
            l.append (a)
    return l

def play (state, move, leaves):
    state.append (move)
    return [state, leaves - 1 + children [move]]

def terminal (state, leaves):
    return leaves == 0

def playout (state, leaves):
    while not terminal (state, leaves):
        moves = legalMoves (state, leaves)
        move = moves [int(random.random () * len (moves))]
        [state, leaves] = play (state, move, leaves)
    return state

def score (state, i):
    if children [state [i]] == 0:
        return [atoms [state [i]], i + 1]
    if children [state [i]] == 2:
        a = atoms [state [i]]
        [s1,i] = score (state, i + 1)
        [s2,i] = score (state, i)
        if a == '+':
            return [s1 + s2, i]
        if a == '-':
            return [s1 - s2, i]


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

def nested (state, leaves, n):
    bestSequence = []
    bestScore = -10e9
    while not terminal (state, leaves):
        moves = legalMoves (state, leaves)
        for m in moves:
            s1 = copy.deepcopy (state)
            [s1, leaves1] = play (s1, m, leaves)
            if (n == 1):
                s1 = playout (s1, leaves1)
            else:
                s1 = nested (s1, leaves1, n - 1)
            [score1, i] = score (s1, 0)
            if score1 > bestScore:
                bestScore = score1
                bestSequence = s1
        [state, leaves] = play (state, bestSequence [len (state)], leaves)
    return state

import sys
 
def printExpression (state):
    for i in state:
        sys.stdout.write (str (atoms [i]) + ' ')
    sys.stdout.write ('\n')

def test ():
    for i in range (10):
        s = playout ([], 1)
        printExpression (s)
        print (score (s, 0) [0])
    for i in range (10):
        s = nested ([], 1, 2)
        printExpression (s)
        print (score (s, 0) [0])
 
test ()
