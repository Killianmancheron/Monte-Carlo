from TP.Misere_Breakthrough import Board_Misere
import random
import copy

T = []
Game = Board_Misere()

def delta(s):
    moves = Game.legalMoves()
    next_s = []
    for m in moves:
        next_s.append(Game.play(m))
        Game.board = s 
    return next_s
