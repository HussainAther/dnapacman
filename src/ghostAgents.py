from game import Agent
import random
from util import chooseFromDistribution
from util import manhattanDistance
from game import Actions

class RandomGhost( Agent ):
  def __init__( self, index ):
    self.index = index
    
  def getAction( self, state ):
    return random.choice( state.getLegalActions( self.index ) )
  
  def getDistribution( self, state ):
    actions = state.getLegalActions( self.index )
    prob = 1.0 / len( actions )
    return [( prob, action ) for action in actions]

class DirectionalGhost( Agent ):
  def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.1 ):
    self.index = index
    self.prob_attack = prob_attack
    self.prob_scaredFlee = prob_scaredFlee
    
  def getAction( self, state ):
    dist = self.getDistribution( state )
    return chooseFromDistribution( dist )
  
  def getDistribution( self, state ):
    # Read variables from state
    ghostState = state.getGhostState( self.index )
    legalActions = state.getLegalActions( self.index )
    pos = state.getGhostPosition( self.index )
    isScared = ghostState.scaredTimer > 0
    
    speed = 1
    if isScared: speed = 0.5
    
    actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
    newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
    pacman_pos = state.getPacmanPosition()

    # Select best actions given the state
    distancesToPacman = [manhattanDistance( pos, pacman_pos ) for pos in newPositions]
    if isScared:
      bestScore = max( distancesToPacman )
      bestProb = self.prob_scaredFlee
    else:
      bestScore = min( distancesToPacman )
      bestProb = self.prob_attack
    bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]
    
    # Construct distribution
    numBest = len( bestActions )
    distribution = [( bestProb / numBest, action ) for action in bestActions]
    numActions = len( legalActions )
    distribution += [( ( 1-bestProb ) / numActions, action ) for action in legalActions]
    return distribution
