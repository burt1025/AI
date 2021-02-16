import heapq 
import copy
import time
import random

class Hero:
	def __init__(self, id, power, myMastery, oppMatery, member):
		self.id = id
		self.power = power
		self.myMastery = myMastery
		self.oppMatery = oppMatery
		self.myScore = self.power * self.myMastery
		self.oppScore = self.power * self.oppMatery
		self.member = member

	def __str__(self):
		return str(self.id) + ", " + str(self.power) \
		+ ", " + str(self.myMastery) + ", " + str(self.oppMatery) \
		+ ", " + str(self.member)

	def isChosen(self):
		return (self.member != 0)

	def isInMyTeam(self):
		return (self.member == 1)

	def getParty(self):
		return self.member

	def unChoose(self):
		self.member = 0

	def setParty(self, isMyChoice):
		self.member = 1 if isMyChoice else 2

	def getScore(self, isMyChoice):
		return self.myScore if isMyChoice else self.oppScore

class Board:
	def __init__(self, heroList, heroIdMap) :
		self.heroList = heroList
		self.heroIdMap = heroIdMap

		self.pool = []
		self.myStart = []
		self.oppStart = []
		
		self.numMy = 0
		self.numOpp = 0

		self.mySyn = False
		self.oppSyn = False

		self.initialize()

	def initialize(self):
		for hero in self.heroList:
			if hero.isChosen():
				if hero.isInMyTeam():
					self.myStart.append(hero.id)
					self.numMy += 1
				else:
					self.oppStart.append(hero.id)
					self.numOpp += 1
			else:
				self.pool.append(hero.id)

	def getAdvantage(self):
		return self.getMyScore() - self.getOppScore()

	def isGoal(self):
		return self.numOpp == 5 and self.numMy == 5

	def getHeroByID(self, heroid):
		return heroIdMap[heroid]

	def getMyScore(self):
		s = 0
		for i in self.myStart:
			hero = self.heroIdMap[i]
			s += hero.getScore(True)

		if self.mySyn:
			s += 120
		return s

	def getOppScore(self):
		s = 0
		for i in self.oppStart:
			hero = self.heroIdMap[i]
			s += hero.getScore(False)
		if self.oppSyn:
			s += 120
		return s

	def isMyMove(self):
		return (self.numMy == self.numOpp and not self.isGoal())

	def checkSynergy(self, isMyChoice):
		q = self.myStart if isMyChoice else self.oppStart
		l = []
		for i in q:
			r = i % 10
			if r in l:
				return False
			l.append(r)
		return len(l) == 5

	def chooseHero(self, heroid, isMyChoice):
		if heroid in self.pool:
			self.pool.remove(heroid)
		else:
			print("choose hero error: hero not in pool")

		tHero = self.heroIdMap[heroid]

		tHero.setParty(isMyChoice)
		if isMyChoice:
			self.numMy += 1
			self.myStart.append(heroid)
			if self.numMy == 5:
				if self.checkSynergy(isMyChoice):
					self.mySyn = True
		else:
			self.numOpp += 1
			self.oppStart.append(heroid)
			if self.numOpp == 5:
				if self.checkSynergy(isMyChoice):
					self.oppSyn = True

	def unChooseHero(self, heroid, isMyChoice):
		if heroid not in self.pool:
			self.pool.append(heroid)
		else:
			print("unchoose hero error: hero in pool")

		tHero = self.heroIdMap[heroid]
		tHero.unChoose()
		if isMyChoice:
			if self.mySyn:
				self.mySyn = False
			self.numMy -= 1
			del self.myStart[-1]
		else:
			if self.oppSyn:
				self.oppSyn = False
			self.numOpp -= 1
			del self.oppStart[-1]

	def getPool(self):
		return self.pool

	def printHeroList(self):
		for hero in self.heroList:
			print hero

