import random
from colorama import init
init()
from colorama import Fore, Style


class Solitare:
    def __init__(self, deck):
        self.game = []
        self.deck = deck
        self.found = [0,0,0,0]
        self.max_length = 12
        self.suits = '♦♣♥♠' 

    def display_game(self):
        print('\n------------------ Solitare Game -------------------\n')

        for row in range(self.max_length):
            for col in self.game:
                if row < len(col):
                    # print(col[row])
                    if col[row].shown == True:
                        # print((col[row].name + col[row].suit).center(6), end = ' ')
                    
                        if col[row].suit == self.suits[0] or col[row].suit == self.suits[2]:
                            print(Fore.RED + (col[row].name + col[row].suit).center(6) + Style.RESET_ALL, end = ' ')

                        elif col[row].suit == self.suits[1] or col[row].suit == self.suits[3]:
                            print(Fore.BLACK + (col[row].name + col[row].suit).center(6) + Style.RESET_ALL, end = ' ')
                    
                    else:
                        print('🞩'.center(6), end = ' ')

                else:
                    print(' '.center(6), end = ' ')

            print('\n')

        print()

        for item in self.found:
            if item:
                # print((item.name + item.suit).center(6), end = ' ')

                if item.suit == self.suits[0] or item.suit == self.suits[2]:
                    print(Fore.RED + (item.name + item.suit).center(6) + Style.RESET_ALL, end = ' ')

                elif item.suit == self.suits[1] or item.suit == self.suits[3]:
                    print(Fore.BLACK + (item.name + item.suit).center(6) + Style.RESET_ALL, end = ' ')
            
            else:
                print('🞩'.center(6), end = ' ')

        print()
        print('\n------------------ Solitare Game -------------------\n\n')
  
    def show_prev(self, pos):
        if pos[0] - 1 >= 0:
            self.game[pos[1]][pos[0]-1].shown = True
  
    def check_found(self, card, pos):
        row, col = pos[0], pos[1]
        card = self.format_card(card)
        check_card = self.found[self.suits.find(card[-1])]

        if len(self.game[col]) - 1 == row:
            if check_card == 0:
                if card[0] == 'A':
                    self.found[self.suits.find(card[-1])] = self.game[col][row]
                    del self.game[col][row]
                    self.show_prev(pos)
                    self.display_game()
                    print('\n', card, 'moved to ', card[-1], ' pile!\n')
                    return True

            elif check_card.value + 1 == self.game[col][row].value:
                self.found[self.suits.find(card[-1])] = self.game[col][row]
                del self.game[col][row]
                self.show_prev(pos)
                self.display_game()
                print('\n', card, 'moved to ', card[-1], ' pile!\n')
                return True
            
            self.update_max()
            
        return False

    def check_card(self, pos, pos2):
        # check if the card matches or move to empty column
        if pos[1] == pos2[1]:
            return False
        
        if pos2[0] == -1 or (self.game[pos2[1]][pos2[0]].value - 1 == self.game[pos[1]][pos[0]].value and self.game[pos2[1]][pos2[0]].suit == self.game[pos[1]][pos[0]].suit):
            self.game[pos2[1]] += self.game[pos[1]][pos[0]:]
            self.update_max()
            card_name = self.game[pos[1]][pos[0]].name + self.game[pos[1]][pos[0]].suit
            del self.game[pos[1]][pos[0]:]
            self.show_prev(pos)

            self.display_game()
            if pos2[0] == -1:
                print('\n', card_name, ' moved to column ', pos2[1] + 1)
            else:
                print('\n', card_name, ' moved under ', self.game[pos2[1]][pos2[0]].name, self.game[pos2[1]][pos2[0]].suit,'\n')
            return True 
        
        return False

    def is_shown(self,card):
        # check if first card is shown in game 
        card = self.format_card(card)

        for col in range(7):
            for row in range(len(self.game[col])):
                if self.game[col][row].name + self.game[col][row].suit == card and self.game[col][row].shown == True:
                    return [row, col]
                
        print('\ninvalid card\n')
        print('please choose another card\n')
        return None

    def is_valid(self, card):
        # check if second card is shown and last card
        card = self.format_card(card)

        for col in range(7):
            if len(self.game[col]) != 0:
                row = len(self.game[col]) - 1
                if self.game[col][row].name + self.game[col][row].suit == card and self.game[col][row].shown == True:
                    return [row, col]

        print('\ninvalid move\n')
        print('choose another card or re-enter first card to re-select\n')
        return None

    def check_complete(self):
        # check if all cards are found
        # if self.found[0] != 0 and self.found[0].value == 13:
        #     if self.found[1] != 0 and self.found[1].value == 13:
        #         if self.found[2] != 0 and self.found[2].value == 13:
        #             if self.found[3] != 0 and self.found[3].value == 13:
        #                 print('\nyay!! you did it!!')
        #                 return True

        for col in self.game:
            if len(col) != 0 and col[0].shown == False:
                return False
    
        print('\nyay!! you did it!!')
        return True

    def create_game(self):
        game = [] # 2D array of 7 columns

        for i in range(2):
            random.shuffle(self.deck) # shuffle 2 times

        first_card = self.deck[0]
        first_card.shown = True
        self.deck = self.deck[1:]
        game.append([first_card])

        for x in range(6):
            col, self.deck = self.deck[:6], self.deck[6:]

            for card in col:
                card.shown = True

            game.append(col)

        for y in range(2,7):
            arr, self.deck = self.deck[:y-1], self.deck[y-1:]
            game[y] = arr + game[y]

        self.game = game

    def check_moves(self):
        card_dic = {}
        dic = {'2':'A','J':'10', 'Q':'J', 'K':'Q'}

        for col in range(7):
            row = len(self.game[col])-1 # empty = -1
            if row == -1:
                card_dic[col] = 'K'
            else:
                card = self.game[col][row]
                if card.name == 'A':
                    card_dic[col] = 'A'
                elif card.name in dic:
                    card_dic[col] = dic[card.name] + card.suit
                else:
                    card_dic[col] = str(card.value-1) + card.suit

            temp_names = self.get_names(col)
            # print(temp_names, ' ', card_dic[col])

            if card_dic[col] in temp_names:
                card_dic[col] = ''

        # print('values', card_dic.values())

        temp_last = self.get_last()
        for i in range(4):
            if self.found[i] != 0:
                if self.found[i].name in dic:
                    item = dic[self.found[i].name] + self.found[i].suit
                else:
                    item = str((self.found[i].value)+1) + self.found[i].suit
                
                # print('temp_last: ', temp_last,' item: ',item,'\n')
                if item in temp_last:
                    card_dic[i+7] = item
          

        for col in range(7):
            for row in range(len(self.game[col])):
                card = self.game[col][row]
                if card.shown == True and (card.name in card_dic.values() or card.name + card.suit in card_dic.values()):
                    # print('card: ', card.name, card.suit, '\navailable moves: ', card_dic.values(), '\n')
                    return True 

        return False
                
    def format_card(self, card):
        dic = {'D': self.suits[0], 'C': self.suits[1], 'H': self.suits[2], 'S': self.suits[3]}

        if card[0].isalpha():
            card = card[0].upper() + card[-1]

        if card[-1].upper() in dic.keys():
            card = card[0:-1] + dic[card[-1].upper()]

        return card

    def get_names(self,col):
        arr = []
        for item in self.game[col]:
            arr.append(item.name+item.suit)
        return arr

    def get_last(self):
        arr = []
        for col in self.game:
            row = len(col)-1
            if row >= 0:
                arr.append(col[row].name+col[row].suit)
        return arr

    def update_max(self):
        num = 0 
        for col in self.game:
            rows = len(col)
            if rows > num:
                num = rows

        self.max_length = num 


