import random
import time

face_values = ["T", "J", "Q", "K"]
player_cards = []
player_value = 0
dealer_cards = []
dealer_value = 0
deck = []

for rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']:
    for suit in "♠♥♦♣":
        card = (rank, suit)
        deck.append(card) 

deck = deck*4

def deal_card():
    return deck.pop()

def value_from_rank(rank: str) -> int:
    if rank == "A":
        return 11
    if rank in face_values:
        return 10
    return int(rank)

def card_value(person: list) -> int:
    total = 0
    aces = 0
    if person == player_cards:
        for rank, _ in person:
            if rank == "A":
                aces += 1

            total += value_from_rank(rank)
            
            if total > 21 and aces > 0:
                total -= 10
                aces -= 1
        return total
    
    elif person == dealer_cards:
        for rank, _ in person:
            total += value_from_rank(rank)
        return total
        
    else:
        rank = dealer_cards[1][0]
        return value_from_rank(rank)

def display_cards(situation: str) -> str:
    print(f"\nYour cards: {card_value(player_cards)} {player_cards}")
    if situation == "finish":
        print(f"My Cards:   {card_value(dealer_cards)}  {dealer_cards}\n")
    else:
        print(f"My visible card: {card_value("hidden")} [{dealer_cards[1]}]\n")

def start_of_game():
    player_cards.clear()
    player_value = 0
    dealer_cards.clear()
    dealer_value = 0
    random.shuffle(deck)

    for _ in range(2):
        player_cards.append(deal_card())
        dealer_cards.append(deal_card())

    player_value = card_value(player_cards)
    dealer_value = card_value(dealer_cards)

    print("I have dealt both of us two cards.")
    display_cards(0)

    while player_value < 21 and dealer_value < 21:
        choice = input("Would you like to (hit) or (stand): ")
        if choice == "hit":
            player_cards.append(deal_card())
            player_value = card_value(player_cards)
            display_cards(0)
        if choice == "stand":
            display_cards("finish")
            break
        
    if player_value > 21:
        print("Bust. You Lose!")
        time.sleep(5)
        return

    while dealer_value <= 16:
        time.sleep(3)
        dealer_cards.append(deal_card())
        dealer_value = card_value(dealer_cards)
        display_cards("finish")

    if dealer_value > 21:
        print("Dealer Bust. You Win!")
    elif dealer_value == player_value:
        print("Push")
    elif dealer_value == 21:
        display_cards("finish")
        print("Dealer has blackjack. You Lose!")
    elif dealer_value > player_value:
        print("You Lose!")
    else:
        print("You Win!")

    time.sleep(5)
    return

while True:
    start_of_game()