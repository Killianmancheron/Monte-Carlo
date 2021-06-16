import copy 
from math import sqrt, log
from Table_transposition import TranspoMonteCarlo
from UCT import UCT
from AMAF_class import AMAF
from GRAVE_class import GRAVE
import numpy as np

Empty = 0
White = 1
Black = 2

class SHUSS():
    def __init__(self):
            self.TMC = TranspoMonteCarlo()
            self.AMAF = AMAF()
            self.GRAVE = GRAVE()
            #self.Dx=5
            #self.Dy=5
            self.Side=8
            self.MaxCodeLegalMoves = 2 * self.Side * self.Side * 8
            self.MaxLegalMoves=32
    

    def BestMove (self, state, budget):
        """Algorithme Sequential Halfing combiné avec GRAVE

        Args:
            state (Board): Etat du jeu courant
            budget (int): Budjet allouer aux noeuds

        Returns:
            Move: Meilleur mouvement selon SHUSS
        """    
        #Table ={}
        self.AMAF = AMAF()
        self.AMAF.addAMAF (state)
        t = self.AMAF.look (state)
        moves = state.legalMoves ()
        total = len (moves)
        nplayouts = [0.0 for x in range (self.MaxCodeLegalMoves)]
        nwins = [0.0 for x in range (self.MaxCodeLegalMoves)]
        while (len (moves) > 1):
            for m in moves:
                rang=budget // (len (moves) * np.log2 (total))
                rang=rang.astype(int)
                for i in range (rang):
                    s = copy.deepcopy (state)
                    s.play (m)
                    code = m.code ()
                    played =  [code]
                    res = self.GRAVE.GRAVE(s, played, t)
                    self.AMAF.updateAMAF (t, played, res)
                    nplayouts [code] += 1
                    if state.turn == White:
                        nwins [code] += res
                    else:
                        nwins [code] += 1.0 - res
            moves = self.bestHalfSHUSS (t, state, moves, nwins, nplayouts)
        return moves [0]


    def bestHalfSHUSS (self, t, state, moves, nwins, nplayouts):
        """Permet de sélectionner le meilleur mouvement selon SHUSS

        Args:
            t (np.array): Tableau/arbre des noeuds
            state (Board): Etat du jeu courant
            moves (List<Move>): Liste des mouvements
            nwins (list): Liste du nombre de victoire de chaque noeuds
            nplayouts ([type]): Liste du nombre de parties jouées de chaque noeuds

        Returns:
            [type]: [description]
    """    
        half = []
        notused = [True for x in range (self.MaxCodeLegalMoves)]
        c = 128
        rang=np.ceil(len (moves) / 2)
        rang=rang.astype(int)
        for i in range (rang):
            best = -1.0
            bestMove = moves [0]
            for m in moves:
                code = m.code ()
                if notused [code]:
                    AMAF = t [4] [code] / t [3] [code]
                    if state.turn == Black:
                        AMAF = 1 - AMAF
                    mu = nwins [code] / nplayouts [code] + c * AMAF / nplayouts [code]
                    if mu > best:
                        best = mu
                        bestMove = m
            notused [bestMove.code ()] = False
            half.append (bestMove)
        return half





   