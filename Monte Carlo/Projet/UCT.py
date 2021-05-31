import copy 
from math import sqrt, log
from Table_transposition import TranspoMonteCarlo

class UCT():

    def __init__(self):
        self.TMC = TranspoMonteCarlo()

    def Update_Tree (self, board):
        """Algorithme récursif UCT permettant empiriquement d'évaluer un noeud/état du board 

        Args:
            board (Board): Etat du jeu à compléter

        """    
        if board.terminal ():
            return board.score ()
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
            res = self.Update_Tree (board)
            t [0] += 1
            t [1] [best] += 1
            t [2] [best] += res
            return res
        else:
            self.TMC.add (board)
            return board.playout()


    def BestMove (self, board, n):
        """Applique l'estimation UCT pour choisir le meilleur mouvement

        Args:
            board (Board): Etat du jeu dont on souhaite le meilleur mouvement
            n (int): Nombre de parties à jouer que l'on souhaite par noeud

        Returns:
            Move: meilleur mouvement selon l'algorithme.
        """    
        Table = {}
        for i in range (n):
            b1 = copy.deepcopy (board)
            res = self.Update_Tree (b1)
        t = self.TMC.look (board)
        moves = board.legalMoves ()
        best = moves [0]
        bestValue = t [1] [0]
        for i in range (1, len(moves)):
            if (t [1] [i] > bestValue):
                bestValue = t [1] [i]
                best = moves [i]
        return best

