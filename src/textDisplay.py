import pacman, time

drawevery = 1
sleeptime = 0.5 # This can be overwritten by __init__.
displaymoves = False
quiet = False # Supresses output.

"""
Display the text like the score on the screen.
"""

class NullGraphics:
    """
    Helper functions if needed for more uses
    """
    def initialize(self, state):
        pass
  
    def update(self, state):
        pass
  
    def finish(self):
        pass

class PacmanGraphics:
    """
    Control the Pac-Man graphics themselves.
    """
    def __init__(self, speed=None):
        if speed != None:
            global sleeptime
            sleeptime = speed
  
    def initialize(self, state):
        self.draw(state)
        self.pause()
        self.turn = 0
        self.agentCounter = 0
    
    def update(self, state):
        numAgents = len(state.agentStates)
        self.agentCounter = (self.agentCounter + 1) % numAgents
        if self.agentCounter == 0:
            self.turn += 1
            if displaymoves:
                ghosts = [pacman.nearestPoint(state.getGhostPosition(i)) for i in range(1, numAgents)]
                print("%4d) P: %-8s" % (self.turn, str(pacman.nearestPoint(state.getPacmanPosition()))),"| Score: %-5d" % state.score,"| Ghosts:", ghosts)
            if self.turn % drawevery == 0:
                self.draw(state)
                self.pause()
      if state._win or state._lose:
          self.draw(state)
    
    def pause(self):
        time.sleep(sleeptime)
    
    def draw(self, state):
        print(state)
  
    def finish(self):
        pass
