def PUCT (board):
    """Algorithme récursif UCT modifié utilisant les réseaux de neurones pour estimer une politique et une valeur.

    Args:
        board (Board): Etat du jeu

    Returns:
        float: Valeur de l'état
    """    
    if board.terminal ():
        return board.score ()
    t = look (board)
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
        res = PUCT (board)
        t [0] += 1
        t [1] [best] += 1
        t [2] [best] += res
        return res
    else:
        t = add (board)
        return t [4]