from random import randint
from operator import itemgetter
#Made by badooga.


"""Welcome! If you want to use this, first download the file. If you know how to edit and run your downloaded version, you can use this to quickly roll
initiative for both your players and your enemy combatants. Below are a few comments that will explain how to customize this tracker to your liking. Have fun!"""

initiative = {
    #The format goes as follows, with the name being either player name or character name.
    #(PC or Player Name): d20 roll + initiative mod
    "Player 1": randint(1,20) + 0,
    "Player 2": randint(1,20) + 0,
    "Player 3": randint(1,20) + 0,
    "Player 4": randint(1,20) + 0,
    #To add more players or monsters, remove the "#" before the appropriate lines, and then fill in the appropriate data. To remove a player, add a "#" to comment out the line.
    #"Player 5": randint(1,20) + 0,
    #"Player 6": randint(1,20) + 0,
    #"Player 7": randint(1,20) + 0,
    #"Player 8": randint(1,20) + 0,

    #Use the following lines to add enemies (including groups of enemies) to your scenario with ease:
    #"Enemy A": randint(1,20) + 0,
    #"Enemy B": randint(1,20) + 0,
    #"Enemy C": randint(1,20) + 0,
    #"Enemy D": randint(1,20) + 0,
    #"Enemy E": randint(1,20) + 0,
    #"Enemy F": randint(1,20) + 0,
    #"Enemy G": randint(1,20) + 0,
}

tracker = sorted([(k,v) for k,v in initiative.items()], key=itemgetter(1), reverse=True)
print("\nInitiative Order:")
for pair in tracker:
    print("{} - {}".format(pair[0], pair[1]))