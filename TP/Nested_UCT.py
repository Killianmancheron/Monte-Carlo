from Projet.UCT import UCT
from TP.Misere_Breakthrough import Board_Misere

from math import sqrt, log

class NUCT(UCT):

    def Update_Tree (self, board, t1):
        """Algorithme récursif UCT permettant empiriquement d'évaluer un noeud/état du board 

        Args:
            board (Board): Etat du jeu à compléter

        """    
        if board.terminal ():
            return board.misereScore () / (t1 + 1)
        t = self.TMC.look (board)

        if t != None:
            bestValue = -1000000.0
            best = 0
            moves = board.legalMoves ()
            for i in range (0, len (moves)):
                val = 1000000.0
                if t [1] [i] > 0:
                    Q = t [2] [i] / t [1] [i]
                    val = Q + 0.4 * sqrt (log (t [0]) / t [1] [i])
                if val > bestValue:
                    bestValue = val
                    best = i
            board.play (moves [best])
            res = self.Update_Tree (board, t1+1)
            t [0] += 1
            t [1] [best] += 1
            t [2] [best] += res
            return res
        else:
            self.TMC.add (board)
            return board.nestedDiscountedPlayout(t1)



def UCTNested (board, t1):
    if board.terminal ():
        return board.misereScore () / (t1 + 1)
    t = look (board)
    if t != None:
        bestValue = -1000000.0
        best = 0
        moves = board.legalMoves ()
        for i in range (0, len (moves)):
            val = 1000000.0
            if t [1] [i] > 0:
                Q = t [2] [i] / t [1] [i]
                if board.turn == Black:
                    Q = -Q
                val = Q + 0.4 * sqrt (log (t [0]) / t [1] [i])
            if val > bestValue:
                bestValue = val
                best = i
        board.play (moves [best])
        res = UCTNested (board, t1 + 1)
        t [0] += 1
        t [1] [best] += 1
        t [2] [best] += res
        return res
    else:
        add (board)
        return board.nestedDiscountedPlayout (t1)