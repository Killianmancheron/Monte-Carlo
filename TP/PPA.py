import math
import random
import copy

def playout (state, policy):
    while not state.terminal ():
        l = state.legalMoves ()
        z = 0
        for i in range (len (l)):
            z = z + math.exp (policy.get (state.code (l [i])))
        stop = random.random () * z
        move = 0
        z = 0
        while True:
            z = z + math.exp (policy.get (state.code (l [move])))
            if z >= stop:
                break
            move = move + 1
        state.play (l [move])
    return state.score ()

def adapt (s, winner, state, policy):
    polp = copy.deepcopy (policy)
    alpha = 0.32
    while not s.terminal ():
        l = s.legalMoves ()
        move = state.rollout [len (s.rollout)]
        if s.turn == winner:
            z = 0
            for i in range (len (l)):
                z = z + math.exp (policy.get (state.code (l [i])))
            polp.put (s.code (move), polp.get(s.code (move)) + alpha)
            for i in range (len (l)):
                proba = math.exp (policy.get (state.code (l [i]))) / z
                polp.put (s.code (l [i]), polp.get(s.code (l [i])) - alpha * proba)
        s.play (move)
    return polp

def PPAF (board, policy):
    if board.terminal ():
        return board.score ()
    t = look (board)
    if t != None:
        bestValue = -1000000.0
        best = 0
        moves = board.legalMoves()
        for i in range (0, len (moves)):
            val = 1000000.0
            if t [1] [i] > 0:
                Q = t [2] [i] / t [1] [i]
                if board.turn == Black:
                    Q = 1 - Q
                val = Q + 0.4 * sqrt (log (t [0]) / t [1] [i])
            if val > bestValue:
                bestValue = val
                best = i
        board.play (moves [best])
        res = PPAF (board, policy)
        t [0] += 1
        t [1] [best] += 1
        t [2] [best] += res
        return res
    else:
        add (board)
        return playout (board, policy)

def BestMovePPAF (board, n):
    Table = {}
    policy = Policy ()
    for i in range (n):
        b1 = copy.deepcopy (board)
        res = PPAF (b1, policy)
        b2 = copy.deepcopy (board)
        if res == 1:
            policy = adapt (b2, White, b1, policy)
        else:
            policy = adapt (b2, Black, b1, policy)
    t = look (board)
    moves = board.legalMoves ()
    best = moves [0]
    bestValue = t [1] [0]
    for i in range (1, len(moves)):
        if (t [1] [i] > bestValue):
            bestValue = t [1] [i]
            best = moves [i]
    return best