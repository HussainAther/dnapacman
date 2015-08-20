from util import *
from util import raiseNotDefined
import time

#######################
# Parts worth reading #
#######################

class Agent:
  """
  An agent must define a getAction method, but may also define the
  following methods which will be called if they exist:
  
  def registerInitialState(self, state): # inspects the starting state
  """
  def __init__(self, index=0):
    self.index = index
      
  def getAction(self, state):
    """
    The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
    must return an action from Directions.{North, South, East, West, Stop}
    """
    raiseNotDefined()

class Directions:
  NORTH = 'North'
  SOUTH = 'South'
  EAST = 'East'
  WEST = 'West'
  STOP = 'Stop'
  
  LEFT =       {NORTH: WEST,
                 SOUTH: EAST,
                 EAST:  NORTH,
                 WEST:  SOUTH,
                 STOP:  STOP}
  
  RIGHT =      dict([(y,x) for x, y in LEFT.items()])

class Configuration:
  """
  A Configuration holds the (x,y) coordinate of a character, along with its 
  traveling direction.
  
  The convention for positions, like a graph, is that (0,0) is the lower left corner, x increases 
  horizontally and y increases vertically.  Therefore, north is the direction of increasing y, or (0,1).
  """
  
  def __init__(self, pos, direction):
    self.pos = pos
    self.direction = direction
    
  def getPosition(self):
    return (self.pos)
  
  def getDirection(self):
    return self.direction
  
  def __eq__(self, other):
    return (self.pos == other.pos and self.direction == other.direction)
  
  def __hash__(self):
    x = hash(self.pos)
    y = hash(self.direction)
    return (x + 13 * y) % sys.maxint
  
  def __str__(self):
    return "(x,y)="+str(self.pos)+", "+str(self.direction)
  
  def generateSuccessor(self, vector):
    """
    Generates a new configuration reached by translating the current
    configuration by the action vector.  This is a low-level call and does
    not attempt to respect the legality of the movement.
    
    Actions are movement vectors.
    """
    x, y= self.pos
    dx, dy = vector
    direction = Actions.vectorToDirection(vector)
    if direction == Directions.STOP: 
      direction = self.direction # There is no stop direction
    return Configuration((x + dx, y+dy), direction)

class AgentState:
  """
  AgentStates hold the state of an agent (configuration, speed, scared, etc).
  """

  def __init__( self, startConfiguration, isPacman ):
    self.start = startConfiguration
    self.configuration = startConfiguration
    self.isPacman = isPacman
    self.scaredTimer = 0

  def __str__( self ):
    if self.isPacman: 
      return "Pacman: " + str( self.configuration )
    else:
      return "Ghost: " + str( self.configuration )
  
  def __eq__( self, other ):
    if other == None:
      return False
    return self.configuration == other.configuration and self.scaredTimer == other.scaredTimer
  
  def __hash__(self):
    return hash(self.configuration) + 13* hash(self.scaredTimer)
  
  def copy( self ):
    state = AgentState( self.start, self.isPacman )
    state.configuration = self.configuration
    state.scaredTimer = self.scaredTimer
    return state
  
  def getPosition(self):
    return self.configuration.getPosition()

  def getDirection(self):
    return self.configuration.getDirection()
  
class Grid:
  """
  A 2-dimensional array of objects backed by a list of lists.  Data is accessed
  via grid[x][y] where (x,y) are positions on a Pacman map with x horizontal,
  y vertical and the origin (0,0) in the bottom left corner.  
  
  The __str__ method constructs an output that is oriented like a pacman board.
  """
  def __init__(self, width, height, initialValue=False):
    if initialValue not in [False, True]: raise Exception('Grids can only contain booleans')
    self.width = width
    self.height = height
    self.data = [[initialValue for y in range(height)] for x in range(width)]

  def __getitem__(self, i):
    return self.data[i]
  
  def __setitem__(self, key, item):
    self.data[key] = item
    
  def __str__(self):
    out = [[str(self.data[x][y])[0] for x in range(self.width)] for y in range(self.height)]
    out.reverse()
    return '\n'.join([''.join(x) for x in out])
  
  def __eq__(self, other):
    if other == None: return False
    return self.data == other.data

  def __hash__(self):
    return hash(str(self))
    base = 1
    h = 0
    for l in self.data:
      for i in l:
        if i:
          h += base
        base *= 2
    return hash(h)
  
  def copy(self):
    g = Grid(self.width, self.height)
    g.data = [x[:] for x in self.data]
    return g
  
  def deepCopy(self):
    return self.copy()
  
  def shallowCopy(self):
    g = Grid(self.width, self.height)
    g.data = self.data
    return g
    
  def count(self, item =True ):
    return sum([x.count(item) for x in self.data])
    
  def asList(self, key = True):
    list = []
    for x in range(self.width):
      for y in range(self.height):
        if self[x][y] == key: list.append( (x,y) )
    return list
  
