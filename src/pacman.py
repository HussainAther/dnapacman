#!/bin/python3.7

"""
To play your first game, type "python pacman.py" from the command line.
The keys are "A", "S", "D", and "W" to move (or arrow keys).  

Have fun!
"""

import os, random, sys, time, types, util

from game import Actions, Directions, Game, GameStateData
from util import manhattanDistance, nearestPoint

print("================================================.\n .-.   .-.     .--.                             |\n| O    O| | OO|   / _.-'    A   C   U   G   U   C   |\n|   | |   |   \  '-.                            |\n'^^^' '^^^'        '--'                         C   |\n===============.       .================.       |\n               |           |                |   U   |\n               |       |                |       |\n               |       |                    |   U   |\n               |       |                |       |\n==============='       '================'       A   |")

def restart_program():
    """
    Restarts the current program.
        Note: this function does not return. Any cleanup action (like saving data) must be done before calling this function.
    """
    python = sys.executable
    os.execl(python, python, * sys.argv)

class GameState:
  
    def getLegalActions( self, agentIndex=0 ):
        if self.isWin() or self.isLose(): return []
      
        if agentIndex == 0:
            return PacmanRules.getLegalActions( self )
        else:
            return GhostRules.getLegalActions( self, agentIndex )
      
    def generateSuccessor( self, agentIndex, action):
        if self.isWin() or self.isLose(): raise Exception("Can\'t generate a successor of a terminal state.")
      
        state = GameState(self)
  
        if agentIndex == 0:
            state.data._eaten = [False for i in range(state.getNumAgents())]
            PacmanRules.applyAction(state, action)
        else:
            GhostRules.applyAction(state, action, agentIndex)
      
        if agentIndex == 0:
            state.data.scoreChange += 0
        else:
            GhostRules.decrementTimer( state.data.agentStates[agentIndex] )
        
        GhostRules.checkDeath( state, agentIndex )
    
        state.data._agentMoved = agentIndex
        state.data.score += state.data.scoreChange
        return state
    
    def getLegalPacmanActions( self ):
        return self.getLegalActions( 0 )
    
    def generatePacmanSuccessor( self, action ):
        return self.generateSuccessor( 0, action )
    
    def getPacmanState( self ):
        return self.data.agentStates[0].copy()
    
    def getPacmanPosition( self ):
        return self.data.agentStates[0].getPosition()
    
    def getGhostStates( self ):
        return self.data.agentStates[1:]
    
    def getGhostState( self, agentIndex ):
        if agentIndex == 0 or agentIndex >= self.getNumAgents():
            raise BaseException("Invalid index passed to getGhostState")
        return self.data.agentStates[agentIndex]
    
    def getGhostPosition( self, agentIndex ):
        if agentIndex == 0:
            raise BaseException("Pacman's index passed to getGhostPosition")
        return self.data.agentStates[agentIndex].getPosition()
    
    def getNumAgents( self ):
        return len( self.data.agentStates )
    
    def getScore( self ):
        return self.data.score
    
    def getCapsules(self):
        return self.data.capsules
     
    def getNumFood( self ):
        return self.data.food.count()
    
    def getFood(self):
        return self.data.food
    
    def getWalls(self):
        return self.data.layout.walls
  
    def hasFood(self, x, y):
        return self.data.food[x][y]
    
    def hasWall(self, x, y):
      return self.data.layout.walls[x][y]
  
    def isLose( self ):
      return self.data._lose
    
    def isWin( self ):
      return self.data._win
    
    
    def __init__( self, prevState = None ):
        if prevState != None: # Initial state
            self.data = GameStateData(prevState.data)
        else:
            self.data = GameStateData()
      
    def deepCopy( self ):
        state = GameState( self )
        state.data = self.data.deepCopy()
        return state
      
    def __eq__( self, other ):
        if other == None:
            return self.data == other
        return self.data == other.data
                                                        
    def __hash__( self ):
        return hash( str( self ) )
  
    def __str__( self ):
      
        return str(self.data)
        
    def initialize( self, layout, numGhostAgents=1000 ):
        self.data.initialize(layout, numGhostAgents)

  
