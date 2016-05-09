from Game import Game
import random, copy, sys, pygame
from pygame.locals import *


class FourInARow(Game):

	def __init__(self,a,b,match_in_a_row=4): # Agent a ,Agent b
		Game.__init__(self,a,b,match_in_a_row)
		
		self.a.setRole(0)   # The first argument/agent is always assigned O (0)
		self.b.setRole(1)   # The second argument/agent is always assigned X (1)

	  	""" NOtice that, here first dows not mean that afent a will make the first move of the game.
	    Here, first means the first argument of the constructor
	    Which of a and b will actually give the first move is chosen randomly. See Game class """
		
		self.name = "Four In A Row"
		
	######################### Set grid Size #############################

	def setGridSize(self,rowSize,colSize):
		if rowSize < self.match_in_a_row :
			raise ValueError('Grid\'s length is less then maching number ')
		self.rowSize=rowSize;
		self.colSize=colSize;

	#####################################################################

	"""
	 * Called by the play method of Game class. It must update the winner variable. 
	 * In this implementation, it is done inside checkForWin() function.
	 */ """

	def isFinished(self):

		if self.checkForWin() is not -1:
			return True
		elif self.isBoardFull():
			return True;
		else :
			return False
	######################### initialize grid from file  #############################
	def initialize(self,fromFile):
		if fromFile :
			try:
				file = open("ini.txt",'r')
				l=[]
				for line in file.readlines():
					l.append(map(int,line.split()))
				self.board=l

			except:
				print "file not found"
			return 
		self.board=[ [-1 for i in range(0,self.rowSize)] for j in range(0,self.colSize)]   #### list comprehension

		
	#################################################################################


	# Prints the current board (may be replaced/appended with by GUI)
	def showGameState(self):
		print "-"*self.rowSize*5
		for i in range(0,self.rowSize):
			print "|",
			for j in range(0,self.colSize):
				if self.board[i][j]==-1 :
					print "  | ",
				elif self.board[i][j]==0 :
					print "O | ",
				else :
					print "X | ",
			print "\n",
			print "-"*self.rowSize*5

	def isBoardFull(self):
		for i in range(0,self.rowSize): 
			for j in range(0,self.colSize):
				if self.board[i][j] == -1 :
					return False
		return True;
	
	
	def checkForWin(self) :
		self.winner = None
		winRole=-1
		for i in range(self.rowSize-1,-1,-1):
			for j in range(0,(self.rowSize-self.match_in_a_row+1)):
				check_list=[]
				for k in range(j,self.match_in_a_row+j):
					check_list.append(self.board[i][k])
				if check_list[0]!=-1 and self.__checkRowCol(check_list):
					winRole=check_list[0]
					self.winner = self.agent[winRole]
					return winRole

		#check Col
		for i in range(self.colSize-1,-1,-1):
			for j in range(0,(self.colSize-self.match_in_a_row+1)):
				check_list=[]
				for k in range(j,self.match_in_a_row+j):
					check_list.append(self.board[k][i])
				if check_list[0]!=-1 and self.__checkRowCol(check_list):
					winRole=check_list[0]
					self.winner = self.agent[winRole]
					return winRole

		#check diagonal "/"
		for i in range(self.colSize-3):
			for j in range(3,self.rowSize):
				check_list=[]
				for k in range(0,self.match_in_a_row):
					check_list.append(self.board[i+k][j-k])
				if check_list[0]!=-1 and self.__checkRowCol(check_list):
					winRole=check_list[0]
					self.winner = self.agent[winRole]
					return winRole

		#check diagonal "\"
		for i in range(self.colSize-3):
			for j in range(self.rowSize-3):
				check_list=[]
				for k in range(0,self.match_in_a_row):
					check_list.append(self.board[i+k][j+k])
				#print check_list
				if check_list[0]!=-1 and self.__checkRowCol(check_list):
					winRole=check_list[0]
					self.winner = self.agent[winRole]
					return winRole
					
		return winRole
	
	
	
    # Check to see if all three values are the same (and not empty) indicating a win.
	def __checkRowCol(self,check_list) :
		#print "check ",check_list
		first_value=check_list[0]
		for i in check_list:
			if i!=first_value:
				return False
		return True

	
	def isValidCell(self,row,col):
		if (row<0 or row>2 or col<0 or col>2) : return False
		if self.board[row][col]!=-1  :  return False
		
		return True

	def updateMessage(self,msg):
		print msg


	
	
	