class Card:
    def __init__(self, name, value, suit):
        self.suit = suit # eg: ♦
        self.value = value # eg: 1
        self.name = name # eg: A
        self.shown = False


class Deck:
    def __init__(self):
        self.deck = []

    def create_deck(self):
        suits = '♦♣♥♠'
        card_deck = []

        for suit in suits:
            card_deck.append(Card('A',1,suit))
            card_deck.append(Card('J',11,suit))
            card_deck.append(Card('Q',12,suit))
            card_deck.append(Card('K',13,suit))

            for i in range(2,11):
                card_deck.append(Card(str(i),i,suit))

        self.deck = card_deck

    def display_deck(self):
        for card in self.deck:
            print(card.name+card.suit, end = ' ')


def solitare_rules():
    print('\n------------------ Game Rules -------------------\n')
    print('1. enter cards in this format: <num><suit> eg: "A♥" "AH" ')
    print('2. to end the game, enter "x"')
    print('3. to re-enter your choice, enter the first card again')
    print('4. to move a king card to an empty column, enter the column number [1-7] ')
    print() 


def start_solitare():
    solitare_rules()

    newdeck = Deck()
    newdeck.create_deck()
    # newdeck.display_deck()

    newgame = Solitare(newdeck.deck) 
    newgame.create_game()

    print()
    newgame.display_game()

    while True:
        pos = None
        check = False

        while pos == None:
            card = input('source card: ')

            if card == 'x':
                msg = input('enter "x" again to end the game: ')
                if msg == 'x':
                    check = True
                    break

            pos = newgame.is_shown(card)

        if check == True:
            break 

        is_found = newgame.check_found(card, pos)

        if not is_found:
            pos2 = None

            while pos2 == None:
                card2 = input('destination card: ')

                if card2 == 'x':
                    msg = input('enter "x" again to end the game: ')
                    if msg == 'x':
                        check = True
                        break
                        
                elif card2 == card:
                    pos2 = pos
                    print('\nplease re-enter!')
                    break

                elif card2.isdigit():
                    col = int(card2)-1
                    print('col: ', col,' length: ', len(newgame.game[col]))
                    if col >= 0 and col <= 6 and len(newgame.game[col]) == 0:
                        pos2 = [-1,col]
                        print('pos2: ', pos2)
                        break

                    else:
                        pos2 = pos
                        break

                
                pos2 = newgame.is_valid(card2)
                # break # test

            if check == True:
                break

            result = newgame.check_card(pos, pos2)

            # if not result:
                # # if true, card is moved, if false, dont match 
                # print('\ncards dont match! please choose another card!\n')

        if newgame.check_complete():
            break

        elif not newgame.check_moves():
            print('\nno moves left :<\n')
            break

    print('\ngame has ended!')

   
def menu():
    print('\n------------- Game Menu -------------\n')
    games = ['Solitare','Blackjack']

    for i in range(len(games)):
        print(i+1, ' - ', games[i])

    choice = input('\nWould you like to play Solitare? [y/n]  ')

    if choice == 'y':
        start_solitare()

    else:
        print('\no wells')

menu()

