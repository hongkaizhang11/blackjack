"""
Blackjack Card Game

Game Rules:
https://bicyclecards.com/how-to-play/blackjack/

"""
import random
import logging

class Card:
    """
    Base class for blackjack card game

    it has two attributes, face and suit, and a getValue() function which return the face value of the card.
    where A=1, 2=2, ..., J=11, Q=12, K=13
    """
    def __init__(self, face, suit):
        """
        Sample code for create Card instance:

        card = Card("A", "DIAMONDS")

        here is all SUITS "SPADES, DIAMONDS, CLUBS, HEARTS".
        """
        self.face = face
        self.suit = suit

    def __repr__(self): # this dunder function return a string to represent this object(card).
        """
        return a string to represent the card, for intance, (A, HEARTS).
        """
        return f"({self.face}, {self.suit})"

    def getValue(self): # Test Driving Development
        """
        use dictionary to get value of A, J, Q, K
        """
        if self.face.isdigit():
            return int(self.face)
        pictured = {"A":1, "J":11, "Q":12, "K":13}
        return pictured[self.face]

class BlackjackCard(Card):
    def getValue(self): # override getValue() from superclass
        if self.face.isdigit():
            return int(self.face)
        pictured = {"A":11, "J":10, "Q":10, "K":10}
        return pictured[self.face]

class Deck:
    FACES = ('A','2','3','4','5','6','7','8','9','10','J','Q','K') # class level attribute
    SUITS = ('SPADES','CLUBS','DIAMONDS','HEARTS')
    def __init__(self):
        self.stackOfCards = [BlackjackCard(face, suit) for face in Deck.FACES for suit in Deck.SUITS]
        self.currentIndex = 51

    def shuffle(self):
        random.shuffle(self.stackOfCards)

    def nextCard(self):
        card = self.stackOfCards[self.currentIndex]
        self.currentIndex -= 1
        if self.currentIndex==0:
            self.shuffle()
            self.currentIndex = 51
        return card

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.winCount = 0

    def win(self):
        self.winCount += 1

    def __repr__(self):
        return self.name

    def addCardToHand(self, card):
        self.hand.append(card)
    
    def cleanHand(self):
        self.hand.clear()

    def getHandSize(self):
        return len(self.hand)

    def showHand(self):
        return f"{self.name}: {self.hand}:{self.getHandValue()}:{self.winCount}"

    def getHandValue(self):
        value = 0
        for card in self.hand: #A,Q,A,Q = 42
            value += card.getValue()
        count = self.countAce()
        while value > 21 and count>0: # A=11,
            value -= 10 # change A=1
            count -= 1
        return value # 22

    def countAce(self):
        count = 0
        for card in self.hand:
            if card.face == 'A':
                count += 1
        return count # return number of Ace in hand

    def hit(self):
        value = self.getHandValue()
        if value >= 20:
            return False
        moreCard = input(self.name + ", do you want another card? (y/n) ")
        if moreCard=='y':
            return True
        return False

class Dealer(Player):
    def __init__(self):
        self.name = "Dealer"
        self.hand = []
        self.deck = Deck()
        self.winCount = 0

    def hit(self):
        value = self.getHandValue()
        if value < 17:
            return True
        return False

    def shuffle(self):
        self.deck.shuffle()

    def deal(self):
        return self.deck.nextCard()

    def showHand(self, faceUp):
        if not faceUp:
            return f"{self.name}: [{self.hand[0]}, HIDDEN]"
        return super().showHand()

