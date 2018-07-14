from random import randint
from os import path
from operator import itemgetter
from functions import input_num, input_str, XdY_Z_roller, input_question
from pickle import dump, load
from fractions import Fraction
dir_path = path.dirname(path.realpath(__file__))

#Made by badooga. Requires functions.py found at https://github.com/badooga/Python-Files

def save(mod_dict, monster_dict):
    with open(dir_path + "\\dm_data.p", "wb") as f:
        data = [mod_dict, monster_dict]
        dump(data, f)

try:
    with open(dir_path + "\\dm_data.p", "rb") as f:
        data = load(f)
        modifiers = data[0]
        monsters = data[1]

except:
    print("Data file not found. Commencing setup.")
    num_players = input_num("How many players does your party have? ", int, 1)
    modifiers = {}
    monsters = {}
    for player in range(num_players):
        player_name = input_str("Player {} Name: ".format(player + 1), True).rstrip()
        player_mod = input_num("Player {} Initiative Modifier: ".format(player + 1), int)
        modifiers[player_name] = player_mod
    save(modifiers, monsters)

def entercombat(mod_dict):
    global monsters
    initiative = {}
    num_enemygroups = input_num("\nHow many non-player factions, enemy groups, or individual NPCs are present in combat? ", int, 0)
    if num_enemygroups != 0:
        for enemygroup in range(num_enemygroups):
            enemygroup_name = input_str("Faction/Enemy/NPC {} Name: ".format(enemygroup + 1), True).rstrip()
            if enemygroup_name in monsters.keys():
                enemygroup_mod = monsters[enemygroup_name]["Initiative Modifier"]
                print(enemygroup_name + " loaded from Monster Helper.")
            else:
                enemygroup_mod = input_num("Faction/Enemy/NPC {} Initiative Modifier: ".format(enemygroup + 1), int)
            initiative[enemygroup_name] = randint(1,20) + enemygroup_mod

    if mod_dict != {}:
        for player in mod_dict.keys():
            initiative[player] = randint(1, 20) + mod_dict[player]
    
    tracker = sorted([(k,v) for k,v in initiative.items()], key=itemgetter(1), reverse=True)
    print("\nInitiative Order:")
    for pair in tracker:
        print("{}: {}".format(pair[0], pair[1]))
    

def editplayer(mod_dict):
    while True:
        if mod_dict == {}:
            print("\nYou have no players saved.")
            break
        
        ecommand = input_num("\nWould you like to edit a player's initiative modifier (1) or a player's name (2)? (enter 0 to cancel): ", int)
        if ecommand == 0:
            break

        elif ecommand == 1:
            while True:
                player_mod_edit = input_str("What player's modifier would you like to edit (enter 0 to cancel)? ", True).rstrip()
                if player_mod_edit == "0":
                    break
                elif player_mod_edit not in mod_dict.keys():
                    print("Invalid player. Please try again.")
                else:
                    player_mod_new = input_num("New Initiative Modifier: ", int)
                    mod_dict[player_mod_edit] = player_mod_new
                    print("\nEdit saved!")
                    break
            break
        
        elif ecommand == 2:
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
                    print("\nEdit saved!")
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
                if num_players_add == 1:
                    print("\nPlayer saved!")
                elif num_players_add > 1:
                    print("\Players saved!")
            break

        elif command == 2:
            while True:
                if mod_dict == {}:
                    print("\nYou have no players saved.")
                    break

                player_del = input_str("What player would you like to delete (enter 0 to cancel)? ", True)
                if player_del == "0":
                    break
                elif player_del not in mod_dict.keys():
                    print("Invalid player. Please try again.")
                else:    
                    if input_question("Are you sure you want to delete {} from the list of players (Y/N)? ".format(player_del), ["y", "n"]) == "y":
                        del mod_dict[player_del]
                        print("\nPlayer successfully deleted.")
                    break
            break

        else:
            print("Invalid command. Please try again.")