# Minimax
def mm(board, isMyTurn):
	bestVal = float("-inf")
	bestID = 100000
	l = copy.deepcopy(board.getPool())
	for freeHero in l:
		board.chooseHero(freeHero, isMyTurn)
		value = mm_min(board, not isMyTurn)
		board.unChooseHero(freeHero, isMyTurn)
		if bestVal < value:
			bestVal = value
			bestID = freeHero
		elif bestVal == value:
			bestID = min(freeHero, bestID)	
	return (bestVal, bestID)


def mm_max(board, isMyTurn):
	if board.isGoal():
		return board.getAdvantage()
	else:
		max_val = float("-inf")
		l = copy.deepcopy(board.getPool())
		for freeHero in l:
			board.chooseHero(freeHero, isMyTurn)
			value = mm_min(board, not isMyTurn)
			board.unChooseHero(freeHero, isMyTurn)
			max_val = max(max_val, value)
	return max_val

def mm_min(board, isMyTurn):
	if board.isGoal():
		return board.getAdvantage()
	else:
		min_val = float("inf")
		l = copy.deepcopy(board.getPool())
		for freeHero in l:
			board.chooseHero(freeHero, isMyTurn)
			value = mm_max(board, not isMyTurn)
			board.unChooseHero(freeHero, isMyTurn)
			min_val = min(min_val, value)
	return min_val

#Alpha-beta Pruning
def abp(board, isMyTurn):
	bestVal = float("-inf")
	bestID = 100000
	beta = float("inf")
	l = copy.deepcopy(board.getPool())
	for freeHero in l:
		board.chooseHero(freeHero, isMyTurn)
		value = ab_min(board, not isMyTurn, bestVal, beta)
		board.unChooseHero(freeHero, isMyTurn)
		if bestVal < value:
			bestVal = value
			bestID = freeHero
		elif bestVal == value:
			bestID = min(freeHero, bestID)
		if value >= beta:
			return (bestVal, bestID)
	return (bestVal, bestID)

def ab_max(board, isMyTurn, alpha, beta):
	if board.isGoal():
		return board.getAdvantage()
	else:
		max_val = float("-inf")
		l = copy.deepcopy(board.getPool())
		for freeHero in l:
			board.chooseHero(freeHero, isMyTurn)
			value = ab_min(board, not isMyTurn, alpha, beta)
			board.unChooseHero(freeHero, isMyTurn)
			if value > max_val:
				max_val = value
			if value >= beta:
				return value
			alpha = max(alpha, value)
	return max_val

def ab_min(board, isMyTurn, alpha, beta):
	if board.isGoal():
		return board.getAdvantage()
	else:
		min_val = float("inf")
		l = copy.deepcopy(board.getPool())
		for freeHero in l:
			board.chooseHero(freeHero, isMyTurn)
			value = ab_max(board, not isMyTurn, alpha, beta)
			board.unChooseHero(freeHero, isMyTurn)
			if value < min_val:
				min_val = value
			if value <= alpha:
				return value
			beta = min(value, beta)
	return min_val

#Start Timer
start_time = time.time()
#Start File IO
f = open('input.txt', 'r')
fw = open("output.txt", 'w')

n = int(f.readline())
method = f.readline().replace('\n', '')

heroList = []
heroIdMap = {}

line = f.readline()
while line:
	x = line.strip().split(',')
	newhero = Hero(int(x[0]), float(x[1]), float(x[2]), float(x[3]), int(x[4]))
	heroList.append(newhero)
	heroIdMap[int(x[0])] = newhero
	line = f.readline()
f.close()
#End File IO

outcome = 0
newBoard = Board(heroList, heroIdMap)
random.shuffle(heroList)

if (method == "minimax") :
	res, outcome = mm(newBoard, True)
elif (method == "ab") :
	res, outcome = abp(newBoard, True)

#test
fw.write("%d" % outcome)
#Cleaning
fw.close()
print("Output is %d" % outcome)
print("--- %s seconds ---" % (time.time() - start_time))