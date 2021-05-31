def SHUSS (state, budget):
    """Algorithme Sequential Halfing combiné avec GRAVE

    Args:
        state (Board): Etat du jeu courant
        budget (int): Budjet allouer aux noeuds

    Returns:
        Move: Meilleur mouvement selon SHUSS
    """    
    Table = {}
    addAMAF (state)
    t = look (state)
    moves = legalMoves (state)
    total = len (moves)
    nplayouts = [0.0 for x in range (MaxCodeLegalMoves)]
    nwins = [0.0 for x in range (MaxCodeLegalMoves)]
    while (len (moves) > 1):
        for m in moves:
            for i in range (budget // (len (moves) * np.log2 (total))):
                s = copy.deepcopy (state)
                play (s, m)
                code = m.code (state)
                played =  [code]
                res = GRAVE (s, played, t)
                updateAMAF (t, played, res)
                nplayouts [code] += 1
                if state.turn == White:
                    nwins [code] += res
                else:
                    nwins [code] += 1.0 - res
        moves = bestHalfSHUSS (t, state, moves, nwins, nplayouts)
    return moves [0]