SCARED_TIME = 40 # moves ghosts are scared 
COLLISION_TOLERANCE = 0.7 # How close ghosts must be to Pacman to kill
TIME_PENALTY = 1 # Number of points lost each round

class ClassicGameRules:
    def newGame( self, layout, pacmanAgent, ghostAgents, display ):
        agents = [pacmanAgent] + ghostAgents[:layout.getNumGhosts()]
        initState = GameState()
        initState.initialize( layout, len(ghostAgents) )
        game = Game(agents, display, self)
        game.state = initState
        return game
    
    def process(self, state, game):
        if state.isWin(): self.win(state, game)
        if state.isLose(): self.lose(state, game)
        
    def win(self, state, game):
        print("You won! Score: %d" % state.data.score)
        answer = input("Press Enter to play again.")
        game.gameOver = True
        if answer.lower().strip() in "\n":
            restart_program()
  
    def lose( self, state, game ):
        print("You died! Score: %d" % state.data.score)
        answer = input("Press Enter to play again.")
        game.gameOver = True
        if answer.lower().strip() in "\n":
            restart_program()
    
class PacmanRules:
    PACMAN_SPEED=1
  
    def getLegalActions( state ):
        return Actions.getPossibleActions( state.getPacmanState().configuration, state.data.layout.walls )
    getLegalActions = staticmethod( getLegalActions )

    def applyAction(state, action ):
        legal = PacmanRules.getLegalActions( state )
        if action not in legal:
            raise BaseException("Illegal action" + str(action))
  
        pacmanState = state.data.agentStates[0]
      
        # Update Configuration
        vector = Actions.directionToVector( action, PacmanRules.PACMAN_SPEED )
        pacmanState.configuration = pacmanState.configuration.generateSuccessor( vector )
      
        # Eat
        next = pacmanState.configuration.getPosition()
        nearest = nearestPoint( next )
        if manhattanDistance( nearest, next ) <= 0.5 :
            # Remove food
            PacmanRules.consume( nearest, state )
    applyAction = staticmethod( applyAction )
  
    def consume( position, state ):
        x,y = position
        # Eat food
        if state.data.food[x][y]:
            state.data.scoreChange += 10
            state.data.food = state.data.food.copy()
            state.data.food[x][y] = False
            state.data._foodEaten = position
            # TODO: cache numFood?
            numFood = state.getNumFood()
            if numFood == 0 and not state.data._lose:
                state.data.scoreChange += 500
                state.data._win = True
        # Eat capsule
        if( position in state.getCapsules() ):
            state.data.capsules.remove( position )
            state.data._capsuleEaten = position
            # Reset all ghosts" scared timers
            for index in range( 1, len( state.data.agentStates ) ):
                state.data.agentStates[index].scaredTimer = SCARED_TIME
    consume = staticmethod( consume )

