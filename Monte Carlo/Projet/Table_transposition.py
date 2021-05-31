import pickle
 


#Cas du Goki Solitaire

Dx=5
MaxLegalMoves = 26
class TranspoMonteCarlo():

    def __init__(self):
        self.table = {}

    def add(self, board):
            nplayouts = [0.0 for x in range (MaxLegalMoves)]
            nwins = [0.0 for x in range (MaxLegalMoves)]
            self.table [board.h] = [0, nplayouts, nwins]
        
    def look(self, board):
        return self.table.get (board.h, None)

    def save_table(self, filename):
        # Open a file and use dump()
        with open(filename, 'wb') as file:
            # A new file will be created
            pickle.dump(self.table, file)

    def load_table(self, filename):
        # Open the file in binary mode
        with open(filename, 'rb') as file:
            # Call load method to deserialze
            self.table = pickle.load(file)