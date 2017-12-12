'''
Solve Sudoku puzzles using Arc-Consistency 3 and Backtracking Search

Joshua Nguyen
Brett Behring
Donovan Prehn
'''
from collections import defaultdict
import math
import itertools
import time
import argparse

#parser.add_argument('--foo', help='foo help')

row = "ABCDEFGHI"
col = "123456789"

class csp:
    	
	def __init__(self, variables, domains, constraints):
		self.variables = variables
		self.domains = domains
		self.constraints = constraints
	
	def solved(self):
		return not any(len(self.domains[var])!=1 for var in self.variables)
	
	def __str__(self):
		output=""
		for i in range(0,9):
			if(i%3==0 and i!=0):
				output+=("- - - + - - - + - - - \n")
			for j in range(0,9):
				var="ABCDEFGHI"[i]+"123456789"[j]
				if(j%3==0 and j!=0):
					output+="| "
				if len(self.domains[var])==1:
					value=self.domains[var].pop()
					output+=str(value) + " "
					self.domains[var].add(value)
				else:
					output+='X '
			output+="\n"
		return(output)

def AC3 (csp, queue=None):
 	
	def arc_reduce(x,y):
		removals=[]
		change=False
		for vx in csp.domains[x].copy():
			found=False

			for vy in csp.domains[y]:
				if diff(vx,vy):
					found=True
			if(not found):
				csp.domains[x].remove(vx)	
				removals.append((x,vx))
				change=True

		return change,removals
	removals=[]
	
	if queue is None:
		queue=[]
		for x in csp.variables:
			queue = queue + [(x, y) for y in csp.constraints[x]]

	while queue:
		x,y= queue.pop()

		b,r=arc_reduce(x,y)
		
		if r:
			removals.extend(r)
		if(b):
    		#not arc consistent
			if(len(csp.domains[x])==0):
				return False, removals
			#if we remove a value, check all neighbours
			else:
				queue = queue + [(x, z) for z in csp.constraints[x] if z!=y]

	return True, removals

def diff(x,y):
	return (x!=y)

def readCSPFromFile(pathToFile):
	#return all binary constraints that contain var 
	
	def constraints(x, listOfNeighbours):
    	# {y : xRy}
		constrain_to = set()
		for pair in listOfNeighbours:
			if x in pair:
				if x==pair[0]:
					constrain_to.add(pair[1])
				elif x==pair[1]:
					constrain_to.add(pair[0])
		return constrain_to

	#read puzzle to 2d list
	with open(pathToFile) as file:
		matrix = [[int(x) if x.isdigit() else 0 for x in line.strip() if x.isdigit() or x=="X"] for line in file if "-" not in line]
	
	neighbours=[]
	for r in "ABCDEFGHI":
		row = [r+c for c in "123456789"]
		neighbours.extend(itertools.combinations(row, 2))

	for c in "123456789":
		col = [r+c for r in "ABCDEFGHI"]
		neighbours.extend(itertools.combinations(col, 2))
	
	for y in range(0,9,3):
		for x in range(0,9,3):
			box=["ABCDEFGHI"[i+y]+"123456789"[x+j] for i in range(0,3) for j in range(0,3)]
			neighbours.extend(itertools.combinations(box, 2))

	# List of strings "A1", "A2",... "I9"
	variables = [x+y for x in "ABCDEFGHI" for y in "123456789"]
	
	# Dictionary {Variable : Domain(Variable)}
	domains={"ABCDEFGHI"[y]+"123456789"[x]:{1,2,3,4,5,6,7,8,9} if matrix[y][x]==0 else {matrix[y][x]} for y in range(0,9) for x in range(0,9)}
	
	constraints = {x:constraints(x, neighbours) for x in variables}
	
	return csp(variables,domains,constraints)

def selectUnassignedVariable(csp,assigned):
	for var in csp.variables:
		if var not in assigned: return var

#no ordering
def OrderDomainValues(csp, assignment, var):
	values = [val for val in csp.domains[var]] 
	return values

def backTrackingSearch(csp): #returns a solution or failure
	return backtrack({},csp)

#todo (mostly pseudo)
def backtrack(assignment, csp): #returns a solution or failure 
	if csp.solved():
		return csp

	var = selectUnassignedVariable(csp, assignment)
	
	for value in OrderDomainValues(csp, assignment, var):
    	
		assignment[var] = value

		removals = [(var, a) for a in csp.domains[var] if a != value]
		
		#Assume Var = Value => D(Var) = Value
		csp.domains[var] = {value}

		consistent, removed = AC3(csp, [(x,var) for x in csp.constraints[var]])

		#if values were removed by AC3, add them to the list to be restored
		if removed:
			removals.extend(removed)
		
		#if AC3 consistent
		if(consistent):
    		
			#continue search
			result = backtrack(assignment,csp)
			
			#if the search didn't fail, return the solution
			if(result!=False):
				return result
		
		#If CSP is not AC3 consistent, restore the values removed by inference
		for variable, value in removals:
			csp.domains[variable].add(value)

	# Unable to find an available solution for this path, step back and choose a different path
	del assignment[var]
	return False

parser = argparse.ArgumentParser(description='Sudoku Solver')
parser.add_argument("file_path")
parser.parse_args()

def main():
	args = parser.parse_args()
	Sudoku = readCSPFromFile(args.file_path)

	print("Initial Puzzle: {}".format(args.file_path))
	print(Sudoku)
	AC3(Sudoku)

	print("Attempting AC-3...")
	
	if(Sudoku.solved()):
		print("Sudoku solved by AC-3 only: ")
		print(Sudoku)
	else:
		print("Sudoku partially solved by AC-3")
		print(Sudoku)
		
		print("Attempting backtrack search...")
		
		t1=time.time()
		solution = backTrackingSearch(Sudoku)
		t2=time.time()
		print("Time elapsed {0:.2f}s".format(t2-t1))
		
		if(solution):
			print("Solution found by Backtrack Search: ")
			print(solution)
		else:
			print("Backtrack Search unable to find a solution.")

if __name__ == "__main__":
	main()