class GhostRules:
    GHOST_SPEED=1.0
    def getLegalActions( state, ghostIndex ):
  
        conf = state.getGhostState( ghostIndex ).configuration
        possibleActions = Actions.getPossibleActions( conf, state.data.layout.walls )
        reverse = Actions.reverseDirection( conf.direction )
        if Directions.STOP in possibleActions:
            possibleActions.remove( Directions.STOP )
        if reverse in possibleActions and len( possibleActions ) > 1:
            possibleActions.remove( reverse )
        return possibleActions
    getLegalActions = staticmethod( getLegalActions )

    def applyAction(state, action, ghostIndex):
  
        legal = GhostRules.getLegalActions( state, ghostIndex )
        if action not in legal:
            raise BaseException("Illegal ghost action", action)
  
        ghostState = state.data.agentStates[ghostIndex]
        speed = GhostRules.GHOST_SPEED
        if ghostState.scaredTimer > 0: speed /= 2.0
        vector = Actions.directionToVector( action, speed )
        ghostState.configuration = ghostState.configuration.generateSuccessor( vector )
    applyAction = staticmethod( applyAction )
      
    def decrementTimer( ghostState):
        timer = ghostState.scaredTimer
        if timer == 1: 
            ghostState.configuration.pos = nearestPoint( ghostState.configuration.pos )
        ghostState.scaredTimer = max( 0, timer - 1 )
    decrementTimer = staticmethod( decrementTimer )
        
    def checkDeath( state, agentIndex):
        pacmanPosition = state.getPacmanPosition()
        if agentIndex == 0: # Pacman just moved; Anyone can kill him
            for index in range( 1, len( state.data.agentStates ) ):
                ghostState = state.data.agentStates[index]
                ghostPosition = ghostState.configuration.getPosition()
                if GhostRules.canKill( pacmanPosition, ghostPosition ):
                    GhostRules.collide( state, ghostState, index )
        else:  
            ghostState = state.data.agentStates[agentIndex]
            ghostPosition = ghostState.configuration.getPosition()
            if GhostRules.canKill( pacmanPosition, ghostPosition ):
                GhostRules.collide( state, ghostState, agentIndex )  
    checkDeath = staticmethod( checkDeath )
    
    def collide( state, ghostState, agentIndex):
        if ghostState.scaredTimer > 0:
            state.data.scoreChange += 200
            GhostRules.placeGhost(state, ghostState)
            ghostState.scaredTimer = 0
            # Added for first-person
            state.data._eaten[agentIndex] = True
        else:
            if not state.data._win:
                state.data.scoreChange -= 0
                state.data._lose = True
    collide = staticmethod( collide )
  
    def canKill( pacmanPosition, ghostPosition ):
        return manhattanDistance( ghostPosition, pacmanPosition ) <= COLLISION_TOLERANCE
    canKill = staticmethod( canKill )
    
    def placeGhost(state, ghostState):
        ghostState.configuration = ghostState.start
    placeGhost = staticmethod( placeGhost )

#############################
# FRAMEWORK TO START A GAME #
#############################

def default(str):
    return str + " [Default: %default]"

def readCommand( argv ):
    """
    Processes the command used to run pacman from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python pacman.py <options>
    EXAMPLES:   (1) python pacman.py
                    - starts an interactive game
                (2) python pacman.py --layout smallClassic --zoom 2
                OR  python pacman.py -l smallClassic -z 2
                    - starts an interactive game on a smaller board, zoomed in
    """
    parser = OptionParser(usageStr)
    
    parser.add_option("-n", "--numGames", dest="numGames", type="int",
                      help=default("the number of GAMES to play"), metavar="GAMES", default=1)
    parser.add_option("-l", "--layout", dest="layout", 
                      help=default("the LAYOUT_FILE from which to load the map layout"), 
                      metavar="LAYOUT_FILE", default="mediumClassic")
    parser.add_option("-p", "--pacman", dest="pacman", 
                      help=default("the agent TYPE in the pacmanAgents module to use"), 
                      metavar="TYPE", default="KeyboardAgent")
    parser.add_option("-d", "--depth", dest="depth", type="int",
                      help=default("the search DEPTH passed to the agent"), metavar="DEPTH", default=2)
    parser.add_option("-t", "--textGraphics", action="store_true", dest="textGraphics", 
                      help="Display output as text only", default=False)
    parser.add_option("-q", "--quietTextGraphics", action="store_true", dest="quietGraphics", 
                      help="Generate minimal output and no graphics", default=False)
    parser.add_option("--textGraphicsDelay", type="float", dest="delay", 
                      help="Pause length between moves in the text display", default=0.1)
    parser.add_option("-g", "--ghosts", dest="ghost", 
                      help=default("the ghost agent TYPE in the ghostAgents module to use"), 
                      metavar = "TYPE", default="RandomGhost")
    parser.add_option("-k", "--numghosts", type="int", dest="numGhosts", 
                      help=default("The maximum number of ghosts to use"), default=4)
    parser.add_option("-z", "--zoom", type="float", dest="zoom", 
                      help=default("Zoom the size of the graphics window"), default=1.0)
    parser.add_option("-f", "--fixRandomSeed", action="store_true", dest="fixRandomSeed", 
                      help="Fixes the random seed to always play the same game", default=False)
    parser.add_option("-r", "--recordActions", action="store_true", dest="record", 
                      help="Writes game histories to a file (named by the time they were played)", default=False)
    parser.add_option("--replay", dest="gameToReplay", 
                      help="A recorded game file (pickle) to replay", default=None)
    
    options, otherjunk = parser.parse_args()
    if len(otherjunk) != 0: 
        raise Exception("Command line input not understood: " + otherjunk)
    args = dict()
  
    # Fix the random seed
    if options.fixRandomSeed: random.seed("rseed")
    
    # Choose a layout
    import layout
    args["layout"] = layout.getLayout( options.layout )
    if args["layout"] == None: raise BaseException("The layout " + options.layout + " cannot be found")
    
    # Choose a pacman agent
    noKeyboard = options.gameToReplay == None and (options.textGraphics or options.quietGraphics)
    pacmanType = loadAgent(options.pacman, noKeyboard)
  
    pacman = pacmanType() # Figure out how to instantiate pacman
    if "setDepth" in dir(pacman): pacman.setDepth(options.depth)
    try:
        import evaluation
        if "setEvaluation" in dir(pacman):
            evalFn = getattr(evaluation, options.evaluationFn) 
            pacman.setEvaluation(evalFn)
    except ImportError: 
        pass
    args["pacman"] = pacman
      
    # Choose a ghost agent
    import ghostAgents
    ghostType = getattr(ghostAgents, options.ghost)
    args["ghosts"] = [ghostType( i+1 ) for i in range( options.numGhosts )]
      
    # Choose a display format
    if options.quietGraphics:
        import textDisplay
        args["display"] = textDisplay.NullGraphics()
    elif options.textGraphics:
        import textDisplay
        textDisplay.SLEEP_TIME = options.delay
        args["display"] = textDisplay.PacmanGraphics()      
    else:
        import graphicsDisplay
        args["display"] = graphicsDisplay.PacmanGraphics(options.zoom)
    args["numGames"] = options.numGames
    args["record"] = options.record
    
    # Special case: recorded games don"t use the runGames method or args structure
    if options.gameToReplay != None:
        import cPickle
        recorded = cPickle.load(open(options.gameToReplay))
        recorded["display"] = args["display"]
        replayGame(**recorded)
        sys.exit(0)
    
    return args

