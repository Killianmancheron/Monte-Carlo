from TP.Breakthrough import Board
import numpy as np
import random
import copy

#constants
Dx = 5
Dy = 5
Empty = 0
White = 1
Black = 2

class Board_Misere(Board):

    def misereScore (self):
        """Permet d'attribuer un score à la partie

        Returns:
            [float]: renvoie 0.5 si rien ne se passe, 1 (resp 0) si les blancs (resp noirs)
            atteignent la ligne ou que les noirs (resp blancs) n'ont plus de coups possibles
        """        
        s = Board.score()
        if s==1:
            return 1
        else:
            return -1

    def discountedPlayout (self):
        """Permet de jouer aléatoirement un partie sans imposer une politique

        Returns:
            [float]: Score de la partie aléatoire jouée
        """        
        turn = 0
        while (True):
            moves = self.legalMoves ()
            if self.terminal ():
                return self.score ()/(turn+1)
            n = random.randint (0, len (moves) - 1)
            self.play (moves [n])
            turn+=1


    def nestedDiscountedPlayout (self, t):
        while (True):
            if self.terminal ():
                return self.misereScore () / (t + 1)
            moves = self.legalMoves ()
            bestMove = moves [0]
            best = -2
            for i in range (len (moves)):
                b = copy.deepcopy (self)
                b.play (moves [i])
                s = b.discountedPlayout (t)
                if self.turn == Black:
                    s = -s
                if s > best:
                    best = s
                    bestMove = moves [i]
            self.play (bestMove)
            t = t + 1

    def code (self, move):
        direction = 1
        if move.y2 > move.y1:
            direction = 0
        if move.y2 < move.y1:
            direction = 2
        capture = 0
        if self.board [move.x2] [move.y2] != Empty:
            capture = 1
        if move.color == White:
            return 6 * (Dy * move.x1 + move.y1) + 2 * direction + capture
        else:
            return 6 * Dx * Dy + 6 * (Dy * move.x1 + move.y1) + 2 * direction + capture
