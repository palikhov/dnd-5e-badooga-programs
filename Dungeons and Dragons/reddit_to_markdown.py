import pyperclip

#Made by badooga. https://github.com/badooga/Programs

#This program can be used to convert Reddit-style stat blocks, such as from the D&D Monster Maker to a markdown format used by tools like GMBinder.
#D&D Monster Maker - http://thegeniusinc.com/dd-monster-maker-download/
#This program works by editing a Reddit-style stat block that is copied to the clipboard. To use this with the tool linked above, choose the "Reddit" option in the Monster Maker (bottom right of the left half) to preview your monster in the Reddit format, click the Reddit button on the righthand side to copy this to your clipboard, and then run this program.

def main():
    while True:
        sb = [x.replace("\\r", "").rstrip() for x in repr(pyperclip.paste())[1:-1].split(r"\n") if x.rstrip() != ""]
        test = sb[0].replace("\\r", "").rstrip()
        if not (test.startswith("**") and test.endswith("**")):
            z = input("Invalid stat block. Once you have a valid stat block copied, hit enter. ")
            continue
        break


    le = len(sb)-1
    for k in range(len(sb)):
        if sb[k].startswith("**Challenge**"):
            b = k + 1
        if sb[k].startswith("**--A"):
            e = k
        if "**--Legendary " in sb[k]:
            le = k

    monstername = sb[0][2:-2]

    damage = 0
    l = 0
    length = len(sb)

    while not (l > length):
        
        try:
            test = sb[l]
        except:
            break

        sb[l] = sb[l].replace(" piercing and", " piercing, and").replace("damage from nonmagical", "from nonmagical").replace("nonmagical weapons", "nonmagical attacks").replace("**--Legendary Action", "**--Legendary Actions").replace("Melee Weapon Attack: ", "*Melee Weapon Attack:* ").replace("Ranged Weapon Attack: ", "*Ranged Weapon Attack:* ").replace("Melee Spell Attack: ", "*Melee Spell Attack:* ").replace("Ranged Spell Attack: ", "*Ranged Weapon Attack:* ")

        if sb[l].startswith("**Damage"):
            if "piercing, and " in sb[l]:
                sb[l] = sb[l].replace(",", ";").replace("bludgeoning; piercing; and ", "bludgeoning, piercing, and ")

        if l == 0:
            sb[l] = "## " + monstername

        if sb[l].startswith("**--") and sb[l].endswith("--**"): #section heading
            sb[l] = sb[l].replace("**--", "### ").replace("--**", "")

        if sb[l].startswith("**Senses** "):
            senses = sb[l][11:].split(", ")
            for x in range(len(senses)):
                if senses[x].startswith("passive P"):
                    senses[-1], senses[x] = senses[x], senses[-1]
            sb[l] = "**Senses** " + ", ".join(senses).rstrip()

        if sb[l].startswith("- ") and sb[l] in sb[b:le]: #spellcasting
            sb[l] = sb[l].replace("1 slots", "1 slot").replace("- ", "")

        elif (sb[l].startswith("**") and sb[l] in sb[0:b]) or (sb[l] in sb[le:] and sb[l].startswith("*")): #indentation
            sb[l] = sb[l].replace("**", "- **", 1)
        
        elif sb[l].startswith("**") and sb[l] in sb[b:le]: #proper bolding
            sb[l] = sb[l].replace("**", "***")

        elif sb[l] in sb[le:]:
            sb[l].replace("***", "**")

        if "**Damage" in sb[l]:
            if damage == 1 and "Resistances" in sb[l]:
                sb[l], sb[l-1] = sb[l-1], sb[l]
            else:
                damage = 1

        if l in range(b, length) and sb[l] != "" and not (l >= le):
            sb.insert(l + 1, "")
            e, le = e + 1, le + 1

        length = len(sb)
        l = l + 1

    sb = ["___"] + [">"+y+"  " for y in sb]

    sbs = ""
    for l in sb:
        sbs = sbs + l + "\n"

    pyperclip.copy(sbs)

while True:
    main()
    if input("Markdown copied to clipboard. Repeat operation (Y/N)? ").lower() == "n":
        quit()