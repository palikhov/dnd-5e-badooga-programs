#Made by badooga.
#Requires the file functions.py that can be found at https://github.com/badooga/Python-Files
from random import choice as rchoice
from os import startfile, path, listdir
from getpass import getuser
from time import ctime
from functions import *
from re import split as rsplit
from webbrowser import open_new_tab
from pickle import dump, load
dir_path = path.dirname(path.realpath(__file__))

def natural_key(string_): #used to properly sort file names
    """See http://www.codinghorror.com/blog/archives/001018.html"""
    return [int(s) if s.isdigit() else s for s in rsplit(r'(\d+)', string_)]

def openfile(filepath, filename):
    try:
        startfile(filepath + filename)
    except:
        try:
            startfile(filepath + "\\" + filename)
        except:
            startfile(filepath + "/" + filename)

#loading of saved data
try:
    with open(dir_path + "\\assistant.p", "rb") as f:
        data = load(f)
except:
    data = {}

error = False

#user
try:
    user = data["user"]
except:
    error = True
    while True:
        user = input_str("Name data not found.\nWhat name would you like to go by? ", True).rstrip()
        if user == "":
            print("Invalid name. Please try again.")
        else:
            break

#music
try:
    music_paths = data["music"]
    filepath_playlists = music_paths[0]
    filepath_songs = music_paths[1]
except:
    error = True
    while True:
        filepath_playlists = input_str("Music filepath data not found.\nPlease enter the filepath that you want this program to open playlists from: ", True).rstrip()
        if not path.isdir(filepath_playlists):
            print("Invalid filepath. Please try again.")
        else:
            break
    while True:
        filepath_songs = input_str("Next, please enter the filepath that you want this program to open songs from: ", True).rstrip()
        if not path.isdir(filepath_songs):
            print("Invalid filepath. Please try again.")
        else:
            break
    music_paths = [filepath_playlists, filepath_songs]

hour = int(ctime().split()[3][:2])

if error:
    print("")

if hour < 12:
    print("Good morning, {}.".format(user))
elif hour > 18:
    print("Good evening, {}.".format(user))
else:
    print("Good afternoon, {}.".format(user))

#reminders
try:
    r_list = data["reminders"]
    if r_list == []:
        print("\nYou have no reminders.")
    else:
        print("\nReminders:")
        for r in range(len(r_list)):
            print("{}) ".format(r + 1) + r_list[r])
except:
    print("\nYou have no reminders.")
    r_list = []

def save():
    global r_list
    global user
    global music_paths
    data = {
        "user": user,
        "reminders": r_list,
        "music": music_paths
    }
    with open(dir_path + "\\assistant.p", "wb") as f:
        dump(data, f)

save()

#keep in mind that for general user input, I'm starting at 1 and not 0 for the sake of typing ease

def music():
    global filepath_songs
    global filepath_playlists
    global music_paths

    while True:
        choice = input_num("\nMusic commands: Playlist (1), Song (2), Filepath Options (3)\nCommand (enter 0 to cancel): ", int)
        if choice not in range(4):
            print("Invalid command. Please try again.")
            continue
        break

    mcommand = [False, False, False]
    if choice != 0:
        mcommand[choice - 1] = True

    song_list = sorted(listdir(filepath_songs), key=natural_key)
    playlist_list = sorted(listdir(filepath_playlists), key=natural_key)

    while mcommand[0]:
        choice = input_str("What music playlist would you like to play (enter 0 to cancel, -1 for a random playlist)? ", True)
        if choice == "0":
            pass
        elif choice == "-1":
            openfile(filepath_playlists, rchoice(playlist_list))
        elif choice == "":
            print("Invalid playlist name. Please try again.")
            continue
        else: #if a filename starts with what you enter, this will play that file; this works well if you start your filenames with the number of the song in the list
            for playlist in playlist_list:
                if playlist.lower().startswith(choice.lower()):
                    openfile(filepath_playlists, playlist)
                    break
            else:
                print("Error: File not found.")
                continue
        break
    while mcommand[1]:
        choice = input_str("What song would you like to play (enter 0 to cancel, -1 for a random song)? ", True)
        if choice == "0":
            pass
        elif choice == "":
            print("Invalid song name. Please try again.")
            continue
        elif choice == "-1":
            openfile(filepath_songs, rchoice(song_list))            
        else: #if a filename starts with what you enter, this will play that file
            for song in song_list:
                if song.lower().startswith(choice.lower()):
                    openfile(filepath_songs, song)
                    break
            else:
                print("Error: File not found.")
                continue
        break
    
    while mcommand[2]:
        music_choice = input_num("\nMusic filepath commands: Print Filepaths (1), Edit Playlist Filepath (2), Edit Song Filepath (3)\nCommand (enter 0 to cancel): ", int)
        if music_choice == 0:
            break
        elif music_choice == 1:
            print("\nPlaylists filepath: " + filepath_playlists +"\nSongs filepaths: " + filepath_songs)
        elif music_choice == 2:
            while True:
                new_filepath_playlists = input_str("New playlist filepath (enter 0 to cancel): ", True).rstrip()
                if new_filepath_playlists == "0":
                    break
                elif new_filepath_playlists == filepath_playlists:
                    print("{} already set as playlist path. Please try again.".format(new_filepath_playlists))
                elif not path.isdir(new_filepath_playlists):
                    print("Invalid filepath. Please try again.")
                else:
                    filepath_playlists = new_filepath_playlists
                    music_paths = [filepath_playlists, filepath_songs]
                    save()
                    break
        elif music_choice == 3:
            while True:
                new_filepath_songs = input_str("New song filepath (enter 0 to cancel): ", True).rstrip()
                if new_filepath_songs == "0":
                    break
                elif new_filepath_songs == filepath_songs:
                    print("{} already set as song path. Please try again.".format(new_filepath_songs))
                elif not path.isdir(new_filepath_songs):
                    print("Invalid filepath. Please try again.")
                else:
                    filepath_songs = new_filepath_songs
                    music_paths = [filepath_playlists, filepath_songs]
                    save()
                    break
        else:
            print("Invalid command. Please try again.")

