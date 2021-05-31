import copy
import math

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
