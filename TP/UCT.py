def UCB (board, n):
    """Algorithme UCB permettant d'estimer le meilleur mouvement possbile à partir d'un état du jeu

    Args:
        board (Board): Jeu dans lequel on souhaite extraire le meilleur mouvement
        n (int): Nombre d'estimation que l'on souhaite réaliser pour estimer le meilleur mouvement

    Returns:
        Move: Meilleur mouvement sélectionné
    """    
    moves = board.legalMoves ()
    sumScores = [0.0 for x in range (len (moves))]
    nbVisits = [0 for x in range (len(moves))]
    for i in range (n):
        bestScore = 0
        bestMove = 0
        for m in range (len(moves)):
            score = 1000000
            if nbVisits [m] > 0:
                 score = sumScores [m] / nbVisits [m] + 0.4 * math.sqrt (math.log (i) / nbVisits [m])
            if score > bestScore:
                bestScore = score
                bestMove = m
        b = copy.deepcopy (board)
        b.play (moves [bestMove])
        r = b.playout ()
        if board.turn == Black:
            r = 1.0 - r
        sumScores [bestMove] += r
        nbVisits [bestMove] += 1
    bestScore = 0
    bestMove = 0
    for m in range (len(moves)):
        score = nbVisits [m]
        if score > bestScore:
            bestScore = score
            bestMove = m
    return moves [bestMove]

#voir si faire .py poour générer la hash table à part
hashTable = []
# blanc vide et noir
for k in range (3):
    l = []
    for i in range (Dx):
        l1 = []
        for j in range (Dy):
            l1.append (random.randint (0, 2 ** 64))
        l.append (l1)
    hashTable.append (l)
hashTurn = random.randint (0, 2 ** 64)


MaxLegalMoves = 2 * (3 * (Dx - 2) + 4)
Table = {}
 
def add (board):
    """Ajoute dans la table un nouveau noeud pour inserer les informations

    Args:
        board (Board): Etat du jeu
    """    
    nplayouts = [0.0 for x in range (MaxLegalMoves)]
    nwins = [0.0 for x in range (MaxLegalMoves)]
    Table [board.h] = [0, nplayouts, nwins]
 
def look (board):
    """Extrait les informations d'un noeud

    Args:
        board (Board): Etat du jeu que l'on souhaite extraire

    Returns:
        list: list contenant le nombre de playout réalisés et le nombre de victoires.
    """    
    return Table.get (board.h, None)

def UCT (board):
    """Algorithme récursif UCT permettant empiriquement d'évaluer un noeud/état du board 

    Args:
        board (Board): Etat du jeu à compléter

    """    
    if board.terminal ():
        return board.score ()
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
                    Q = 1 - Q
                val = Q + 0.4 * sqrt (log (t [0]) / t [1] [i])
            if val > bestValue:
                bestValue = val
                best = i
        board.play (moves [best])
        res = UCT (board)
        t [0] += 1
        t [1] [best] += 1
        t [2] [best] += res
        return res
    else:
        add (board)
        return board.playout()


def BestMoveUCT (board, n):
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
        res = UCT (b1)
    t = look (board)
    moves = board.legalMoves ()
    best = moves [0]
    bestValue = t [1] [0]
    for i in range (1, len(moves)):
        if (t [1] [i] > bestValue):
            bestValue = t [1] [i]
            best = moves [i]
    return best

