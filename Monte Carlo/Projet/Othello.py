import numpy as np
import random
import matplotlib.pyplot as plt


#constants
Side = 8 #Longueur maximale du plateau
Empty = 0 #espace vide
White = 1 #palets blancs
Black = 2 #palets noirs

BODY_COLOR = 'sienna'
TABLE_COLOR = 'green'
GRID_COLOR = 'gray'
BLACK_COLOR = 'black'
WHITE_COLOR = 'white'

class Board():

    def __init__(self, Side=Side):
        #hashcde de l'état de l'environnement
        self.h=0 

        assert Side%2==0
        #Constantes de l'environnement :
        self.turn = White
        self.Side=Side
        self.board=self.Reset_Board()
        self.set_Hashing()

    def Reset_Board(self):
        """Réinitialise la plateau du jeu

        Returns:
            np.array: Array numpy représentant le jeu et la position des billes par défaut
        """
        self.turn = White
        board = np.zeros((self.Side,self.Side))+Empty
        middle = self.Side//2
        board[middle,middle]=White
        board[middle-1,middle-1]=White
        board[middle,middle-1]=Black
        board[middle-1,middle]=Black
        return board

    def set_Hashing(self, seed=2100):
        if seed : random.seed(seed)
        hashTable = []
        # vide ou Noir ou Blanc
        for k in range (3):
            l = []
            # ligne
            for i in range (Side):
                l1 = []
                # colonne
                for j in range (Side):
                    l1.append (random.randint (0, 2 ** 64))
                l.append (l1)
            hashTable.append (l)
        hashTurn = random.randint (0, 2 ** 64)
        self.hashTable=hashTable
        self.hashTurn=hashTurn

    def legalMoves(self):
        """Permet d'extraire une liste des mouvements possibles

        Returns:
            list<Move>: Liste des mouvements valides
        """        
        moves=[]
        for i in range(self.Side):
            for j in range(self.Side):
                if self.board[i,j]==Empty:
                    m = Move(self.turn, i, j)
                    if m.valid(self):
                        moves.append(m)
                
        return moves

    def score(self):
        """Score du jeu en cours : 
            - Vaut 1 s'il n'y a plus qu'une bille restante
            - Vaut 0 s'il y a plus d'une bille restante et aucun mouvement possible
            - Vaut 0.5 si la partie n'est pas encore terminée

        Returns:
            float: Score du jeu
        """        
        l=self.legalMoves ()
        if len (l) != 0:
            return 0.5
        else:
            nb_white = (self.board==White).sum()
            nb_black = (self.board==Black).sum()
            if nb_black>nb_white:
                return 1.0
            else :
                return 0.0
        
    def terminal(self):
        """Permet d'informer si une partie est finie ou non

        Returns:
            boolean: True si la partie est finie, False sinon
        """        
        return (self.score()!=0.5)

    def replace(self, how, board, x, y):
        if (self.turn == Black):
            self.adv = White
        else:
            self.adv = Black
        
        if how=='vertical':
            array = board[:,y]
            split_array = [np.flip(array[:x],0),array[x+1:]]
        elif how=='diagonal':
            k=y-x
            array=board.ravel()[max(k,-board.shape[1]*k):max(0,(board.shape[1]-k))*board.shape[1]:board.shape[1]+1]
            split_array = [np.flip(array[:min(x,y)],0),array[min(x,y)+1:]]
        else :
            raise ValueError('Mise à jour non définie : {}'.format(how))

        for t,sub_array in enumerate(split_array):
            i=0
            while (i<len(sub_array)) :
                if(sub_array[i]==Empty):
                    break
                if sub_array[i]==self.turn and i>0 and (sub_array[0]!=self.turn) :
                    if how=='diagonal':
                        for l in range(i+1):
                            if t==0:
                                board[x-l,y-l]=self.turn
                                self.h = self.h ^ self.hashTable [self.turn] [x-l] [y-l]
                            else:
                                board[x+l,y+l]=self.turn
                                self.h = self.h ^ self.hashTable [self.turn] [x+l] [y+l]
                    else:
                        for l in range(i+1):
                            if t==0:
                                board[x-l,y]=self.turn
                                self.h = self.h ^ self.hashTable [self.turn] [x-l] [y]
                            else:
                                board[x+l,y]=self.turn
                                self.h = self.h ^ self.hashTable [self.turn] [x+l] [y]
                i+=1


    def play(self, move):
        """Execute le mouvement sur le plateau du jeu

        Args:
            move (Move): Mouvement à éffectuer
        """   
        self.board [move.x,move.y] = move.color
        self.h = self.h ^ self.hashTable [move.color] [move.x] [move.y]
        if move.valid_scope('vertical',self.board, move.x, move.y): 
            self.replace('vertical', self.board, move.x, move.y)
        elif move.valid_scope('vertical',self.board.T,move.y,move.x):
            self.replace('vertical', self.board.T, move.y, move.x)
        elif move.valid_scope('diagonal', self.board, move.x, move.y):
            self.replace('diagonal', self.board, move.x, move.y)
        elif move.valid_scope('diagonal', np.flip(self.board,1), move.x, self.Side-1-move.y):
            self.replace('diagonal', np.flip(self.board,1), move.x, self.Side-1-move.y)

        self.h = self.h ^ self.hashTurn
        if (move.color == White):
            self.turn = Black
        else:
            self.turn = White
        
    def playout (self, plot=False):
        """Permet de jouer aléatoirement un partie sans imposer une politique

        Returns:
            [float]: Score de la partie aléatoire jouée
        """     
        if plot : 
            plt.ion()
            fig = plt.figure()
            ax = fig.add_subplot(111)
        while (True):
            if plot :
                self.render(ax)
                fig.canvas.draw()
                plt.pause(0.01)
            moves = self.legalMoves ()
            if self.terminal ():
                return self.score ()
            n = random.randint (0, len (moves) - 1)
            self.play (moves [n])

    #Fonctions permettant un rendu graphique :
    def render(self, ax):
        """Permet d'afficher le plateau sous forme d'une figure

        Args:
            ax (Axes): Axe de la figure
        """          
        #Dessine le plateau
        ax.set_aspect( 1 ) 
        cc = plt.Rectangle(( 0. , 0. ), 1, 1, color=BODY_COLOR) 
        ax.add_artist( cc ) 
        cc = plt.Rectangle(( 0.02 , 0.02 ), .96, .96, color=TABLE_COLOR)
        ax.add_artist( cc ) 
        y_coord = np.linspace(0.15,0.85,self.Side)
        for i in range(self.Side) : 
            cc = plt.hlines(y_coord[i]+0.05, .05, .95, color=GRID_COLOR)
            ax.add_artist( cc )
        cc = plt.hlines(.1, .05, .95, color=GRID_COLOR)
        ax.add_artist( cc )
        x_coord = np.linspace(0.15,0.85,self.Side)
        for i in range(self.Side) : 
            cc = plt.vlines(y_coord[i]+0.05, .05, .95, color=GRID_COLOR)
            ax.add_artist( cc )
        cc = plt.vlines(.1, .05, .95, color=GRID_COLOR)
        ax.add_artist( cc )
        ax.axis('off')
        ax.grid()
        plt.title( 'Goki Solitaire' )
        self.__update_render__(ax)

    def __update_render__(self, ax):
        """Met à jour la figure selon l'état du plateau

        Args:
            ax (Axes): Axe de la figure à mettre à jour
        """        
        x_coord = np.linspace(0.15,0.85,self.Side)
        y_coord = np.linspace(0.15,0.85,self.Side)
        for i in range(self.Side) :
            for j in range(self.Side) : 
                if self.board[i,j] == White :
                    cc = plt.Circle(( x_coord[i], y_coord[j] ), 0.04, color=WHITE_COLOR)
                    ax.add_artist( cc )
                elif self.board[i,j] == Black :
                    cc = plt.Circle(( x_coord[i], y_coord[j] ), 0.04, color=BLACK_COLOR)
                    ax.add_artist( cc )


