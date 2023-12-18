import pandas as pd
import numpy as np 
import random



######## Players ############
class Player:
    def __init__(self, player_count, starting_chips):
        self.player_count =player_count
        self.starting_chips = starting_chips
        self.player_dict ={}
        self.current_chips =None


    def betting_order(self):
        
        self.betting_order =[]

        for idx in range(self.player_count):
            self.betting_order.append(idx)
        random.shuffle(self.betting_order)

        return self.betting_order
        
    
    
    
    
    
    
    
    
    def player_number(self):

        
        
        betting_order = self.betting_order()
        
        for i in range(self.player_count):
            
            #self.starting_seat = i
            
            if i ==0:
                self.smallblind =True
            else: self.smallblind =False

            if i ==1:
                self.bigblind =True
            else: self.bigblind = False


            self.chips = round(random.uniform(self.starting_chips, 600), 2)

            self.player_dict[i] = {'chip count':self.chips, 'seat': betting_order[i], 'smallblind':self.smallblind, 'bigblind':self.bigblind   }
    
        return self.player_dict
    def player_update(self):
        pass


#########  DECK #########
class Deck:
    def __init__(self, deck, players):
        self.deck = deck
        self.rank = None
        self.flop1=None
        self.flop2=None
        self.flop3=None
        self.turn=None
        self.river=None
        self.burnpile =[]
        self.t_cards =None
        self.players =players    
    def draw(self):
        
        arr =np.arange(1,52)
        np.random.shuffle(arr)

        
        #for player_num, playerinfo in self.players.items():


        player_num = len(self.players)

        #for i in range(player_num):

        
        
        
        self.flop1= self.deck[arr[-1]]
        self.flop2=self.deck[arr[-2]]
        self.flop3=self.deck[arr[-3]]
        self.turn=self.deck[arr[-4]]
        self.river=self.deck[arr[-5]]

        self.t_cards =[self.flop1, self.flop2, self.flop3, self.turn, self.river]

        player_cards =[]
        for i in range(player_num):
            holecards = [self.deck[arr[i]],self.deck[arr[player_num+i]]]
            self.players[i]['holecards'] = holecards
            self.players[i]['communitycards'] = self.t_cards
            self.players[i]['totalcards'] = self.t_cards + holecards



        #print(self.t_cards[0])
        return  self.players, self.t_cards
    


    
######### Hand Order ##############
class Hand_defs:
    def __init__(self, players):
        self.t_cards =players
        self.pair =None
        self.trips =None
        self.quads =None

        

    ##### Check for pair ###### 
    def check_pair(self):
        
        pair_order =None
        #### Find Pair ####
        for i in range(len(self.t_cards)):
            count =0
            for j in range(i + 1, len(self.t_cards)):
                if self.t_cards[i][0] == self.t_cards[j][0]:
                    count +=1
                    self.pair_order = self.t_cards[i][2] 
            if count ==1:        
                    return True #, self.pair_order
        return False
    
    def check_two_pair(self):
        pairs = []
        for i in range(len(self.t_cards)):
            count = 0
            for j in range(i + 1, len(self.t_cards)):
                if self.t_cards[i][0] == self.t_cards[j][0]:
                    count += 1
            if count == 1 and self.t_cards[i][0] not in pairs:
                pairs.append(self.t_cards[i][2])
        if len(pairs) == 2:
            return True #, pairs
        else: return False

    
    #### Check for trips ######
    def check_trips(self):

        for i in range(len(self.t_cards)):
            count = 0
            for j in range(len(self.t_cards)):
                if self.t_cards[i][0] == self.t_cards[j][0]:
                    count += 1
            if count == 3:
                return True
        return False
        
        
        #### Find Trips ####
    def check_quads(self):

        for i in range(len(self.t_cards)):
            count = 0
            for j in range(len(self.t_cards)):
                if self.t_cards[i][0] == self.t_cards[j][0]:
                    count += 1
            if count == 4:
                return True
        return False

    def check_flush(self):

        for i in range(len(self.t_cards)):
            count = 0
            for j in range(len(self.t_cards)):
                if self.t_cards[i][1] == self.t_cards[j][1]:
                    count += 1
            if count == 5:
                return True
        return False
    
    def check_straight(self):
        card_hold = []
        for i in range(len(self.t_cards)):
            card_hold.append(float(self.t_cards[i][2]))
    
        card_hold = np.array(card_hold)
        card_hold = np.sort(card_hold)

    # Check if all differences are 1

        if np.all(np.diff(card_hold) == 1) == True:
            return True
        #### Wheel straight
        elif card_hold[0]==2.0 and card_hold[1] ==3.0 and card_hold[2] ==4.0 and card_hold[3]==5.0 and card_hold[4]==14.0:
            return True
        else: return False
    
    def check_straight_flush(self):

        flush = self.check_flush()
        straight = self.check_straight()

        if flush == True and straight == True:
            return True
        else: return False

    def check_full_house(self):
        pair =self.check_pair()
        trips = self.check_trips()

        if pair == True and trips == True:
            return True
        else: return False


