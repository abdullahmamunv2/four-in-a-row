
from Agent import *
from Game import *
from gameConfig import *

class HumanFIARAgent(Agent):

	def __init__(self,name):
		Agent.__init__(self,name)

	def makeMove(self,game):
		#game.showGameState()
		
		first = True
		brk=True
		while brk:
			if first :
				print "Insert column : "
			else:
				print "Invalid column! Insert column again : "

			var1 = raw_input("Enter column here: ")
			col = int(var1)
			############ search for empty cell ############
			index=0
			for i in range(0,game.rowSize):
				if game.board[i][col]==-1:
					index=index+1
					continue
			###############################################
			if index ==0 :
				first=False
				continue
			index=index-1
			game.board[index][col] = self.role
			first=True
			break
