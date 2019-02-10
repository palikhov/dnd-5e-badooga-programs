"""
Made by badooga. Converts an adventure or book from markdown form to 5eTools.
To use this script, pass the md file as an argument in the cmd.

This script does not automatically input metadata, tables, or images, nor does it automatically content like monsters and spells to 5eTools:
- For tables, make them manually in markdown, and then use the 5eTools Text Converter to turn it into JSON. Paste this table into the main adventure/book once you are done.
- For monsters, use CritterDB to transcribe a monster and to export it to Homebrewery/Markdown (you can transcribe it manually, but CritterDB speeds that up). Then use the 5eTools Text Converter to turn it into JSON, and include the monster in the adventure as normal.
- For images, use the JSON format below and paste it into the main adventure/book.
- You'll have to do the metadata yourself. However, this script handles the table of contents for you.

{
	"type": "image",
	"href": {
		"type": "external",
		"url": "https://i.imgur.com/fBjhiNG.png"
	},
	"title": "Player Handout 1"
},

See the example md file for formatting guidelines. In particular, note that all forms of extra formatting require spaces:

#### This h4 header is valid
####This h4 header is not.

> ##### Sidebar          >#####Sidebar
> This is valid          >This is not

>> This read aloud text is valid
>>This read aloud text is not

Happy converting! And also, please don't try to decipher this garbage. I already lost my parents to it.
"""

from sys import argv
import json

with open(argv[1], "r") as f:
	text = f.readlines()
	htext = [(x, i.replace("\n","")) for x, i in enumerate(text)]
	text = "\n" + "".join(text)

h1, h2, h3, h4 = [[i.replace("#"*h,"").strip() for x, i in htext if i.startswith("#"*h + " ")] for h in range(1,5)]

data = [{"type": "section", "name": i, "entries":[]} for i in h1]
text = text.split("\n# ")[1:]

z = [0, 0, 0]
h1c, h2c, h3c, h4c = -1, *z

bInset, bRead, bInline1, bInline2, bList, h3_h2, bListInset = False, False, False, False, False, False, False

inset = {"type": "inset", "name": "", "entries": []}
insetReadAloud = {"type": "insetReadaloud", "entries": []}
inlineHeader = {"type": "entries", "name": "", "entries": []}
unorderedList = {"type": "list", "items": []}

