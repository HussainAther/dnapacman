import random

from game import Actions, Agent
from util import chooseFromDistribution, manhattanDistance

class RandomGhost( Agent ):
    """
    For the ghosts that move randomly, program how they
    get an action from a set of legal actions.
    """
    def __init__( self, index ):
        """
        Initialize the index of locations on the board.
        """
        self.index = index
    
  def getAction( self, state ):
      """
      Get a random action from the possible (legal) actions.
      """ 
      return random.choice( state.getLegalActions( self.index ) )
  
  def getDistribution( self, state ):
      """
      Get the distribution of possible actions.
      """
      actions = state.getLegalActions( self.index )
      prob = 1.0 / len( actions )
      return [( prob, action ) for action in actions]

class DirectionalGhost( Agent ):
     """
     For the ghosts that move in a specific direction relative
     to the player, figure out how they will move.
     """
     def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.1 ):
         """
         Initialize the index (board location) and the probabilities the ghost
         will attack or run away from Pac-Man.
         """
         self.index = index
         self.prob_attack = prob_attack
         self.prob_scaredFlee = prob_scaredFlee
    
    def getAction( self, state ):
        """
        Get the action the ghost will do based on a distribution
        of possible actions.
        """
        dist = self.getDistribution( state )
        return chooseFromDistribution( dist )
  
    def getDistribution( self, state ):
        """
        Get the distribution of possible actions.
        """
        # Read variables from state.
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0
    
        speed = 1
        if isScared: speed = 0.5
    
        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
        pacman_pos = state.getPacmanPosition()

        # Select best actions given the state.
        distancesToPacman = [manhattanDistance( pos, pacman_pos ) for pos in newPositions]
        if isScared:
            bestScore = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min( distancesToPacman )
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]
        
        # Construct distribution.
        numBest = len( bestActions )
        distribution = [( bestProb / numBest, action ) for action in bestActions]
        numActions = len( legalActions )
        distribution += [( ( 1-bestProb ) / numActions, action ) for action in legalActions]
        return distribution
