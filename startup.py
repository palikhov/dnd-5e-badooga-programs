import os
from getpass import getuser
from time import ctime
from functions import input_str as pstr

user = getuser()
filepath = "C:\\Users\\{}\\Music\\Playlists\\".format(user)
hour = int(ctime().split()[3][:2])
loop = True

if hour < 12:
    print("Good morning, {}.".format(user))
elif hour > 18:
    print("Good evening, {}.".format(user))
else:
    print("Good afternoon, {}.".format(user))
while loop:
    choice = pstr("What music playlist would you like to play today (enter None for no music)? ", True, 1, True)
    if choice == "None":
        loop = False
    else:
        try:
            os.startfile(filepath + choice + ".wpl")
            loop = False
        except:
            print("Error: File not found.")