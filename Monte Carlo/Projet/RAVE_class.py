import copy 
from math import sqrt, log
from Table_transposition import TranspoMonteCarlo
from AMAF_class import AMAF

Empty = 0
White = 1
Black = 2

class RAVE ():
    """Algorithme récursif RAVE permettant de mettre à mouj un arbre de noeuds

    Args:
        board (Board): Etat du jeu actuel
        played (list<int>): Liste des coups déjà joués, peut être vide

    """    

    def __init__(self):
        self.TMC = TranspoMonteCarlo()
        self.AMAF = AMAF()

    def Update_Tree (self, board, played):

        if board.terminal ():
            return board.score ()
            
        t = self.AMAF.look (board)


        if t != None:
            bestValue = -1000000.0
            best = 0
            moves = board.legalMoves ()
            bestcode = moves [0].code ()
            for i in range (0, len (moves)):
                val = 1000000.0
                code = moves [i].code ()
                if t [3] [code] > 0:
                    beta = t [3] [code] / (t [1] [i] + t [3] [code] + 1e-5 * t [1] [i] * t [3] [code])
                    Q = 1
                    if t [1] [i] > 0:
                        Q = t [2] [i] / t [1] [i]
                        if board.turn == Black:
                            Q = 1 - Q
                    AMAF = t [4] [code] / t [3] [code]
                    if board.turn == Black:
                        AMAF = 1 - AMAF
                    val = (1.0 - beta) * Q + beta * AMAF
                if val > bestValue:
                    bestValue = val
                    best = i
                    bestcode = code
            board.play (moves [best])
            played.append (bestcode)
            res = self.Update_Tree (board, played) 
            t [0] += 1
            t [1] [best] += 1
            t [2] [best] += res
            self.AMAF.updateAMAF (t, played, res)
            return res
        else:
            self.AMAF.addAMAF (board)
            return self.AMAF.playoutAMAF (board, played)


    def BestMove (self, board, n):
        """Permet d'obtenir le meilleur mouvement selon l'algorithme RAVE

        Args:
            board (Board): Etat du jeu dont on souhaite le meilleur coup
            n (int): Nombre d'itération pour une estimation

        Returns:
            Move: Meilleur mouvement estimé
        """    
        self.AMAF = AMAF()
        for i in range (n):
            b1 = copy.deepcopy (board)
            res = self.Update_Tree (b1, [])
        
        t = self.AMAF.look (board)
        moves = board.legalMoves ()
        best = moves [0]
        bestValue = t [1] [0]
        for i in range (1, len(moves)):
            if (t [1] [i] > bestValue):
                bestValue = t [1] [i]
                best = moves [i]
        return best