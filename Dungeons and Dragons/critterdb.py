"""
Made by badooga. https://github.com/badooga/Python-Files

Converts Homebrewery from CritterDB to be in proper GM Binder format.
To use this, click the Copy to Clipboard option for Natural Crit exporting and then run this script; your clipboard will now have the fixed version.

Other things this script can't fix:
- for Legendary Actions, you may have to fix the naming scheme (e.g. it'll refer to them as "The joe can..." instead of "Joe can") as well as the gender (it will always say "it" even if it should be his/her/they/etc).
- for resistances, immunities, and vulnerabilities, make sure it is formatted along the lines of "cold, fire; bludgeoning, piercing, and slashing from nonmagical attacks" with respect to commas and semicolons

Happy brewing!
"""

import pyperclip

spellcasting = [">" + x for x in ["At will: ", "Cantrip (at will)", "1/day", "2/day", "3/day", "1st level", "2nd level", "3rd level", "4th level", "5th level", "6th level", "7th level", "8th level", "9th level"]]

statblock = pyperclip.paste().replace("\r","").split("\n")

switch = 0
l = 0

while l < len(statblock):
	statblock[l] = statblock[l].replace("Deep speech", "Deep Speech").replace("Languages** All", "Languages** all")

	if "###" in statblock[l]:
		switch = 0

	if switch and statblock[l] == ">":
		del statblock[l]
		l -= 1

	if any(statblock[l].lower().startswith(x.lower()) for x in spellcasting):
		statblock.insert(l + 1, ">")

	elif switch:
		statblock[l] = statblock[l].replace(">***", ">- **").replace("***", "**")
		#print(statblock[l])
	
	if "Legendary Actions" in statblock[l] and "###" in statblock[l]:
		switch = 1

	l += 1

pyperclip.copy("\n".join(statblock))
