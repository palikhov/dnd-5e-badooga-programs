#Made by badooga.
#Use the Task Scheduler (or a similar program) to have this file open on startup; requires you to have the file functions.py that can be found at https://github.com/badooga/Python-Files
from random import choice as rchoice
from os import startfile, path, listdir
from getpass import getuser
from time import ctime
from functions import *
from re import split as rsplit
from webbrowser import open_new_tab
dir_path = path.dirname(path.realpath(__file__))


hour = int(ctime().split()[3][:2])

def natural_key(string_): #used to properly sort file names
    """See http://www.codinghorror.com/blog/archives/001018.html"""
    return [int(s) if s.isdigit() else s for s in rsplit(r'(\d+)', string_)]

#Edit these variables if you want to customize them - for example, you may store your music in a different folder

filepath_playlists = "C:\\Users\\{}\\Music\\Playlists\\".format(getuser())
filepath_songs = "C:\\Users\\{}\\Music\\Songs\\".format(getuser())

try:
    with open(dir_path + "\\name.txt", "r") as n:
        user = n.readline().rstrip()
    if user == "":
        raise EOFError
except:
    with open(dir_path + "\\name.txt", "w") as n:
        while True:
            user = input_str("Name not found. What name would you like to go by? ", True).rstrip()
            if user == "":
                print("Invalid name. Please try again.")
            else:
                break
        n.write(user)

if hour < 12:
    print("Good morning, {}.".format(user))
elif hour > 18:
    print("Good evening, {}.".format(user))
else:
    print("Good afternoon, {}.".format(user))

r_list = []
try:
    with open(dir_path + "\\reminders.txt", "r") as r:
        r_list_original = r.readlines()
        if r_list_original == []:
            print("\nYou have no reminders.")
        else:
            print("\nReminders:")
            for line in r_list_original:
                print(line.rstrip())
                r_list.append(line.rstrip())
except:
    print("\nYou have no reminders.")
    with open(dir_path + "\\reminders.txt", "w") as r:
        pass



#keep in mind that for general user input, I'm starting at 1 and not 0 for the sake of typing ease

def music():
    while True:
        choice = input_num("\nMusic commands: Playlist (1), Song (2), File Locations (3)\nCommand (enter 0 to cancel): ")
        if choice not in [x for x in range(4)]:
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
    
    while mcommand[2]:
        print("Playlists filepath: " + filepath_playlists +"\nSongs filepaths: " + filepath_songs)
        break

def misc():
    while True:
        choice = input_num("\nMisc commands: Dice (1), Stats (2)\nCommand (enter 0 to cancel): ", int)
        if choice == 0:
            pass
        elif choice == 1:
            XdY_Z_roller()
        elif choice == 2: 
            statistical_analysis_print(statistical_analysis_input())
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
        command = input_num("\nReminder commands: Print Reminder (1), New (2), Edit (3), Delete (4)\nCommand (enter 0 to cancel): ", int)
        if command == 0:
            break

        elif command == 1:
            while True:
                print_reminder = input_num("Choose a reminder to print (enter 0 to print all reminders): ", int, 0)
                if print_reminder == 0:
                    if r_list == []:
                        print("\nYou have no reminders.")
                    else:
                        print("\nReminders:")
                        for line in r_list:
                            print(line)
                    break
                else:
                    try:
                        print("\nReminder {}:\n".format(print_reminder) + r_list[print_reminder - 1])
                        break
                    except IndexError:
                        if r_list == []:
                            print("\nYou have no reminders.")
                            break
                        else:
                            print("Invalid reminder. Please try again.")

        elif command == 2:
            new_reminder = input_str("New reminder (input empty space to cancel): ", True).rstrip()
            if new_reminder != "":
                r_list.append(new_reminder)

        elif command == 3:
            while True:
                edit_reminder = input_num("Choose a reminder to edit (enter 0 to cancel): ", int, 0)
                if edit_reminder == 0:
                    break
                try:
                    r_list[edit_reminder - 1]
                    r_list[edit_reminder - 1] = input_str("Reminder: ", True)
                    break
                except IndexError:
                    if r_list == []:
                        print("\nYou have no reminders.")
                        break
                    else:
                        print("Invalid reminder. Please try again.")

        elif command == 4:
            while True:
                delete_reminder = input_num("Reminder to delete (enter 0 to cancel): ", 0)
                if delete_reminder == 0:
                    break
                try:
                    r_list[delete_reminder - 1]
                    del r_list[delete_reminder - 1]
                    break
                except IndexError:
                    if r_list == []:
                        print("\nYou have no reminders.")
                        break
                    else:
                        print("Invalid reminder. Please try again.")

        else:
            print("Invalid command. Please try again.")

        with open(dir_path + "\\reminders.txt", "w") as r:
            for line in r_list:
                r.write(line + "\n")

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