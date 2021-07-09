import math, random 
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

def adapt (sequence, policy):
    polp = copy.deepcopy (policy)
    s = WS ()
    while not s.terminal ():
        l = s.legalMoves ()
        z = 0
        for i in range (len (l)):
            z = z + math.exp (policy.get (s.code (l [i])))
        move = sequence [len (s.sequence)]
        polp.put (s.code (move), polp.get(s.code (move)) + 1)
        for i in range (len (l)):
            proba = math.exp (policy.get (s.code (l [i]))) / z
            polp.put (s.code (l [i]), polp.get(s.code (l [i])) - proba)
        s.play (move)
    return polp


def NRPA (level, policy):
    state = WS ()
    if level == 0:
        playout (state, policy)
        return state
    pol = copy.deepcopy (policy)
    for i in range (100):
        ws = NRPA (level - 1, pol)
        if ws.score () >= state.score ():
            state = ws
        pol = adapt (state.sequence, pol)
    return state
 
ws = NRPA (2, Policy ())
print (ws.partitions)
[[1, 2, 4, 8, 11, 16, 22], [3, 5, 6, 7, 19, 21, 23], [9, 10, 12, 13, 14, 15, 17, 18, 20]]
 
 #\GNRPA

def playout (state, policy):
    while not state.terminal ():
        l = state.legalMoves ()
        z = 0
        for i in range (len (l)):
            z = z + math.exp (policy.get (state.code (l [i])) + state.beta (l [i]))
        stop = random.random () * z
        move = 0
        z = 0
        while True:
            z = z + math.exp (policy.get (state.code (l [move])) + state.beta (l [move]))
            if z >= stop:
                break
            move = move + 1
        state.play (l [move])


        def adapt (sequence, policy):
    polp = copy.deepcopy (policy)
    s = WS ()
    while not s.terminal ():
        l = s.legalMoves ()
        z = 0
        for i in range (len (l)):
            z = z + math.exp (policy.get (s.code (l [i])) + s.beta (l [i]))
        move = sequence [len (s.sequence)]
        polp.put (s.code (move), polp.get(s.code (move)) + 1)
        for i in range (len (l)):
            proba = math.exp (policy.get (s.code (l [i])) + s.beta (l [i])) / z
            polp.put (s.code (l [i]), polp.get(s.code (l [i])) - proba)
        s.play (move)
    return polp


        def beta (self, p):
        last = len (self.sequence)
        if last == 0:
            return 0
        if p == self.sequence [last – 1]:
            return 10
        return 0