for x, i in htext:
	if not x or i == "":
		if not x:
			h1c += 1
		if bInline1:
			bInline1 = False
			bInline2 = True
		else:
			continue
	
	if type(i) == str and i.startswith("> ") or i.startswith(">- "):
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
		if h4c > 0:
			data[h1c]["entries"][-1]["entries"][-1]["entries"][-1]["entries"].append(inset)
		elif h3c > 0:
			data[h1c]["entries"][-1]["entries"][-1]["entries"].append(inset)
		elif h2c > 0:
			data[h1c]["entries"][-1]["entries"].append(inset)
		else:
			data[h1c]["entries"].append(inset)
		inset = {"type": "inset", "name": "", "entries": []}
		bInset = False

	if type(i) == str and i.startswith(">> "):
		bRead = True
		insetReadAloud["entries"].append(i.replace(">>", "").strip())
		continue
	elif bRead:
		if h4c > 0:
			data[h1c]["entries"][-1]["entries"][-1]["entries"][-1]["entries"].append(insetReadAloud)
		elif h3c > 0:
			data[h1c]["entries"][-1]["entries"][-1]["entries"].append(insetReadAloud)
		elif h2c > 0:
			data[h1c]["entries"][-1]["entries"].append(insetReadAloud)
		else:
			data[h1c]["entries"].append(insetReadAloud)
		insetReadAloud = {"type": "insetReadaloud", "entries": []}
		bRead = False

	if type(i) == str and i.startswith("***"):
		bInline1 = True
		i = i.replace("***", "", 1)
		k = i.index("***") - 1
		inlineHeader["name"] = i[:k]
		inlineHeader["entries"].append(i[k+5:])
		continue

	if bInline1:
		inlineHeader["entries"].append(i)
	if bInline2:
		if h4c > 0:
			pass
		elif h3c > 0:
			inlineHeader ={"type": "entries", "entries": [inlineHeader]}
		elif h2c > 0:
			inlineHeader ={"type": "entries", "entries": [inlineHeader]}
			inlineHeader ={"type": "entries", "entries": [inlineHeader]}
		elif h1c > 0:
			inlineHeader ={"type": "entries", "entries": [inlineHeader]}
			inlineHeader ={"type": "entries", "entries": [inlineHeader]}
			inlineHeader ={"type": "entries", "entries": [inlineHeader]}
		i = inlineHeader
		bInline1, bInline2 = False, False
		inlineHeader = {"type": "entries", "name": "", "entries": []}
	
	
	if type(i) == str and i.startswith("-"):
		bList = True
		unorderedList["items"].append(i[1:].strip())
		continue
	elif bList:
		if h4c > 0:
			data[h1c]["entries"][-1]["entries"][-1]["entries"][-1]["entries"].append(unorderedList)
		elif h3c > 0:
			data[h1c]["entries"][-1]["entries"][-1]["entries"].append(unorderedList)
		elif h2c > 0:
			data[h1c]["entries"][-1]["entries"].append(unorderedList)
		else:
			data[h1c]["entries"].append(unorderedList)
		unorderedList = {"type": "list", "items": []}
		bList = False
		
	if type(i) == str and i[2:] in h1:
		h1c += 1
		h2c, h3c, h4c = z

	elif type(i) == str and i[3:] in h2:
		h2c += 1
		data[h1c]["entries"].append({"type": "section", "name": i[3:], "entries":[]})
		h3c, h4c = z[1:]
		h3_h2 = False

	elif type(i) == str and i[4:] in h3:
		h3c += 1
		h4c = 0
		if not h2c and not h3_h2:
			h3_h2 = True
			data[h1c]["entries"].append({"type": "entries", "entries":[]})
		data[h1c]["entries"][-1]["entries"].append({"type": "entries", "name": i[4:], "entries": []})

	elif type(i) == str and i[5:] in h4:
		data[h1c]["entries"][-1]["entries"][-1]["entries"].append({"type": "entries", "name": i[5:], "entries": []})
		h4c += 1
	

	else:
		if h4c > 0:
			data[h1c]["entries"][-1]["entries"][-1]["entries"][-1]["entries"].append(i)
		elif h3c > 0:
			data[h1c]["entries"][-1]["entries"][-1]["entries"].append(i)
		elif h2c > 0:
			data[h1c]["entries"][-1]["entries"].append(i)
		else:
			data[h1c]["entries"].append(i)

h1, h2, h3, h4 = [[(x, i.replace("#"*h,"").strip()) for x, i in htext if i.startswith("#"*h + " ")] for h in range(1,5)]

hlist = sorted(h1 + h2, key=lambda z: z[0])
headers = []
counter = -1
for x, i in hlist:
	if (x, i) in h1:
		counter += 1
		headers.append({"name": i, "headers": []})
	else:
		headers[counter]["headers"].append(i)

hlist = sorted(h1 + h3, key=lambda z: z[0])
counter = -1
bNoH2 = False
for x, i in hlist:
	if (x, i) in h1:
		counter += 1
		bNoH2 = headers[counter]["headers"] == []
	elif bNoH2:
		headers[counter]["headers"].append(i)

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

data = repr(data)

b = ["{@b ", "}"]
v = 0
while "**" in data:
	data = data.replace("**", b[v], 1)
	v = not v

b = ["{@i ", "}"]
v = 0
while "*" in data:
	data = data.replace("*", b[v], 1)
	v = not v

data = eval("{}".format(data))

with open("{}.json".format(argv[1][:-3]), "w") as f:
	json.dump(data, f)