class Move():

    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        
    def valid_scope(self, how, board, x, y):
    
        Side=board.shape[0]
        if not ((x>=0 and x<Side) & (y>=0 and y<Side)):
            raise ValueError("coordonates doesn't exists")

        is_valid = False
        if how=='vertical':
            array = board[:,y]
            split_array = [np.flip(array[:x],0),array[x+1:]]
        elif how=='diagonal':
            k=y-x
            array=board.ravel()[max(k,-board.shape[1]*k):max(0,(board.shape[1]-k))*board.shape[1]:board.shape[1]+1]
            split_array = [np.flip(array[:min(x,y)],0),array[min(x,y)+1:]]
        else :
            raise ValueError('Mise à jour non définie : {}'.format(how))

        for sub_array in split_array:
            i=0
            while (i<len(sub_array)) :
                if(sub_array[i]==Empty):
                    break
                if sub_array[i]==self.color and i>0 and (sub_array[0]!=self.color) :
                    is_valid=True
                i+=1
        return is_valid

    def valid(self, Board):
        """Affirme si un mouvement est valide

        Args:
            Board (Board): Objet représentant le jeu

        Returns:
            boolean: True si le mouvement est possible, False sinon.
        """        
        board=Board.board
        return (
            self.valid_scope('vertical', board,self.x,self.y) or
            self.valid_scope('vertical',board.T,self.y,self.x) or
            self.valid_scope('diagonal',board, self.x, self.y) or
            self.valid_scope('diagonal',np.flip(board,1), self.x, Side-1-self.y)
        )

    def code(self):
        """Code du mouvement pour les algorithmes RAVE ou GRAVE.

        Returns:
            int: Hashcode du mouvement
        """        
        if self.color == White:
            return Side * self.x + self.y
        else:
            return Side*Side + Side * self.x + self.y
        
if __name__ == "__main__":
    print("Vérification de l'initialisation de la grille : ")
    game = Board()
    print(game.board)
    print('Playout : ')
    game.playout(plot=True)
    print('Etat de fin de partie :')
    print(game.board)
    