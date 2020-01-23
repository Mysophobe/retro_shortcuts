#! python3

# RA Shortcut Creator
# Original by lilbud
# Updated by Teoma
# Version 1.0

###########
#	Not fully tested
#	TODO: OS checks to automatically check paths
#	TODO: Fix array list disorder. cores[] games[]
#	TODO: Suffix core to game, for optional emulators with same game
###########

import os, sys, stat
from pprint import pprint

# REPLACE THESE LINES WITH PATHS TO YOUR FOLDERS v
_quest = ""
while _quest not in ('y','n'):
	_quest = eval('input("Use Windows paths? (y/n): ")')

	# Useful if you host games on different OS types, otherwise you can remove the line above and section below you don't need
	if _quest != "y":
		##### *NIX PATHS #####
		_ext = ".sh" # Doesn't matter, unless you're a GUI user
		RABINARY = "retroarch"
		RAFOLDER = r'/mnt/c/Users/teoma/AppData/Roaming/RetroArch'
		ROM_PATH = r'/mnt/d/My Documents/Downloads/Games/ROMS'
	else:
		##### Windows PATHS #####
		_ext = ".bat"
		RABINARY = "retroarch.exe"
		RAFOLDER = r'C:\Users\teoma\AppData\Roaming\RetroArch'
		ROM_PATH = r'D:\My Documents\Downloads\Games\ROMS'
	
CORES_DIR = os.path.join(RAFOLDER, "cores")
RA_LOCATION = os.path.join(RAFOLDER, RABINARY)

# REPLACE THESE LINES WITH PATHS TO YOUR FOLDERS ^

RA = "\"" + RA_LOCATION + "\""
games = []
cores = []

try:
	# List only ROM Files, not directories
	cores = [c for c in os.listdir(CORES_DIR) if os.path.isfile(os.path.join(CORES_DIR, c))]
	# List only Game Files, not directories
	games = [g for g in os.listdir(ROM_PATH) if os.path.isfile(os.path.join(ROM_PATH, g))]
	
	#pprint(locals())
	#exit()
	
except OSError:
	print ("Script could not find either the ROM or Games folder! Are your paths set correctly?")
	exit()
	
# Should be changed to Approved extensions only, as this could get quite extensive.
hiddenext = [".srm", ".sav", ".bat", ".ups", ".bsz", ".txt", ".cht", ".sh"] 
hidden = []

for item in games:
	if item.endswith(tuple(hiddenext)):
		hidden.append(item)
		continue

global romlist

romlist = [i for i in games if i not in hidden]

def corechoice():
	x = 0
	for item in cores:
		x = x + 1
		print(x, "- " + item)

	global new_core_string, finalcorepath

	corechoice = (int(input("Which Core Would You Like to Use?: ")))
	make_string = (str(cores[corechoice - 1:corechoice]))
	new_core_string = make_string.replace("'",'').replace("[","").replace("]", "")
	corepath = os.path.join(CORES_DIR, new_core_string)
	finalcorepath = "\"" + corepath + "\""

def romlisting():
	x = 0
	for item in romlist:
		x = x + 1
		print(x, "- " + item)
	
def romchoice():
	global new_rom_string, finalrompath
	gamechoice = (int(input("Which Game Would You Like to Choose?: ")))
	make_string = (str(romlist[gamechoice - 1:gamechoice]))
	new_rom_string = make_string.replace("'", "").replace("[", "").replace("]", "").replace('"', "")
	rompath = os.path.join(ROM_PATH, new_rom_string)
	finalrompath = " " + "\"" + rompath + "\""

def filewrite():
	_filename = new_rom_string + _ext
	_err = False
	try:
		if not os.path.exists('Game Shortcuts'):
			folderpath = os.makedirs('Game Shortcuts') # could fail
			os.chdir('Game Shortcuts') # won't change if creation fails, DO CHECKS
		with open(_filename, 'w+') as f:
			if os.access(_filename, os.W_OK):
				f.write(RA)
				f.write(" -L ")
				f.write( os.path.normpath( finalcorepath ) )
				f.write( os.path.normpath( finalrompath ) )
				os.chmod(_filename, stat.S_IEXEC) # Make executable (for *nix systems)
			else:
				print ("File may exist for ROM, please delete it")
				exit
			pass
	except IOError as x:
		if x.errno == errno.EACCES:
			print (f, ' Cannot be written to.')
			_err = True
		elif x.errno == errno.EISDIR:
			print ("Script tried to write a Directory, try again")
			_err = True
			
	if _err == True:
		print ("\n++++++\nErrors were encountered, please check the file doesn't exist and re-reun this script\n++++++\n")
		exit
		
def rerun():
	romchoice()
	filewrite()

def check():
	_question = "Would You Like to Make Another Shortcut? (y/n): "
	anotherone = ""
	while anotherone not in ('y','n'):
		anotherone = eval( 'input(_question)' )		
	if anotherone == 'y':
		rerun()
		check()
	else:
		print ("\nGoodbye!\n")
		exit()

def main():
	corechoice()
	romlisting()
	romchoice()
	filewrite()
	check()

main()
