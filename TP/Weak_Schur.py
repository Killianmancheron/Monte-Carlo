import random
import math
import copy
N = 3

class WS (object):
    def __init__ (self):
        self.partitions = [[] for i in range (N)]
        self.possible = [[True for j in range (10000)] for i in range (N)]
        self.next = 1
        self.sequence = []
 
    def legalMoves (self):
        l = []
        for i in range (N):
            if self.possible [i] [self.next]:
                l.append (i)
        return l
 
    def code (self, p):
        return N * self.next + p


    def terminal (self):
        l = self.legalMoves ()
        if l == []:
            return True
        return False
 
    def score (self):
        return self.next - 1
 
    def play (self, p):
        for i in range (len (self.partitions [p])):
            self.possible [p] [self.next + self.partitions [p] [i]] = False
        self.partitions [p].append (self.next)
        self.next = self.next + 1
        self.sequence.append (p)

    def playout (self, policy):
        while not self.terminal():
            move = self.randomMove (policy)
            state = self.play (move)
        return state

    def randomMove (self, policy):
        moves = self.legalMoves ()
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

    def adapt (self, policy):
        polp = copy.deepcopy (policy)
        for best in self.sequence:
            moves = self.legalMoves ()
            sum = 0.0
            for m in moves:
                if policy.get (m) == None:
                    policy.put(m,0.0)
                sum = sum + math.exp (policy [m])
            for m in moves:
                if polp.get (m) == None:
                    polp.put(m,0.0)
                w = polp.get (m)
                w -= math.exp (policy [m]) / sum
                polp.put(m,w)
            w = polp.get (m)
            w += 1.0
            polp.put(best,w)
            self.play(best)
        return polp

    def NRPA(self, level, policy):
        if level==0:
            return self.playout([], policy)
        bestScore = -100
        for i in range(100):
            (result, new) = self.NRPA(level-1, policy)
            if result >= bestScore:
                bestScore = result
                seq = new
            policy = self.adapt(policy, seq)
        return (bestScore, seq)

class Policy (object):

    def __init__ (self):
        self.dict = {}

    def get (self, code):
        w = 0
        if code in self.dict:
            w = self.dict [code]
        return w

    def put (self, code, w):
        self.dict [code] = w

    
