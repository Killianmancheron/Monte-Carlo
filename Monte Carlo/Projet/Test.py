import matplotlib.pyplot as plt
from Breakthrough import Board
from Goki_solitaire import Board
from UCB import UCB
from UCT import UCT
import os
import numpy as np
#from TranspoMonteCarlo import TranspoMonteCarlo

print("Vérification de l'initialisation de la grille : ")
game = Board()

print(game.playout(plot=True))

# print('Playing UCB : ')
# plt.ion()
# fig = plt.figure()
# ax = fig.add_subplot(111)
# while not game.terminal():
#     game.render(ax)
#     fig.canvas.draw()
#     plt.pause(0.000001)
#     move = UCB(game,5)
#     game.play(move)
#     print(game.board)
# game.render(ax)
# fig.canvas.draw()
# plt.pause(10)


# game.board = game.Reset_Board()
# print("Playing UCT :")
# policy=UCT()
# if os.path.isfile('UCT_tree.pkl'):
#     print('Loading Tree')
#     policy.TMC.load_table('UCT_tree.pkl')
# # plt.ion()
# # fig = plt.figure()
# # ax = fig.add_subplot(111)
# while not game.terminal():
#     # game.render(ax)
#     # fig.canvas.draw()
#     # plt.pause(0.000001)
#     print(game.board)
#     move = policy.BestMove(game,100000)
#     game.play(move)
#     policy.TMC.save_table('UCT_tree.pkl')
# # game.render(ax)
# # fig.canvas.draw()
# # plt.pause(3)
# print('Tree saved')
# print(policy.TMC.table)