class Hands:
    def __init__(self, players):
        self.players =players
        self.pair =None
        self.trips =None
        self.quads =None

    def hand_importance(self):
        self.rank = {'straight flush':1, 'four of a kind':2,'full house':3,'flush':4, 'three of a kind':5, 'two pair':6, 'pair':7, 'high card':8 }


    def check_hands(self):

        for idx, player in self.players.items():
            totalcards = player['totalcards']

            hand_defs = Hand_defs(totalcards)

            best_hand =[]
            pair=hand_defs.check_pair()

            two_pair = hand_defs.check_two_pair()
            trips = hand_defs.check_trips()
            quads = hand_defs.check_quads()
            flush = hand_defs.check_flush()
            straight = hand_defs.check_straight()
            straight_flush = hand_defs.check_straight_flush()
            full_house =hand_defs.check_full_house()

            player['pair'] = pair
            #player['pair_order'] = pair_order
            player['two_pair'] = two_pair
            player['trips'] = trips
            player['quads'] = quads
            player['flush'] = flush
            player['straight'] = straight
            player['straight_flush'] = straight_flush
            player['full_house'] = full_house


            if player['pair'] == True:
                best_hand.append(8)
            elif player['two_pair'] == True:
                best_hand.append(7)
            elif player['trips'] == True:
                best_hand.append(6)
            elif player['straight'] == True:
                best_hand.append(5)
            elif player['flush'] ==True:
                best_hand.append(4)
            elif player['full_house'] ==True:
                best_hand.append(3)
            elif player['quads'] == True:
                best_hand.append(2)
            elif player['straight_flush'] ==True:
                best_hand.append(1)
            else: best_hand.append(9)



            best_hand = min(best_hand)

            player['best_hand'] = best_hand
            
            #player['pairs'] = pairs


        #stmnt = f"pair:{self.pair}, twopair:{self.two_pair}, trip:{self.trips},quads:{self.quads},flush:{self.flush}, straight:{self.straight}, straight flush: {self.straight_flush}, fullhouse: {self.full_house}"

        return self.players


        
        
        

    def hand_importance(self):
        self.rank = {'straight_flush':1, 'quads':2,'full_house':3,'flush':4, 'trips':5, 'two_pair':6, 'pair':7, 'high_card':8 }


class GameSequence:
    def __init__(self, cards, players, hand_number ):
        self.community_cards = cards
        self.flop = []
        self.turn = None
        self.river = None
        self.players = players
        self.pot = None
        self.game_tracker = {}
        self.hand_number = hand_number


    def hand_counter(self):
        
        self.game_tracker['hand_number'] = self.hand_number
        
        self.game_tracker
    
    
    def betting_order(self):
        
        self.betting_order =[]

        for idx, player in self.players.items():
            self.betting_order.append(idx)
        random.shuffle(self.betting_order)

        self.game_tracker['betting_order'] = self.betting_order
        self.game_tracker


    def show_flop(self):
        self.flop.append(self.community_cards[:2])
        
        self.game_tracker['flop'] = self.flop
    
    def show_turn(self):
        self.turn = self.community_cards[3]
        
        self.game_tracker['turn'] = self.turn
    
    def show_river(self):
        self.river = self.community_cards[4]

        self.game_tracker['river'] = self.river
    
    def create_hand(self):
        self.hand_counter()
        self.betting_order()
        self.show_flop()
        self.show_turn()
        self.show_river()

        hands = Hands(self.players)
        hands.check_hands()
        self.game_tracker['players'] = self.players
        
        
        
        return self.game_tracker


    
    
            














if __name__ in "__main__":
    
    
    deck = {1:['2','diamond',2.0],2:['3','diamond',3.0],3:['4','diamond',4.0],4:['5','diamond',5.0],5:['6','diamond',6.0],6:['7','diamond',7.0],7:['8','diamond',8.0],8:['9','diamond',9.0],9:['10','diamond',10.0], 10:['J','diamond',11.0],11:['Q','diamond',12.0],12:['K','diamond',13.0],13:['A','diamond',14.0],
            14:['2','spade',2.0],15:['3','spade',3.0],16:['4','spade',4.0],17:['5','spade',5.0],18:['6','spade',6.0],19:['7','spade',7.0],20:['8','spade',8.0],21:['9','spade',9.0],22:['10','spade',10.0], 23:['J','spade',11.0],24:['Q','spade',12.0],25:['K','spade',13.0], 26:['A','spade',14.0],
            27:['2','club',2.0],28:['3','club',3.0],29:['4','club',4.0],30:['5','club',5.0],31:['6','club',6.0],32:['7','club',7.0],33:['8','club',8.0],34:['9','club',9.0],35:['10','club',10.0], 36:['J','club',11.0],37:['Q','club',12.0], 38:['K','club',13.0], 39:['A','club',14.0],
            40:['2','heart',2.0],41:['3','heart',3.0],42:['4','heart',4.0],43:['5','heart',5.0],44:['6','heart',6.0],45:['7','heart',7.0],46:['8','heart',8.0],47:['9','heart',9.0],48:['10','heart',10.0], 49:['J','heart',11.0],50:['Q','heart',12.0], 51:['K','heart',13.0], 52:['A','heart',14.0]}
    
    '''
    player = Player(8, 0)
    r =player.player_number()
    #print(r)
    
    
    
    r1 = Deck(deck, r)
    players, community_cards =r1.draw()
    #print(players)
    
    
    d =Hands(players)
    p_dict =d.check_hands()

    game =GameSequence(community_cards, p_dict, 0)

    g = game.create_hand()
    print(g)
    '''
    total =[]
    for i in range(20000):
        player = Player(9, 0)
        r =player.player_number()
    
    
    
    
        r1 = Deck(deck, r)
        players, community_cards =r1.draw()
    
    
    
        d =Hands(players)
        p_dict =d.check_hands()

        game =GameSequence(community_cards, p_dict, i)
        g = game.create_hand()
        
        print(g)
        total.append(g)

    df = pd.DataFrame(total)

    df.to_csv('totalhands.csv', index=False)    




   
   # print('community cards:',community_cards)




    
    
    

######## TABLE ########


######## PLAYER #######



