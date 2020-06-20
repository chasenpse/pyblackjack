import random

playing = True

class Card():
    def __init__(self, suit, value, name):
        self.suit = suit
        self.value = value
        self.name = name

    def __str__(self):
        return self.name + ' of ' + self.suit

class Deck():
    def __init__(self):
        self.cards = []
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for i in range(1,14):
                if i == 1:
                    self.cards.append(Card(s,11,"Ace"))
                elif i == 11:
                    self.cards.append(Card(s,10,"Jack"))
                elif i == 12:
                    self.cards.append(Card(s,10,"Queen"))
                elif i == 13:
                    self.cards.append(Card(s,10,"King"))
                else:
                    self.cards.append(Card(s,i,str(i)))
    
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self):
        return self.cards.pop()

class Hand():
    def __init__(self):
        self.cards = []
        self.total = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.total += card.value
        
        if card.name == 'Ace':
            self.aces += 1

    def adjust_aces(self):
        while self.total > 21 and self.aces:
            self.total -= 10
            self.aces -= 1

class Chips():
    def __init__(self):
        self.total = 100
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def place_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Invalid input, please enter an integer.')
        else:
            if chips.bet > chips.total:
                print(f"Not enough chips, your bet can't exceed {chips.total}\n")
            else:
                break

def hit(hand, deck):
    hand.add_card(deck.deal())
    hand.adjust_aces()

def hit_or_stay(hand, deck):
    global playing
    while True:
        ans = input("[H] Hit or [S] Stay? ").lower()
        if ans[0] == 'h':
            hit(hand, deck)
        elif ans[0] == 's':
            print('Player stays. Dealer\'s turn...')
            playing = False
        else:
            print('Invalid chioce entered, please try again.')
            continue
        break

def show_partial(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nYour Hand:", *player.cards, sep='\n ')
    print("\nYour Total =",player.total,'\n')

def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Total =",dealer.total)
    print("\nYour Hand:", *player.cards, sep='\n ')
    print("\nYour Total =",player.total,'\n')

def player_busts(chips):
    print('You bust!')
    chips.lose_bet()

def player_wins(chips):
    print('You Win!')
    chips.win_bet()

def dealer_busts(chips):
    print('Dealer busts!')
    chips.win_bet()

def dealer_wins(chips):
    print('Dealer wins!')
    chips.lose_bet()

def push():
    print("It's a tie.")

def show_balance(chips):
    print(f'Current balance: {chips.total}\n')

chips = Chips()

while True:
    print('\n************************************************')
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!')
    print('Dealer hits until they reach 17. Aces count as 1 or 11.')
    print('************************************************\n')
    
    deck = Deck()
    deck.shuffle()
    
    player = Hand()
    dealer = Hand()

    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())

    show_balance(chips)
    place_bet(chips)

    show_partial(player,dealer)

    while playing:
        hit_or_stay(player,deck)
        show_partial(player,dealer)
        
        if player.total > 21:
            player_busts(chips)
            break
    if player.total <= 21:
        
        while dealer.total < 17:
            hit(dealer,deck)
            
        # Show all cards
        show_all(player,dealer)
        
        # Test different winning scenarios
        if dealer.total > 21:
            dealer_busts(chips)

        elif dealer.total > player.total:
            dealer_wins(chips)

        elif dealer.total < player.total:
            player_wins(chips)

        else:
            push()
    
    # Inform Player of their chips total    
    show_balance(chips)
    
    # Ask to play again
    if chips.total == 0:
        print("Oh dear, you're all out of chips...")
        print("Thanks for playing!")
        break
    else:
        new_game = input("[P] Play another hand or [Q] Quit\n")
        if new_game[0].lower()=='p':
            playing=True
            continue
        else:
            print("Thanks for playing!")
            break
