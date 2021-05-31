def SequentialHalving (state, budget):
    """Algorithme de Sequantial Halving minimisant le regret

    Args:
        state (Board): Etat du jeu actuel
        budget (int): Budget à allouer à chaque noeud

    Returns:
        Move: Mouvement sélectionné, minimisant le regret
    """    
    Table = {}
    add (board)
    moves = legalMoves (state)
    total = len (moves)
    nplayouts = [0.0 for x in range (MaxCodeLegalMoves)]
    nwins = [0.0 for x in range (MaxCodeLegalMoves)]
    while (len (moves) > 1):
        for m in moves:
            for i in range (budget // (len (moves) * np.log2 (total))):
                s = copy.deepcopy (state)
                play (s, m)
                res = UCT (s)
                nplayouts [m.code (state)] += 1
                if state.turn == White:
                    nwins [m.code (state)] += res
                else:
                    nwins [m.code (state)] += 1.0 - res
        moves = bestHalf (state, moves, nwins, nplayouts)
    return moves [0]


def bestHalf (state, moves, nwins, nplayouts):
    """Choisi le meilleur mouvement pour un état du jeu

    Args:
        state (Board): Etat du jeu
        moves (list<Move>): Liste des mouvements
        nwins (list<int>): liste du nombre de victoire pour chaque noeud/état
        nplayouts (list<int>): liste du nombre de parties jouées pour chaque noeud/état

    Returns:
        list<Move>: Liste des meilleurs mouvements
    """    
    half = []
    notused = [True for x in range (MaxCodeLegalMoves)]
    for i in range (np.ceil(len (moves) / 2)):
        best = -1.0
        bestMove = moves [0]
        for m in moves:
            code = m.code (state)
            if notused [code]:
                mu = nwins [code] / nplayouts [code]
                if mu > best:
                    best = mu
                    bestMove = m
            notused[bestMove.code (state)] = False
            half.append (bestMove)
    return half


def bestHalfSHUSS (t, state, moves, nwins, nplayouts):
    """Permet de sélectionner le meilleur mouvement selon SHUSS

    Args:
        t (np.array): Tableau/arbre des noeuds
        state (Board): Etat du jeu courant
        moves (List<Move>): Liste des mouvements
        nwins (list): Liste du nombre de victoire de chaque noeuds
        nplayouts ([type]): Liste du nombre de parties jouées de chaque noeuds

    Returns:
        [type]: [description]
    """    
    half = []
    notused = [True for x in range (MaxCodeLegalMoves)]
    c = 128
    for i in range (np.ceil(len (moves) / 2)):
        best = -1.0
        bestMove = moves [0]
        for m in moves:
            code = m.code (state)
            if notused [code]:
                AMAF = t [4] [code] / t [3] [code]
                if state.turn == Black:
                    AMAF = 1 - AMAF
                mu = nwins [code] / nplayouts [code] + c * AMAF / nplayouts [code]
                if mu > best:
                    best = mu
                    bestMove = m
        notused [bestMove.code (state)] = False
        half.append (bestMove)
    return half