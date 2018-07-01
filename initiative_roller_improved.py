from random import randint
from os import path
from operator import itemgetter
from functions import input_num, input_str
dir_path = path.dirname(path.realpath(__file__))

#Made by badooga. Requires functions.py found at https://github.com/badooga/Python-Files

try:
    with open(dir_path + "\\initiative.txt", "r") as f:
        raw_tracker = f.readlines()
except:
    with open(dir_path + "\\initiative.txt", "w") as f:
        print("Tracker file not found. Commencing setup.")
        num_players = input_num("How many players does your party have? ", int, 1)
        for player in range(num_players):
            player_name = input_str("Player {} Name: ".format(player + 1), True).rstrip()
            player_mod = input_num("Player {} Initiative Modifier: ".format(player + 1), int)
            f.write("{}: {}\n".format(player_name, player_mod))
    with open(dir_path + "\\initiative.txt", "r") as f:
        raw_tracker = f.readlines()

tracker = []
initiative = {}
modifiers = {}

def initialize():
    global raw_tracker
    global tracker
    global modifiers

    raw_tracker = []
    tracker = []
    initiative = {}
    modifiers = {}

    with open(dir_path + "\\initiative.txt", "r") as f:
        for line in f:
            raw_tracker.append(line.rstrip("\n"))

    for pair in raw_tracker:
        raw_pair = pair.rsplit(": ")
        if raw_pair != [""]:
            modifiers[raw_pair[0]] = int(raw_pair[1])
            initiative[raw_pair[0]] = randint(1,20) + int(raw_pair[1])

def entercombat():
    global tracker
    global raw_tracker
    global initiative
    num_enemygroups = input_num("\nHow many non-player factions, enemy groups, or individual NPCs are present in combat? ", int, 0)
    if num_enemygroups != 0:
        for enemygroup in range(num_enemygroups):
            enemygroup_name = input_str("Faction/Enemy/NPC {} Name: ".format(enemygroup + 1), True).rstrip()
            enemygroup_mod = input_num("Faction/Enemy/NPC {} Initiative Modifier: ".format(enemygroup + 1), int)
            initiative[enemygroup_name] = randint(1,20) + enemygroup_mod
    
    for player in modifiers.keys():
        initiative[player] = randint(1, 20) + modifiers[player]

    tracker = sorted([(k,v) for k,v in initiative.items()], key=itemgetter(1), reverse=True)
    print("\nInitiative Order:")
    for pair in tracker:
        print("{}: {}".format(pair[0], pair[1]))
    
    initiative = {}
    for pair in raw_tracker:
        raw_pair = pair.rsplit(": ")
        initiative[raw_pair[0]] = randint(1,20) + int(raw_pair[1])

def editplayer():
    command = input_num("\nWould you like to edit a player's modifier (1) or a player's name (2)? (enter 0 to cancel): ", int)
    while True:
        if command == 0:
            break

        elif command == 1:
            while True:
                player_mod_edit = input_str("What player's modifier would you like to edit (enter 0 to cancel)? ", True).rstrip()
                if player_mod_edit == "0":
                    break
                try:
                    index = raw_tracker.index("{}: {}".format(player_mod_edit, modifiers[player_mod_edit]))
                    player_mod_new = input_num("New Initiative Modifier: ", int)
                    raw_tracker[index] = "{}: {}".format(player_mod_edit, player_mod_new)
                    break
                except:
                    print("Invalid player. Please try again.")

            with open(dir_path + "\\initiative.txt", "w") as f:
                for line in raw_tracker:
                    f.write(line.rstrip("\n") + "\n")
            break
        
        elif command == 2:
            while True:
                player_name_edit = input_str("What player's name would you like to edit (enter 0 to cancel)? ", True).rstrip()
                if player_name_edit == "0":
                    break
                try:
                    preserved_modifier = modifiers[player_name_edit]
                    index = raw_tracker.index("{}: {}".format(player_name_edit, preserved_modifier))
                    player_name_new = input_str("New Player Name: ", True).rstrip()
                    raw_tracker[index] = "{}: {}".format(player_name_new, preserved_modifier)
                    break
                except:
                    print("Invalid player. Please try again.")

            with open(dir_path + "\\initiative.txt", "w") as f:
                for line in raw_tracker:
                    f.write(line.rstrip("\n") + "\n")
            break

        else:
            print("Invalid command. Please try again.")

def addordeleteplayer():
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
                        if player_name_add in modifiers.keys():
                            print("Player already exists.")
                        elif player_name_add == "":
                            print("Invalid name. Please try again.")
                        else:
                            break
                    player_mod_add = input_num("Player {} Initiative Modifier: ".format(player + 1), int)
                    raw_tracker.append("{}: {}".format(player_name_add, player_mod_add))
                with open(dir_path + "\\initiative.txt", "w") as f:
                    for line in raw_tracker:
                        f.write(line.rstrip("\n") + "\n")
            break

        elif command == 2:
            while True:
                player_del = input_str("What player would you like to delete (enter 0 to cancel)? ", True)
                if player_del == "0":
                    break
                elif player_del not in modifiers.keys():
                    print("Invalid player. Please try again.")
                else:    
                    confirmation = input_num("Are you sure you want to delete {}? Press 1 for yes, 0 for no. ".format(player_del), int, 0, 1)
                    if confirmation == 1:
                        raw_tracker.remove("{}: {}".format(player_del, modifiers[player_del]))
                    break

            with open(dir_path + "\\initiative.txt", "w") as f:
                for line in raw_tracker:
                    f.write(line.rstrip("\n") + "\n")
            break

        else:
            print("Invalid command. Please try again.")


initialize()
while True:
    command = input_num("\nCommands: Quit (1), Print Player Modifiers (2), Edit Player (3), Add or Delete Players (4), Enter Combat (5) \nCommand: ", int)
    if command == 1:
        break
    elif command == 2:
        print(raw_tracker)
    elif command == 3:
        editplayer()
    elif command == 4:
        addordeleteplayer()
        initialize()
    elif command == 5:
        entercombat()
        initialize()
    else:
        print("Invalid command. Please try again.")