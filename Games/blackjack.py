import random

class Card:

  def __init__(self, value, suit):
    self.value = value
    self.suit = suit
    self.name = f"{value} of {suit}"

class Deck(Card):

  def __init__(self):
    values = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
    suits = ("Spades", "Clubs", "Diamonds", "Hearts")
    self.cards = []
    self.discards = []
    for value in values:
      for suit in suits:
        self.cards.append(Card(value, suit))

  def draw_card(self):
    card = random.choice(self.cards)
    self.cards.remove(card)
    self.discards.append(card)
    return card


class Player:

  def __init__(self, name):
    self.name = name
    self.hand = []
    self.hand_value = 0
    self.aces_in_hand = 0

  def calc_hand_value(self):
    card_weights = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}
    aces_high = [0, 11, 12, 13, 14]
    aces_low = [0, 1, 2, 3, 4]
    self.hand_value = 0
    for card in self.hand:
      if not card.value == 'A':
        self.hand_value += card_weights[card.value]
    self.hand_value += aces_high[self.aces_in_hand]
    if self.hand_value > 21:
      self.hand_value -= aces_high[self.aces_in_hand]
      self.hand_value += aces_low[self.aces_in_hand]


class Dealer(Player):

  def __init__(self, name):
    self.hand = []
    self.name = name
    self.hand_value = 0
    self.aces_in_hand = 0

class Game():
  
  def __init__(self, deck, player_list):
    self.turn_counter = 0
    self.deck = deck
    self.player_list = player_list
    self.dealer_score = 0

  def start_round(self):
    round_in_progress = True
    self.shuffle()
    self.turn_counter = 0
    self.dealer_score = 0
    for player in self.player_list:
      player.aces_in_hand = 0
      card = self.deck.draw_card()
      player.hand.append(card)
      print(f"{player.name} has a face-up {card.name}")
      if card.value == 'A':
        player.aces_in_hand += 1
      card = self.deck.draw_card()
      player.hand.append(card)
      print(f"{player.name} has a face-up {card.name}")
      if card.value == 'A':
        player.aces_in_hand += 1

  def player_turn(self):
    player = self.player_list[self.turn_counter]
    if not player.name == 'dealer':
      player.calc_hand_value()
      if player.hand_value == 21:
        print(f"{player.name} got a BLACKJACK!")
        self.turn_counter += 1
        self.player_turn()
      elif player.hand_value < 21:
        print(f"{player.name}, your hand total is {player.hand_value}")
        choice = input("Would you like to hit or stay?: ")
        if choice.lower() == "hit":
          card = self.deck.draw_card()
          player.hand.append(card)
          print(f"{player.name} drew the {card.name}")
          if card.value == 'A':
            player.aces_in_hand += 1
          self.player_turn()
        else:
          self.turn_counter += 1
          self.player_turn()
      elif player.hand_value > 21:
        print(f"Cya {player.name}, you busted")
        self.turn_counter += 1
        self.player_turn()
    else:
      player.calc_hand_value()
      if player.hand_value < 17:
        print(f"The dealer's hand total is {player.hand_value}. The dealer hits.")
        card = self.deck.draw_card()
        player.hand.append(card)
        print(f"The dealer drew the {card.name}")
        if card.value == 'A':
          player.aces_in_hand += 1
        self.player_turn()
      elif player.hand_value <= 21:
        self.dealer_score = player.hand_value
        print(f"The dealer's hand total is {player.hand_value}. The dealer stays.")
        self.turn_counter = 0
      else:
        self.dealer_score = player.hand_value
        print(f"The dealer busts with a hand total of {player.hand_value}")
        self.turn_counter = 0

  def end_round(self):
    i = 0
    player = self.player_list[self.turn_counter]
    while i < len(player.hand):
      card = player.hand[i]
      player.hand.remove(card)
    if not player.name == 'dealer':
      if player.hand_value < 21:
        if self.dealer_score < 21:
          if player.hand_value > self.dealer_score:
            print(f"Atta boy {player.name}, you beat the dealer")
            self.turn_counter += 1
            self.end_round()
          elif player.hand_value == self.dealer_score:
            print(f"Oof {player.name}, you tied with the dealer, sorry bud.")
            self.turn_counter += 1
            self.end_round()
          else:
            print(f"Get rekt {player.name}, you got cucked by the dealer")
            self.turn_counter += 1
            self.end_round()
        elif self.dealer_score == 21:
          print(f"gg {player.name}, the dealer hit a blackjack")
          self.turn_counter += 1
          self.end_round()
        else:
          print(f"Good news {player.name}, the dealer busted, you won!")
          self.turn_counter += 1
          self.end_round()
      elif player.hand_value == 21:
        print(f"{player.name} hit BLACKJACK")
        self.turn_counter += 1
        self.end_round()
      elif player.hand_value > 21:
        if self.dealer_score > 21:
          print(f"Whelp {player.name}, you busted but so did the dealer. Winner winner.")
          self.turn_counter += 1
          self.end_round()
        else:
          print(f"R.I.P {player.name}, you lose")
          self.turn_counter += 1
          self.end_round()
    round_in_progress = False

  def shuffle(self):
    i = 0
    while i < len(self.deck.discards):
      card = self.deck.discards[i]
      self.deck.cards.append(card)
      self.deck.discards.remove(card)


def main():
  game_in_progress = False
  while not game_in_progress:
    player_list = []
    new_game = input("Would you like to start a new game? (y/n): ")
    if new_game.lower() in ('y', 'yes'):
      game_in_progress = True
      for num in range(1, int(input("How many players are there?: "))+1):
        name = input(f"Enter name for Player {str(num)}: ")
        player_list.append(Player(name))
      player_list.append(Dealer('dealer'))
      deck = Deck()
      game = Game(deck, player_list)
      while game_in_progress:
        round_in_progress = False
        while not round_in_progress:
          new_round = input("Would you like to start a new round? (y/n): ")
          if new_round.lower() in ('y', 'yes'):
            game.start_round()
            game.player_turn()
            game.end_round()
          else:
            main()

if __name__ == '__main__':
  main()