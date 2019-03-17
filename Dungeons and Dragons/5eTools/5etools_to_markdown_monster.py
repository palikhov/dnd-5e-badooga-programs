"""
Made by badooga. https://github.com/badooga/Programs/

This script converts a monster from 5eTools' JSON format to markdown. To use it, pass the md file as an argument in the cmd.

When using this, use the following format for the data you want to convert:

{
	"monster": [
		{
			"name": "monster name",
			"size": "M",
			...
		},
		...
	]
}

At the moment, this script does not handle data such as legendaryGroup data and so on; nor does it parse variant features.

"""
from sys import argv
import json, re, codecs
from math import floor
from fractions import Fraction

# challenge rating: [proficiency bonus, XP]
xp = {"0": 10, "0.125": 25, "0.25": 50, "0.5": 100, "1": 200, "2": 450, "3": 700, "4": 1100, "5": 1800, "6": 2300, "7": 2900, "8": 3900, "9": 5000, "10": 5900, "11": 7200, "12": 8400, "13": 10000, "14": 11500, "15": 13000, "16": 15000, "17": 18000, "18": 20000, "19": 22000, "20": 25000, "21": 33000, "22": 41000, "23": 50000, "24": 62000, "25": 75000, "26": 90000, "27": 105000, "28": 120000, "29": 135000, "30": 155000}
cr = {x: 2 for x in [1/8, 1/4, 1/2, *range(5)]}
for x, i in enumerate(range(5, 30, 4)):
	for y in range(i, min(i + 4, 31)): cr[y] = x + 3
for i in cr:
	cr[i] = [cr[i], xp[str(i)]]

# ability score: ability mod
ability = {x: floor(x/2 - 5) for x in range(1, 31)}

# size[0]: size
size = {i[0]: i for i in "Tiny Small Medium Large Huge Gargantuan".split()}

# alignment[0]: [alignment, order in alignment string]
alignment = {
	"L": ["lawful", 1],
	"N": ["neutral", .5],
	"C": ["chaotic", 1],
	"G": ["good", 0],
	"E": ["evil", 0],
	"U": ["unaligned", .5],
	"A": ["any alignment", .5]
}

#Loads the data as a python dict
with open(argv[1], "r") as f:
	monsters = json.load(f)["monster"]

def trait(m, tr):
	t1 = ["Saving Throws", "Skills", "Damage Vulnerabilties", "Damage Resistances", "Damage Immunities", "Condition Immunities", "Senses", "Languages"]
	t2 = ["save", "skill", "vulnerable", "resist", "immune", "conditionImmune", "senses", "languages"]
	t3 = {x: y for x, y in zip(t1, t2)}
	if t3[tr] in m:
		return "- **{}** ".format(tr)
	else:
		return False

