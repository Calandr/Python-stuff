#!/usr/bin/env python.
import xlsxwriter, re, os
import pandas as pd

stats = [
		"Hp",
		"Res",
		"Fat",
		"Matk",
		"Ratk",
		"Mdef",
		"Rdef",
		"Init"]

skip = [
		"character_background.nut",
		"converted_cultist_background.nut",
		"kings_guard_background.nut",
		"legend_enchanter_background.nut",
		"legend_entrancer_background.nut",
		"legend_herbalist_background.nut",
		"legend_runesmith_background.nut",
		"legend_spiritualist_background.nut",
		"mage_background.nut",
		"monk_turned_flagellant_background.nut",
		"pacified_flagellant_background.nut"]

special = {
	"companion_2h_background.nut": "Companion 1h",
	"companion_1h_background.nut": "Companion 2h",
	"companion_ranged_background.nut": "Companion Ranged",
	"legend_berserker_commander_background.nut": "Berserker Commander",
	"legend_crusader_commander_background.nut": "Holy Crusader Commander",
	"legend_beggar_commander_background.nut": "Framed Beggar Commander",
	"legend_assassin_commander_background.nut": "Assassin Commander",
	"legend_ranger_commander_background.nut": "Ranger Commander",
	"legend_beggar_female_commander_background.nut": "Framed Beggar Female",
	"legend_noble_commander_background.nut": "Captain Commander",
	"legend_necro_commander_background.nut": "Necromancer Commander",
	"legend_inventor_commander_background.nut": "Inventor Commander",
	"legend_female_inventor_commander_background.nut": "Inventor Commander Female",
	"legend_beggar_female_commander_background.nut": "Framed Beggar Commander Female",
	"legend_witch_commander_background.nut": "Witch Commander",
	"legend_trader_commander_background.nut": "Trader Commander",
	"legend_vala_commander_background.nut": "Vala Commander"
	}

backgrounds_path = str(os.getcwd()) + "\\mod_legends_beta\\scripts\\skills\\backgrounds"

#simplest class in the world. bunch of variables.
class background:
	hp1 = 0
	hp2 = 0
	res1 = 0
	res2 = 0
	fat1 = 0
	fat2 = 0
	msk1 = 0
	msk2 = 0
	rsk1 = 0
	rsk2 = 0
	md1 = 0
	md2 = 0
	rd1 = 0
	rd2 = 0
	ini1 = 0
	ini2 = 0

	def __init__(self, name):
			self.name = name

#scrape provided file for name and stats
def getStats(bg):
	file = open(backgrounds_path + "\\" + bg, "r")
	text = file.read()
	file.close()
	
	#use hardcoded name for non-unique backgrounds
	#otherwise just use name in the file
	if bg in special:
		bgdata = background(special[bg])
	else:
		pattern = "Name = \"([a-zA-Z ]*)\""
		nameMatch = re.search(pattern, text)
		bgdata = background(nameMatch.group(1))
	
	pattern = "(-?\\d+),\\n\\t*(-?\\d+)\\n\\t*"
	statsMatch = re.findall(pattern, text)
	bgdata.hp1 = statsMatch[0][0]
	bgdata.hp2 = statsMatch[0][1]
	bgdata.res1 = statsMatch[1][0]
	bgdata.res2 = statsMatch[1][1]
	bgdata.fat1 = statsMatch[2][0]
	bgdata.fat2 = statsMatch[2][1]
	bgdata.msk1 = statsMatch[3][0]
	bgdata.msk2 = statsMatch[3][1]
	bgdata.rsk1 = statsMatch[4][0]
	bgdata.rsk2 = statsMatch[4][1]
	bgdata.md1 = statsMatch[5][0]
	bgdata.md2 = statsMatch[5][1]
	bgdata.rd1 = statsMatch[6][0]
	bgdata.rd2 = statsMatch[6][1]
	bgdata.ini1 = statsMatch[7][0]
	bgdata.ini2 = statsMatch[7][1]
	return bgdata

def main():

	files = [f for f in os.listdir(backgrounds_path) if f.endswith(".nut")]
	
	#some backgrounds don't have stats, we skip them
	filterfiles = [x for x in files if x not in skip]
	
	backgrounds = []
	for bg in filterfiles:
		backgrounds.append(getStats(bg))
	
	workbook = xlsxwriter.Workbook("Legend Backgrounds.xlsx")
	worksheet = workbook.add_worksheet("Backgrounds stat modifiers")
	
	col = 0
	
	for i in range(0, 8):
		col +=1
		worksheet.write(0, col, stats[i] + " min")
		col +=1
		worksheet.write(0, col, stats[i] + " max")
	
	row = 0
	
	for b in backgrounds:
		row +=1
		worksheet.write(row, 0, b.name)
		worksheet.write(row, 1, int(b.hp1))
		worksheet.write(row, 2, int(b.hp2))
		worksheet.write(row, 3, int(b.res1))
		worksheet.write(row, 4, int(b.res2))
		worksheet.write(row, 5, int(b.fat1))
		worksheet.write(row, 6, int(b.fat2))
		worksheet.write(row, 7, int(b.msk1))
		worksheet.write(row, 8, int(b.msk2))
		worksheet.write(row, 9, int(b.rsk1))
		worksheet.write(row, 10, int(b.rsk2))
		worksheet.write(row, 11, int(b.md1))
		worksheet.write(row, 12, int(b.md2))
		worksheet.write(row, 13, int(b.rd1))
		worksheet.write(row, 14, int(b.rd2))
		worksheet.write(row, 15, int(b.ini1))
		worksheet.write(row, 16, int(b.ini2))
		
	
	format1 = workbook.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})
	
	format2 = workbook.add_format({'bg_color': '#C6EFCE',
                               'font_color': '#006100'})
							   
	worksheet.freeze_panes(1, 1)
							   
	worksheet.conditional_format('B2:Q124', {'type': 'cell',
											 'criteria': '<',
											 'value': 0,
											 'format': format1})

	worksheet.conditional_format('B2:Q124', {'type': 'cell',
											 'criteria': '>',
											 'value': 0,
											 'format': format2})
		
	workbook.close()
	
if __name__ == '__main__':
    main()