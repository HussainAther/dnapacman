import math, random, time

from graphicsUtils import *        

FRAME_TIME=0.1 # The time that pacman's animation last
PAUSE_TIME=0   # Pause time between frames
DEFAULT_GRID_SIZE = 30.0
INFO_PANE_HEIGHT = 35
BACKGROUND_COLOR = formatColor(0,0,0)    
WALL_COLOR = formatColor(0.0/255.0, 51.0/255.0, 255.0/255.0)
INFO_PANE_COLOR = formatColor(.4,.4,0)
SCORE_COLOR = formatColor(.9, .9, .9)

GHOST_COLORS = []                       
GHOST_COLORS.append(formatColor(200.0/255.0,200.0/255.0,61.0/255))
GHOST_COLORS.append(formatColor(0,1,1))
GHOST_COLORS.append(formatColor(221.0/255.0,0,0))
GHOST_COLORS.append(formatColor(1,.5,.8))
GHOST_COLORS.append(formatColor(255.0/255.0,150.0/255.0,0))
GHOST_SHAPE = [                
    ( 0,    0.3 ),            
    ( 0.25, 0.75 ),           
    ( 0.5,  0.3 ),
    ( 0.75, 0.75 ),
    ( 0.75, -0.5 ),
    ( 0.5,  -0.75 ),
    (-0.5,  -0.75 ),
    (-0.75, -0.5 ),
    (-0.75, 0.75 ),
    (-0.5,  0.3 ),
    (-0.25, 0.75 )
  ]
GHOST_SIZE = 0.65
SCARED_COLOR = formatColor(1,1,1)    

GHOST_VEC_COLORS = map(colorToVector, GHOST_COLORS)

PACMAN_COLORS = []
PACMAN_COLORS.append(formatColor(255.0/255.0,255.0/255.0,61.0/255))
PACMAN_COLORS.append(formatColor(0.0/255.0,255.0/255.0,255.0/255.0))
PACMAN_COLORS.append(formatColor(255.0/255.0,100.0/255.0,0.0/255))
PACMAN_COLORS.append(formatColor(50.0/255.0,255.0/255.0,200.0/255.0))
PACMAN_SCALE = 0.5  
pacman_speed = 0.25

# Food
FOOD_COLOR = formatColor(1,1,1)     
FOOD_SIZE = 0.1
FOOD_BANK=["A", "C", "U", "G"]
COLOR_BANK={"A":formatColor(.2,.8,1), "U":formatColor(1,0,1),"C":formatColor(1,1,0), "G":formatColor(1,.5,.5)}
AMINO_BANK={"UUU":"F", "UUC":"F", "UUA":"L", "UUG":"L", "UCU":"S", "UCC":"S", "UCA":"S", "UCG":"S", "UAU":"Y", "UAC":"Y", "UAA":" *", "UAG":" *", "UGU":"C", "UGC":"C", "UGA":" *", "UGG":"W", "CUU":"L", "CUC":"L", "CUA":"L", "CUG":"L", "CCU":"P", "CCC":"P", "CCA":"P", "CCG":"P", "CAU":"H", "CAC":"H", "CAA":"Q", "CAG":"Q", "CGU":"R", "CGC":"R", "CGA":"R", "CGG":"R", "AUU":"I", "AUC":"I", "AUA":"I", "AUG":"M", "ACU":"T", "ACC":"T", "ACA":"T", "ACG":"T", "AAU":"N", "AAC":"N", "AAA":"K", "AAG":"K", "AGU":"S", "AGC":"S", "AGA":"R", "AGG":"R", "GUU":"V", "GUC":"V", "GUA":"V", "GUG":"V", "GCU":"A", "GCC":"A", "GCA":"A", "GCG":"A", "GAU":"D", "GAC":"D", "GAA":"E", "GAG":"E", "GGU":"G", "GGC":"G", "GGA":"G", "GGG":"G"}
CODON_BANK=[]
AMINO=BANK=[]
ALL_ACIDS=[]
food_matrix={}
start=0
codon_string=""
amino_string=""


# LaS
LAS_COLOR = formatColor(1,0,0)     
LAS_SIZE = 0.02   

# Capsule graphics
CAPSULE_COLOR = formatColor(1,1,1)
CAPSULE_SIZE = 0.25 

# Drawing walls
WALL_RADIUS = 0.15