####################################
# Parts you shouldn't have to read #
####################################
  
class Actions:
  """
  A collection of static methods for manipulating move actions.
  """
  # Directions
  _directions = {Directions.NORTH: (0, 1), 
                 Directions.SOUTH: (0, -1), 
                 Directions.EAST:  (1, 0), 
                 Directions.WEST:  (-1, 0), 
                 Directions.STOP:  (0, 0)}

  _directionsAsList = _directions.items()

  TOLERANCE = .001
  
  def reverseDirection(action):
    if action == Directions.NORTH:
      return Directions.SOUTH
    if action == Directions.SOUTH:
      return Directions.NORTH
    if action == Directions.EAST:
      return Directions.WEST
    if action == Directions.WEST:
      return Directions.EAST
    return action
  reverseDirection = staticmethod(reverseDirection)
  
  def vectorToDirection(vector):
    dx, dy = vector
    if dy > 0:
      return Directions.NORTH
    if dy < 0:
      return Directions.SOUTH
    if dx < 0:
      return Directions.WEST
    if dx > 0:
      return Directions.EAST
    return Directions.STOP
  vectorToDirection = staticmethod(vectorToDirection)
  
  def directionToVector(direction, speed = 1.0):
    dx, dy =  Actions._directions[direction]
    return (dx * speed, dy * speed)
  directionToVector = staticmethod(directionToVector)

  def getPossibleActions(config, walls):
    possible = []
    x, y = config.getPosition()
    x_int, y_int = int(x + 0.5), int(y + 0.5)
    
    # In between grid points, all agents must continue straight
    if (abs(x - x_int) + abs(y - y_int)  > Actions.TOLERANCE):
      return [config.getDirection()]
    
    for dir, vec in Actions._directionsAsList:
      dx, dy = vec
      next_y = y_int + dy
      next_x = x_int + dx
      if not walls[next_x][next_y]: possible.append(dir)

    return possible

  getPossibleActions = staticmethod(getPossibleActions)

  def getLegalNeighbors(position, walls):
    x,y = position
    x_int, y_int = int(x + 0.5), int(y + 0.5)
    neighbors = []
    for dir, vec in Actions._directionsAsList:
      dx, dy = vec
      next_x = x_int + dx
      if next_x < 0 or next_x == walls.width: continue
      next_y = y_int + dy
      if next_y < 0 or next_y == walls.height: continue
      if not walls[next_x][next_y]: neighbors.append((next_x, next_y))
    return neighbors
  getLegalNeighbors = staticmethod(getLegalNeighbors)

