"""
Made by badooga. https://github.com/badooga/Programs/

This script converts an adventure or book from markdown form to 5eTools. To use it, pass the md file as an argument in the cmd.

This script does not automatically input tags, metadata, or images, nor does it automatically add content like monsters and spells to 5eTools:
- For tags, add them to the markdown before using this script. Other than bold and italics tags, this script does not handle that sort of thing.
- For monsters, use CritterDB to transcribe a monster and to export it to Homebrewery/Markdown (you can transcribe it manually, but CritterDB speeds that up). Then use the 5eTools Text Converter to turn it into JSON, and include the monster in the adventure as normal.
- For images, use the JSON format below and paste it into the main adventure/book after using this script.
- If you're using this for homebrew, you'll have to do the metadata (_meta) yourself. This script also handles the table of contents for you, but you might want to double check it to make sure it's to your satisfaction.

Example image format:
{
	"type": "image",
	"href": {
		"type": "external",
		"url": "https://i.imgur.com/fBjhiNG.png"
	},
	"title": "Player Handout 1"
},

See the example md file in the linked repository (in the same folder as this script) for formatting guidelines. In particular, note that all forms of extra formatting require spaces:

#### This h4 header is valid
####This h4 header is not.

> ##### Sidebar          >#####Sidebar
> This is valid          >This is not

>> This read aloud text is valid
>>This read aloud text is not

This list:
- ***Is not valid.*** Triple asterisks are reserved for inline headers.

This list:
- **Is valid.** Using double asterisks to bold the text conveys the same meaning and avoids any issues with this script.

##### This table
| Is Valid | A version of line below is necessary |
|----------|--------------------------------------|
| Entry 1  | Description 1       |

##### This table

| Is not   | Note the above line break is not valid, and that the line with dashes is absent. |
| Entry 1  | Description 1       |

Happy converting!
"""

# Line 54 through 62 read the data from the file passed as an argument and convert it to a list of lines to be iterated through

from sys import argv
import json

with open(argv[1], "r") as f:
	text = f.readlines()
	htext = [(x, i.replace("\n","")) for x, i in enumerate(text)]
	text = "\n" + "".join(text)

h1, h2, h3, h4 = [[i.replace("#"*h,"").strip() for x, i in htext if i.startswith("#"*h + " ")] for h in range(1,5)]
h3d = []

data = [{"type": "section", "name": i, "entries":[]} for i in h1]
text = text.split("\n# ")[1:]

# Initializes flags for header nesting and its tracking

z = [0, 0, 0]
h1c, h2c, h3c, h4c = -1, *z

# Initializes flags for each type of special formatting; the "b" stands for "boolean"; h3_h2 is a special flag used when detecting h3 headers that don't have h2 parents

bInset, bRead, bInline1, bInline2, bList, h3_h2, bListInset, bTable, bTable2, bTable3 = [False] * 10

# Initializes structure used for each type of special formatting

inset = {"type": "inset", "name": "", "entries": []}
insetReadAloud = {"type": "insetReadaloud", "entries": []}
inlineHeader = {"type": "entries", "name": "", "entries": []}
unorderedList = {"type": "list", "items": []}
table = {"type": "table", "colLabels": [], "colStyles": [], "rows": []}

# Function used to add various data to the output based on the appropriate nesting structure
# i_switch is kinda weird, it prevents syntax errors so I don't want to touch it; if you get any errors citing line 92 below, mention that i_switch is the problem in the bug report

def add(dtext, i_switch=False):
	global h1c, h2c, h3c, h4c, h3_h2, data
	if h4c > 0:
		if not (i_switch or h3_h2) and not (not i_switch and h2c):
			data[h1c]["entries"][-1]["entries"][-1]["entries"][-1]["entries"].append(dtext)
		else:
			data[h1c]["entries"][-1]["entries"][-1]["entries"].append(dtext)
	elif h3c > 0:
		if not h3_h2:
			data[h1c]["entries"][-1]["entries"][-1]["entries"].append(dtext)
		else:
			data[h1c]["entries"][-1]["entries"].append(dtext)
	elif h2c > 0:
		data[h1c]["entries"][-1]["entries"].append(dtext)
	else:
		data[h1c]["entries"].append(dtext)

# Function used to create inlineHeaders while taking into account the nesting structure

def indent():
	global h1c, h2c, h3c, h4c
	def iter():
		global inlineHeader
		inlineHeader = {"type": "entries", "entries": [inlineHeader]}
	if not [h1c, h2c, h3c, h4c] == [0, 0, 0, 0] and not (h4c and not h3_h2): iter()
	if any([h3c and h3_h2, h2c, h1c]): iter()
	if h1c: iter()

