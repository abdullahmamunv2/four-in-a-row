

class Agent(object): 

	def __init__(self,name):
		self.name = name # Name of the agent
		
	"""
	 * Sets the role of this agent. Typlically will be called by your extended Game class (The  class which extends the Game Class).
	  @param role
	 """
	def setRole(self,role):
		self.role = role;

	"""
	 * Implement this method to select a move, and change the game state according to the chosen move.
	 * @param game
	 * """
	def makeMove(game):
		raise NotImplementedError('subclasses must override makeMove()!')
	