from random import randint
from os import path
from operator import itemgetter
from functions import input_num, input_str
from pickle import dump, load
dir_path = path.dirname(path.realpath(__file__))

#Made by badooga. Requires functions.py found at https://github.com/badooga/Python-Files

def save(mod_dict):
    with open(dir_path + "\\data.p", "wb") as f:
        dump(mod_dict, f)

try:
    print(dir_path + "\\data.p")
    with open(dir_path + "\\data.p", "rb") as f:
        modifiers = load(f)
except:
    print("Data file not found. Commencing setup.")
    num_players = input_num("How many players does your party have? ", int, 1)
    modifiers = {}
    for player in range(num_players):
        player_name = input_str("Player {} Name: ".format(player + 1), True).rstrip()
        player_mod = input_num("Player {} Initiative Modifier: ".format(player + 1), int)
        modifiers[player_name] = player_mod
    save(modifiers)

def entercombat(mod_dict):
    initiative = {}
    num_enemygroups = input_num("\nHow many non-player factions, enemy groups, or individual NPCs are present in combat? ", int, 0)
    if num_enemygroups != 0:
        for enemygroup in range(num_enemygroups):
            enemygroup_name = input_str("Faction/Enemy/NPC {} Name: ".format(enemygroup + 1), True).rstrip()
            enemygroup_mod = input_num("Faction/Enemy/NPC {} Initiative Modifier: ".format(enemygroup + 1), int)
            initiative[enemygroup_name] = randint(1,20) + enemygroup_mod
    
    for player in mod_dict.keys():
        initiative[player] = randint(1, 20) + mod_dict[player]
    
    tracker = sorted([(k,v) for k,v in initiative.items()], key=itemgetter(1), reverse=True)
    print("\nInitiative Order:")
    for pair in tracker:
        print("{}: {}".format(pair[0], pair[1]))
    

def editplayer(mod_dict):
    command = input_num("\nWould you like to edit a player's modifier (1) or a player's name (2)? (enter 0 to cancel): ", int)
    while True:
        if command == 0:
            break

        elif command == 1:
            while True:
                player_mod_edit = input_str("What player's modifier would you like to edit (enter 0 to cancel)? ", True).rstrip()
                if player_mod_edit == "0":
                    break
                elif player_mod_edit not in mod_dict.keys():
                    print("Invalid player. Please try again.")
                else:
                    player_mod_new = input_num("New Initiative Modifier: ", int)
                    mod_dict[player_mod_edit] = player_mod_new
                    break
            break
        
        elif command == 2:
            while True:
                player_name_edit = input_str("What player's name would you like to edit (enter 0 to cancel)? ", True).rstrip()
                if player_name_edit == "0":
                    break
                elif player_name_edit not in mod_dict.keys():
                    print("Invalid player. Please try again.")
                else:
                    while True:
                        player_name_new = input_str("New Player Name: ", True).rstrip()
                        if player_name_new in mod_dict.keys():
                            print("Name already taken. Please try again.")
                        else:
                            break
                    mod_dict[player_name_new] = mod_dict[player_name_edit]
                    del mod_dict[player_name_edit]
                    break
            break

        else:
            print("Invalid command. Please try again.")

def addordeleteplayer(mod_dict):
    command = input_num("\nWould you like to add a player or players (1), or would you like to delete a player (2) (enter 0 to cancel)? ", int)
    while True:
        if command == 0:
            break

        elif command == 1:
            num_players_add = input_num("How many players would you like to add (enter 0 to cancel)? ", int, 0)
            if num_players_add == 0:
                pass
            else:
                for player in range(num_players_add):
                    while True:
                        player_name_add = input_str("Player {} Name: ".format(player + 1), True).rstrip()
                        if player_name_add in mod_dict.keys():
                            print("Player already exists.")
                        elif player_name_add == "":
                            print("Invalid name. Please try again.")
                        else:
                            break
                    player_mod_add = input_num("Player {} Initiative Modifier: ".format(player + 1), int)
                    mod_dict[player_name_add] = player_mod_add
            break

        elif command == 2:
            while True:
                player_del = input_str("What player would you like to delete (enter 0 to cancel)? ", True)
                if player_del == "0":
                    break
                elif player_del not in mod_dict.keys():
                    print("Invalid player. Please try again.")
                else:    
                    confirmation = input_num("Are you sure you want to delete {}? Press 1 to confirm, 0 to cancel. ".format(player_del), int, 0, 1)
                    if confirmation == 1:
                        del mod_dict[player_del]
                    break
            break

        else:
            print("Invalid command. Please try again.")

while True:
    command = input_num("\nCommands: Quit (1), Print Player Modifiers (2), Edit Player (3), Add or Delete Players (4), Enter Combat (5) \nCommand: ", int)
    if command == 1:
        break
    elif command == 2:
        print(modifiers)
    elif command == 3:
        editplayer(modifiers)
        save(modifiers)
    elif command == 4:
        addordeleteplayer(modifiers)
        save(modifiers)
    elif command == 5:
        entercombat(modifiers)
    else:
        print("Invalid command. Please try again.")