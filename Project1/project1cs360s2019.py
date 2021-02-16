import heapq 
import copy
import time
import random

class Board:
	def __init__(self, width, nCamera, nTiger, tCordList, tCordCountMap):
		self.width = width
		self.nCamera = nCamera
		self.nTiger = nTiger
		self.tCordList = tCordList
		self.currCordList = list(tCordList)
		self.tCordCountMap = tCordCountMap
		self.count = 0
		self.placedCord = []
		self.tigerCount = 0

		self.cordPoint = {}

		for i in range(width) :
			for j in range(width):
				newCord = (i, j)
				self.cordPoint[newCord] = 0

	def resetBoard(self):
		self.currCordList = list(self.tCordList)
		self.count = 0
		self.placedCord = []
		self.tigerCount = 0
		self.cordPoint = {}
		for i in range(self.width) :
			for j in range(self.width):
				newCord = (i, j)
				self.cordPoint[newCord] = 0

	def printState(self):
		print ("Current Count is %d\n" % self.tigerCount)
		print placedCord
		print "\n"

	def printBasic(self):
		print("Width is %d, has %d camera, has %d tiger"%(self.width, self.nCamera, self.nTiger))
		print self.count
		print "\n"

	def isGoal(self):
		if self.count == self.nCamera:
			return True
		else:
			return False

	def getScoreByCord(self, cord):
		if cord in self.tCordCountMap:
			return self.tCordCountMap[cord]
		else:
			return 0

	def place(self, row, column):
		newCord = (row, column)
		self.placedCord.append(newCord)
		self.count += 1
		self.changePoint(row, column, 1)
		self.tigerCount += self.getScoreByCord(newCord)
		self.ruleOutTiger(row, column, True)

	def unPlace(self, row, column):
		newCord = (row, column)
		self.placedCord.remove(newCord)
		self.count -= 1
		self.changePoint(row, column, -1)
		self.tigerCount -= self.getScoreByCord(newCord)
		self.ruleOutTiger(row, column, False)

	def freeCellPoints(self):
		s = 0
		for i in range(self.width):
			for j in range(self.width):
				if self.cordPoint[(i, j)] == 0:
					s += 1;
		return s

	def changePoint(self, row, column, num):
		for i in range(self.width) :
			self.cordPoint[(i, column)] += num
			self.cordPoint[(row, i)] += num
			if i > 0:
				if row + i < self.width and column + i < self.width:
					self.cordPoint[(row + i, column + i)] += num
				if row - i >= 0 and column - i >= 0:
					self.cordPoint[(row - i, column - i)] += num
				if (row - i >= 0 and column + i < self.width):
					self.cordPoint[(row - i, column + i)] += num
				if (row + i < self.width and column - i >= 0):
					self.cordPoint[(row + i, column - i)] += num

	def removeFromCurrCordList(self, row, column, remove):
		if remove == True:
			if (row, column) in self.currCordList:
				self.currCordList.remove((row, column))
		else:
			if (row, column) not in self.currCordList:
				self.currCordList.append((row, column))

	def ruleOutTiger(self, row, column, remove):
		for i in range(self.width) :
			self.removeFromCurrCordList(i, column, remove)
			self.removeFromCurrCordList(row, i, remove)
			if i > 0:
				if row + i < self.width and column + i < self.width:
					self.removeFromCurrCordList(row + i, column + i, remove)
				if row - i >= 0 and column - i >= 0:
					self.removeFromCurrCordList(row - i, column - i, remove)
				if (row - i >= 0 and column + i < self.width):
					self.removeFromCurrCordList(row - i, column + i, remove)
				if (row + i < self.width and column - i >= 0):
					self.removeFromCurrCordList(row + i, column - i, remove)

	def printPoint(self):
		for i in range(self.width):
			l = []
			for j in range(self.width):
				l.append(self.cordPoint[(i,j)])
			print l

	def rowSafe(self, i):
		if not self.placedCord:
			return True
		for cord in self.placedCord:
			if cord[0] == i:
				return False
		return True

	def spotSafe(self, row, column):
		newCord = (row, column)
		if self.cordPoint[newCord] == 0:
			return True
		else:
			return False

	def bestInRow(self, row):
		b = 0
		for i in range(self.width):
			if (row, i) in self.currCordList:
				num = self.tCordCountMap[(row, i)]
				if b <= num :
					b = num 
		return b

	# After current row
	def bestInRest(self, row):
		l = []
		cameraLeft = self.nCamera - self.count
		while row < self.width:
			l.append(self.bestInRow(row))
			row += 1 
		l.sort(reverse=True)
		s = 0
		if len(l) > cameraLeft:
			for i in range(cameraLeft):
				s += l[i]
		else:
			s = sum(l)
		# print "Camera Left: " + str(cameraLeft)
		return s

