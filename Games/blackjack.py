import random

class Card:

  def __init__(self, value, suit):
    self.value = value
    self.suit = suit
    self.name = "{} of {}".format(value, suit)

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
      print("{} has a face-up {}".format(player.name, card.name))
      if card.value == 'A':
        player.aces_in_hand += 1
      card = self.deck.draw_card()
      player.hand.append(card)
      print("{} has a face-up {}".format(player.name, card.name))
      if card.value == 'A':
        player.aces_in_hand += 1

  def player_turn(self):
    player = self.player_list[self.turn_counter]
    if not player.name == 'dealer':
      player.calc_hand_value()
      if player.hand_value == 21:
        print("{} got a BLACKJACK!".format(player.name))
        self.turn_counter += 1
        self.player_turn()
      elif player.hand_value < 21:
        print("{}, your hand total is {}".format(player.name, player.hand_value))
        choice = input("Would you like to hit or stay?: ")
        if choice.lower() == "hit":
          card = self.deck.draw_card()
          player.hand.append(card)
          print("{} drew the {}".format(player.name, card.name))
          if card.value == 'A':
            player.aces_in_hand += 1
          self.player_turn()
        else:
          self.turn_counter += 1
          self.player_turn()
      elif player.hand_value > 21:
        print("Cya {}, you busted".format(player.name))
        self.turn_counter += 1
        self.player_turn()
    else:
      player.calc_hand_value()
      if player.hand_value < 17:
        print("The dealer's hand total is {}. The dealer hits.".format(player.hand_value))
        card = self.deck.draw_card()
        player.hand.append(card)
        print("The dealer drew the {}".format(card.name))
        if card.value == 'A':
          player.aces_in_hand += 1
        self.player_turn()
      elif player.hand_value <= 21:
        self.dealer_score = player.hand_value
        print("The dealer's hand total is {}. The dealer stays.".format(player.hand_value))
        self.turn_counter = 0
      else:
        self.dealer_score = player.hand_value
        print("The dealer busts with a hand total of {}".format(player.hand_value))
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
            print("Atta boy {}, you beat the dealer".format(player.name))
            self.turn_counter += 1
            self.end_round()
          elif player.hand_value == self.dealer_score:
            print("Oof {}, you tied with the dealer, sorry bud.".format(player.name))
            self.turn_counter += 1
            self.end_round()
          else:
            print("Get rekt {}, you got cucked by the dealer".format(player.name))
            self.turn_counter += 1
            self.end_round()
        elif self.dealer_score == 21:
          print("gg {}, the dealer hit a blackjack".format(player.name))
          self.turn_counter += 1
          self.end_round()
        else:
          print("Good news {}, the dealer busted, you won!".format(player.name))
          self.turn_counter += 1
          self.end_round()
      elif player.hand_value == 21:
        print("Nice blackjack {}, too bad it's worth 3/5ths of a whitejack".format(player.name))
        self.turn_counter += 1
        self.end_round()
      elif player.hand_value > 21:
        if self.dealer_score > 21:
          print("Whelp {}, you busted but so did the dealer. Winner winner.".format(player.name))
          self.turn_counter += 1
          self.end_round()
        else:
          print("R.I.P {}, you lose".format(player.name))
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
        name = input("Enter name for Player {}: ".format(str(num)))
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