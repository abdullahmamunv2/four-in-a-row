from HumanFIARAgent import *
from MinimaxFIARAgent import *
from FourInARow import *
from Game import *
from FourInARow import *



human =HumanFIARAgent("Charlie")
#Agent human = new MinimaxTTTAgent("007");
machine =MinimaxFIARAgent("Computer")

#System.out.println(human.name+" vs. "+machine.name)

game = FourInARow(human,machine)
game.StartAnimation()
