#Made by badooga. Requires functions.py found at https://github.com/badooga/Programs

#5eTools: https://5e.tools/
#This program only supports base 5eTools content at the moment; your 5eTools homebrew sadly won't work with this.
#Also, a very minor issue is that this tool uses Google Chrome, so if you don't have Google Chrome, you need to download it in order to use this.

from os import listdir, path
from subprocess import call
from functions import input_str, input_num
import json
dir_path = path.dirname(path.realpath(__file__)) + "\\"

if "5etools.html" not in listdir(dir_path):
    error = input("This program is intended to be used alongside an offline copy of 5eTools. For this to work, put this program in the same folder as 5eTools.html, as it uses filepaths relative to that folder.\nEnter any key to quit: ")
    quit()

modules = {
    "bestiary": (1),
    "spells": (2),
    "backgrounds": (3),
    "items": (4),
    "classes": (5),
    "conditionsdiseases": (6, 21),
    "feats": (7),
    "invocations": (8),
    "psionics": (9),
    "races": (10),
    "rewards": (11),
    "variantrules": (12),
    "adventure": (13),
    "deities": (14),
    "objects": (15),
    "trapshazards": (16, 17),
    "quickreference": (18),
    "cultsboons": (19, 20),
    }

modules_switch = {}
for k,v in modules.items():
    if type(v) != int:
        for i in v:
            modules_switch[i] = k
    else:
        modules_switch[v] = k

for m in modules.keys():
    exec("""
def {}(query=False):
    search(query, {})
""".format(m, modules[m]))


def help():
    #help menu - print all commands, have further input for detailed descriptions and parameters
    print("\nBelow is the list of commands usable in this program. Text shown [like this] next to a command means that there is an optional parameter you can add (without the brackets) after the command.\nFor example, to search for the Magic Missile spell, you can input !spells Magic Missile.\n")
    print("!quit: exits the program.")
    print("!search [query]: searches through most of the below categories.")
    print("!bestiary [monster]: searches for a monster stat block.")
    print("!spells: searches for a spell.")
    print("!backgrounds [background]: searches for a player background.")
    print("!items [item]: searches for any item in the game.")
    print("!classes [class]; [subclass]: searches for a player class, optionally including a subclass via a semicolon. Example usage - !classes Bard; College of Lore")
    print("!conditionsdiseases [condition or disease]: searches for a disease (DMG) or condition.")
    print("!feats [feat]: searches for a feat.")
    print("!invocations [invocation]: searches for a Warlock Eldritch Invocation.")
    print("!psionics [psionic]: searches for a Mystic (UA: The Mystic Class) psionic.")
    print("!races [race]: searches for a playable race.")
    print("!rewards [rewards]: searches for a blessing, boon, or charm (DMG).")
    print("!variantrules [rule]: searches for a variant rule.")
    print("!adventure [adventure]: searches for an official campaign book or adventure.")
    print("!deities [deity]: searches for a god found in D&D.")
    print("!objects [object]: searches for a generic object or siege weapon.")
    print("!trapshazards [trap or hazard]: searches for a trap or hazard.")
    print("!quickreference [rule]: searches for a common rule to be referenced.")
    print("!cultsboons [cult or boon]: searches for a cult or a demonic boon.")
    print("!names: opens the page for racial name tables.")
    print("!lifegen: opens the This Is Your Life generator.")
    print("!crcalculator: opens the CR calculator.")
    print("!lootgen: opens the loot generator.")
    print("!dmscreen: opens the DM screen.")

def search(s, c=0): #search, command
    global modules
    global modules_switch
    global chromedir

    if type(c) == tuple:
        c = c[0]
    if s == False and c == 0:
        print("Please enter a valid search query.")
        return
    elif s == False and type(c) == int:
        call("\"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe\" --allow-file-access-from-files " + "\"" + 'file:\\\\\\' + dir_path + modules_switch[c] + ".html" + "\"", shell=True)
        return

    with open(dir_path + "search\\index.json", "r") as k:
        data = json.load(k)
    if c == 0:
        searchpool = data
    else:
        searchpool = [x for x in data if x["c"] == c]
    
    resultpool = []
    for result in searchpool:
        if s in result["n"].lower():
            resultpool.append(result)
    if resultpool == []:
        print("No results found for '{}'.".format(s))
    else:
        rlist = []
        filepath = 'file:\\\\\\' + dir_path + modules_switch[resultpool[0]["c"]] + ".html#"
        if len(resultpool) == 1 and s == resultpool[0]["n"].lower():
            call("\"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe\" --allow-file-access-from-files " + "\"" + filepath + resultpool[0]["u"] + "\"")
        else:
            for result in resultpool:
                try:
                    rlist.append(modules_switch[result["c"]].title() + ": " + result["n"] + ", " + result["s"] + " page {}".format(result["p"]))
                except KeyError:
                    try:
                        if result["c"] == 13:
                            raise Exception
                        rlist.append(modules_switch[result["c"]].title() + ": " + result["n"] + ", " + result["s"])
                    except:
                        rlist.append(modules_switch[result["c"]].title() + ": " + result["n"])
            if len(rlist) == 1:
                print("\n{} result found for '{}':".format(len(rlist), s))
            else:
                print("\n{} results found for '{}':".format(len(rlist), s))
            x = 0
            for r in rlist:
                print("[{}] ".format(rlist.index(r) + 1) + r)
            search_picker = input_num("\nEnter the number of the result you are looking for (enter 0 to cancel): ", int, 0, len(rlist)) - 1
            if search_picker > -1:
                filepath = "file:\\\\\\" + dir_path + modules_switch[resultpool[search_picker]["c"]] + ".html#"
                call("\"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe\" --allow-file-access-from-files " + "\"" + filepath + resultpool[search_picker]["u"] + "\"")
        

print("Welcome to the 5eTools Assistant. Use !help for a list of available commands, and use !quit to quit.")
while True:
    command = input_str("\nCommand: ", int).lower().split(maxsplit=1)      
    if command[0][1:] in ["names", "lifegen", "crcalculator", "lootgen", "dmscreen"]:
        call("\"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe\" --allow-file-access-from-files " + "\"" + "file:\\\\\\" + "{}{}.html".format(dir_path, command[0][1:]) + "\"")
    elif command[0][1:] in ["help", "quit"] or (len(command) == 1 and command[0][1:] in modules.keys()):
        exec("{}()".format(command[0][1:]))
    elif command[0] == "!search":
        exec("{}('{}')".format(command[0][1:], command[1]))
    elif command[0][1:] in modules.keys():
        exec("{}('{}')".format(command[0][1:], command[1]))
    else:
        print("Invalid command. Please try again.")