class InfoPane:
    def __init__(self, layout, gridSize):
        self.gridSize = gridSize
        self.width = (layout.width) * gridSize
        self.base = (layout.height + 1) * gridSize
        self.height = INFO_PANE_HEIGHT 
        self.drawPane()

    def toScreen(self, pos, y = None):
        """
        Translates a point relative from the bottom left of the info pane.
        """
        if y == None:
            x,y = pos
        else:
            x = pos

        x = self.gridSize + x # MRin
        y = self.base + y 
        return x,y

    def drawPane(self):
        color = PACMAN_COLORS[0]
        size = 24
        self.scoreText = text( self.toScreen(0, 0  ), color, "SCORE:    0", "Times", size, "bold")

    def updateScore(self, score):
        changeText(self.scoreText, "SCORE: % 4d" % score)

    def initializeGhostDistances(self, distances):
        self.ghostDistanceText = []

        size = 20
        if self.width < 240:
           size = 12
        if self.width < 160:
           size = 10

        for i, d in enumerate(distances):
            t = text( self.toScreen(self.width/2 + self.width/8 * i, 0), GHOST_COLORS[i+1], d, "Times", size, "bold")
            self.ghostDistanceText.append(t)

    def updateGhostDistances(self, distances):
        if 'ghostDistanceText' not in dir(self): self.initializeGhostDistances(distances)
        else:
            for i, d in enumerate(distances):
                changeText(self.ghostDistanceText[i], d)

    def drawGhost(self):
        pass

    def drawPacman(self):
        pass

    def drawWarning(self):
        pass

    def clearIcon(self):
        pass

    def updateMessage(self, message):
        pass

    def clearMessage(self):
        pass


