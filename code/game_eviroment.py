#import game_rules
import pandas as pd
import numpy as np




class Betting:

    def __init__(self, hand):
        
        self.prebet =False
        self.flopbet =False
        self.turnbet =False
        self.riverbet =False
        self.hand = hand

    
    def prebet_(self):

        #s =self.hand['players']
        #print(self.hand)
       for i in self.hand:
            print(i['players'])
        #    print(i, pl['seat'])

        




if __name__ in "__main__":
    
    hands = pd.read_csv('totalhands.csv')

    hands_dict = hands.to_dict('records')
    x = Betting(hands_dict)


    for i in x:
        

    print(x.prebet_())