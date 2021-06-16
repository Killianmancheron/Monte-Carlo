import copy 
from math import sqrt, log
from Table_transposition import TranspoMonteCarlo
import random

#Cas du Goki Solitaire




class AMAF():
    def __init__(self):
        #self.Dx=5
        #self.Dy=5
        self.Side=8
        self.MaxCodeLegalMoves = 2 * self.Side * self.Side * 8
        self.MaxLegalMoves=32
        self.Table = {}

    def playoutAMAF (self, board, played):
        """Applqiue l'algorithme AMAF sur le jeu 

        Args:
            board (Board): Etat du jeu
            played (list<int>): Liste encodée des mouvements déjà joués.

        Returns:
            float: Score de la partie jouée
        """    
        while (True):
            moves = []
            moves = board.legalMoves ()
            if len (moves) == 0 or board.terminal ():
                return board.score ()
            n = random.randint (0, len (moves) - 1)
            played.append (moves [n].code ())
            board.play (moves [n])

    
    
    def addAMAF (self, board):
        """Ajoute les informations de AMAF pour un noeud

        Args:
            board (Board): Noeud/Etat du jeu à créer
        """    
        nplayouts = [0.0 for x in range (self.MaxLegalMoves)]
        nwins = [0.0 for x in range (self.MaxLegalMoves)]
        nplayoutsAMAF = [0.0 for x in range (self.MaxCodeLegalMoves)]
        nwinsAMAF = [0.0 for x in range (self.MaxCodeLegalMoves)]
        self.Table [board.h] = [0, nplayouts, nwins, nplayoutsAMAF, nwinsAMAF]

    def updateAMAF (self, t, played, res):
        """Met à jour la table/l'arbre des noeuds sur les différents coups joués

        Args:
            t (np.array): Table / Arbre des noeuds
            played (list<int>): Liste de noeuds joués
            res (float): Résultats d'une partie.
        """    
        for i in range (len (played)):
            code = played [i]
            seen = False
            for j in range (i):
                if played [j] == code:
                    seen = True
            if not seen:
                t [3] [code] += 1
                t [4] [code] += res

    def look(self, board):
        return self.Table.get (board.h, None)

    # def AMAF (self, board):
    #     """Permet d'executer l'algorithme récursif AMAF sur un jeu pour metter à jour l'arbre des noeuds

    #     Args:
    #         board (Board): Etat du jeu à compléter

    #     """    
    #     if board.terminal ():
    #         return board.score ()
    #     t = self.TMC.look (board)
    #     if t != None:
    #         bestValue = -1000000.0
    #         best = 0
    #         moves = board.legalMoves ()
    #         for i in range (0, len (moves)):
    #             val = 1000000.0
    #             if t [1] [i] > 0:
    #                 Q = t [2] [i] / t [1] [i]
    #                 if board.turn == Black:
    #                     Q = 1 - Q
    #                 val = Q + 0.4 * sqrt (log (t [0]) / t [1] [i])
    #             if val > bestValue:
    #                 bestValue = val
    #                 best = i
    #         board.play (moves [best])
    #         res = self.AMAF (board)
    #         self.updateAMAF (t, played, res)
    #         return res
    #     else:
    #         self.addAMAF (board)
    #         return board.playout 