class PacmanGraphics:
    def __init__(self, zoom=1.0):  
        self.have_window = 0
        self.currentGhostImages = {}
        self.pacmanImage = None
        self.zoom = zoom
        self.gridSize = DEFAULT_GRID_SIZE * zoom

    def initialize(self, state):
        self.startGraphics(state)
        self.drawStaticObjects(state)
        self.drawAgentObjects(state)

    def startGraphics(self, state):
        self.layout = state.layout
        layout = self.layout
        self.width = layout.width
        self.height = layout.height
        self.make_window(self.width, self.height)
        self.infoPane = InfoPane(layout, self.gridSize)
        self.currentState = layout

    def drawStaticObjects(self, state):
        layout = self.layout
        self.drawWalls(layout.walls)
        self.food = self.drawFood(layout.food)
        self.capsules = self.drawCapsules(layout.capsules)
        refresh

    def drawAgentObjects(self, state):
        self.agentImages = [] # (agentState, image)
        for index, agent in enumerate(state.agentStates):
            if agent.isPacman:
                image = self.drawPacman(agent, index)
                self.agentImages.append( (agent, image) )
            else:  
                image = self.drawGhost(agent, index)
                self.agentImages.append( (agent, image) )
        refresh

    def swapImages(self, agentIndex, newState):
        prevState, prevImage = self.agentImages[agentIndex]
        for item in prevImage: remove_from_screen(item)
        if newState.isPacman:
            image = self.drawPacman(newState, agentIndex)
            self.agentImages[agentIndex] = (newState, image )
        else:
            image = self.drawGhost(newState, agentIndex)
            self.agentImages[agentIndex] = (newState, image )
        refresh

    def update(self, newState):
        global start
        agentIndex = newState._agentMoved
        agentState = newState.agentStates[agentIndex]

        if agentIndex == 0 and PAUSE_TIME > 0:
            sleep(PAUSE_TIME)
            refresh

        if self.agentImages[agentIndex][0].isPacman != agentState.isPacman: self.swapImages(agentIndex, agentState)
        prevState, prevImage = self.agentImages[agentIndex]
        if agentState.isPacman:
            self.animatePacman(agentState, prevState, prevImage)
        else:
            self.moveGhost(agentState, agentIndex, prevState, prevImage)
        self.agentImages[agentIndex] = (agentState, prevImage)

        if newState._foodEaten != None:
            self.removeFood(newState._foodEaten, self.food)
            if start==1:
                newState.score+=20
        if newState._capsuleEaten != None:
            self.removeCapsule(newState._capsuleEaten, self.capsules)

        self.infoPane.updateScore(newState.score)

    def make_window(self, width, height):
        grid_width = (width-1) * self.gridSize 
        grid_height = (height-1) * self.gridSize 
        screen_width = 2*self.gridSize + grid_width
        screen_height = 2*self.gridSize + grid_height + INFO_PANE_HEIGHT 
  
        begin_graphics(screen_width,    
                       screen_height,
                       BACKGROUND_COLOR,
                       "DNA Pac-Man")

    def drawPacman(self, pacman, index):
        position = pacman.getPosition()
        screen_point = self.to_screen(position)
        endpoints = self.getEndpoints(pacman.configuration.direction)
        return [circle(screen_point, PACMAN_SCALE * self.gridSize, 
                       color = PACMAN_COLORS[index],
                       filled = 1,
                       endpoints = endpoints,
                       width = 1)]
  
    def getEndpoints(self, direction, position=(0,0)):
        x, y = position
        pos = x - int(x) + y - int(y)
        width = 30 + 80 * math.sin(math.pi*pos)
  
        delta = width / 2
        if (direction == 'West'):
            endpoints = (180+delta, 180-delta)
        elif (direction == 'North'):
            endpoints = (90+delta, 90-delta)
        elif (direction == 'South'):
            endpoints = (270+delta, 270-delta)
        else:
            endpoints = (0+delta, 0-delta)
        return endpoints

    def movePacman(self, position, direction, image):
        screenPosition = self.to_screen(position)
        endpoints = self.getEndpoints( direction, position )
        r = PACMAN_SCALE * self.gridSize 
        moveCircle(image[0], screenPosition, r, endpoints)
        refresh

    def animatePacman(self, pacman, prevPacman, image):
        if FRAME_TIME > 0.01:
            start = time.time()
            fx, fy = prevPacman.configuration.getPosition()
            px, py = pacman.configuration.getPosition()
            frames = 4.0
            for i in range(int(frames)):
                pos = px*i/frames + fx*(frames-i)/frames, py*i/frames + fy*(frames-i)/frames 
                self.movePacman(pos, pacman.configuration.direction, image)
                # if time.time() - start > FRAME_TIME: return
                sleep(FRAME_TIME / 2 / frames)
        else:
            self.movePacman(pacman.configuration.pos, pacman.configuration.direction, image)


    def getGhostColor(self, ghost, ghostIndex):
        if ghost.scaredTimer > 0:
            return SCARED_COLOR
        else:
            return GHOST_COLORS[ghostIndex]
  
    def getGhostPos(self, ghost):
        # Overridden in FirstPersonGraphics
        return ghost.getPosition()

    def drawGhost(self, ghost, agentIndex):
        pos = self.getGhostPos(ghost)
        dir = ghost.configuration.direction
        (screen_x, screen_y) = (self.to_screen(pos) ) 
        coords = []          
        for (x, y) in GHOST_SHAPE:
            coords.append((x*self.gridSize*GHOST_SIZE + screen_x, y*self.gridSize*GHOST_SIZE + screen_y))

        colour = self.getGhostColor(ghost, agentIndex)
        body = polygon(coords, colour, filled = 1)
        WHITE = formatColor(1.0, 1.0, 1.0)
        BLACK = formatColor(0.0, 0.0, 0.0)

        dx = 0
        dy = 0
        if dir == 'North':
            dy = -0.2
        if dir == 'South':
            dy = 0.2
        if dir == 'East':
            dx = 0.2
        if dir == 'West':
            dx = -0.2
        leftEye = circle((screen_x+self.gridSize*GHOST_SIZE*(-0.3+dx/1.5), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy/1.5)), self.gridSize*GHOST_SIZE*0.2, WHITE)
        rightEye = circle((screen_x+self.gridSize*GHOST_SIZE*(0.3+dx/1.5), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy/1.5)), self.gridSize*GHOST_SIZE*0.2, WHITE)
        leftPupil = circle((screen_x+self.gridSize*GHOST_SIZE*(-0.3+dx), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy)), self.gridSize*GHOST_SIZE*0.08, BLACK)
        rightPupil = circle((screen_x+self.gridSize*GHOST_SIZE*(0.3+dx), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy)), self.gridSize*GHOST_SIZE*0.08, BLACK)
        ghostImageParts = []
        ghostImageParts.append(body)
        ghostImageParts.append(leftEye)
        ghostImageParts.append(rightEye)
        ghostImageParts.append(leftPupil)
        ghostImageParts.append(rightPupil)

        return ghostImageParts

    def moveEyes(self, pos, dir, eyes):
        (screen_x, screen_y) = (self.to_screen(pos) ) 
        dx = 0
        dy = 0
        if dir == 'North':
            dy = -0.2
        if dir == 'South':
            dy = 0.2
        if dir == 'East':
            dx = 0.2
        if dir == 'West':
            dx = -0.2
        moveCircle(eyes[0],(screen_x+self.gridSize*GHOST_SIZE*(-0.3+dx/1.5), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy/1.5)), self.gridSize*GHOST_SIZE*0.2)
        moveCircle(eyes[1],(screen_x+self.gridSize*GHOST_SIZE*(0.3+dx/1.5), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy/1.5)), self.gridSize*GHOST_SIZE*0.2)
        moveCircle(eyes[2],(screen_x+self.gridSize*GHOST_SIZE*(-0.3+dx), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy)), self.gridSize*GHOST_SIZE*0.08)
        moveCircle(eyes[3],(screen_x+self.gridSize*GHOST_SIZE*(0.3+dx), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy)), self.gridSize*GHOST_SIZE*0.08)
  
    def moveGhost(self, ghost, ghostIndex, prevGhost, ghostImageParts):
        old_x, old_y = self.to_screen(self.getGhostPos(prevGhost))
        new_x, new_y = self.to_screen(self.getGhostPos(ghost))
        delta = new_x - old_x, new_y - old_y

        for ghostImagePart in ghostImageParts:
            move_by(ghostImagePart, delta)
        refresh

        if ghost.scaredTimer > 0:
            color = SCARED_COLOR
        else:
            color = GHOST_COLORS[ghostIndex]
        edit(ghostImageParts[0], ('fill', color), ('outline', color))  
        self.moveEyes(self.getGhostPos(ghost), ghost.configuration.direction, ghostImageParts[-4:])
        refresh

    def finish(self):
        end_graphics()

    def to_screen(self, point):
        ( x, y ) = point
        #y = self.height - y
        x = (x + 1)*self.gridSize
        y = (self.height  - y)*self.gridSize
        return ( x, y )
  
    # Fixes some TK issue with off-center circles
    def to_screen2(self, point):
        ( x, y ) = point
        #y = self.height - y
        x = (x + 1)*self.gridSize
        y = (self.height  - y)*self.gridSize
        return ( x, y )

    def drawWalls(self, wallMatrix):
        for xNum, x in enumerate(wallMatrix):
            for yNum, cell in enumerate(x):
                if cell: # There's a wall here
                    pos = (xNum, yNum)
                    screen = self.to_screen(pos)
                    screen2 = self.to_screen2(pos)

                    # draw each quadrant of the square based on adjacent walls
                    wIsWall = self.isWall(xNum-1, yNum, wallMatrix)
                    eIsWall = self.isWall(xNum+1, yNum, wallMatrix)
                    nIsWall = self.isWall(xNum, yNum+1, wallMatrix)
                    sIsWall = self.isWall(xNum, yNum-1, wallMatrix)
                    nwIsWall = self.isWall(xNum-1, yNum+1, wallMatrix)
                    swIsWall = self.isWall(xNum-1, yNum-1, wallMatrix)
                    neIsWall = self.isWall(xNum+1, yNum+1, wallMatrix)
                    seIsWall = self.isWall(xNum+1, yNum-1, wallMatrix)

                    # NE quadrant
                    if (not nIsWall) and (not eIsWall):
                        # inner circle
                        circle(screen2, WALL_RADIUS * self.gridSize, WALL_COLOR, 0, (0,91), 'arc')
                    if (nIsWall) and (not eIsWall):
                        # vertical line
                        line(add(screen, (self.gridSize*WALL_RADIUS, 0)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-0.5)-1)), WALL_COLOR)
                    if (not nIsWall) and (eIsWall):
                        # horizontal line
                        line(add(screen, (0, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(-1)*WALL_RADIUS)), WALL_COLOR)
                    if (nIsWall) and (eIsWall) and (not neIsWall):
                        # outer circle
                        circle(add(screen2, (self.gridSize*2*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, WALL_COLOR, 0, (180,271), 'arc')
                        line(add(screen, (self.gridSize*2*WALL_RADIUS-1, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(-1)*WALL_RADIUS)), WALL_COLOR)
                        line(add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS+1)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-0.5))), WALL_COLOR)

                    # NW quadrant
                    if (not nIsWall) and (not wIsWall):
                        # inner circle
                        circle(screen2, WALL_RADIUS * self.gridSize, WALL_COLOR, 0, (90,181), 'arc')
                    if (nIsWall) and (not wIsWall):
                        # vertical line
                        line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, 0)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-0.5)-1)), WALL_COLOR)
                    if (not nIsWall) and (wIsWall):
                        # horizontal line
                        line(add(screen, (0, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5)-1, self.gridSize*(-1)*WALL_RADIUS)), WALL_COLOR)
                    if (nIsWall) and (wIsWall) and (not nwIsWall):
                        # outer circle
                        circle(add(screen2, (self.gridSize*(-2)*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, WALL_COLOR, 0, (270,361), 'arc')
                        line(add(screen, (self.gridSize*(-2)*WALL_RADIUS+1, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5), self.gridSize*(-1)*WALL_RADIUS)), WALL_COLOR)
                        line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS+1)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-0.5))), WALL_COLOR)

                    # SE quadrant
                    if (not sIsWall) and (not eIsWall):
                        # inner circle
                        circle(screen2, WALL_RADIUS * self.gridSize, WALL_COLOR, 0, (270,361), 'arc')
                    if (sIsWall) and (not eIsWall):
                        # vertical line
                      line(add(screen, (self.gridSize*WALL_RADIUS, 0)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(0.5)+1)), WALL_COLOR)
                    if (not sIsWall) and (eIsWall):
                        # horizontal line
                        line(add(screen, (0, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(1)*WALL_RADIUS)), WALL_COLOR)
                    if (sIsWall) and (eIsWall) and (not seIsWall):
                        # outer circle
                        circle(add(screen2, (self.gridSize*2*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, WALL_COLOR, 0, (90,181), 'arc')
                        line(add(screen, (self.gridSize*2*WALL_RADIUS-1, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5, self.gridSize*(1)*WALL_RADIUS)), WALL_COLOR)
                        line(add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS-1)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(0.5))), WALL_COLOR)

                    # SW quadrant
                    if (not sIsWall) and (not wIsWall):
                        # inner circle
                        circle(screen2, WALL_RADIUS * self.gridSize, WALL_COLOR, 0, (180,271), 'arc')
                    if (sIsWall) and (not wIsWall):
                        # vertical line
                        line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, 0)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(0.5)+1)), WALL_COLOR)
                    if (not sIsWall) and (wIsWall):
                        # horizontal line
                        line(add(screen, (0, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5)-1, self.gridSize*(1)*WALL_RADIUS)), WALL_COLOR)
                    if (sIsWall) and (wIsWall) and (not swIsWall):
                        # outer circle
                        circle(add(screen2, (self.gridSize*(-2)*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, WALL_COLOR, 0, (0,91), 'arc')
                        line(add(screen, (self.gridSize*(-2)*WALL_RADIUS+1, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5), self.gridSize*(1)*WALL_RADIUS)), WALL_COLOR)
                        line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS-1)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(0.5))), WALL_COLOR)

    def isWall(self, x, y, walls):
        if x < 0 or y < 0:
            return False
        if x >= walls.width or y >= walls.height:
            return False
        return walls[x][y]

    def drawFood(self, foodMatrix ):
        foodImages = []
        for xNum, x in enumerate(foodMatrix):
            imageRow = []
            foodImages.append(imageRow)
            for yNum, cell in enumerate(x):
                if cell: # There's food here
                    screen = self.to_screen((xNum-.25, yNum+.4 ))
                    a=random.choice(FOOD_BANK)
                    b=COLOR_BANK[a]
                    dot = text( screen,
                            color = b,
                            contents=a,
                            font='Arial', size=20, style='normal')
                    food_matrix[xNum,yNum]=a
                    imageRow.append(dot)
                else:
                    imageRow.append(None)
        return foodImages

    def drawCapsules(self, capsules ):
        capsuleImages = {}
        for capsule in capsules:
            ( screen_x, screen_y ) = self.to_screen(capsule)
            dot = circle( (screen_x, screen_y), 
                          CAPSULE_SIZE * self.gridSize, 
                          color = CAPSULE_COLOR, 
                          filled = 1,
                          width = 1)
            capsuleImages[capsule] = dot
        return capsuleImages

    def removeFood(self, cell, foodImages ):
        global start
        global AMINO_BANK
        global CODON_BANK
        global codon_string
        global amino_string
        x, y = cell
        remove_from_screen(foodImages[x][y])
        CODON_BANK.append(str((food_matrix[x,y])))
        if food_matrix[x,y]!="" and food_matrix[x,y]!=" ":
            codon_string+=str(food_matrix[x,y])
        if (codon_string[-3:]=="AUG" and start==0) or (codon_string[-3:]=="AUG" and start==1 and len(codon_string)%3==0):
            print("START!")
            start=1
            codon_string=""
            del CODON_BANK[:]
            amino_string="M"
        if food_matrix[x,y]!="" and food_matrix[x,y]!=" ":
            pass
  #      print str((food_matrix[x, y]))
        if start==1 and len(CODON_BANK)>2:
            codon_string=""
            for i in CODON_BANK:
                codon_string+=str(i)
            del CODON_BANK[:]
            amino_acids=[codon_string[i:i+3] for i in range(0, len(codon_string), 3)]
            for i in amino_acids:
                if i in AMINO_BANK:
                    amino_string+=AMINO_BANK[i]
                    print("AMINO ACID " + str(amino_string))
                else:
                    start=0
                    ALL_ACIDS.append(amino_string)
                    del CODON_BANK[:]
                    codon_string=""
                    amino_string="M"
                    break
                if amino_string[-1]=="*":
                    start=0
                    ALL_ACIDS.append(amino_string)
                    del CODON_BANK[:]
                    codon_string=""
                    amino_string="M"
                    break
  

    def removeCapsule(self, cell, capsuleImages ):
        x, y = cell
        remove_from_screen(capsuleImages[(x, y)])

    def drawExpandedCells(self, cells):
        """
        Draws an overlay of expanded grid positions for search agents
        """
        n = float(len(cells))
        baseColor = [1.0, 0.0, 0.0]
        self.clearExpandedCells()
        self.expandedCells = []
        for k, cell in enumerate(cells):
            screenPos = self.to_screen( cell)
            cellColor = formatColor(*[(n-k) * c * .5 / n + .25 for c in baseColor])
            block = square(screenPos, 
                    0.5 * self.gridSize, 
                    color = cellColor, 
                    filled = 1, behind=True)
            self.expandedCells.append(block)

    def clearExpandedCells(self):
        if 'expandedCells' in dir(self) and len(self.expandedCells) > 0:
            for cell in self.expandedCells:
                remove_from_screen(cell)