def initiative_roller():
    while True:
        ccommand = input_num("\nInitiative Commands: Enter Combat (1), Print Player Modifiers (2), Edit Player (3), Add or Delete Players (4)\nCommand (enter 0 to cancel): ", int)
        if ccommand == 0:
            break
        elif ccommand == 1:
            entercombat(modifiers)
            break
        elif ccommand == 2:
            if modifiers == {}:
                print("\nYou have no players saved.")
            else:
                print("")
                print(modifiers)
            break
        elif ccommand == 3:
            editplayer(modifiers)
            if modifiers != {}:
                save(modifiers, monsters)
        elif ccommand == 4:
            addordeleteplayer(modifiers)
            if modifiers != {}:
                save(modifiers, monsters)
        else:
            print("Invalid command. Please try again.")

def addordeletemonster():
    global monsters
    while True:
        add_or_delete = input_num("Would you like to add a monster (1), or would you like to delete a monster (2) (enter 0 to cancel)? ", int)
        if add_or_delete == 0:
            break
        elif add_or_delete == 1:
            while True:
                monster_name = input_str("Monster name: ", True)
                if monster_name in monsters.keys():
                    print("Monster already exists. Please try again.")
                else:
                    monsters[monster_name] = {}
                    m = monsters[monster_name]
                    break

            m["Challenge Rating"] = Fraction(input_num("Challenge Rating: "))
            m["Hit Points"] = input_num("Hit Points: ", int)
            m["Armor Class"] = input_num("Armor Class: ", int)
            m["Initiative Modifier"] = input_num("Initiative Modifier: ", int)
            m["Stats"] = input_str("Stats (ability scores, saves, modifiers, etc) that you find important: ", True)
            m["Features"] = input_str("Features (resistances, passive abilities, speed, etc), that you find important: ", True)
            m["Description"] = input_str("Description (tactics, lore, behavior, etc) that you find important: ", True)
            if input_question("Does this monster have Multiattack (Y/N)? ", ["y", "n"]) == "y":
                m["Multiattack"] = input_str("Multiattack description: ", True)
            else:
                m["Multiattack"] = False
            num_actions = input_num("How many available actions (including attacks) does your monster have? ", int, 1)
            m["Actions"] = {}
            for a in range(num_actions):
                while True:
                    action_name = input_str("Action {} Name: ".format(a + 1), True)
                    if action_name in m["Actions"]:
                        print("Action already exists. Please try again.")
                    else:
                        break
                action_desc = input_str("Action {} Description: ".format(a + 1), True)
                m["Actions"][action_name] = action_desc
            print("\nMonster saved!")

        elif add_or_delete == 2:
            while True:
                if monsters == {}:
                    print("\nYou have no monsters saved.")
                    break
                monster_del = input_str("What monster would you like to delete (enter 0 to cancel)? ", True)
                if monster_del == "0":
                    break
                elif monster_del not in monsters.keys():
                    print("Invalid monster. Please try again.")
                else:    
                    if input_question("Are you sure you want to delete {} from the list of monsters (Y/N)? ".format(monster_del), ["y", "n"]) == "y":
                        del monsters[monster_del]
                        print("\nMonster successfully deleted.")
                    break
        else:
            print("Invalid command. Please try again.")
            continue
        break


