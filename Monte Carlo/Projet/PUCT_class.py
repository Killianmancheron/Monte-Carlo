import copy 
from math import sqrt, log
from Table_transposition import TranspoMonteCarlo

Empty = 0
White = 1
Black = 2

class PUCT():

    def __init__(self):
        self.TMC = TranspoMonteCarlo()

    def PUCT (self, board):
        """Algorithme récursif UCT modifié utilisant les réseaux de neurones pour estimer une politique et une valeur.

        Args:
            board (Board): Etat du jeu

        Returns:
            float: Valeur de l'état
        """    
        if board.terminal ():
            return board.score ()
        t = self.TMC.look (board)
        if t != None:
            bestValue = -1000000.0
            best = 0
            moves = board.legalMoves ()
            for i in range (0, len (moves)):
                # t [4] = value from the neural network
                Q = t [4]
                if t [1] [i] > 0:
                    Q = t [2] [i] / t [1] [i]
                if board.turn == Black:
                    Q = 1 - Q
                # t [3] = policy from the neural network
                val = Q + 0.4 * t [3] [i] * sqrt (t [0]) / (1 + t [1] [i])
                if val > bestValue:
                    bestValue = val
                    best = i
            board.play (moves [best])
            res = self.PUCT (board)
            t [0] += 1
            t [1] [best] += 1
            t [2] [best] += res
            return res
        else:
            t = self.TMC.add (board)
            return t [4]

    def BestMove (self, board, n):
        """Applique l'estimation PUCT pour choisir le meilleur mouvement

        Args:
            board (Board): Etat du jeu dont on souhaite le meilleur mouvement
            n (int): Nombre de parties à jouer que l'on souhaite par noeud

        Returns:
            Move: meilleur mouvement selon l'algorithme.
        """    
        self.TMC = TranspoMonteCarlo()
        #Table = {}
        for i in range (n):
            b1 = copy.deepcopy (board)
            res = self.PUCT (b1)
        t = self.TMC.look (board)
        moves = board.legalMoves ()
        best = moves [0]
        bestValue = t [1] [0]
        for i in range (1, len(moves)):
            if (t [1] [i] > bestValue):
                bestValue = t [1] [i]
                best = moves [i]
        return best