class FirstPersonPacmanGraphics(PacmanGraphics):
    def __init__(self, zoom = 1.0, showGhosts = False):
        PacmanGraphics.__init__(self, zoom)
        self.showGhosts = showGhosts

    def initialize(self, state):

      PacmanGraphics.startGraphics(self, state)
      # Initialize distribution images
      walls = state.layout.walls
      dist = []
      self.layout = state.layout
  
      for x in range(walls.width):
          distx = []
          dist.append(distx)
          for y in range(walls.height):
              ( screen_x, screen_y ) = self.to_screen( (x, y) )
              block = square( (screen_x, screen_y), 
                            0.5 * self.gridSize, 
                            color = BACKGROUND_COLOR, 
                            filled = 1)
              distx.append(block)
      self.distributionImages = dist
  
      # Draw the rest
      self.drawStaticObjects(state)
      self.drawAgentObjects(state)
  
      # Information
      self.previousState = state

    def updateDistributions(self, distributions):
        for x in range(len(self.distributionImages)):
            for y in range(len(self.distributionImages[0])):
                image = self.distributionImages[x][y]
                weights = [dist.getCount( (x,y) ) for dist in distributions]

                if sum(weights) != 0:
                    pass
                # Fog of war
                color = [0.0,0.0,0.0]
                for weight, gcolor in zip(weights, GHOST_VEC_COLORS[1:]):
                    color = [min(1.0, c + 0.95 * g * weight ** .3) for c,g in zip(color, gcolor)]
                changeColor(image, formatColor(*color))
        refresh

    def lookAhead(self, config, state):
        if config.getDirection() == 'Stop':
            return
        else:
            pass
        # Draw relevant ghosts
        allGhosts = state.getGhostStates()
        visibleGhosts = state.getVisibleGhosts()
        for i, ghost in enumerate(allGhosts):
              if ghost in visibleGhosts:
                  self.drawGhost(ghost, i)
              else:
                  self.currentGhostImages[i] = None
  
    def getGhostColor(self, ghost, ghostIndex):
        return GHOST_COLORS[ghostIndex]
  
    def getGhostPos(self, ghostState):
        if not self.showGhosts and ghostState.getPosition()[1] > 1:
            return (-1000, -1000)
        else:
            return ghostState.getPosition()

def add(x, y):
  return (x[0] + y[0], x[1] + y[1])
