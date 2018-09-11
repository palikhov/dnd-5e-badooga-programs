from os import path, listdir, system, startfile
from sys import argv
import pyperclip
from subprocess import call
dir_path = path.dirname(path.realpath(__file__)) + '\\'
import webbrowser

#Made by badooga. https://github.com/badooga/Programs
#This program can be used to convert Reddit-style stat blocks from the D&D Monster Maker to a markdown format used by the 5eTools JSON Parser.
#D&D Monster Maker - http://thegeniusinc.com/dd-monster-maker-download/
#This program works by editing your clipboard data. To use this, choose the "Reddit" option in the Monster Maker (bottom right of the left half) to preview your monster in the Reddit format, copy all of that text, and then run this program.
#Now that the page has loaded, simply replace the default Parser text with what you now have copied and let the Parser do all the work.

#For use with an offline version of 5eTools, go down to line 65.

while True:
    sb = [x.replace("\\r", "").rstrip() for x in repr(pyperclip.paste())[1:-1].split(r"\n") if x.rstrip() != ""]
    test = sb[0].replace("\\r", "").rstrip()
    if not (test.startswith("**") and test.endswith("**")):
        z = input("Invalid stat block. Once you have a valid stat block copied, hit enter. ")
        continue
    break

for k in range(len(sb)):
    if sb[k].startswith("**Challenge**"):
        b = k + 1
    if sb[k].startswith("**--"):
        e = k
        break

monstername = sb[0][2:-2]

for l in range(len(sb)):
    
    sb[l] = sb[l].replace(" piercing and", " piercing, and").replace("damage from nonmagical", "from nonmagical").replace("nonmagical weapons", "nonmagical attacks").replace("**--Legendary Action", "**--Legendary Actions")

    if l == 0:
        sb[l] = "## " + monstername
    else:
        sb[l] = sb[l].replace(monstername, monstername.lower())

    if sb[l].startswith("**Senses** "):
        senses = sb[l][11:].split(", ")
        for x in range(len(senses)):
            if senses[x].startswith("passive P"):
                senses[-1], senses[x] = senses[x], senses[-1]
        sb[l] = "**Senses** " + ", ".join(senses)

    if sb[l].startswith("- "):
        sb[l] = sb[l].replace("- ", "• ").replace("*", "").replace("1 slots", "1 slot")

    elif sb[l].startswith("**--") and sb[l].endswith("--**"):
        sb[l] = sb[l].replace("**--", "### ").replace("--**", "")

    elif sb[l].startswith("**") and l in range(b, e):
        sb[l] = sb[l].replace("**", "***")

sb = ["___"] + [">"+y for y in sb]
sb[sb.index(">:-:|:-:|:-:|:-:|:-:|:-:|")] = sb[sb.index(">:-:|:-:|:-:|:-:|:-:|:-:|")][1:]

sbs = ""
for l in sb:
    sbs = sbs + l + "\n"

pyperclip.copy(sbs)

#If you want to use this program with an offline copy of 5eTools, comment out line 68, remove the '#' from line 66, and then edit in the appropriate file path as noted below.
#call("\"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe\" --allow-file-access-from-files " + "\"" + "file:\\\\\\" + "{}{}".format("c:\\your\\file\\path\\goes\\here\\", "converter.html") + "\"")

webbrowser.open("5e.tools/converter.html")