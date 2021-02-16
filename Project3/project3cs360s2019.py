## Name: Buting Xu
## Email: butingxu@usc.edu
## Notes:
## No rounding used in utility
## Destination stays constant in value iteration
## Obstacles are counted as valid steps in value iteration
## Obstacles are not terminals while Destination is


import heapq 
import copy
import time
import random
from enum import Enum

class Action(Enum): 
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Map:
	def __init__(self, grid_size, obs_list, dest, gamma = 0.9):
		
		self.size = grid_size
		self.obs_list = obs_list
		self.dest = dest
		self.gamma = gamma
		self.states = set();
		self.reward = {}
		self.actionList = []
		self.initialize()

	def initialize(self):
		self.actionList = [e.value for e in Action]
		## initialize empty grid
		grid = []
		for  i in range (self.size):
			row = []
			for j in range(self.size):
				row.append(-1)
			grid.append(row) 

		## place in obstacle and dest
		for obs in obs_list:
			grid[obs[0]][obs[1]] = -101
		grid[dest[0]][dest[1]] = 99

		for x in range(self.size):
			for y in range(self.size):
				self.reward[x, y] = grid[x][y]
				if grid[x][y] is not 99:
					self.states.add((x, y))

	def GetReward(self, pos):
		return self.reward[pos]

	def GetTransition(self, state, action):
		result = []
		if action == None:
			result.append((0.0, state))
		else:
			result.append((0.7, self.Move(state, action)))
			for a in self.GetOtherDirection(action):
				p = 0.1
				result.append((p, self.Move(state, a)))
		return result

	def Move(self, state, direction):
		newState = StateMove(state, direction)
		return newState if ((newState in self.states) or (self.isDest(newState))) else state

	def GetActions(self, state):
		if self.isDest(state):
			return [None]
		else:
			return self.actionList

	def isDest(self, state):
		return state[0] == self.dest[0] and state[1] == self.dest[1]

	def GetOtherDirection(self, direction):
		result = []
		for a in self.actionList:
			if direction[0] != a[0] or direction[1] != a[1]:
				result.append(a)
		return result


	## chagne policy to grid view
	def ToGrid(self, policy):
		charmap = {(1, 0):'>', (0, 1):'v', (-1, 0):'<', (0, -1):'^', None: '.'}
		newcol = []
		for i in range(self.size):
			newrow = []
			for j in range(self.size):
				if (i, j) in obs_list:
					newrow.append("o")
				else:
					newrow.append(charmap[policy[(i, j)]])
			newcol.append(newrow)
		return newcol
	
	## Helper functions to print array and set

	def printArray(self, array):
		p = ""
		for i in range(self.size):
			for j in range(self.size):
				p += array[j][i]
			if i != self.size -1:
				p += "\n"
		return p

	def printSet(self, s):
		p = ""
		for i in range(self.size):
			for j in range(self.size):
				amount = str(round(s[(j, i)], 4))
				p += amount + "    "
			if i != self.size -1:
				p += "\n"
		return p

def value_iteration(mdp, epsilon=0.1):
    U1 = dict([(s, 0) for s in mdp.states])
    U1[mdp.dest] = 99
    reward, trans, gamma = mdp.GetReward, mdp.GetTransition, mdp.gamma
    while True:
        U = U1.copy()
        delta = 0
        for s in mdp.states:
            U1[s] = reward(s) + gamma * max([sum([p * U[s1] for (p, s1) in trans(s, a)])
                                        for a in mdp.GetActions(s)])
            delta = max(delta, abs(U1[s] - U[s]))
        if delta < epsilon * (1 - gamma) / gamma:
             return U

def ProducePolicy(mdp, U):
    result = {}
    for s in mdp.states:
    	maximum = -float("inf")
    	choice = None
    	for a in mdp.GetActions(s):
    		eu = expected_utility(a, s, U, mdp)
    		if eu >= maximum:
    			maximum = eu
    			choice = a
        result[s] = choice
    result[mdp.dest] = None
    return result
 
def expected_utility(a, s, U, mdp):
    return sum([p * U[s1] for (p, s1) in mdp.GetTransition(s, a)])

## Helper function to read grid position

def readPos(f):
	line = f.readline()
	x = line.strip().split(',')
	return (int(x[0]), int(x[1]))
## Helper function to calculate movement

def StateMove(state, direction):
	return (state[0] + direction[0], state[1] + direction[1])



#Start Timer
start_time = time.time()
#Start File IO
f = open('input.txt', 'r')
fw = open("output.txt", 'w')

grid_size = int(f.readline())
num_obs = int(f.readline())

obs_list = []

for i in range(num_obs):
	pos = readPos(f)
	obs_list.append(pos)

dest = readPos(f)

testMap = Map(grid_size, obs_list, dest)


U = value_iteration(testMap)
mapping = ProducePolicy(testMap, U)
smap = testMap.ToGrid(mapping)
# print(testMap.printSet(U))
outcome = testMap.printArray(smap)

#test
fw.write("%s" % outcome)
#Cleaning
fw.close()
print("--- %s seconds ---" % (time.time() - start_time))