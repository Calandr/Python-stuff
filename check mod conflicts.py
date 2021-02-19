#!/usr/bin/env python.
import io, os, sys
from zipfile import ZipFile

class mod:
	def __init__(self, zip, file):
		self.zip = zip
		self.file = file
	
	def __str__(self):
		return "File: \"" + self.file + "\" of mod \"" + self.zip + "\""
		
class conflict:
	def __init__(self, file, problems):
		self.file = file
		self.problems = problems
	
	def addConflict(self, problem):
		self.problems.append(problem)
		
	def __str__(self):
		line = "File: \"" + self.file + "\" is conflicting in these mods:\n"
		for problem in self.problems:
			line+="    Mod: \"" + str(problem) + "\"\n"
		return line
		

def main():

	newstdout = io.StringIO()
	sys.stdout = newstdout
	mods = []

	for item in os.listdir(os.getcwd()):
		if item.endswith(".zip"):
			with ZipFile(item, 'r') as zip:
				zip.printdir()
			
			output = newstdout.getvalue().split("\n")
			sys.stdout = sys.__stdout__


			for line in output:
				if "." in line and ".cnut" not in line and ".css" not in line:
					mods.append(mod(item.split(".", 1)[0], line.split(".", 1)[0]))
					
		sys.stdout.flush()
		newstdout = io.StringIO()
		sys.stdout = newstdout

	sys.stdout = sys.__stdout__
	seen = {}
	confs = []
		
	for item in mods:
		if item.file not in seen:
			seen[item.file] = 1
		else:
			if seen[item.file] == 1:
				confs.append(conflict(item.file, [item.zip]))
			seen[item.file] += 1

	for item in seen:
		if seen[item] > 1:
			for thing in mods:
				if thing.file == item:
					for conflicts in confs:
						if conflicts.file == item and thing.zip not in conflicts.problems:
							conflicts.addConflict(thing.zip)

	for problem in confs:
		print(problem)
	
	print("Finished with " + str(len(confs)) + " conflicts!")
	
if __name__ == '__main__':
    main()
