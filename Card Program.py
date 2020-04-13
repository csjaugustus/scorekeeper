class Player():
    """Class to store each player's attributes, and game functions."""
    def __init__(self, name, score=0):
        self.name = name.title()
        self.score = score
    
    def update_score(self, increment):
        self.score += increment
    
    def show_score(self):
        print(self.name + ": " + str(round(self.score, 2)))
    
    def calc_payment(self, bombs):
        self.payment_amount = 0.1 * self.cards_left * 2**float(bombs)
    
    def pay_instruction(self, winner):
        print(self.name + " should pay " + winner.title() + " " + str(round(self.payment_amount, 2)))

def enter_player_names():
    """Prompt user to enter player names.
    Create instance for each name, and compile names to list of players."""
    print("Enter your player names one by one.\nEnter 'q' to finish.\n")
    while True:
        name_input = input()
        if name_input == "q":
            break
        player = name_input
        players.append(player)
    print("\nPlayers:")
    for player in players:
        print("- " + player.title())
        player_instances[player] = Player(player.title())

def menu_after_game():
    """After each round, provide user with the option to continue,
    or update score manually in case they entered wrongly."""
    while True:
        action = input("'c' = Continue.\n'm' - Manually update score.\n")
        print("\n")
        
        if action == "c":
            break
        elif action == "m":
            print("Enter scores:\n")
            for player in players:
                updated_score = float(input(player.title() + "'s updated score: "))
                player_instances[player] = Player(player.title(), updated_score)
            print("\nUpdated scores:")
            for player in players:
                print(player.title() + ": " + str(round(player_instances[player].score, 2)))
            print("\n----------\n")
            break
        else:
            continue    

def save_game():
    saved_data = {}
    for player in players:
        saved_data[player] = player_instances[player].score
    with open("saved_data.json", "w") as f:
        json.dump(saved_data, f)

    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    winner_amount = 0
    for loser in losers:
        winner_amount += player_instances[loser].payment_amount
    with open("game_logs.txt", "a") as f:
        f.write(dt_string)
        f.write("\n\nBombs: " + str(bombs) + "\n")
        for loser in losers:
            f.write(loser.title() + "'s cards left: " + str(round(player_instances[loser].cards_left)) + "\n")
        f.write("\nWin/loss for current round:\n")
        for loser in losers:
            f.write(loser.title() + ": -" + str(round(player_instances[loser].payment_amount, 2)) + "\n")
        f.write(winner.title() + ": +" + str(round(winner_amount, 2)))
        f.write("\n\nScoreboard:\n")
        for player in players:
            f.write(player.title() + ": " + str(round(player_instances[player].score, 2)) + "\n")
        f.write("----------\n")
        
def retrieve_saved_data():
    """Retrieve saved data from previous session if available，
    then ask to resume or start new game.
    Otherwise, start new game automatically."""
    try:
        with open("saved_data.json") as f:
            loaded_data = json.load(f)
    except FileNotFoundError:
        with open("saved_data.json", "w") as f:
            json.dump(empty_dict, f)
        loaded_data = {}

    if loaded_data:
        print("Found saved data from previous session.\nScoreboard:")
        for player, score in loaded_data.items():
            print(player.title() + ": " + str(round(score, 2)))
        print("\n----------\n")
        
        while True:
            choice = input("'r' - Resume game with saved data.\n'n' - Wipe data, start new game.\n")
            print("\n----------\n")
            
            if choice == "r":
                for player, score in loaded_data.items():
                    players.append(player)
                    player_instances[player] = Player(player.title(), score)
                print("Data loaded. Resuming game.")
                break
                
            elif choice == "n":
                with open("saved_data.json", "w") as f:
                    json.dump(empty_dict, f)
                with open("game_logs.txt", "a") as f:
                    f.write("NEW GAME")
                    f.write("\n----------\n")
                print("Data wiped. Starting new game.\n")
                enter_player_names()
                break
            
            else:
                continue

    else:
        print("No saved data found. Starting new game.\n")
        enter_player_names()
    print("\n----------\n")
        
#creating empty lists and dicts
player_instances = {}
players = []
empty_dict = {}

#Checking for saved data
import json
retrieve_saved_data()

#Main Program
while True:
    #acquire info from user input
    winner = input("Who won? ")
    
    if winner not in players:
        print("The name you entered is not a player.\n")
        continue
        
    losers = players[:]
    losers.remove(winner)
    bombs = input("How many bombs? ")
    
    if bombs.isdigit() == False:
        print("You entered a non-number.\n")
        continue

    stopper = False
    for loser in losers:
        answer = input("How many cards does " + loser.title() + " have left? ")
        if answer.isdigit():
            player_instances[loser].cards_left = float(answer)
        else:
            print("You entered a non-number.\n")
            stopper = True
            break
    if stopper == True:
        continue
    print("\n")

    #calculating, displaying payment instructions
    for loser in losers:
        player_instances[loser].calc_payment(bombs)
        player_instances[loser].pay_instruction(winner)
    print("\n")
    
    #updating scores
    for loser in losers:
        player_instances[loser].update_score(-player_instances[loser].payment_amount)
        player_instances[winner].update_score(player_instances[loser].payment_amount)
    
    #printing scoreboard
    print("Scoreboard:")
    for player in players:
        player_instances[player].show_score()
    print("\n----------\n")
    
    save_game()
    menu_after_game()