class StarNode:
	def __init__(self, board, currentRow):
		self.board = board
		self.currentRow = currentRow
		self.currentScore = 0
		self.expectedScore = self.board.bestInRest(currentRow)
		self.lastPlaced = -1
		self.count = 0
		self.placedCord = []
		

	def placePlaced(self):
		for cord in self.placedCord:
			self.board.place(cord[0], cord[1])

	def place(self, column):
		# print (self.currentRow, column)
		self.placePlaced()
		if not self.board.spotSafe(self.currentRow, column):
			self.board.resetBoard()
			return False

		self.placedCord.append((self.currentRow, column))
		self.count += 1

		self.board.place(self.currentRow, column)
		self.currentScore += self.board.getScoreByCord((self.currentRow, column))
		self.lastPlaced = column
		if (self.currentRow + 1 < self.board.width):
			self.expectedScore = self.board.bestInRest(self.currentRow + 1) 
		else:
			self.expectedScore = 0
		self.board.resetBoard()
		return True

	def isGoal(self):
		return self.count == self.board.nCamera

	def getTotalS(self):
		return self.currentScore + self.expectedScore

	def childNode(self, column):

		node = StarNode(self.board, self.currentRow + 1)
		node.currentScore = self.currentScore
		node.lastPlaced = self.lastPlaced
		node.placedCord = list(self.placedCord)
		node.count = self.count

		if column == self.board.width:
			return node
		if node.place(column):
			return node
		else:
			return None

	def checkExceed(self):
		return self.board.nCamera - self.count > self.board.width - 1 - self.currentRow

	def getLastPlaced(self):
		return (self.currentRow, self.lastPlaced)

def AStar(board):
	priorQ = []
	for i in range(board.width + 1):
		node = StarNode(board, 0)
		if i < board.width:
			node.place(i)
		heapq.heappush(priorQ, (-node.getTotalS(), node))
	while priorQ is not None:

		negScore, node = heapq.heappop(priorQ)

		# print node.getLastPlaced()
		# print "Current score " + str(-negScore)
		if node.isGoal():
			node.board.resetBoard()
			node.placePlaced()
			return node.board

		if node.checkExceed():
			continue

		for i in range(board.width + 1):
			newNode = node.childNode(i)
			if newNode != None:
				heapq.heappush(priorQ, (-newNode.getTotalS(), newNode))

	return board

def DFSBasic(board):
	if (board.isGoal()):
		return board
	else:
		for i in range (board.width):
			if board.rowSafe(i):
				for j in range (board.width):
					if (board.spotSafe(i, j)):
						#print ("Detected safe at %d, %d" % (i, j))
						board.place(i, j)
						res = DFSBasic(board)
						if res != None:
							return res
						else:
							board.unPlace(i, j)
		return None

def DFS(board):
	if board.isGoal():
		# print "Goal reached"
		return board
	
	hasEmpty = False
	maxPlaced = Board(board.width, board.nCamera, board.nTiger, board.tCordList, board.tCordCountMap)


	for i in range (board.nTiger):

		newBoard = copy.deepcopy(board)
		if len(newBoard.placedCord)==0:
			print "First round : %d" % i
		newCord = newBoard.tCordList[i]
		if newCord in newBoard.placedCord:
			continue
		if newBoard.spotSafe(newCord[0], newCord[1]):
			# print ("Detected safe at %d" % i)
			# print newCord
			
			newBoard.place(newCord[0], newCord[1])
			res = DFS(newBoard)
			if res != None:
				if res.tigerCount > maxPlaced.tigerCount:
					hasEmpty = True
					maxPlaced = res
	if hasEmpty == False:
		# print board.placedCord
		return DFSBasic(board)
	return maxPlaced










start_time = time.time()

f = open('input.txt', 'r')
fw = open("output.txt", 'w')

n = int(f.readline())
c = int(f.readline())
a = int(f.readline())
method = f.readline().replace('\n', '')
#print ("n is %d, c is %d, a is %d, method is %s" % (n, c, a, method))

animalCordList = []
cordCountMap = {}

line = f.readline()

while line:
	x = line.strip().split(',')
	newCord = (int(x[0]), int(x[1]))

	if newCord in animalCordList:
		cordCountMap[newCord] += 1
	else:
		animalCordList.append(newCord)
		cordCountMap[newCord] = 1
	line = f.readline()

f.close()

outcome = 0

def doDFS():
	random.shuffle(animalCordList)
	board = Board(int(n), int(c), len(animalCordList), animalCordList, cordCountMap)
	# board.printBasic()

	res = DFS(board)
	# res.printPoint()
	print res.placedCord
	# print res.bestByRow
	# print res.bestRestByRow
	return res.tigerCount
def doAStar():
	random.shuffle(animalCordList)
	board = Board(int(n), int(c), len(animalCordList), animalCordList, cordCountMap)
	# board.printBasic()
	res = AStar(board)
	print res.placedCord
	return res.tigerCount

if (method == "dfs") :
	outcome = doDFS()
elif (method == "astar") :
	outcome = doAStar()

fw.write("%d" % outcome)

fw.close()
print("Output is %d" % outcome)
print("--- %s seconds ---" % (time.time() - start_time))

