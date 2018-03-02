#Made by badooga.
#Use the Task Scheduler (or a similar program) to have this file open on startup; requires you to have the file functions.py that can be found at https://github.com/badooga/Python-Files
from random import choice as rchoice
from os import startfile
from os import listdir
from getpass import getuser
from time import ctime
from functions import *
from re import split as rsplit
from webbrowser import open_new_tab

hour = int(ctime().split()[3][:2])

def natural_key(string_): #used to properly sort file names
    """See http://www.codinghorror.com/blog/archives/001018.html"""
    return [int(s) if s.isdigit() else s for s in rsplit(r'(\d+)', string_)]

#Edit these variables if you want to customize them - for example, you may store your music in a different folder, or you may not want to be referred to by your account username
user = getuser()
filepath_playlists = "C:\\Users\\{}\\Music\\Playlists\\".format(user)
filepath_songs = "C:\\Users\\{}\\Music\\Songs\\".format(user)

if hour < 12:
    print("Good morning, {}.".format(user))
elif hour > 18:
    print("Good evening, {}.".format(user))
else:
    print("Good afternoon, {}.".format(user))

#keep in mind that for user input, I'm starting at 1 and not 0 for the sake of typing ease
def music(playlist_extension="", song_extension=""):
    choice = input_num("Would you like to play a playlist (1), a specific song (2), or remain silent (3)? ", int, 1, 3)
    mcommand = [False, False, False]
    mcommand[choice - 1] = True

    song_list = sorted(listdir(filepath_songs), key=natural_key)
    playlist_list = sorted(listdir(filepath_playlists), key=natural_key)

    while mcommand[0]:
        choice = input_str("What music playlist would you like to play (enter 0 to cancel, -1 for a random playlist)? ", True, 1, True)
        if choice == "0":
            mcommand[0] = False
        else:
            try:
                startfile(filepath_playlists + choice + playlist_extension)
                mcommand[0] = False
            except:
                try: #if a filename starts with what you enter, this will play it; this works well if you start your filenames with the number of the song in the list
                    file_found = False
                    for playlist in playlist_list:
                        if playlist.lower().startswith(choice.lower()):
                            startfile(filepath_playlists + playlist)
                            file_found = True
                            mcommand[0] = False
                            break
                    if not file_found:
                        file_found = False
                        raise EOFError
                except:
                    print("Error: File not found.")
    while mcommand[1]:
        choice = input_str("What song would you like to play (enter 0 to cancel, -1 for a random song)? ", True, 1, True)
        if choice == "0":
            mcommand[1] = False
        else:
            try:
                startfile(filepath_songs + choice + song_extension)
                mcommand[1] = False
            except:
                try:
                    file_found = False
                    for song in song_list:
                        if song.lower().startswith(choice.lower()):
                            startfile(filepath_songs + song)
                            file_found = True
                            mcommand[1] = False
                            break
                    if not file_found:
                        file_found = False
                        raise EOFError
                except:
                    print("Error: File not found.")

def website():
    choice = input_str("What site would you like to visit (enter 0 to cancel)? ", True, 1, True).lower()
    if choice != "0":
        open_new_tab("http://www." + choice + ".com")

def misc():
    while True:
        choice = input_num("\nMisc commands: Cancel (1), Dice (2), Stats (3)\nCommand: ", int)
        if choice == 1:
            pass
        elif choice == 2:
            XdY_Z_roller()
        elif choice == 3: 
            statistical_analysis_print(statistical_analysis_input())
        else:
            print("Invalid command. Please try again.")
            continue
        break

while True:
    command = input_num("\nCommands: Quit (1), Music (2), Website (3), Misc (4)\nCommand: ", int)
    if command == 1:
        break
    elif command == 2:
        music()
    elif command == 3:
        website()
    elif command == 4:
        misc()
    else:
        print("Invalid command. Please try again.")