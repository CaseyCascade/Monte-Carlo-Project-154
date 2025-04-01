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

def create_standard_deck()->list[Card]:
    result_deck:list[Card] = []
    for i in range(1,5):
        for j in range(1,14):
            result_deck.append(Card(Rank(j), Suit(i)))
    return result_deck

class Deck: 
    def __init__(self, cards:list[Card]):
        self.deck = cards

    def add_card(self, card:Card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def get_size(self):
        return len(self.deck)

    def draw_card(self):
        random_index = random.randint(0, (len(self.deck) - 1))
        #TODO

    def print(self):
        for card in self.deck: 
            card.print()

def main():
    new_deck = Deck(create_standard_deck())
    new_deck.shuffle()
    new_deck.print()
    print(new_deck.get_size())

if __name__ == "__main__":
    main()