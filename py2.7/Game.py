import random
from Agent import *
from MinimaxFIARAgent import CellValueTuple

############## author charlie ###########

################## animation #######################
import random, copy, sys, pygame
from pygame.locals import *

BOARDWIDTH = 7  # how many spaces wide the board is
BOARDHEIGHT = 7 # how many spaces tall the board is
assert BOARDWIDTH >= 4 and BOARDHEIGHT >= 4, 'Board must be at least 4x4.'

DIFFICULTY = 2 # how many moves to look ahead. (>2 is usually too much)

SPACESIZE = 70 # size of the tokens and individual board spaces in pixels

FPS = 40 # frames per second to update the screen
WINDOWWIDTH = 1200 # width of the program's window, in pixels
WINDOWHEIGHT = 800 # height in pixels

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) / 2)

BRIGHTBLUE = (0, 50, 255)
WHITE = (255, 255, 255)

BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

#RED = 'red'
#BLACK = 'black'
RED = 0
BLACK = 1
EMPTY = -1
HUMAN = 0
COMPUTER = 1


 
class Game(object):
	"""Doc string :  This is an abstract class"""
	def __init__(self,a,b,match_in_a_row=4):
		self.a=a
		self.b=b 								# Agent a , Agent b 
		self.agent = []                             # list containing all the agents, here we only consider two player games.
		self.agent.append(a)
		self.agent.append(b)
		self.name="A Generic Game"                  # A name for the Game object, it will be changed by the actual game class extending it 
		self.winner=None							# The winning agent will be saved here after the game compeltes, if null the game is drawn.
		self.match_in_a_row=match_in_a_row
	
	"""
	 * The actual game loop, each player takes turn.
	 * The first player is selected randomly
	 * """
	def play(self,isFirstGame):
		#self.updateMessage("Starting " + self.name + " between "+ self.agent[0].name+ " and "+ self.agent[1].name+".")
		if isFirstGame:
	        # Let the computer go first on the first game, so the player
	        # can see how the tokens are dragged from the token piles.
	        #turn = COMPUTER
			turn=1
			showHelp = True
		else:
			# Randomly choose who goes first.
			if random.randint(0, 1) == 0:
				turn = COMPUTER
			else:
				turn = HUMAN
			showHelp = False
		#turn = random.randint(0,1);
		#print self.agent[turn].name , " makes the first move."
		self.setGridSize(BOARDHEIGHT,BOARDWIDTH)
		self.initialize(False)



		while not self.isFinished():
			if turn==0:
				self.makeMove(self.board,showHelp)
				if showHelp:
					# turn off help arrow after the first move
					showHelp = False
			else :
				#self.updateMessage(self.agent[turn].name+ "'s turn. ")
				best=self.agent[turn].makeMove(self)
				self.animateComputerMoving(self.board, best.col)
				self.board[best.row][best.col]=turn

			
			#self.showGameState()
			turn = (turn+1)%2
		print self.winner.name
		if self.winner.name=="charlie":
			#self.updateMessage(self.winner.name+ " wins!!!")
			winnerImg=HUMANWINNERIMG
		elif self.winner.name=="Computer":
			winnerImg = COMPUTERWINNERIMG
		else:
			#self.updateMessage("Game drawn!!")
			winnerImg = TIEWINNERIMG
		while True:
	        # Keep looping until player clicks the mouse or quits.
			self.drawBoard(self.board)
			DISPLAYSURF.blit(winnerImg, WINNERRECT)
			pygame.display.update()
			FPSCLOCK.tick()
			for event in pygame.event.get(): # event handling loop
				if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
					pygame.quit()
					sys.exit()
				elif event.type == MOUSEBUTTONUP:
					return
		
	def StartAnimation(self):
		global FPSCLOCK, DISPLAYSURF, REDPILERECT, BLACKPILERECT, REDTOKENIMG
		global BLACKTOKENIMG, BOARDIMG, ARROWIMG, ARROWRECT, HUMANWINNERIMG
		global COMPUTERWINNERIMG, WINNERRECT, TIEWINNERIMG

		pygame.init()
		FPSCLOCK = pygame.time.Clock()
		DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
		pygame.display.set_caption('Four in a Row')

		REDPILERECT = pygame.Rect(int(SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
		BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
		REDTOKENIMG = pygame.image.load('4row_red.png')
		REDTOKENIMG = pygame.transform.smoothscale(REDTOKENIMG, (SPACESIZE, SPACESIZE))
		BLACKTOKENIMG = pygame.image.load('4row_black.png')
		BLACKTOKENIMG = pygame.transform.smoothscale(BLACKTOKENIMG, (SPACESIZE, SPACESIZE))
		BOARDIMG = pygame.image.load('4row_board.png')
		BOARDIMG = pygame.transform.smoothscale(BOARDIMG, (SPACESIZE, SPACESIZE))

		HUMANWINNERIMG = pygame.image.load('4row_humanwinner.png')
		COMPUTERWINNERIMG = pygame.image.load('4row_computerwinner.png')
		TIEWINNERIMG = pygame.image.load('4row_tie.png')
		WINNERRECT = HUMANWINNERIMG.get_rect()
		WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

		ARROWIMG = pygame.image.load('4row_arrow.png')
		ARROWRECT = ARROWIMG.get_rect()
		ARROWRECT.left = REDPILERECT.right + 10
		ARROWRECT.centery = REDPILERECT.centery

		isFirstGame = True

		while True:
			self.play(isFirstGame)
			isFirstGame = False

	def drawBoard(self,board, extraToken=None):
	    DISPLAYSURF.fill(BGCOLOR)

	    # draw tokens
	    spaceRect = pygame.Rect(0, 0, SPACESIZE, SPACESIZE)
	    for x in range(BOARDHEIGHT):
	        for y in range(BOARDWIDTH):
	            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
	            if board[y][x] == RED:
	                DISPLAYSURF.blit(REDTOKENIMG, spaceRect)
	            elif board[y][x] == BLACK:
	                DISPLAYSURF.blit(BLACKTOKENIMG, spaceRect)

	    # draw the extra token
	    if extraToken != None:
	        if extraToken['color'] == RED:
	            DISPLAYSURF.blit(REDTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))
	        elif extraToken['color'] == BLACK:
	            DISPLAYSURF.blit(BLACKTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))

	    # draw board over the tokens
	    for x in range(BOARDHEIGHT):
	        for y in range(BOARDWIDTH):
	            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
	            DISPLAYSURF.blit(BOARDIMG, spaceRect)

	    # draw the red and black tokens off to the side
	    DISPLAYSURF.blit(REDTOKENIMG, REDPILERECT) # red on the left
	    DISPLAYSURF.blit(BLACKTOKENIMG, BLACKPILERECT) # black on the right

	def makeMove(self,board, isFirstMove):
	    draggingToken = False
	    tokenx, tokeny = None, None
	    while True:
	        for event in pygame.event.get(): # event handling loop
	            if event.type == QUIT:
	                pygame.quit()
	                sys.exit()
	            elif event.type == MOUSEBUTTONDOWN and not draggingToken and REDPILERECT.collidepoint(event.pos):
	                # start of dragging on red token pile.
	                draggingToken = True
	                tokenx, tokeny = event.pos
	            elif event.type == MOUSEMOTION and draggingToken:
	                # update the position of the red token being dragged
	                tokenx, tokeny = event.pos
	            elif event.type == MOUSEBUTTONUP and draggingToken:
	                # let go of the token being dragged
	                if tokeny < YMARGIN and tokenx > XMARGIN and tokenx < WINDOWWIDTH - XMARGIN:
	                    # let go at the top of the screen.
	                    column = int((tokenx - XMARGIN) / SPACESIZE)

	                    if self.isValidMove(board, column):
	                        self.animateDroppingToken(board, column, RED)
	                        board[self.getLowestEmptySpace(board, column)][column] = RED
	                        self.drawBoard(board)
	                        pygame.display.update()
	                        return
	                tokenx, tokeny = None, None
	                draggingToken = False
	        if tokenx != None and tokeny != None:
	            self.drawBoard(board, {'x':tokenx - int(SPACESIZE / 2), 'y':tokeny - int(SPACESIZE / 2), 'color':RED})
	        else:
	            self.drawBoard(board)

	        if isFirstMove:
	            # Show the help arrow for the player's first move.
	            DISPLAYSURF.blit(ARROWIMG, ARROWRECT)

	        pygame.display.update()
	        FPSCLOCK.tick()


	def animateDroppingToken(self,board, column, color):
	    x = XMARGIN + column * SPACESIZE
	    y = YMARGIN - SPACESIZE
	    dropSpeed = 1.0

	    lowestEmptySpace = self.getLowestEmptySpace(board, column)

	    while True:
	        y += int(dropSpeed)
	        dropSpeed += 0.5
	        if int((y - YMARGIN) / SPACESIZE) >= lowestEmptySpace:
	            return
	        self.drawBoard(board, {'x':x, 'y':y, 'color':color})
	        pygame.display.update()
	        FPSCLOCK.tick()


	def animateComputerMoving(self,board, column):
	    x = BLACKPILERECT.left
	    y = BLACKPILERECT.top
	    speed = 1.0
	    # moving the black tile up
	    while y > (YMARGIN - SPACESIZE):
	        y -= int(speed)
	        speed += 0.5
	        self.drawBoard(board, {'x':x, 'y':y, 'color':BLACK})
	        pygame.display.update()
	        FPSCLOCK.tick()
	    # moving the black tile over
	    y = YMARGIN - SPACESIZE
	    speed = 1.0
	    while x > (XMARGIN + column * SPACESIZE):
	        x -= int(speed)
	        speed += 0.5
	        self.drawBoard(board, {'x':x, 'y':y, 'color':BLACK})
	        pygame.display.update()
	        FPSCLOCK.tick()
	    # dropping the black tile
	    self.animateDroppingToken(board, column, BLACK)

	def getLowestEmptySpace(self,board, column):
	    # Return the row number of the lowest empty row in the given column.
	    for x in range(BOARDHEIGHT-1, -1, -1):
	        if board[x][column] == EMPTY:
	            return x
	    return -1


	def isValidMove(self,board, column):
	    # Returns True if there is an empty space in the given column.
	    # Otherwise returns False.
	    if column < 0 or column >= (BOARDWIDTH) or board[0][column] != EMPTY:
	        return False
	    return True
	##########################################################################
	def __str__(self):
		str = ""
		return str
	
 	# return Returns true if the game has finished. Also must update the winner member variable.
	def isFinished(self):
		raise NotImplementedError('subclasses must override initialize()!')
	
	"""
	 * Initializes the game as needed. If the game starts with different initial configurations, it can be read from file.
	 * @param fromFile if true loads the initial state from file. 
	 """
	def initialize(self,fromFile):
		raise NotImplementedError('subclasses must override initialize()!')
	
	# Prints the game state in console, or show it in the GUI
	def showGameState(self):
		raise NotImplementedError('subclasses must override showGameState()!')

	 # Shows game messages in console, or in the GUI
	def updateMessage(self,msg):                                  
		raise NotImplementedError('subclasses must override updateMessage()!')


	
