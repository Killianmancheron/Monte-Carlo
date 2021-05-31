import numpy as np
import random
import matplotlib.pyplot as plt


#constants
Side = 7 #Longueur maximale du plateau
Cross_side = 3 #Largeur de la croix du plateau
Empty = 0 #espace vide
Ball = 1 #localistation des billes

BODY_COLOR = 'sienna'
HOLE_COLOR = 'chocolate'
BALL_COLOR = 'saddlebrown'

class Board():

    def __init__(self, size=(Side,Side), Cross_side=Cross_side):
        for dim in size :
            if (dim-Cross_side)%2==1:
                raise ValueError("Dimensions non conformes : {} et {} doivent être pairs ou impair".format(dim, Cross_side))
        #hashcde de l'état de l'environnement
        self.h=0 
        #Constantes de l'environnement :
        self.size=size
        self.Cross_side=Cross_side
        self.board=self.Reset_Board()
        self.set_Hashing()

    def Reset_Board(self):
        """Réinitialise la plateau du jeu

        Returns:
            np.array: Array numpy représentant le jeu et la position des billes par défaut
        """
        board = np.zeros(self.size)+Empty
        #remplissage des frontières du jeu
        x_start = (self.size[0]-self.Cross_side)//2
        board[:,x_start:(x_start+self.Cross_side)] = Ball
        y_start = (self.size[1]-self.Cross_side)//2
        board[y_start:(y_start+self.Cross_side),:] = Ball
        #Règle : le trou du milieu est vide par défaut
        board[self.size[0]//2,self.size[1]//2] = Empty
        return board

    def set_Hashing(self, seed=2100):
        if seed : random.seed(seed)
        hashTable = []
        # vide ou bille
        for k in range (2):
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
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                #Les mouvements possibles sont à deux cases verticales ou horizontales de la bille
                for k in [-2,0,2]:
                    for l in [-2,0,2]:
                        m = Move(i, j, i+k, j+l)
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
        nb_ball = self.board.sum()//Ball
        if nb_ball == 1:
            print('Victoire')
            return 1.0
        if len (self.legalMoves ()) == 0:
            return 0.0
        else:
            return 0.5

    def terminal(self):
        """Permet d'informer si une partie est finie ou non

        Returns:
            boolean: True si la partie est finie, False sinon
        """        
        return (self.score()!=0.5)

    def play(self, move, plot=False):
        """Execute le mouvement sur le plateau du jeu

        Args:
            move (Move): Mouvement à éffectuer
        """   
        #ajoute la bille sur la destination     
        self.h = self.h ^ self.hashTable [Ball] [move.x2] [move.y2]
        # equivalent à : 
        self.board [move.x2,move.y2] = Ball

        #retire la bille de l'emplacement :
        self.h = self.h ^ self.hashTable [Empty] [move.x1] [move.y1]
        # equivalent à : 
        self.board [move.x1,move.y1] = Empty

        #retire la bille entre l'origine et la destination du mouvement
        dx=move.x2-move.x1
        dy=move.y2-move.y1
        self.h = self.h ^ self.hashTable [Empty] [move.x1+dx//2] [move.y1+dy//2]
        # equivalent à : 
        self.board [move.x1+dx//2,move.y1+dy//2] = Empty
        
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
    def __make_cross__(self):
        """Permet de créer la croix symbolisant les emplacements possibles

        Returns:
            np.array: Matrice composée de 1 sur la croix et de 0 ailleurs.
        """        
        cross = np.zeros(self.size)+Empty
        x_start = (self.size[0]-self.Cross_side)//2
        cross[:,x_start:(x_start+self.Cross_side)] = Ball
        y_start = (self.size[1]-self.Cross_side)//2
        cross[y_start:(y_start+self.Cross_side),:] = Ball
        return cross

    def render(self, ax):
        """Permet d'afficher le plateau sous forme d'une figure

        Args:
            ax (Axes): Axe de la figure
        """          
        #Dessine le plateau
        ax.set_aspect( 1 ) 
        cc = plt.Circle(( 0.5 , 0.5 ), 0.495, color=BODY_COLOR) 
        ax.add_artist( cc ) 
        cc = plt.Circle(( 0.5 , 0.5 ), 0.48, alpha=.7, color=HOLE_COLOR)
        ax.add_artist( cc ) 
        cc = plt.Circle(( 0.5 , 0.5 ), 0.45, color=BODY_COLOR) 
        ax.add_artist( cc ) 
        #Dessine la croix des emplacements possibles
        cross = self.__make_cross__()
        x_coord = np.linspace(0.15,0.85,cross.shape[0])
        y_coord = np.linspace(0.15,0.85,cross.shape[1])
        for i in range(cross.shape[0]) :
            for j in range(cross.shape[1]) : 
                if cross[i,j] == 1 :
                    cc = plt.Circle(( x_coord[i], y_coord[j] ), 0.05, alpha=.7, color=HOLE_COLOR)
                    ax.add_artist( cc ) 
        ax.axis('off')
        plt.title( 'Goki Solitaire' )
        self.__update_render__(ax)

    def __update_render__(self, ax):
        """Met à jour la figure selon l'état du plateau

        Args:
            ax (Axes): Axe de la figure à mettre à jour
        """        
        x_coord = np.linspace(0.15,0.85,self.size[0])
        y_coord = np.linspace(0.15,0.85,self.size[1])
        for i in range(self.size[0]) :
            for j in range(self.size[1]) : 
                if self.board[i,j] == 1 :
                    cc = plt.Circle(( x_coord[i], y_coord[j] ), 0.04, color=BALL_COLOR)
                    ax.add_artist( cc ) 



class Move():

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def valid(self, Board):
        """Affirme si un mouvement est valide

        Args:
            Board (Board): Objet représentant le jeu

        Returns:
            boolean: True si le mouvement est possible, False sinon.
        """        
        #Destination dans le plan
        for destination in [self.x2, self.y2]:
            if destination<0 or destination>=Board.size[0]:
                return False
        #Prise en compte de la bordure
        border = (Board.size[0]-Board.Cross_side)/2
        for x,y in [(self.x1,self.y1),(self.x2,self.y2)]:
            if x<border and y<border:
                return False
            if x<border and y>=(Side-border):
                return False
            if x>=Side-border and y<border:
                return False
            if x>=Side-border and y>=(Side-border):
                return False
        #le mouvement est initié par une bille vers une case vide
        if Board.board[self.x2,self.y2]!=Empty:
            return False
        if Board.board[self.x1,self.y1]!=Ball:
            return False
        dx = self.x2-self.x1
        dy = self.y2-self.y1
        #la bille se trouve à deux cases, verticalement ou horizontalement, de la destination
        if (abs(dx)==0 and abs(dy)==2) or (abs(dx)==2 and abs(dy)==0):
            #la bille doit sauter par dessus une autre bille
            if Board.board[self.x1+dx//2,self.y1+dy//2] == Empty :
                return False
            else :
                return True
        else :
            False

    def code(self):
        
        if self.x1<self.x2 :
            direction = 0
        elif self.x1>self.x2 :
            direction = 1
        elif self.y1<self.y2:
            direction = 2
        else : 
            direction=3
        if self.x1%2==0 and self.y1%2==0:
            return 4*self.hashfunc() + direction
        elif self.x1%2==0 and self.y1%2!=0:
            return 4*16 + 4*self.hashfunc() + direction
        elif self.x1%2!=0 and self.y1%2==0:
            return 4*(16+12) + 4*self.hashfunc() + direction
        else :
            return 4*(16+12+12) + 4*self.hashfunc() + direction

    def hashfunc(self):
        return 4 * self.x1//2 + self.y1//2

if __name__ == "__main__":
    print("Vérification de l'initialisation de la grille : ")
    game = Board()
    print(game.board)
    print('Playout : ')
    game.playout(plot=True)
    print('Etat de fin de partie :')
    print(game.board)
    print('Test sur 10 000 parties :')
    nb_parties = 10_000
    nb_wins= 0
    for i in range(nb_parties):
        game.board=game.Reset_Board()
        nb_wins+=game.playout()
        if i%100==0:
            print(i,nb_wins, game.board.sum())