def loadAgent(pacman, nographics):
    import os
    moduleNames = [f for f in os.listdir(".") if f.endswith("gents.py")]
    moduleNames += ["searchAgents.py", "multiAgents.py"]
    for modulename in moduleNames:
        try:
            module = __import__(modulename[:-3])
        except ImportError: 
            continue
        if pacman in dir(module):
            if nographics and modulename == "keyboardAgents.py":
                raise BaseException("Using the keyboard requires graphics (not text display)")
            return getattr(module, pacman)
    raise BaseException("The agent " + pacman + " is not specified in any *Agents.py.")

def replayGame( layout, agents, actions, display ):
    rules = ClassicGameRules()
    game = rules.newGame( layout, agents[0], agents[1:], display )   
    state = game.state
    display.initialize(state.data)
    
    for action in actions:
        # Execute the action.
        state = state.generateSuccessor( *action )
        # Change the display.
        display.update( state.data )
        # Allow for game specific conditions (winning, losing, etc.).
        rules.process(state, game)
    
    display.finish()


def runGames( layout, pacman, ghosts, display, numGames, record ):
    import __main__
    __main__.__dict__["_display"] = display
  
    rules = ClassicGameRules()
    games = []
  
    for i in range( numGames ):
        game = rules.newGame( layout, pacman, ghosts, display )              
        game.run()
        games.append(game)
        if record:
            import time, cPickle
            fname = ("recorded-game-%d" % (i + 1)) +  "-".join([str(t) for t in time.localtime()[1:6]])
            f = file(fname, "w")
            components = {"layout": layout, "agents": game.agents, "actions": game.moveHistory}
            cPickle.dump(components, f)
            f.close()
      
    if numGames > 1:
        scores = [game.state.getScore() for game in games]
        wins = [game.state.isWin() for game in games]
        print("Average Score:", sum(scores) / float(numGames))
        print("Scores:       ", ", ".join([str(score) for score in scores]))
        print("Win Rate:     ", wins.count(True) / float(numGames))
        print("Record:       ", ", ".join([ ["Loss", "Win"][int(w)] for w in wins]))

    return games
  
if __name__ == "__main__":
    args = readCommand( sys.argv[1:] ) # Get game components based on input.
    runGames( **args )