def editmonster():
    global monsters
    while True:
        if monsters == {}:
            print("\nYou have no monsters saved.")
            break
        monster = input_str("Monster to edit (enter 0 to cancel): ", True)
        if monster == "0":
            break
        elif monster not in monsters.keys():
            print("Invalid monster. Please try again.")
        else:
            e_m_v = {
                "Stats": "Features (resistances, passive abilities, speed, etc), that you find important: ",
                "Challenge Rating": "Challenge Rating: ",
                "Features": "Features (resistances, passive abilities, speed, etc), that you find important: ",
                "Description": "Description (tactics, lore, behavior, etc) that you find important: ",
                "CR": "Challenge Rating: ",
                }
            
            m = monsters[monster]
            print_monsters(2, monster)
            print("")
            while True:
                m_edit = input_str("What value would you like to edit (enter 0 to cancel)? ", True)
                m_e = m_edit.lower().title()
                if m_e == "0":
                    break

                abbreviations = {
                    "Cr": "Challenge Rating",
                    "Hp": "Hit Points",
                    "Health": "Hit Points",
                    "Ac": "Armor Class",
                    "Initiative Mod": "Initiative Modifier",
                    "Init Mod": "Initiative Modifier",
                    "Initiative": "Initiative Modifier",
                    "Init": "Initiative Modifier",
                    "Initiative Bonus": "Initiative Modifier",
                    "Init Bonus": "Initiative Modifier",
                    "Bonus To Initiative": "Initiative Modifier",
                    "Plus To Initiative": "Initiative Modifier",
                }
                if m_e in abbreviations.keys():
                    m_e = abbreviations[m_e]

                if m_e in [x.lower().title() for x in m["Actions"].keys()]:
                    while True:
                        new_action_desc = input_str("New {} Description: ".format(m_e), True)
                        if new_action_desc == m["Actions"][m_e]:
                            print("New description matches old description. Please try again.")
                        else:
                            m["Actions"][m_e] = new_action_desc
                            monsters[monster] = m
                            print("\nEdit saved!")
                            break
                    break

                elif m_e == "Name":
                    while True:
                        m_name = input_str("New Monster Name: ", True)
                        if m_name == monster:
                            print("New name matches old name. Please try again.")
                        else:
                            v = monsters.pop(monster)
                            monsters[m_name] = v
                            print("\nEdit saved!")
                            break
                    break   

                elif m_e in [y.lower().title() for y in m.keys()] and m_e != "Actions":
                    if m_e == "Challenge Rating":
                        m[m_e] = Fraction(input_num("Challenge Rating: "))
                    elif m_e in ["Hit Points", "Armor Class", "Initiative Modifier"]:
                        m[m_e] = input_num(m_e + ": ", int)
                    else:
                        m[m_e] = input_str(e_m_v[m_e], True)
                    monsters[monster] = m
                    print("\nEdit saved!")
                    break
                
                else:
                    print("Invalid data value. Please try again.")
            break

def print_monsters(list_or_stat, jumptoprint=False):
    global monsters
    if monsters == {}:
        print("\nYou have no monsters saved.")

    elif list_or_stat == 1:
        while True:
            monster_key = input_num("Would you like to sort your monsters by CR (1) or by name (2)? ")
            if monster_key not in [1,2]:
                print("Invalid command. Please try again.")
                continue
            break

        if monster_key == 1:
            print_monsters = sorted(monsters.keys(), key=lambda k: monsters[k]["Challenge Rating"])
        elif monster_key == 2:
            print_monsters = sorted(monsters.keys())

        print("")
        for monster_name in print_monsters:
            print(monster_name + ": CR {}".format(monsters[monster_name]["Challenge Rating"]))

    elif list_or_stat == 2:
        while True:
            if jumptoprint:
                monster_to_print = jumptoprint
            else:
                monster_to_print = input_str("What monster's stats would you like to print? ", True)
                if monster_to_print not in monsters.keys():
                    print("Monster not found. Please try again.")
                    continue
            break
        m = monsters[monster_to_print]
        print("\n" + monster_to_print + ": CR {}".format(m["Challenge Rating"]))
        if m["Initiative Modifier"] < 0:
            print("{} HP, {} AC, {} to Initiative Rolls".format(m["Hit Points"], m["Armor Class"], m["Initiative Modifier"]))
        else:
            print("{} HP, {} AC, +{} to Initiative Rolls".format(m["Hit Points"], m["Armor Class"], m["Initiative Modifier"]))
        print("\nStats: " + m["Stats"])
        print("Description: " + m["Description"])
        print("\nActions")
        if m["Multiattack"]:
            print("Multiattack: " + m["Multiattack"])
        for a in m["Actions"].keys():
            print("{}: {}".format(a, m["Actions"][a]))

