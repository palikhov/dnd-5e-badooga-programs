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
def music():
    while True:
        choice = input_num("Would you like to play a playlist (1), play a song (2), or cancel (3)? ")
        if choice not in [x for x in range(4)]:
            print("Invalid command. Please try again.")
            continue
        break

    mcommand = [False, False, False]
    mcommand[choice - 1] = True

    song_list = sorted(listdir(filepath_songs), key=natural_key)
    playlist_list = sorted(listdir(filepath_playlists), key=natural_key)

    while mcommand[0]:
        choice = input_str("What music playlist would you like to play (enter 0 to cancel, -1 for a random playlist)? ", True)
        if choice == "0":
            pass
        elif choice == "-1":
            startfile(filepath_playlists + rchoice(playlist_list))
        else: #if a filename starts with what you enter, this will play that file; this works well if you start your filenames with the number of the song in the list
            for playlist in playlist_list:
                if playlist.lower().startswith(choice.lower()):
                    startfile(filepath_playlists + playlist)
                    break
            else:
                print("Error: File not found.")
                continue
        break
    while mcommand[1]:
        choice = input_str("What song would you like to play (enter 0 to cancel, -1 for a random song)? ", True)
        if choice == "0":
            pass
        elif choice == "-1":
            startfile(filepath_songs + rchoice(song_list))            
        else: #if a filename starts with what you enter, this will play that file
            for song in song_list:
                if song.lower().startswith(choice.lower()):
                    startfile(filepath_songs + song)
                    break
            else:
                print("Error: File not found.")
                continue
        break

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

#in the last loop, add an argument containing the appropriate site extension if you are not from the US (e.x. co.uk if you are from the UK)
def search(extension=".com"):
    search_type = input_num("\nSearch types: Default (1), Images (2), News (3), YouTube (4)\nSearch type (enter 0 to cancel): ", int)
    while search_type not in [x for x in range(5)]:
        print("Invalid search type. Please try again.")
        search_type = input_num("\nSearch types: Default (1), Images (2), News (3), YouTube (4)\nSearch type (enter 0 to cancel): ", int)
    url = "google" + extension
    if search_type == 0:
        return
    elif search_type == 1:
        url = url + "/search?q="
    elif search_type == 2:
        url = url + "/search?tbm=isch&q="
    elif search_type == 3:
        url = url + "/search?tbm=nws&q="
    elif search_type == 4:
        url = "youtube" + extension + "/results?search_query="
    search = input_str("Query to search: ", True).replace("+", "%2B").replace(" ", "+")
    open_new_tab("https://www." + url + search)

while True:
    command = input_num("\nCommands: Quit (1), Music (2), Google (3), Misc (4)\nCommand: ", int)
    if command == 1:
        break
    elif command == 2:
        music()
    elif command == 3:
        search()
    elif command == 4:
        misc()
    else:
        print("Invalid command. Please try again.")