import pygame as py
import random 

py.init()

screenWidth = 600
screenHeight = 600

screen = py.display.set_mode((screenWidth,screenHeight))
py.display.set_caption("Snake")

#define game variable
cell_size = 10
direction = 1 # 1 = Up , 2 = Right 3 = Down , 4 = Left
update_snake = 0 
food = [0,0]
newFood = True
newPiece = [0,0]
score = 0
gameOver = False
clicked  = False

#create snake
snake_pos = [[int(screenWidth / 2), int(screenHeight / 2)]]
snake_pos.append([int(screenWidth / 2), int(screenHeight / 2) + cell_size])
snake_pos.append([int(screenWidth / 2), int(screenHeight / 2) + cell_size*2])
snake_pos.append([int(screenWidth / 2), int(screenHeight / 2) + cell_size*3])

#define font
font = py.font.SysFont(None , 35 )

# again button 
againRect = py.Rect(screenWidth / 2 - 80 , screenHeight / 2 + 15 , 200 , 50)

#define colours
bg = (255 , 200 ,150)
bodyOuter = (100, 100, 200)
bodyInner = (50, 175, 25)
foodCol = (0, 0, 0)
red = (255 ,0 ,0)
blue = (0,0,255)

def drawScreen() :
    screen.fill(bg)

def drawScore() :
    scoreText = " Score : " + str(score)
    scoreImg = font.render(scoreText , True , blue)
    screen.blit(scoreImg, (0,0))

def checkGameOver(gameOver) :
    if gameOver == False :
        
        # if snake has eaten itself
        headCount = 0
        for segment in snake_pos:
            if snake_pos[0] == segment and headCount > 0:
                gameOver = True
            headCount += 1
            
        # if snake has gone off the screen : out of bounds 
        if snake_pos[0][0] < 0 or snake_pos[0][0] > screenWidth or snake_pos[0][1] < 0 or snake_pos[0][1] > screenHeight :
            gameOver = True
            
        return gameOver

def drawGameOver() :
    overText = " GAME OVER !!! "
    overImg = font.render(overText,True , red)
    py.draw.rect(screen , blue , (screenWidth / 2 - 80 , screenHeight / 2 - 60 , 200 , 50))
    screen.blit(overImg , (screenWidth / 2 - 80 , screenHeight / 2 - 50))

    againText = " PLAY AGAIN ? "
    againImg = font.render(againText, True , red)
    py.draw.rect(screen , blue , againRect)
    screen.blit(againImg , (screenWidth / 2 - 75 , screenHeight / 2 + 30))

run = True
while run :

    drawScreen()
    drawScore()

    for events in py.event.get() : 
        if events.type == py.QUIT :
            run = False
        elif events.type == py.KEYDOWN :
            if events.key == py.K_UP and direction != 3 :
                direction = 1
            if events.key == py.K_RIGHT and direction != 4 :
                direction = 2
            if events.key == py.K_DOWN and direction != 1 :
                direction = 3
            if events.key == py.K_LEFT and direction != 2 :
                direction = 4
    
    # create food
    if newFood == True:
        newFood = False
        food[0] = cell_size * random.randint(0, int(screenWidth / cell_size) - 1) 
        food[1] = cell_size * random.randint(0, int(screenHeight / cell_size) - 1)
    
    #draw food
    py.draw.rect(screen , foodCol , (food[0], food[1] , cell_size , cell_size))

    #collision detection 
    if snake_pos[0] == food :
        newFood = True
        # create new piece
        newPiece = list(snake_pos[-1])
        if direction == 1 :
            newPiece[1] += cell_size
        if direction == 3 :
            newPiece[1] -= cell_size
        if direction == 2 :
            newPiece[0] -= cell_size
        if direction == 4 :
            newPiece[0] += cell_size
        
        #add the new piece 
        snake_pos.append(newPiece)
        score += 1

    if gameOver == False :
        if update_snake > 99 :
            update_snake = 0 
            snake_pos = snake_pos[-1:] + snake_pos[:-1]
            if direction == 1 :
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] - cell_size
            if direction == 3 :
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] + cell_size
            if direction == 2 :
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] + cell_size
            if direction == 4 :
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] - cell_size
            gameOver = checkGameOver(gameOver)

    if gameOver == True :
        drawGameOver()
        if events.type == py.MOUSEBUTTONDOWN and clicked == False :
            clicked  = True
        if events.type == py.MOUSEBUTTONUP and clicked == True :
            clicked  = False
            pos = py.mouse.get_pos()
            if againRect.collidepoint(pos) == True :
                #variable reset 
                cell_size = 10
                direction = 1 # 1 = Up , 2 = Right 3 = Down , 4 = Left
                update_snake = 0 
                food = [0,0]
                newFood = True
                newPiece = [0,0]
                score = 0
                gameOver = False

                #create snake
                snake_pos = [[int(screenWidth / 2), int(screenHeight / 2)]]
                snake_pos.append([int(screenWidth / 2), int(screenHeight / 2) + cell_size])
                snake_pos.append([int(screenWidth / 2), int(screenHeight / 2) + cell_size*2])
                snake_pos.append([int(screenWidth / 2), int(screenHeight / 2) + cell_size*3])

    # draw snake
    head = 1
    for x in snake_pos :
        if head == 0 :
            py.draw.rect(screen , bodyOuter , (x[0] , x[1],cell_size,cell_size))
            py.draw.rect(screen , bodyInner , (x[0] + 1 , x[1] + 1,cell_size - 2 ,cell_size - 2))
        elif head == 1 :
            py.draw.rect(screen , bodyOuter , (x[0] , x[1],cell_size,cell_size))
            py.draw.rect(screen , red , (x[0] + 1 , x[1] + 1,cell_size - 2 ,cell_size - 2))
            head = 0

    update_snake += 1
    py.display.update()

py.quit()
