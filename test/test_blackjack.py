import unittest
from src.blackjack import *

class TestCard(unittest.TestCase):
    heartsA = Card("A", "HEARTS")
    diamonds4 = Card("4", "DIAMONDS")
    clubsQ = Card("Q", "CLUBS")
    black_heartsA = BlackjackCard("A", "HEARTS")
    black_diamonds4 = BlackjackCard("4", "DIAMONDS")
    black_clubsQ = BlackjackCard("Q", "CLUBS")
    black_spades2 = BlackjackCard("2", "SPADE")

    johnny = Player("Johnny")
    johnny.addCardToHand(black_heartsA)
    johnny.addCardToHand(black_clubsQ)
    dealer = Dealer() # create dealer instance

    def test_repr(self):
        self.assertEqual("Dealer", repr(self.dealer))


    def test_getCardValue(self):
        self.assertEqual(4, self.diamonds4.getValue())
        self.assertEqual(1, self.heartsA.getValue())
        self.assertEqual(12, self.clubsQ.getValue())

    def test_getBlackjackCardValue(self):
        self.assertEqual(4, self.black_diamonds4.getValue())
        self.assertEqual(11, self.black_heartsA.getValue())
        self.assertEqual(10, self.black_clubsQ.getValue())
    
    def test_numberOfCardsInDeck(self):
        deck = Deck()
        self.assertTrue(52, len(deck.stackOfCards))

    def test_firstCard(self):
        deck = Deck()
        self.assertEqual('(A, SPADES)', deck.stackOfCards[0].__repr__())

    def test_lastCard(self):
        deck = Deck()
        self.assertEqual('(K, HEARTS)', deck.stackOfCards[51].__repr__())
    
    def test_shuffle(self):
        deck = Deck()
        deck.shuffle()
        self.assertNotEqual('(A, SPADES)', deck.stackOfCards[0].__repr__())
        self.assertNotEqual('(K, HEARTS)', deck.stackOfCards[51].__repr__())

    def getJohnny(self):
        johnny = Player("Johnny")
        johnny.addCardToHand(self.black_heartsA)
        johnny.addCardToHand(self.black_clubsQ)
        return johnny

    def getRoy(self):
        roy = Player("Roy")
        roy.addCardToHand(self.black_heartsA)
        roy.addCardToHand(self.black_clubsQ)
        roy.addCardToHand(self.black_spades2)
        return roy

    def test_playerHand(self):
        johnny = self.getJohnny()
        card = johnny.hand[0]
        self.assertEqual(card, self.black_heartsA)
        card = johnny.hand[1]
        self.assertEqual(card, self.black_clubsQ)
    
    def test_cleanHand(self):
        self.johnny.cleanHand()
        self.assertEqual(0, self.johnny.getHandSize())
    
    def test_showHand(self):
        johnny = self.getJohnny()
        reality = johnny.showHand()
        expectations = "Johnny: [(A, HEARTS), (Q, CLUBS)]:21:0"
        self.assertEqual(expectations, reality)

    def test_getHandValue(self):
        johnny = self.getJohnny()
        reality = johnny.getHandValue()
        self.assertEqual(21, reality)

    def test_getHandValueWithAceBust(self):
        roy = self.getRoy()
        actual = roy.getHandValue()
        self.assertEqual(13, actual)

    def test_dealerHit(self):
        dealer = Dealer()
        dealer.addCardToHand(self.black_diamonds4)
        dealer.addCardToHand(self.black_diamonds4)
        self.assertEqual(True, dealer.hit())
        dealer.addCardToHand(self.black_clubsQ)
        self.assertEqual(False, dealer.hit())

    def test_showHand4Dealer(self):
        dealer = Dealer()
        dealer.addCardToHand(self.black_diamonds4)
        dealer.addCardToHand(self.black_clubsQ)
        actual = dealer.showHand(False)
        expected = "Dealer: [(4, DIAMONDS), HIDDEN]"
        self.assertEqual(expected, actual)
        actual = dealer.showHand(True)
        expected = "Dealer: [(4, DIAMONDS), (Q, CLUBS)]:14:0"
        self.assertEqual(expected, actual)

    def test_tooAce(self):
        johnny = Player("Johnny")
        johnny.addCardToHand(self.black_heartsA)
        johnny.addCardToHand(self.black_clubsQ)
        johnny.addCardToHand(self.black_heartsA)
        johnny.addCardToHand(self.black_clubsQ)
        expected = 22
        actual = johnny.getHandValue()
        self.assertEqual(expected, actual)

    def test_CountAce(self):
        johnny = Player("Johnny")
        johnny.addCardToHand(self.black_heartsA)
        johnny.addCardToHand(self.black_clubsQ)
        johnny.addCardToHand(self.black_heartsA)
        johnny.addCardToHand(self.black_clubsQ)
        expected = 2
        actual = johnny.countAce()
        self.assertEqual(expected, actual)

    def test_treeAce(self):
        johnny = Player("Johnny")
        johnny.addCardToHand(self.black_heartsA)
        johnny.addCardToHand(self.black_clubsQ)
        johnny.addCardToHand(self.black_heartsA)
        johnny.addCardToHand(self.black_heartsA)
        johnny.addCardToHand(self.black_diamonds4)
        expected = 17
        actual = johnny.getHandValue()
        self.assertEqual(expected, actual)

    def test_phorAce(self):
        johnny = Player("Johnny")
        johnny.addCardToHand(self.black_heartsA)
        johnny.addCardToHand(self.black_heartsA)
        johnny.addCardToHand(self.black_clubsQ)
        johnny.addCardToHand(self.black_heartsA)
        johnny.addCardToHand(self.black_heartsA)
        johnny.addCardToHand(self.black_diamonds4)
        expected = 18
        actual = johnny.getHandValue()
        self.assertEqual(expected, actual)