# in general, any variable that is a multiple of "t" is a temp variable that changes often
def monster(m):	
	global alignment, size, ability, cr
	md = []
	md.append("## " + m["name"])
	
	md.append("*" + size[m["size"]] + " ")
	t = m["type"]
	if type(t) == dict and "swarmSize" in t:
		md[-1] += "swarm of " + size[t["swarmSize"]].lower() + " " + t["type"] + "s"
	else:
		if type(t) == dict:
			md[-1] += t["type"] + " (" + ", ".join(t["tags"]) + ")"
		else:
			md[-1] += t
	md[-1] += ", "
	t = m["alignment"]
	specialAlignment = False
	for x, i in enumerate(t):
		if "special" in i: specialAlignment = x
	if not type(specialAlignment) == bool:
		md[-1] += t[specialAlignment]["special"]
	elif not all(type(_) == str for _ in t):
		tt = []
		for i in t:
			tt.append(" ".join(__[0] for __ in sorted([alignment[_] for _ in i["alignment"]], key=lambda y: y[1], reverse=True)) + " (" + str(i["chance"]) + "%)")
		md[-1] += " or ".join(tt)
	elif len(t) > 2:
		if "NX" in t and "NY" in t:
			for i in "LCGE":
				if i not in t: md[-1] += "any non-" + alignment[i][0] + " alignment"
		elif "NX" in t:
			for i in "GE":
				if i in t: md[-1] += "any " + alignment[i][0] + " alignment"
		elif "NY" in t:
			for i in "LC":
				if i in t: md[-1] += "any " + alignment[i][0] + " alignment"
	else:
		md[-1] += " ".join(__[0] for __ in sorted([alignment[_] for _ in t], key=lambda y: y[1], reverse=True))
	md[-1] += "*"

	md.append("___")
	
	md.append("- **Armor Class** ")
	t = m["ac"]
	tt = [type(_) for _ in t]
	if dict in tt:
		iflag = False
		tt = []
		for i in t:
			if type(i) == int:
				tt.append(str(i))
				iflag = True
				continue
			else:
				ttt = str(i["ac"])
				if "braces" in i and i["braces"]:
					ttt = "(" + ttt
			if "from" in i:
				ttt += " (" + ", ".join(i["from"]) + ")"
			if "condition" in i:
				ttt += " " + i["condition"]
				if "condition" in i and "braces" in i and i["braces"]:
					ttt += ")"
			tt.append(ttt)
		md[-1] += ", ".join(tt) if not iflag else " ".join(tt)
	else:
		md[-1] += str(t[0])
	
	md.append("- **Hit Points** " + "{} ({})".format(m["hp"]["average"], m["hp"]["formula"]))
	
	md.append("- **Speed** ")
	tt = []
	ttt = ["walk", "burrow", "climb", "fly", "swim"]
	t = {_: m["speed"][_] for _ in m["speed"] if _ in ttt}

	for i in sorted(t, key=lambda l: ttt.index(l)):
		if type(t[i]) == int:
			if i == "walk": tt.append("{} ft.".format(t[i]))
			else: tt.append("{} {} ft.".format(i, t[i]))
		else:
			tt.append("{} {} ft. {}".format(i, t[i]["number"], t[i]["condition"]))
	md[-1] += ", ".join(tt)
	
	md.append("___")
	md.append("|STR|DEX|CON|INT|WIS|CHA|")
	md.append("|:---:|:---:|:---:|:---:|:---:|:---:|")
	md.append("|".join([""] + ["{} ({:+d})".format(m[a], ability[m[a]]) for a in "str dex con int wis cha".split()] + [""]))
	md.append("___")


	t1 = ["Saving Throws", "Skills", "Damage Vulnerabilties", "Damage Resistances", "Damage Immunities", "Condition Immunities", "Senses", "Languages"]
	t2 = ["save", "skill", "vulnerable", "resist", "immune", "conditionImmune", "senses", "languages"]
	t3 = {x: y for x, y in zip(t1, t2)}

	def trait(tr):
		if t3[tr] in m:
			return "- **{}** ".format(tr)
		else:
			return False

	for i in t1[:2]:
		t = trait(i)
		tt = []
		if t:
			md.append(t)
			for j in m[t3[i]]:
				tt.append("{} {}".format(j.title(), m[t3[i]][j]))
			md[-1] += ", ".join(tt)
	
	for i in t1[2:5]:
		t = trait(i)
		if t:
			md.append(t)
			tt = []
			for j in m[t3[i]]:
				if type(j) == str:
					tt.append(j)
				elif type(j) == dict:
					if "special" not in j:
						if tt == []:
							tt = [", and ".join(j[t3[i]])]
						else:
							tt[-1] += "; " + ", and ".join(j[t3[i]])
						tt[-1] = (j["preNote"] + " " if "preNote" in j else "") + tt[-1].replace(", and ", ", ", tt[-1].count(" and ") - 1) + (" " + j["note"] if "note" in j else "")
					else:
						tt.append(j["special"])
			md[-1] += ", ".join(tt)

	t = trait("Condition Immunities")
	if t: md.append(t + ", ".join(m["conditionImmune"]))
	
	t = trait("Senses")
	if t:
		md.append(t + m["senses"] + ", ")
	else:
		md.append("- **Senses** ")
	md[-1] += "passive Perception " + str(m["passive"])
	
	t = trait("Languages")
	if t: md.append(t + m["languages"])
	
	t = m["cr"]
	u = False
	try:
		if type(t) == str:
			md.append("- **Challenge** {} ({} XP)".format(t, cr[Fraction(t)][1]))
		elif not u and type(t) == dict:
			if "coven" in t:
				md.append("- **Challenge** {} ({} XP) or {} ({} XP) when part of a coven".format(t["cr"], cr[Fraction(t["cr"])][1], t["coven"], cr[Fraction(t["coven"])][1]))
			elif "lair" in t:
				md.append("- **Challenge** {} ({} XP) or {} ({} XP) when encountered in lair".format(t["cr"], cr[Fraction(t["cr"])][1], t["lair"], cr[Fraction(t["lair"])][1]))
	except:
		md.append("- **Challenge** {1} ({0} XP)".format(t, "unknown"))
	
	md.append("___")

	def spellcasting():
		if "spellcasting" not in m: return []
		z = m["spellcasting"]
		slot = {
			"will": "At will: ",
			"1e": "1/day",
			"2e": "2/day",
			"3e": "3/day",
			"0": "Cantrips (at will)",
			"1": "1st level",
			"2": "2nd level",
			"3": "3rd level",
			"4": "4th level",
			"5": "5th level",
			"6": "6th level",
			"7": "7th level",
			"8": "8th level",
			"9": "9th level",
		}
		sp = []
		for t in z:
			spt = []
			spt.append("***{}.*** {}".format(t["name"], "\n>\n>".join(t["headerEntries"])))
			if "will" in t:
				spt.append(slot["will"] + ", ".join(t["will"]))
			if "daily" in t:
				for i in t["daily"]:
					spt.append(slot[i] + [": ", " each: "][len(t["daily"][i]) > 1] + ", ".join(t["daily"][i]))
			if "spells" in t:
				for i in t["spells"]:
					spt.append(slot[i] + "{}: ".format(" ({} slot{})".format(t["spells"][i]["slots"], "s" if t["spells"][i]["slots"] > 1 else "") if "slots" in t["spells"][i] else ""))
					spt[-1] += ", ".join(t["spells"][i]["spells"])
			if "footerEntries" in t:
				spt.append("\n>\n>".join(t["footerEntries"]))
			sp.append("\n>\n>".join(spt + [""]))
		return sp

	def traits():
		if "trait" not in m: return [] 
		t = m["trait"]
		tt = []
		for i in t:
			ttt = []
			for j in i["entries"]:
				if type(j) == dict and j["type"] == "list":
					for k in j["items"]:
						if type(k) == str:
							ttt.append("- " + k)
						elif type(k) == dict and "entry" in k:
							if "name" in k:
								ttt.append("- ***{}*** ".format(k["name"]) + k["entry"])
							else:
								ttt.append("- " + k["entry"])
				elif type(j) == str:
					ttt.append(j)
			tt.append("***{}.*** ".format(i["name"]) + "\n>\n>".join(ttt))
		return tt

	md.append("\n>\n>".join(sorted(traits() + spellcasting(), key=lambda z: z[3:])))

	if "action" in m:
		md.append("")
		md.append("### Actions")
		t = m["action"]
		for i in t:
			tt = []
			for j in i["entries"]:
				if type(j) == dict and j["type"] == "list":
					for k in j:
						if type(k) == str: tt.append("- " + k)
						elif type(k) == dict and "entry" in k: tt.append("- " + k["entry"])
				elif type(j) == str:
					tt.append(j)
			md.append("***{}.*** ".format(i["name"]) + "\n>\n>".join(tt))
			md.append("")
	
	if "reaction" in m:
		md.append("")
		md.append("### Reactions")
		t = m["reaction"]
		tt = []
		for i in t:
			md.append("***{}.*** ".format(i["name"]) + "\n>\n>".join(i["entries"]))
			md.append("")
	
	if "legendary" in m:
		md.append("")
		md.append("### Legendary Actions")
		t = m["legendary"]
		tt = []
		ttt = m["name"]
		if not ("isNamedCreature" in m and m["isNamedCreature"]):
			ttt = "The " + ttt.lower()
		la = 3
		if "legendaryActions" in m:
			la = m["legendaryActions"]
		if "legendaryHeader" not in m:
			md.append("{0} can take {1} legendary actions, choosing from the options below. Only one legendary action can be used at a time and only at the end of another creature's turn. {0} regains spent legendary actions at the start of its turn.".format(ttt, la))
		else:
			md += m["legendaryHeader"]
		for i in t:
			md.append("- **{}.** ".format(i["name"]) + "\n>".join(i["entries"]))

	md = ["___"] + [">" + _ for _ in md] + [""]
	
	# disabled
	if "variant" in m and False:
		t = m["variant"]
		tt = []
		for z in t:
			tt = ["##### " + z["name"]]
			for i in z["entries"]:
				if type(i) == str: tt.append(i)
				elif type(i) == dict:
					if i["type"] == "list":
						print(tt)
						tt += ["- " + x for x in i["items"]]
					elif i["type"] in ["variantSub", "entries"]:
						if "name" in i:
							ttt[0] = "***{}.*** ".format(i["name"]) + ttt[0]
						for j in i["entries"]:
							if type(j) == str: ttt.append(j)
							elif type(j) == dict:
								if j["type"] in ["variantSub", "entries"]:
									tttt = j["entries"]
									if "name" in i:
										tttt[0] = "***{}.*** ".format(j["name"]) + tttt[0]
									ttt += tttt
						tt += ttt
			md.append("\n>\n".join([">" + _ for _ in tt] + [""]))
			

	# Tags: replace spells with italics, attack tags with appropriate data, etc
	static = {
		"{@atk mw}": "*Melee Weapon Attack:*",
		"{@atk rw}": "*Ranged Weapon Attack:*",
		"{@atk rs}": "*Ranged Spell Attack:*",
		"{@atk ms}": "*Melee Spell Attack:*",
		"{@atk mw,rw}": "*Melee or Ranged Weapon Attack:* ",
		"{@atk ms,rs}": "*Melee or Ranged Spell Attack:* ",
	}

	# credit to zhu.exe for making this
	PARSING = {'hit': lambda e: f"{int(e):+}",
		'filter': lambda e: e.split('|')[0],
		'link': lambda e: f"[{e.split('|')[0]}]({e.split('|')[1]})",
		'adventure': lambda e: e.split('|')[0],
		'recharge': lambda e: f"(Recharge {e}-6)" if e else "(Recharge 6)",
		'chance': lambda e: e.split('|')[1] if len(e.split('|')) > 1 else f"{e.split('|')[0]}%",
		'scaledice': lambda e: e.split('|')[-1],
		'book': lambda e: e.split('|')[0],
		'h': lambda e: "*Hit:* ",
		'dice': lambda e: e.split('|')[-1]}

	FORMATTING = {'bold': '**', 'italic': '*', 'b': '**', 'i': '*'}

	ABILITY_MAP = {'str': 'Strength', 'dex': 'Dexterity', 'con': 'Constitution', 'int': 'Intelligence', 'wis': 'Wisdom', 'cha': 'Charisma'}

	DEFAULT = ['condition', 'skill', 'action', 'creature', 'damage', 'race', 'background', '5etools', 'class', 'table', 'sense']

	# credit to zhu.exe for making this
	def render(text, md_breaks=False, join_char='\n'):
		"""Parses a list or string from JSON data.
		:returns str - The final text."""
		if isinstance(text, dict):
			text = [text]
		if not isinstance(text, list):
			return parse_data_formatting(str(text))

		out = []
		join_str = f'{join_char}' if not md_breaks else f'  {join_char}'

		for entry in text:
			if not isinstance(entry, dict):
				out.append(str(entry))
			elif isinstance(entry, dict):
				if 'type' not in entry and 'title' in entry:
					out.append(f"**{entry['title']}**: {render(entry['text'])}")
				elif 'type' not in entry and 'istable' in entry:  # only for races
					temp = f"**{entry['caption']}**\n" if 'caption' in entry else ''
					temp += ' - '.join(f"**{parse_data_formatting(cl)}**" for cl in entry['thead']) + '\n'
					for row in entry['tbody']:
						temp += ' - '.join(f"{parse_data_formatting(col)}" for col in row) + '\n'
					out.append(temp.strip())
				elif 'type' not in entry or entry['type'] in ('entries', 'inset'):
					out.append((f"**{entry['name']}**: " if 'name' in entry else '') + render(
						entry['entries']))  # oh gods here we goooooooo
				elif entry['type'] == 'options':
					pass  # parsed separately in classfeat
				elif entry['type'] == 'list':
					out.append('\n'.join(f"- {render(t)}" for t in entry['items']))
				elif entry['type'] == 'table':
					temp = f"**{entry['caption']}**\n" if 'caption' in entry else ''
					temp += ' - '.join(f"**{parse_data_formatting(cl)}**" for cl in entry['colLabels']) + '\n'
					for row in entry['rows']:
						temp += ' - '.join(f"{render(col)}" for col in row) + '\n'
					out.append(temp.strip())
				elif entry['type'] == 'invocation':
					pass  # this is only found in options
				elif entry['type'] == 'abilityAttackMod':
					out.append(f"`{entry['name']} Attack Bonus = "
							f"{' or '.join(ABILITY_MAP.get(a) for a in entry['attributes'])}"
							f" modifier + Proficiency Bonus`")
				elif entry['type'] == 'abilityDc':
					out.append(f"`{entry['name']} Save DC = 8 + "
							f"{' or '.join(ABILITY_MAP.get(a) for a in entry['attributes'])}"
							f" modifier + Proficiency Bonus`")
				elif entry['type'] == 'bonus':
					out.append("{:+}".format(entry['value']))
				elif entry['type'] == 'dice':
					out.append(f"{entry['number']}d{entry['faces']}")
				elif entry['type'] == 'bonusSpeed':
					out.append(f"{entry['value']} feet")
				elif entry['type'] == 'actions':
					out.append((f"**{entry['name']}**: " if 'name' in entry else '') + render(entry['entries']))
				elif entry['type'] == 'item':
					out.append(f"*{entry['name']}* {render(entry['entry'])}")
				elif entry['type'] == 'cell':
					if 'entry' in entry:
						out.append(render(entry['entry']))
					else:
						if 'exact' in entry['roll']:
							out.append(str(entry['roll']['exact']))
						else:
							out.append(f"{str(entry['roll']['min'])} - {str(entry['roll']['max'])}")

		return parse_data_formatting(join_str.join(out))

	# credit to zhu.exe for making this
	def SRC_FORMAT(e, italics=False):
		"""Extracts text from {@format text|source|text_alias} string."""
		t = e.split('|')[0] if len(e.split('|')) < 3 else e.split('|')[2]
		if italics: t = "*" + t + "*"
		return t

	# credit to zhu.exe for making this
	def parse_data_formatting(text):
		"""Parses a {@format } string."""
		exp = re.compile(r'{@(\w+)(?: ([^{}]+?))?}')

		def sub(match):
			if match.group(1) in ["spell", "item"]:
				out = SRC_FORMAT(match.group(2), True)
			elif match.group(1) in DEFAULT:
				out = SRC_FORMAT(match.group(2))
			elif match.group(1) in PARSING:
				f = PARSING.get(match.group(1), lambda e: e)
				out = f(match.group(2))
			else:
				f = FORMATTING.get(match.group(1), '')
				out = f"{f}{match.group(2)}{f}"
			return out

		while exp.search(text):
			text = exp.sub(sub, text)
		return text
	
	# credit to zhu.exe for making this
	def recursive_tag(value):
		"""
		Recursively renders all tags.
		:param value: The object to render tags from.
		:return: The object, with all tags rendered.
		"""
		if isinstance(value, str):
			return render(value)
		if isinstance(value, list):
			return [recursive_tag(i) for i in value]
		if isinstance(value, dict):
			for k, v in value.items():
				value[k] = recursive_tag(v)
		return value
	
	for x, i in enumerate(md):
		for j in static:
			i = i.replace(j, static[j])
		i = recursive_tag(i)
		md[x] = i
	
	return [x + "\n" for x in md]

# Writes the output to a markdown file
with codecs.open("{}.md".format(argv[1][:-5]), "w", encoding="utf-8") as f:
	for i in monsters:
		f.writelines(monster(i))