def monster_helper():
    while True:
        mcommand = input_num("\nMonster Helper Commands: Print Monster List (1), Print Monster Stats (2), Edit Monster (3), Add or Delete Monster (4), Help (5)\nCommand (enter 0 to cancel): ", int)
        if mcommand == 0:
            break
        elif mcommand == 1:
            print_monsters(1)
            break
        elif mcommand == 2:
            print_monsters(2)
            break
        elif mcommand == 3:
            editmonster()
            if monsters != {}:
                save(modifiers, monsters)
        elif mcommand == 4:
            addordeletemonster()
            if monsters != {}:
                save(modifiers, monsters)
        elif mcommand == 5:
            print("\nYou can use the Monster Helper to access the bare essentials of a D&D 5e monster's stat block for use on the fly.\nTo do this, add your own monster via the 'add or delete monsters' command.\nThe Monster Helper will also work with the Initiative Roller - if you input the name of a saved monster when\nentering combat with the Initiative Roller, it will automatically use the saved monster's initiative.")
        else:
            print("Invalid command. Please try again.")

def misc():
    global monsters
    global modifiers
    while True:
        micommand = input_num("\nMisc Commands: Conditions and Effects (1), Common Spells (2), Delete Player or Monster Data (3)\nCommand (enter 0 to cancel): ")
        if micommand == 0:
            break
        elif micommand == 1:
            print("\nBelow is a list listing the effects of each condition in 5e.\n\nBlinded: Fails sight perception checks, adv. to hit them, disadv. for them to hit")
            print("\nCharmed: Can't harm the charmer, charmer has adv. on social interaction checks with them")
            print("\nCovered: 1/2 Cover = +2 AC and Dex Saves, 3/4 Cover = +5 AC and Dex Saves")
            print("\nFrightened: Disadv. on checks and attacks when source is seen, can't get closer to source")
            print("\nGrappled: 0 speed (grappler 1/2 speed), action for escape contest")
            print("\nHidden: Perception to discover hider, can't normally hide in combat (e.x. except when invisible), adv. on next hit")
            print("\nIncapacitated: No actions or reactions")
            print("\nInvisible: Disadv. to hit them, adv. for them to hit, has to take action to Hide")
            print("\nParalyzed: Incapacitated, 0 speed, fails str/dex saves, adv. to hit from range, autocrit in melee")
            print("\nPetrified: Items transform too, incapacitated, oblivious to world, adv. to hit them, resistance to all damage")
            print("\nPoisoned: Disadv. on attacks and checks")
            print("\nProne: 1/2 speed crawl, 1/2 movement to get up, disadv. for them to hit and to hit them from range, adv. to hit them in melee")
            print("\nRestrained: 0 speed, adv. to hit them, disadv. for them to hit, disadv. on dex saves")
            print("\nStunned: 0 speed, incapacitated, fails str/dex saves, adv. to hit them")
            print("\nSurprised: No surprise round - individuals that are surprised are incapacitated until next round")
            print("\nUnconscious: Same as paralyzed, falls prone, is unaware of surroundings")
            print("\nExhausted: Disadv. on checks => 1/2 speed => disadv. on everything => 1/2 max HP => 0 speed => death\nExhaustion effects stack, -1 exhaustion per long rest")
            break

        elif micommand == 2:
            print("\nBelow is a list outlining the effects of a few common spells in 5e. 'X' = spell level")
            print("\nCantrips - X starts at 1, goes up at char. level 5/11/17")
            print("Fire Bolt: 120ft attack roll, xd10 fire damage")
            print("Vicious Mockery: 60ft, wis save, Xd4 psychic damage and disadv. on next attack")
            print("Mage Hand: 30ft from caster, action to use, 30ft movement, 10 pound carry limit\nArcane Trickster Mage Hand: invis hand, stow or pickpocket, Thieves' Tools, Cunning Action to use, Sleight of Hand vs Perception")
            print("Eldritch Blast: 120ft attack roll, X shots of 1d10 force")
            print("\n1st Level Spells")
            print("Magic Missile: 2 + X darts (1d4 + 1 force each), can be blocked with Shield")
            print("Cure Wounds: touch, heal for Xd8 + ability mod")
            print("Command: 60ft wis save on X creatures in 30ft aoe, targets must understand one word command, no direct harm, done on next turn")
            print("Healing Word: bonus action 60ft, Xd4 + ability mod heal on 1 creature")
            print("Shield: +5 AC reaction to hits or Magic Missile; blocks Magic Missile")
            print("Guiding Bolt: 120ft attack roll, (3 + X)d6 radiant, next attacker gets adv. before end of your next turn")
            print("\n2nd Level Spells")
            print("Darkness: 15ft sphere on non-worn/carried object or a point, everyone inside is Blinded")
            print("Hold Person: 60ft wis save on (X - 1) creatures in 30ft aoe, paralyzed on fail, repeat saves on turn ends")
            print("Spiritual Weapon: bonus action 60ft concentration, spell attack for (X - 1)d8 + ability mod, bonus action for 20ft move and attack, attacks on summon")
            print("Scorching Ray: 120ft attack roll, (X + 1) shots of 2d6 fire")
            print("\n3rd Level Spells")
            print("Counterspell: reaction, interrupt spells X level or lower, spellcasting ability check (DC 10 + their spell level) to beat higher level spells")
            print("Mass Healing Word: bonus action 60ft, (X - 2)d4 + ability mod heal on 6 creatures")
            print("Revivify: 300gp diamond (consumed), touch to undo a non-natural death that happened within 1 min of casting, comes back with 1 HP")
            print("\n4th Level Spells")
            print("Banishment: 60ft concentration wis save on (X - 3) creatures, fail sends incapacitated targets to demiplane, they return in 1 min, if the spell isn't interrupted after 1 min they don't return if they are not native to current plane")
            print("Fire Shield: 10min, caster gets resistance to cold or fire, melee attackers take 2d8 fire or cold, respectively")
            print("Wall of Fire: 1min, 20ft tall and 1ft thick, 60ft long or 20ft diameter, dex save on appearance for (X + 1)d8 fire or half, damaging side of wall does (X + 1)d8 when entering it or ending turn within 10ft")
            print("Polymorph: 60min concentration, unwilling targets wis save, new form is beast less than or equal to target's CR/level, extra HP pool, all stats replaced, gear melds into them")

        elif micommand == 3:
            while True:
                delete = input_num("Would you like to delete all player data (1) or all monster data (2) (enter 0 to cancel)? ", int)
                if delete == 0:
                    break
                elif delete == 1:
                    if modifiers == {}:
                        print("\nThere is no player data to delete.")
                    elif input_question("This action is irreversible. Are you sure you want to delete all player data (Y/N)? ", ["y", "n"]) == "y":
                        modifiers = {}
                        save(modifiers, monsters)
                        print("\nPlayer data successfully deleted.")
                    break
                elif delete == 2:
                    if monsters == {}:
                        print("\nThere is no monster data to delete..")
                    elif input_question("This action is irreversible. Are you sure you want to delete all monster data (Y/N)? ", ["y", "n"]) == "y":
                        monsters = {}
                        save(modifiers, monsters)
                        print("\Monster successfully deleted.")
                    break
                else:
                    print("Invalid command. Please try again.")
            break

        else:
            print("Invalid command. Please try again.")

while True:
    command = input_num("\nCommands: Quit (1), Initiative Roller (2), Monster Helper (3), Dice Roller (4), Misc (5)\nCommand: ", int)
    if command == 1:
        break
    elif command == 2:
        initiative_roller()
    elif command == 3:
        monster_helper()
    elif command == 4:
        XdY_Z_roller()
    elif command == 5:
        misc()
    else:
        print("Invalid command. Please try again.")