def misc():
    global user
    while True:
        choice = input_num("\nMisc commands: Dice (1), Stats (2), Change Name (3)\nCommand (enter 0 to cancel): ", int)
        if choice == 0:
            pass
        elif choice == 1:
            XdY_Z_roller()
        elif choice == 2: 
            statistical_analysis_print(statistical_analysis_input())
        elif choice == 3:
            while True:
                new_name = input_str("New name (enter 0 to cancel): ", True).rstrip()
                if new_name == "0":
                    break
                elif new_name == "":
                    print("Invalid name. Please try again.")
                elif new_name == user:
                    print("{} already set as name. Please try again.".format(new_name))
                else:
                    user = new_name
                    print("\n{} set as new name.".format(user))
                    save()
                    break
        else:
            print("Invalid command. Please try again.")
            continue
        break

#in the last loop where this function is called, add an argument containing the appropriate site extension if you are not from the US (e.x. ".co.uk" if you are from the UK)
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

def reminders():
    while True:
        command = input_num("\nReminder commands: Print Reminders (1), New (2), Edit (3), Delete (4)\nCommand (enter 0 to cancel): ", int)
        if command == 0:
            break

        elif command == 1:
            if r_list == []:
                print("\nYou have no reminders.")
            else:
                print("\nReminders:")
                for r in range(len(r_list)):
                    print("{}) ".format(r + 1) + r_list[r])
            break
                            
        elif command == 2:
            new_reminder = input_str("New reminder (input empty space to cancel): ", True).rstrip()
            if new_reminder != "":
                r_list.append(new_reminder)
                save()

        elif command == 3:
            while True:
                edit_reminder = input_num("Choose a reminder to edit (enter 0 to cancel): ", int, 0)
                if edit_reminder == 0:
                    break
                elif r_list == []:
                    print("\nYou have no reminders.")
                    break
                elif edit_reminder > len(r_list):
                    print("Invalid reminder. Please try again.")
                else:
                    r_list[edit_reminder - 1] = input_str("Reminder: ", True)
                    save()
                    break

        elif command == 4:
            while True:
                delete_reminder = input_num("Reminder to delete (enter 0 to cancel): ", 0)
                if delete_reminder == 0:
                    break
                elif r_list == []:
                    print("\nYou have no reminders.")
                    break
                elif delete_reminder > len(r_list):
                    print("Invalid reminder. Please try again.")
                else:
                    if input_question("Are you sure want to delete this reminder (Y/N)? ", ["y", "n"]) == "y":
                        del r_list[delete_reminder - 1]
                        save()
                    break 

        else:
            print("Invalid command. Please try again.")

while True:
    command = input_num("\nCommands: Quit (1), Music (2), Reminders (3), Search (4), Misc (5) \nCommand: ", int)
    if command == 1:
        break
    elif command == 2:
        music()
    elif command == 3:
        reminders()
    elif command == 4:
        search()
    elif command == 5:
        misc()
    else:
        print("Invalid command. Please try again.")