for x, i in htext:
	# Resets a few things back to default + skips to the next line when it detects a blank line
	# As the first line is always going to be a h1 header and is already accounted for on line 65, it can be skipped
	if not x or i == "":
		if bTable:
			add(table)
			table = {"type": "table", "colLabels": [], "colStyles": [], "rows": []}
			bTable = False
		if not x:
			h1c += 1
		if bInline1:
			bInline1 = False
			bInline2 = True
		else:
			continue

	i = i.strip()

	# Formatting for a table - bTable is switched when the table starts and ends, bTable2 is used when there is an optional caption, and bTable3 is used to format the text-align
	if not bTable and (i.startswith("##### ") or i.startswith("|")):
		bTable = True
		bTable3 = True
		if i.startswith("##### "):
			bTable2 = True
			table["caption"] = i[6:].strip()
			continue
		else:
			table["colLabels"] = [t.strip() for t in i.split("|") if t != ""]
			continue
	elif bTable2:
		bTable2 = False
		table["colLabels"] = [t.strip() for t in i.split("|") if t != ""]
		continue
	elif bTable3:
		talign = [t for t in i.split("|") if t != ""]
		for k in talign:
			if (k[0], k[-1]) == (":", ":"):
				table["colStyles"].append("text-align-center")
			elif k[-1] == ":":
				table["colStyles"].append("text-align-right")
			else:
				table["colStyles"].append("text-align-left")
		bTable3 = False
		continue
	
	elif i.startswith("|"):
		table["rows"].append([t.strip() for t in i.split("|") if t.strip() != ""])
		continue		

	# unorderedList - bList is switched when the list starts and ends; for the sake of line space, this is what every bItem variable does unless it has a number on it
	if i.startswith("-"):
		bList = True
		unorderedList["items"].append(i[1:].strip())
		continue

	elif bList:
		add(unorderedList)
		unorderedList = {"type": "list", "items": []}
		bList = False

	# inset - both regular insets and lists within insets (line 181)
	if i.startswith("> ") or i.startswith(">- "):
		if not bInset:
			bInset = True
			inset["name"] = i.replace("#####", "").replace(">", "").strip()
		else:
			if i.startswith(">- "):
				if not bListInset:
					inset["entries"].append({"type": "list", "items": [i.replace(">-", "").strip()]})
					li = len(inset["entries"]) - 1
					bListInset = True
				else:
					inset["entries"][li]["items"].append(i.replace(">-", "").strip())
			else:
				bListInset = False
				inset["entries"].append(i[2:])
		continue
	elif bInset:
		add(inset)
		inset = {"type": "inset", "name": "", "entries": []}
		bInset = False

	# insetReadAloud
	if i.startswith(">> "):
		bRead = True
		insetReadAloud["entries"].append(i.replace(">>", "").strip())
		continue
	elif bRead:
		add(insetReadAloud)
		insetReadAloud = {"type": "insetReadaloud", "entries": []}
		bRead = False

	# inlineHeader - bInline2 is used alongside bInline1 to continue adding paragraphs until a blank line is encountered
	if i.startswith("***"):
		bInline1 = True
		i = i.replace("***", "", 1)
		k = i.index("***") - 1
		inlineHeader["name"] = i[:k]
		inlineHeader["entries"].append(i[k+5:])
		continue

	if bInline1:
		inlineHeader["entries"].append(i)
		continue
	if bInline2:
		indent()
		add(inlineHeader)
		bInline1, bInline2 = False, False
		inlineHeader = {"type": "entries", "name": "", "entries": []}
		continue
	
	# Headers - lines 227 through 252 detect if a line has a header in it, and then adjusts the nesting accordingly
	if i[2:] in h1:
		h1c += 1
		h2c, h3c, h4c = z

	elif i[3:] in h2:
		h2c += 1
		data[h1c]["entries"].append({"type": "section", "name": i[3:], "entries":[]})
		h3c, h4c = z[1:]
		h3_h2 = False

	elif i[4:] in h3:
		h3c += 1
		h4c = 0
		if not h2c:
			h3_h2 = True
			h3d.append(i[4:])
			data[h1c]["entries"].append({"type": "entries", "name": i[4:], "entries": []})
		else:
			data[h1c]["entries"][-1]["entries"].append({"type": "entries", "name": i[4:], "entries": []})

	elif i[5:] in h4:
		if not h2c:
			data[h1c]["entries"][-1]["entries"].append({"type": "entries", "name": i[5:], "entries": []})
		else:
			data[h1c]["entries"][-1]["entries"][-1]["entries"].append({"type": "entries", "name": i[5:], "entries": []})
		h4c += 1
	
	# if it isn't a header and the line is a normal line, it gets add()-ed here
	else: add(i, True)

# Reparses the headers in (x, i) format where x is the htext index and i is the actual header
h1, h2, h3, h4 = [[(x, i.replace("#"*h,"").strip()) for x, i in htext if i.startswith("#"*h + " ")] for h in range(1,5)]

# Creates a list of headers in order for the table of contents
hlist = sorted(h1 + h2 + h3, key=lambda value: value[0])
headers = []

# Adds h1 and h2 headers to the table of contents; if it encounters any h3 headers without an h2 parent (see line 243), those are added too
counter = -1
for x, i in hlist:
	if (x, i) in h1:
		counter += 1
		headers.append({"name": i, "headers": []})
	elif (x, i) in h2 or i in h3d:
		headers[counter]["headers"].append(i)

# Nests all of this data into the proper 5eTools format, with blank strings for you to fill in
data = {
	"adventure": [
		{
			"name": "",
			"id": "",
			"source": "",
			"contents": headers
		}
	],
	"adventureData": [
		{
			"id": "",
			"source": "",
			"data": data
		}
	]
}

# Turns the text into one big string for the purpose of bold and italics tags
data = repr(data)

b = ["{@b ", "}"]
v = 0
while "**" in data:
	data = data.replace("**", b[v], 1)
	v = not v

b[0] = "{@i "
v = 0
while "*" in data:
	data = data.replace("*", b[v], 1)
	v = not v

# Turns the string back into a dict
data = eval("{}".format(data))

# Writes your new file to a 5eTools JSON file
with open("{}.json".format(argv[1][:-3]), "w") as f:
	json.dump(data, f)
