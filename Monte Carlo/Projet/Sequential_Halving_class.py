import copy 
from math import sqrt, log
from Table_transposition import TranspoMonteCarlo
from UCT import UCT
import numpy as np

Empty = 0
White = 1
Black = 2

class Sequential_Halving():

    def __init__(self):
            self.TMC = TranspoMonteCarlo()
            #self.Dx=5
            #self.Dy=5
            self.Side=8
            self.MaxCodeLegalMoves = 2 * self.Side * self.Side * 8
            self.MaxLegalMoves=32
            self.UCT = UCT()

    def BestMove (self, state, budget):
        """Algorithme de Sequantial Halving minimisant le regret

        Args:
            state (Board): Etat du jeu actuel
            budget (int): Budget à allouer à chaque noeud

        Returns:
            Move: Mouvement sélectionné, minimisant le regret
        """    
        
        #Table = {}
        self.TMC = TranspoMonteCarlo()
        self.TMC.add (state)
        moves = state.legalMoves ()
        total = len (moves)
        nplayouts = [0.0 for x in range (self.MaxCodeLegalMoves)]
        nwins = [0.0 for x in range (self.MaxCodeLegalMoves)]
        while (len (moves) > 1):
            for m in moves:
                rang = budget // (len (moves) * np.log2 (total))
                rang=rang.astype(int)
                for i in range (rang):
                    s = copy.deepcopy (state)
                    s.play (m)
                    res = self.UCT.Update_Tree (s)
                    nplayouts [m.code ()] += 1
                    if state.turn == White:
                        nwins [m.code ()] += res
                    else:
                        nwins [m.code ()] += 1.0 - res
            moves = self.bestHalf (state, moves, nwins, nplayouts)
        return moves [0]


    def bestHalf (self, state, moves, nwins, nplayouts):
        """Choisi le meilleur mouvement pour un état du jeu

        Args:
            state (Board): Etat du jeu
            moves (list<Move>): Liste des mouvements
            nwins (list<int>): liste du nombre de victoire pour chaque noeud/état
            nplayouts (list<int>): liste du nombre de parties jouées pour chaque noeud/état

        Returns:
            list<Move>: Liste des meilleurs mouvements
        """    
        half = []
        notused = [True for x in range (self.MaxCodeLegalMoves)]
        rang=np.ceil(len (moves) / 2)
        rang=rang.astype(int)
        for i in range (rang):
            best = -1.0
            bestMove = moves [0]
            for m in moves:
                code = m.code ()
                if notused [code]:
                    mu = nwins [code] / nplayouts [code]
                    if mu > best:
                        best = mu
                        bestMove = m
            notused[bestMove.code ()] = False
            half.append (bestMove)
        return half

