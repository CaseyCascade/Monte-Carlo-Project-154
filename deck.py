from enum import Enum
import random 

class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6 
    SEVEN = 7 
    EIGHT = 8
    NINE = 9 
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

class Suit(Enum):
    HEART = 1
    DIAMOND = 2
    CLUB = 3
    SPADE = 4

class Card:
    def __init__(self, rank:Rank, suit:Suit):
        self.rank = rank
        self.suit = suit

    def print(self):
        print(self.rank.name + " of " + self.suit.name)

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        if isinstance(other, Rank):
            return self.rank == other
        if isinstance(other, Suit):
            return self.suit == other
        return False

class Deck: 
    def __init__(self):
        self.deck = self.create_standard_deck()

    def create_standard_deck(self)->list[Card]:
        result_deck:list[Card] = []
        for i in range(1,5):
            for j in range(1,14):
                result_deck.append(Card(Rank(j), Suit(i)))
        return result_deck

    def add_card(self, card:Card):
        self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def get_size(self):
        return len(self.deck)
    
    def get_probability(self, parameter)->float: # parameter can be a Card, Suit, or Rank
        card_count = self.deck.count(parameter)
        return float(card_count) / float(len(self.deck))

    def draw_card(self, with_replacement=False):
        drawn_card = self.deck[0]
        if not with_replacement:
            self.deck.pop(0)
        return drawn_card

    def print(self):
        for card in self.deck: 
            card.print()

class Hand: 
    def __init__(self):
        self.hand: list[Card] = []

    def add_card(self, card:Card):
        self.hand.append(card)

    def get_aces_count(self):
        return self.hand.count(Rank.ACE)
    
    def get_non_aces_score(self):
        score:int = 0
        for card in self.hand:
            if card == Rank.ACE:
                continue 
            if card.rank.value >= 10: score += 10
            else: score += card.rank.value
        return score
    
    def calculate_blackjack_score(self):
        score:int = self.get_non_aces_score()
        ace_count = self.get_aces_count()
        for i in range(ace_count):
            if score + 11 <= 21:
                score += 11
            else:
                score += 1
        return score
    
    def is_hard(self):
        if not self.get_aces_count(): return True 
        if self.get_non_aces_score() + 11 > 21: return True 
        return False 
    
    ### MONTE CARLO POLICIES (True is Hit, False is stick) ###
    def policy_1(self)->bool: # Stick if Score >= 17
        if self.calculate_blackjack_score() >= 17: return False
        else: return True

    def policy_2(self)->bool: # Stick if Score >= 17 and Hand is Hard, or if score is 21
        if (self.calculate_blackjack_score() >= 17 and self.is_hard()) or self.calculate_blackjack_score == 21:
            return False
        else: return True

    def policy_3(self)->bool: # Always Stick 
        return False
    
    def policy_4(self)->bool: # Custom Policy #1
        pass
    def policy_5(self)->bool: # Custom Policy # 2
        pass


def main():
    new_deck = Deck()
    new_deck.shuffle()

    new_hand = Hand()
    new_hand.add_card(Card(Rank.KING, Suit.HEART))
    new_hand.add_card(Card(Rank.ACE, Suit.HEART))
    new_hand.add_card(Card(Rank.SEVEN, Suit.HEART))

    print(new_hand.calculate_blackjack_score())
    

if __name__ == "__main__":
    main()