class Game:
    LOG_FORMAT = "%(asctime)s %(levelname)8s - %(message)s"
    logging.basicConfig(filename=r"C:/Users/Hongkai Z/workspace/mypython1/hongkai.log", level=logging.DEBUG, format=LOG_FORMAT)

    logger = logging.getLogger("Huaxia")
    def __init__(self, playerList):
        self.logger.debug("__init__()...")
        self.playerList = playerList
        self.dealer = Dealer()
        self.dealer.shuffle()

    def dealCards(self):
        self.logger.debug("dealCards()...")
        for player in self.playerList: # first round for all player
            player.addCardToHand(self.dealer.deal())
            self.logger.info(f"{player.name}")
        self.dealer.addCardToHand(self.dealer.deal())
        self.logger.info(f"{self.dealer.name}")
        for player in self.playerList: # first round for all player
            player.addCardToHand(self.dealer.deal())
            self.logger.info(f"{player.name}")
            print(player.showHand())
        self.dealer.addCardToHand(self.dealer.deal())
        self.logger.info(f"{self.dealer.name}")
        print(self.dealer.showHand(False))

    def showResult(self):
        self.logger.debug("showResult()...")
        for player in self.playerList:
            print(player.msg)
            print(player.showHand())
            self.logger.info(f"{player.showHand()}")
        print(self.dealer.showHand(True))
        self.logger.info(f"{self.dealer.showHand(False)}")

    def cleanHands(self):
        for player in self.playerList:
            player.cleanHand()
        self.dealer.cleanHand()

    def hit(self):
        self.logger.debug("hit()...")
        for player in self.playerList:
            while player.hit():
                player.addCardToHand(self.dealer.deal())
                print(player.showHand())
                self.logger.info(f"{player.showHand()}")
        while self.dealer.hit():
            self.dealer.addCardToHand(self.dealer.deal())
            self.logger.info(f"{self.dealer.showHand(True)}")

    def play(self, winner): # pass function for flexibility
        """
        After game initialization, this function will be called.
        where winner is a function passed to this function used to determine who is winner
        
        this is good design, so that we can pass different function to determine who is winner.
        ---------------------------------------------------------------------------------------
        winner(dealer, player)
        winner should include two argument (dealer, player)
        """
        while True:
            self.dealCards()
            self.hit()
            for player in self.playerList:
                winner(self.dealer, player)
            self.showResult()
            moreGame = input("Would do like to play another game? (y/n) ")
            if moreGame == "n":
                break
            self.cleanHands()
        print("Game over!")

# if without else: each function takes single responsibility
def winner(dealer, player):
    """
    this function takes two positional arguments, dealer and player.
    It will increase winner count on dealer or player if he wins.
    It will also setup a message of the reason in player.msg.

    it uses if-without-else tech to get rid of elif and else code block by function
    """
    dealer.total = dealer.getHandValue() # dynamically create an attribute in dealer
    player.total = player.getHandValue() # add attribute total to player
    if player.total > 21:
        player.msg = f"Dealer win, {player.name} busted!"
        return dealer.win()
    return dealBusted(dealer, player)

def dealBusted(dealer, player):
    if dealer.total > 21:
        player.msg = f"{player.name} win, dealer busted!"
        return player.win()
    return tiedUp(dealer, player)

def tiedUp(dealer, player):
    if dealer.total == player.total:
        player.msg = f"Tied up, both {player.name} and Dealer lose."
        return
    return playerLarge(dealer, player)

def playerLarge(dealer, player):
    if player.total > dealer.total:
        player.msg = f"{player.name} wins, {player.name} has a larger hand."
        return player.win()
    player.msg = "Dealer wins, dealer has a larger hand."
    return dealer.win()

def determineWinner(dealer, player):
    """
    this function takes two positional arguments, dealer and player.
    It will increase winner count on dealer or player if he wins.
    It will also setup an empty message in player.msg.
    """
    dealerTotal = dealer.getHandValue()
    playerTotal = player.getHandValue()
    if playerTotal > 21:
        dealer.win()
    elif dealerTotal > 21:
        player.win()
    elif playerTotal == dealerTotal:
        pass
    elif playerTotal > dealerTotal:
        player.win()
    else:
        dealer.win()

def buildPlayerList():
    playerList = []
    while True:
        morePlayer = input("more player? (y/n) ")
        if morePlayer == 'n':
            break
        player = Player(getName(playerList))
        playerList.append(player)
    return playerList

def getName(playerList):
    while True:
        name = input("enter a name: ")
        if contains(name, playerList):
            print(f"the name '{name}' is already taken.")
        else: break
    return name

def contains(name, playerList):
    for player in playerList:
        if name == player.name:
            return True
    return False

if __name__ == '__main__':
    game = Game(buildPlayerList())
    game.play(winner) # pass check function to play() function
