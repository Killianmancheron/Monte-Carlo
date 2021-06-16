import copy 
from math import sqrt, log
from Table_transposition import TranspoMonteCarlo
from AMAF_class import AMAF

Empty = 0
White = 1
Black = 2

class GRAVE():
    
    def __init__(self):
        self.TMC = TranspoMonteCarlo()
        self.AMAF = AMAF()

    def GRAVE (self, board, played, tref):
        """Permet de récursivement mettre à jour l'arbre des noeuds selon l'algorithme GRAVE

        Args:
            board (Board): Etat du jeu à compléter
            played (list): Liste des coups joués
            tref (np.array): Tableau/arbre des noeuds de reférence

        Returns:
            [type]: [description]
        """    
        if (board.terminal ()):
            return board.score ()

        t = self.AMAF.look (board)
        
        if t != None:
            tr = tref
            if t [0] > 50:
                tr = t
            bestValue = -1000000.0
            best = 0
            moves = board.legalMoves ()
            bestcode = moves [0].code ()
            for i in range (0, len (moves)):
                val = 1000000.0
                code = moves [i].code ()
                if tr [3] [code] > 0:
                    beta = tr [3] [code] / (t [1] [i] + tr [3] [code] + 1e-5 * t [1] [i] * tr [3] [code])
                    Q = 1
                    if t [1] [i] > 0:
                        Q = t [2] [i] / t [1] [i]
                        if board.turn == Black:
                            Q = 1 - Q
                    AMAF = tr [4] [code] / tr [3] [code]
                    if board.turn == Black:
                        AMAF = 1 - AMAF
                    val = (1.0 - beta) * Q + beta * AMAF
                if val > bestValue:
                    bestValue = val
                    best = i
                    bestcode = code
            board.play (moves [best])
            played.append (bestcode)
            res = self.GRAVE (board, played, tr)
            t [0] += 1
            t [1] [best] += 1
            t [2] [best] += res
            self.AMAF.updateAMAF (t, played, res)
            return res
        else:
            self.AMAF.addAMAF (board)
            return self.AMAF.playoutAMAF (board, played)

    def BestMove (self, board, n):
        """Permet d'obtenier le meilleur mouvement grâce à GRAVE

        Args:
            board (Board): Etat du jeu dont l'on souhaite le meilleur mouvement
            n (int): Nombre d'itérations pour estimer le score de chaqu noeud

        Returns:
            Move: Meilleur mouvement selon l'algorithme.
        """
        self.AMAF = AMAF()    
        self.AMAF.addAMAF (board)
        for i in range (n):
            t = self.AMAF.look (board)
            b1 = copy.deepcopy (board)
            res = self.GRAVE (b1, [], t)
        t = self.AMAF.look (board)
        moves = board.legalMoves ()
        best = moves [0]
        bestValue = t [1] [0]
        for i in range (1, len(moves)):
            if (t [1] [i] > bestValue):
                bestValue = t [1] [i]
                best = moves [i]
        return best