class GameStateData:
  """
  
  """
  def __init__( self, prevState = None ):
    """ 
    Generates a new data packet by copying information from its predecessor.
    """
    if prevState != None: 
      self.food = prevState.food.shallowCopy()
      self.capsules = prevState.capsules[:]
      self.agentStates = self.copyAgentStates( prevState.agentStates )
      self.layout = prevState.layout
      self._eaten = prevState._eaten
      self.score = prevState.score
    self._foodEaten = None
    self._capsuleEaten = None
    self._agentMoved = None
    self._lose = False
    self._win = False
    self.scoreChange = 0
    
  def deepCopy( self ):
    state = GameStateData( self )
    state.food = self.food.deepCopy()
    state.layout = self.layout.deepCopy()
    return state
    
  def copyAgentStates( self, agentStates ):
    copiedStates = []
    for agentState in agentStates:
      copiedStates.append( agentState.copy() )
    return copiedStates
    
  def __eq__( self, other ):
    """
    Allows two states to be compared.
    """
    if other == None: return False
    # TODO Check for type of other
    if not self.agentStates == other.agentStates: return False
    if not self.food == other.food: return False
    if not self.capsules == other.capsules: return False
    if not self.score == other.score: return False
    return True
                                                      
  def __hash__( self ):
    """
    Allows states to be keys of dictionaries.
    """
    for i, state in enumerate( self.agentStates ):
      try:
        hash(state)
      except TypeError, e:
          print e
          hash(state)
    return hash(tuple(self.agentStates)) + 13*hash(self.food) + 113* hash(tuple(self.capsules)) + 7 * hash(self.score)

  def __str__( self ): 
    width, height = self.layout.width, self.layout.height
    map = Grid(width, height)
    for x in range(width):
      for y in range(height):
        food, walls = self.food, self.layout.walls
        map[x][y] = self._foodWallStr(food[x][y], walls[x][y])
    
    for agentState in self.agentStates:
      x,y = [int( i ) for i in nearestPoint( agentState.configuration.pos )]
      agent_dir = agentState.configuration.direction
      if agentState.isPacman:
        map[x][y] = self._pacStr( agent_dir )
      else:
        map[x][y] = self._ghostStr( agent_dir )

    for x, y in self.capsules:
      map[x][y] = 'o'
    
    return str(map) + ("\nScore: %d\n" % self.score) 
      
  def _foodWallStr( self, hasFood, hasWall ):
    if hasFood:
      return '.'
    elif hasWall:
      return '%'
    else:
      return ' '
    
  def _pacStr( self, dir ):
    if dir == Directions.NORTH:
      return 'v'
    if dir == Directions.SOUTH:
      return '^'
    if dir == Directions.WEST:
      return '>'
    return '<'
    
  def _ghostStr( self, dir ):
    return 'G'
    if dir == Directions.NORTH:
      return 'M'
    if dir == Directions.SOUTH:
      return 'W'
    if dir == Directions.WEST:
      return '3'
    return 'E'
    
  def initialize( self, layout, numGhostAgents ):
    """
    Creates an initial game state from a layout array (see layout.py).
    """
    self.food = layout.food.copy()
    self.capsules = layout.capsules[:]
    self.layout = layout
    self.score = 0
    self.scoreChange = 0
        
    self.agentStates = []
    numGhosts = 0
    for isPacman, pos in layout.agentPositions:
      if not isPacman: 
        if numGhosts == numGhostAgents: continue # Max ghosts reached already
        else: numGhosts += 1
      self.agentStates.append( AgentState( Configuration( pos, Directions.STOP), isPacman) )
    self._eaten = [False for a in self.agentStates]

class Game:
  """
  The Game manages the control flow, soliciting actions from agents.
  """
  
  def __init__( self, agents, display, rules ):
    self.agents = agents
    self.display = display
    self.rules = rules
    self.gameOver = False
    self.moveHistory = []
    
  def run( self ):
    """
    Main control loop for game play.
    """
    self.display.initialize(self.state.data)
    # inform learning agents of the game start
    for agent in self.agents:
      # if ("initial" in dir(agent)): agent.initial()
      if ("registerInitialState" in dir(agent)):
        agent.registerInitialState(self.state.deepCopy())
      
    self.numMoves = 0
    agentIndex = 0    
    numAgents = len( self.agents )
    while not self.gameOver:
      # Fetch the next agent
      agent = self.agents[agentIndex]
      # Generate an observation of the state
      if 'observationFunction' in dir( agent ):
        observation = agent.observationFunction(self.state)
      else:
        observation = self.state.deepCopy()
        
      # Solicit an action
      startTime = time.time()
      action = agent.getAction( observation )
      self.moveHistory.append( (agentIndex, action) )
      if 'checkTime' in dir(self.rules):
        self.rules.checkTime(time.time() - startTime)
      
      # Execute the action
      self.state = self.state.generateSuccessor( agentIndex, action )
      # Change the display
      self.display.update( self.state.data )
      # Allow for game specific conditions (winning, losing, etc.)
      self.rules.process(self.state, self)
      # Track progress
      if agentIndex == numAgents + 1: self.numMoves += 1
      # Next agent
      agentIndex = ( agentIndex + 1 ) % numAgents
    
    # inform a learning agent of the game result
    for agent in self.agents:
      if "final" in dir( agent ) :
        agent.final( self.state )
    
    self.display.finish()

