from enum import Enum
import sys, random
import pygame

#window size
frameWidth = 640
frameHeight = 640
squareSize = 40

#colors
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
blue = pygame.Color(0, 50, 255)
green = pygame.Color(0, 155, 0)
white = pygame.Color(255, 255, 255)
grey = pygame.Color(128, 128, 128)

#game logic
class Dir(Enum):
    """Directions"""
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    UP = "UP"
    DOWN = "DOWN"

class Snake(object):
    """The snake class"""
    def __init__(self, 
                dir=Dir.RIGHT,
                headX = random.randint(1, frameWidth//squareSize) * squareSize - squareSize,
                headY = random.randint(1, frameHeight//squareSize) * squareSize - squareSize,
                ):
        self.head = [headX, headY]
        self.body = []  #body doesn't include head
        self.length = len(self.body) #length doesn't include head
        self.direction = dir

    def move(self, dir=None):
        """Moves the snake in a given direction"""
        if(dir is None):
            dir = self.direction    #use previous direction
        #set new direction
        self.direction = dir

        x, y = 0, 0     #variables to update head and body posX and posY
        # x -> horizontal directions, y -> vertical directions
        if(dir == Dir.RIGHT):
            x = squareSize
            y = 0
        elif(dir == Dir.LEFT):
            x = -squareSize
            y = 0
        elif(dir == Dir.UP):
            x = 0
            y = -squareSize
        elif(dir == Dir.DOWN):
            x = 0
            y = squareSize

        #move snake from last body element to head
        if (self.length > 0):
            for i in range(self.length-1, 0, -1):
                self.body[i][0] = self.body[i-1][0]
                self.body[i][1] = self.body[i-1][1]

            self.body[0][0] = self.head[0]
            self.body[0][1] = self.head[1]
        
        self.head[0] += x
        self.head[1] += y
                
        #checking if snake is out of frame
        self.outOfBounds()
    
    def eat(self, food):
        """snake eats food"""
        self.length += food.value
        if(not self.body):  #empty body
            for i in range(0, food.value, 1):
                tmp = self.head.copy()
                self.body.append(tmp)
        else:
            for i in range(0, food.value, 1):
                tmp = self.body[-1].copy()
                self.body.append((tmp))

        food.disappear()

    def damage(self):
        """snake bites herself. True -> bitten, False -> not bitten"""
        for k in self.body:
            if([k[0], k[1]] == self.head):
                return True
        return False

    def outOfBounds(self):
        """check if snakes head is out of bounds"""
        if(self.head[0] < 0):
            self.head[0] = frameWidth - squareSize
        elif(self.head[0] > frameWidth - squareSize):
            self.head[0] = 0
        elif(self.head[1] < 0):
            self.head[1] = frameHeight - squareSize
        elif(self.head[1] > frameHeight - squareSize):
            self.head[1] = 0


class Food(object):
    """General food class. Can be considered as abstract, since only subclasses will be used"""
    def __init__(self):
        self.posX = random.randint(1, frameWidth//squareSize) * squareSize - squareSize
        self.posY = random.randint(1, frameHeight//squareSize) * squareSize - squareSize
        self.visible = True
    
    def disappear(self):
        """make the eaten food disappear"""
        self.visible = False

    def spawnNew(self):
        """spawn new food"""
        self.posX = random.randint(1, frameWidth//squareSize) * squareSize - squareSize
        self.posY = random.randint(1, frameHeight//squareSize) * squareSize - squareSize
        self.visible = True
        return self

class Apple(Food):
    def __init__(self):
        super().__init__()
        self.value = 1
        self.color = red

class Mouse(Food):
    def __init__(self):
        super().__init__()
        self.value = 2
        self.color = grey


############################################################################
pygame.init()
screen = pygame.display.set_mode((frameWidth, frameHeight), pygame.SCALED)
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
fps = 10

background = pygame.Surface(screen.get_size())
background = background.convert()


snake = Snake()
apple = Apple()
mouse = Mouse()

def spawnFood():
    rdn = random.randint(0,30)
    if(rdn <= 20):
        food = apple.spawnNew()
    elif(rdn > 20):
        food = mouse.spawnNew()
    return food

#main loop
going = True
foodSpawn = True
while going:
    dir = None  #init direction
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            going == False
            pygame.quit()
            sys.exit()
        elif(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            going == False
            pygame.quit()
            sys.exit()
        elif(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_RIGHT and snake.direction != Dir.LEFT):
                dir = Dir.RIGHT
            elif(event.key == pygame.K_LEFT and snake.direction != Dir.RIGHT):
                dir = Dir.LEFT
            elif(event.key == pygame.K_UP and snake.direction != Dir.DOWN):
                dir = Dir.UP
            elif(event.key == pygame.K_DOWN and snake.direction != Dir.UP):
                dir = Dir.DOWN

    #move snake
    snake.move(dir)

    #spawn food
    if(foodSpawn):
        food = spawnFood()
        foodSpawn = False

    #check if food can be eaten
    if(snake.head == [food.posX, food.posY] and food.visible):
        snake.eat(food)
        foodSpawn = True    #make food spawn again
    else:
        #check for snake biting herself
        if(snake.damage()):
            snake.__init__(dir=snake.direction, headX=snake.head[0], headY=snake.head[1])

    #draw background
    screen.fill(black)
    #draw snake's body
    for pos in snake.body:
        pygame.draw.rect(screen, green, pygame.Rect(
            pos[0] + 2,
            pos[1] + 2,
            squareSize - 4,
            squareSize - 4,
        ))
    #draw snake's head
    pygame.draw.rect(screen, blue, pygame.Rect(
        snake.head[0] + 2,
        snake.head[1] + 2,
        squareSize - 4,
        squareSize - 4,
    ))
    #draw food
    if(food.visible):
        pygame.draw.rect(screen, food.color, pygame.Rect(
            food.posX,
            food.posY,
            squareSize,
            squareSize,
        ))
	
    pygame.display.update()
    clock.tick(fps)