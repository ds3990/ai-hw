import numpy as np
import random
import time
import sys
import os
from BaseAI import BaseAI
from Grid import Grid


# TO BE IMPLEMENTED
#
class PlayerAI(BaseAI):

    def __init__(self) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = None
        self.player_num = None

    def getPosition(self):
        return self.pos

    def setPosition(self, new_position):
        self.pos = new_position

    def getPlayerNum(self):
        return self.player_num

    def setPlayerNum(self, num):
        self.player_num = num

    def getMove(self, grid: Grid) -> tuple:
        """
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player moves.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Trap* actions,
        taking into account the probabilities of them landing in the positions you believe they'd throw to.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.

        """

        # find all available moves
        available_moves = grid.get_neighbors(self.pos, only_available=True)
        best_util = -100
        best_move = None

        if available_moves:
            for s in available_moves:
                g = Grid()
                g.map = grid.getMap()
                g.move(s, 1)
                util = self.utility(g)
                print("Move to {s}, util is {util}".format(**locals()))
                if util > best_util:
                    best_util = util
                    best_move = s

        return best_move

    def getTrap(self, grid: Grid) -> tuple:
        """
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions,
        taking into account the probabilities of it landing in the positions you want.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.

        """
        # find all available moves for the opponent
        available_moves = grid.get_neighbors(grid.find(2), only_available=True)
        best_util = -100
        best_trap = None

        if available_moves:
            for s in available_moves:
                g = Grid()
                g.map = grid.getMap()
                g.trap(s)
                util = self.utility(g)
                if util > best_util:
                    best_util = util
                    best_trap = s
        else:
            best_trap = grid.getAvailableCells()[0]

        return best_trap

    def utility(self, grid: Grid) -> int:
        """
        Utility function that returns an integer describing the goodness of state for me.

        """

        return self.oneCellLookaheadScore(grid)

    def improvedScore(self, grid: Grid) -> int:
        """
        Utility function that returns an integer describing the goodness of state for me.

        """

        # find the opponent and their available moves
        opponent_space = grid.find(2)
        opponent_available_moves = grid.get_neighbors(opponent_space, only_available=True)

        # find my available moves
        my_space = grid.find(1)
        my_available_moves = grid.get_neighbors(my_space, only_available=True)

        # find diff between them
        improved_score = my_available_moves - opponent_available_moves
        aggressive_improved_score = my_available_moves - (2*opponent_available_moves)

        return aggressive_improved_score

    def oneCellLookaheadScore(self, grid: Grid) -> int:

        # find the opponent and their available moves one step ahead
        opponent_space = grid.find(2)
        opponent_available_moves = 0
        for s in grid.get_neighbors(opponent_space, only_available=True):
            opponent_available_moves += grid.get_neighbors(s, only_available=True).__len__()


        # find my available moves
        my_space = grid.find(1)
        my_available_moves = 0
        for s in grid.get_neighbors(my_space, only_available=True):
            my_available_moves += grid.get_neighbors(s, only_available=True).__len__()

        # find diff (more positive number is better)
        ocls = my_available_moves - opponent_available_moves

        return ocls
