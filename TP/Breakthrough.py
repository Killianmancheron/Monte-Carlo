import numpy as np
import random
from math import sqrt, log

#constants
Dx = 5
Dy = 5
Empty = 0
White = 1
Black = 2

class Board():
    """
    Classe repertoriant controlant le jeu Breaktrough
    """    

    def __init__(self,size=(Dx, Dy)):
        self.h = 0
        self.turn = White
        self.size = size
        self.board = self.Reset_Board()

    def Reset_Board(self):
        """Remet à zeros le jeu

        Returns:
            [np.array]: grille de taille Dx, Dy du jeu
        """        
        self.turn = White
        board = np.zeros(self.size)
        board[:2,:] = White
        board[-2:,:] = Black
        return board

    def legalMoves(self):
        """Liste renvoyant les coups possibles pour me tour du board

        Returns:
            [list<Move>]: liste des coups possibles
        """        
        moves = []
        for i in range (0, Dx):
            for j in range (0, Dy):
                if self.board [i] [j] == self.turn:
                    for k in [-1, 0, 1]:
                        for l in [-1, 0, 1]:
                            m = Move (self.turn, i, j, i + k, j + l)
                            if m.valid (self):
                                moves.append (m)
        return moves
    
    def score (self):
        """Permet d'attribuer un score à la partie

        Returns:
            [float]: renvoie 0.5 si rien ne se passe, 1 (resp 0) si les blancs (resp noirs)
            atteignent la ligne ou que les noirs (resp blancs) n'ont plus de coups possibles
        """        
        for i in range (0, Dy):
            if (self.board [Dx - 1] [i] == White):
                return 1.0
            elif (self.board [0] [i] == Black):
                return 0.0
        l = self.legalMoves ()
        if len (l) == 0:
            if self.turn == Black:
                return 1.0
            else:
                return 0.0
        return 0.5
    
    def terminal (self):
        """Permet de savoir si l'état est treminal

        Returns:
            [boolean]: état terminal
        """        
        if self.score () == 0.5:
            return False
        return True

   
    def play (self, move):
        """fait jouer le mouvement dans le board

        Args:
            move ([Move]): Objet Mouvement qui sera joué.
        """        
        col = int (self.board [move.x2] [move.y2])
        if col != Empty:
            self.h = self.h ^ hashTable [col] [move.x2] [move.y2]
        self.h = self.h ^ hashTable [move.color] [move.x2] [move.y2]
        self.h = self.h ^ hashTable [move.color] [move.x1] [move.y1]
        self.h = self.h ^ hashTurn
        self.board [move.x2] [move.y2] = move.color
        self.board [move.x1] [move.y1] = Empty
        if (move.color == White):
            self.turn = Black
        else:
            self.turn = White
            
    def playout (self):
        """Permet de jouer aléatoirement un partie sans imposer une politique

        Returns:
            [float]: Score de la partie aléatoire jouée
        """        
        while (True):
            moves = self.legalMoves ()
            if self.terminal ():
                return self.score ()
            n = random.randint (0, len (moves) - 1)
            self.play (moves [n])


def flat (board, n):
    """Permet d'obtenir le meilleur mouvement en se basant 
    sur celui qui offre le meilleur score au bout de n parties.

    Args:
        board (Board): Board actuel
        n (int): Nombre de playout joués pour estimer le meilleur coup

    Returns:
        Move : Mouvement avec le meilleur score pour un board donné et un nombre d'essais n.
    """    
    moves = board.legalMoves ()
    bestScore = 0
    bestMove = 0
    for m in range (len(moves)):
        sum = 0
        for i in range (n):
            b = copy.deepcopy (board)
            b.play (moves [m])
            r = b.playout ()
            if board.turn == Black:
                r = 1 - r
            sum = sum + r
        if sum > bestScore:
            bestScore = sum
            bestMove = m
    return moves [bestMove]


class Move():
    """
    Classe gerant les mouvements dans le jeu
    """    
    def __init__(self, color, x1, y1, x2, y2):
        self.color = color
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def valid (self, board):
        """Informe si un mouvement est valide dans un jeu

        Args:
            board (Board): Jeu dans lequel le mouvement veut s'exécuter

        Returns:
            boolean: Renvoie si le mouvement est valide ou non
        """        
        if self.x2 >= Dx or self.y2 >= Dy or self.x2 < 0 or self.y2 < 0:
            return False
        if self.color == White:
            if self.x2 != self.x1 + 1:
                return False
            if board.board [self.x2] [self.y2] == Black:
                if self.y2 == self.y1 + 1 or self.y2 == self.y1 - 1:
                    return True
                return False
            elif board.board [self.x2] [self.y2] == Empty:
                if self.y2 == self.y1 + 1 or self.y2 == self.y1 - 1 or self.y2 == self.y1:
                    return True
                return False
        elif self.color == Black:
            if self.x2 != self.x1 - 1:
                return False
            if board.board [self.x2] [self.y2] == White:
                if self.y2 == self.y1 + 1 or self.y2 == self.y1 - 1:
                    return True
                return False
            elif board.board [self.x2] [self.y2] == Empty:
                if self.y2 == self.y1 + 1 or self.y2 == self.y1 - 1 or self.y2 == self.y1:
                    return True
                return False
        return False
    
    
    def code (self, board):
        """Encode le mouvement

        Args:
            board (Board): Jeu dans lequel on encode le mouvement

        Returns:
            int : Entier du mouvement encodé
        """        
        direction = 0
        if self.y2 > self.y1:
            if board.board [self.x2] [self.y2] == Empty:
                direction = 1
            else:
                direction = 2
        if self.y2 < self.y1:
             if board.board [self.x2] [self.y2] == Empty:
                direction = 3
             else:
                 direction = 4
        if self.color == White:
            return 5 * (Dy * self.x1 + self.y1) + direction
        else:
            return 5 * Dx * Dy + 5 * (Dy * self.x1 + self.y1) + direction
