import threading
from Agent import *
import time
from dfs import *


class MinimaxFIARAgent(Agent):
	
	def __init__(self,name):
		Agent.__init__(self,name)

	def makeMove(self,game):
		#time.sleep(1)
		ab=AlphaBeta()
		ab.alpha=-100000
		ab.beta=100000
		lookAhead=5
		best = self.ABmax(game,ab,lookAhead)
		return best

		if best.col!=-1:
			game.board[best.row][best.col] = self.role
			return best.col


	
	##################
	def ABmax(self,game,ab,lookAhead):
		lookAhead=lookAhead
		maxCVT = CellValueTuple()
		maxCVT.utility = -10000
		ab=ab
		
		winner = game.checkForWin()
		
		#terminal check
		if winner == self.role:
			maxCVT.utility = 512
			return maxCVT

		elif winner!=-1:
			maxCVT.utility = -512
			return maxCVT
		elif lookAhead ==0:
			d=self.heuristic3(game,self.role,self.__minRole())+16
			maxCVT.utility=d
			return maxCVT

		elif game.isBoardFull():
			maxCVT.utility = 0
			return maxCVT
		
		coordinate=[]
		coordinate=self.__get_possible_position(game)
		"""val=[]
		for co in coordinate:
			row=co[0]
			col=co[1]
			game.board[row][col]= self.role
			d=self.heuristic3(game,self.role,self.__minRole())
			val.append((co,d))
			game.board[row][col]= -1
		val.sort(self.cost_inverse_sort)"""
		for co in coordinate:
			#row=co[0][0]
			#col=co[0][1]
			row=co[0]
			col=co[1]
			#if maxCVT.utility<ab.beta:		
			game.board[row][col] = self.role
			v = self.ABmin(game,ab,lookAhead-1).utility
			if v>=maxCVT.utility:
				maxCVT.utility=v
				maxCVT.row = row
				maxCVT.col = col
				ab.alpha=v
			game.board[row][col] = -1
			#else:
			#	return maxCVT

		return maxCVT
			
	
	def ABmin(self, game,ab,lookAhead):
		lookAhead=lookAhead
		minCVT = CellValueTuple()
		minCVT.utility = 10000
		ab=ab
		winner = game.checkForWin()
		
		#terminal check
		if winner == self.role :

			minCVT.utility = 512		#max wins
			return minCVT

		elif winner!=-1 :

			minCVT.utility = -512		#min wins
			return minCVT
		elif lookAhead == 0:
			d=self.heuristic3(game,self.__minRole(),self.role)-16
			minCVT.utility=d
			return minCVT   

		elif game.isBoardFull():

			minCVT.utility = 0; 	#draw
			return minCVT 

		coordinate=[]
		coordinate=self.__get_possible_position(game)

		"""val=[]
		for co in coordinate:
			row=co[0]
			col=co[1]
			game.board[row][col]= self.__minRole()
			d=self.heuristic3(game,self.role,self.__minRole())
			val.append((co,d))
			game.board[row][col]= -1
		val.sort(self.cost_sort)"""

		for co in coordinate:
			#row=co[0][0]
			#col=co[0][1]
			row=co[0]
			col=co[1]
			#if minCVT.utility>ab.alpha:		
			game.board[row][col] = self.__minRole()
			v = self.ABmax(game,ab,lookAhead-1).utility
			if v<=minCVT.utility:
				minCVT.utility=v
				minCVT.row = row
				minCVT.col = col
				ab.beta=v		

			game.board[row][col] = -1
			#else:
			#	return minCVT
				
		return minCVT


	################ co-ordinates of empty cell ###################	
	def __get_possible_position(self,game):
		coordinate=[]     					  
		for i in range(0,game.colSize):
			index=0
			for j in range(0,game.rowSize):
				if game.board[j][i]==-1:
					index=index+1
					continue
			if index!=0:
				coordinate.append((index-1,i))
		return coordinate
	def heuristic2(self,game,player,oppo,position):
		d=dfs(game.board,player)
		dic=d.run(position)
		#print "position : ",position
		#print "player : ",player
		#print game.showGameState()
		#print dic
		val=dic['vertical']*10+dic['horizontal']*5+dic['right_diagonal']*4+dic['left_diagonal']*4
		return val

	def heuristic3(self,game,player,oppo):
		val=0
		for i in range(game.rowSize-1,-1,-1):
			for j in range(0,(game.rowSize-game.match_in_a_row+1)):
				check_list=[]
				for k in range(j,game.match_in_a_row+j):
					check_list.append(game.board[i][k])
				val+=self.evalution_value(check_list,player,oppo)

		#check Col
		for i in range(game.colSize-1,-1,-1):
			for j in range(0,(game.colSize-game.match_in_a_row+1)):
				check_list=[]
				for k in range(j,game.match_in_a_row+j):
					check_list.append(game.board[k][i])
				val+=self.evalution_value(check_list,player,oppo)

		#check diagonal "/"
		for i in range(game.colSize-game.match_in_a_row):
			for j in range(game.match_in_a_row,game.rowSize):
				check_list=[]
				for k in range(0,game.match_in_a_row):
					check_list.append(game.board[i+k][j-k])
				val+=self.evalution_value(check_list,player,oppo)

		#check diagonal "\"
		for i in range(game.colSize-game.match_in_a_row):
			for j in range(game.rowSize-game.match_in_a_row):
				check_list=[]
				for k in range(0,game.match_in_a_row):
					check_list.append(game.board[i+k][j+k])
				val+=self.evalution_value(check_list,player,oppo)
					
		return val
	def evalution_value(self,slot,player,oppo):
		player_count=0
		oppo_count=0
		for i in slot:
			if i==player:
				player_count+=1
			elif i==oppo:
				oppo_count+=1

		if player_count!=0 and oppo_count==0:
			if player_count==1:
				return 1
			elif player_count==2:
				return 10
			elif player_count==3:
				return 50

		elif oppo_count!=0 and player_count==0:
			if player_count==1:
				return -1
			elif player_count==2:
				return -10
			elif player_count==3:
				return -50
		return 0



	def heuristic1(self,game,player,oppo):
		val=0
		role_len=[]
		for i in range(game.rowSize-1,-1,-1):
			for j in range(0,(game.rowSize-game.match_in_a_row+1)):
				same_role=0
				for k in range(j,game.match_in_a_row+j):
					if game.board[i][k]!=oppo and game.board[i][k]==player:
						same_role+=1
					if game.board[i][k]!=oppo and game.board[i][k]==-1:
						same_role+=self.is_downward_empty(game,i-1,k)
					else:
						break
				if same_role==4:
					return 100
				role_len.append(same_role)
		#print role_len

		for i in range(game.colSize-1,-1,-1):
			for j in range(0,(game.colSize-game.match_in_a_row+1)):
				same_role=0
				for k in range(j,game.match_in_a_row+j):
					if game.board[k][i]!=oppo and game.board[k][i]==player:
						same_role+=1
					else :
						break
				if same_role==4:
					return 100
				role_len.append(same_role)
		#print role_len

		for i in range(game.colSize-game.match_in_a_row):
			for j in range(game.match_in_a_row,game.rowSize):
				same_role=0
				for k in range(0,game.match_in_a_row):
					if game.board[i+k][j-k]!=oppo and game.board[i+k][j-k]==player:
						same_role+=1
					if game.board[i+k][j-k]!=oppo and game.board[i+k][j-k]==-1:
						same_role+=self.is_downward_empty(game,i+k-1,j-k)
					else:
						break
				if same_role==4:
					return 100
				role_len.append(same_role)
		for i in range(game.colSize-game.match_in_a_row):
			for j in range(game.rowSize-game.match_in_a_row):
				same_role=0
				for k in range(0,game.match_in_a_row):
					if game.board[i+k][j+k]!=oppo and game.board[i+k][j+k]==player:
						same_role+=1
					if game.board[i+k][j+k]!=oppo and game.board[i+k][j+k]==-1:
						same_role+=self.is_downward_empty(game,i+k-1,j+k)
					else:
						break
				if same_role==4:
					return 100

		for i in role_len:
			if i==1:
				val+=5
			elif i==2:
				val+=10
			else:
				val+=20
		return val
	def is_downward_empty(self,game,i,j):
		if i<game.rowSize and game.board[i-1][j]!=-1:
			return 1
		return 0

	def assign_value(check_list):
		pass
	def cost_inverse_sort(self,a,b):
		return cmp(b[1],a[1])
	def cost_sort(self,a,b):
		return cmp(a[1],b[1])
			
	
	def __minRole(self):

		if self.role==0:
			return 1
		else :
			return 0
	



class CellValueTuple(object):
	def __init__(self):
		self.row =-1
		self.col =-1
		self.utility=0

class AlphaBeta(object):
	def __init__(self):
		self.apha=0
		self.beta=0
