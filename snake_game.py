import pygame, sys, random
from pygame.math import Vector2 #We import Vector2 lonely for can call it without put pygame.math.Vector2() and only use Vector2()

pygame.mixer.pre_init(44100,-16,2,512) #The params are too technicals, so this only makes the game pre init the sounds to make them sound at right time.

pygame.init()
cell_size = 25 
cell_number = 25
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
#With this we put the size of the screen, we multiply the number of cells that we want, and the size of each one, (in this case 25px)
#So the BOARD is 25*25 pixels. (625x625 Pixels)
#Here we create cells, BECAUSE THIS GAME NEEDS THEM, but in onother case, we only put the pixels. 

pygame.display.set_caption('Snake Game - By Feduski :)') #This is the caption of the window.
clock = pygame.time.Clock() #We create a clock object 

#With this i could load the apple image:
#apple = pygame.image.load('graphics/apple.png').convert_alpha() 

#But because of apple's resolution, i have to scale it to the cell size, so i have to do this:
#apple = pygame.transform.scale(apple,(cell_size,cell_size)) 
#Giving the image like parameter and the cell size (x and y) to transform the scale of the screen/board. 
#To save lines of code, i put the 'pygame.image.load' etc in the transform method. It do it shorter. 

apple = pygame.transform.scale(pygame.image.load('graphics/apple.png').convert_alpha(),(cell_size,cell_size)) 
game_font = pygame.font.Font('fonts/game-font.ttf', 20) #Imports the game font.
restart_font  = pygame.font.Font('fonts/game-font.ttf', 15) #Import the restart game font (this only change the size).
SCREEN_UPDATE = pygame.USEREVENT #Every time that there is an event.
pygame.time.set_timer(SCREEN_UPDATE, 90) #Each 90 miliseconds, the screen updates. 

class FRUIT:
    def __init__(self):
        self.randomize() #Create a new fruit, in a random place.
    
    def randomize(self):
        self.x = random.randint(0, (cell_number) -1) #Gives a random number from 0 to the quantity of cells. 
        #We are talking about the X and Y coord from the TOP LEFT, so don't need negatives numbers. 
        #The -1 es because INCLUDES all the cell number, so if we don't substract 1, the fruit can spawn 1 cell out of the screen.
        #|------- The 0 starts on the top left corner, so every number is gonna be positive. 
        #|0 x1 x2 x3
        #|y1 * * *
        #|y2 * * *
        #|y3 * * *
        self.y = random.randint(0, (cell_number) -1)
        self.pos = Vector2(self.x, self.y)  #Creates a Vector with the self.x and self.y values.

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size) 
        #Rect meeds (x pos, y pos, width px, height px)
        #So: The width and height is gonna be our cell_size, to fill ALL the size of the cell.
        #The pos is gonna be our X or Y pos, multiplied per our cell size because if we only put a position X or Y, it's gonna be on PIXELS
        #and how we use cells for our game, we have to resize the positions to cell size. 
        #For ex: If we have 5 px on Y coord, the fruit is gonna be only 5px on Y coord and it isn't the center of a cell.
        #But if we multiply it for the px of a cell(cell_size), fruit is gonna be 5 CELLS POSITIONS on the Y coord.
        screen.blit(apple, fruit_rect) #Here we put the apple the texture, with the rect recently created. 

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)] #We create a initial body, with that coords. 
        self.direction = Vector2(0,0) #We create a default direction. When the player makes an input, it will change.
        self.new_block = False #We set new_block False as default, to modify it later. 

        #Here we load every texture of the snake.
        self.head_up = pygame.transform.scale(pygame.image.load('graphics/head_up.png').convert_alpha(),(cell_size,cell_size)) 
        self.head_down = pygame.transform.scale(pygame.image.load('graphics/head_down.png').convert_alpha(),(cell_size,cell_size)) 
        self.head_right = pygame.transform.scale(pygame.image.load('graphics/head_right.png').convert_alpha(),(cell_size,cell_size)) 
        self.head_left = pygame.transform.scale(pygame.image.load('graphics/head_left.png').convert_alpha(),(cell_size,cell_size)) 

        self.tail_up = pygame.transform.scale(pygame.image.load('graphics/tail_up.png').convert_alpha(),(cell_size,cell_size)) 
        self.tail_down = pygame.transform.scale(pygame.image.load('graphics/tail_down.png').convert_alpha(),(cell_size,cell_size)) 
        self.tail_right = pygame.transform.scale(pygame.image.load('graphics/tail_right.png').convert_alpha(),(cell_size,cell_size)) 
        self.tail_left = pygame.transform.scale(pygame.image.load('graphics/tail_left.png').convert_alpha(),(cell_size,cell_size)) 

        self.body_vertical = pygame.transform.scale(pygame.image.load('graphics/body_vertical.png').convert_alpha(),(cell_size,cell_size)) 
        self.body_horizontal = pygame.transform.scale(pygame.image.load('graphics/body_horizontal.png').convert_alpha(),(cell_size,cell_size)) 

        self.body_tr = pygame.transform.scale(pygame.image.load('graphics/body_tr.png').convert_alpha(),(cell_size,cell_size)) 
        self.body_tl = pygame.transform.scale(pygame.image.load('graphics/body_tl.png').convert_alpha(),(cell_size,cell_size)) 
        self.body_br = pygame.transform.scale(pygame.image.load('graphics/body_br.png').convert_alpha(),(cell_size,cell_size)) 
        self.body_bl = pygame.transform.scale(pygame.image.load('graphics/body_bl.png').convert_alpha(),(cell_size,cell_size)) 

        self.crunch_sound = pygame.mixer.Sound('sounds/crunch.wav') #Here we import the crunch sound.

    def draw_snake(self):
        self.update_head_graphics() #We update the head graphics.
        self.update_tail_graphics() #We update the tail graphics.

        for ind, block in enumerate(self.body): #For each part of the snake (each block)
            x_pos = int(block.x * cell_size) #Sets an X position multiplied * cell_size to talk about cells positions.
            y_pos = int(block.y * cell_size) #Sets an Y position ""  ""  ""  ""  ""  ""  ""  ""  ""  ""  ""  ""  "" 
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size) #We create a rect with the pos and size of the currently block
            
            #Here we update the head graphics
            if ind == 0: #If we are talking about the head:
                screen.blit(self.head, block_rect) #Put the texture that corresponds.

            elif ind == (len(self.body) - 1): #If we are talking about the tail:
                screen.blit(self.tail, block_rect) #Put the texture that corresponds.

            else: #Else (the rest of the body)
                previous_block = self.body[ind +1] - block #Here we get the PREVIUOS block on the SNAKE. 
                #We substract the current block, to know if the snake is going to left, right, top or down.
                next_block = self.body[ind -1] - block #Here we get the NEXT block in the SNAKE. 
                if previous_block.x == next_block.x: #If the X of previous and next block are the same, 
                    #means that the snake is going vertical.
                    #Ex: [(5,10), (5,11), (5,12)]
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    #And if the Y are the same, it is because the snake is going horizontal.
                    #Ex: [(5,10), (4,10), (3,10)]
                    screen.blit(self.body_horizontal, block_rect)
                else: 
                    #Too many to explain in code, but when we declare previous_block and next_block, and rest 'block',
                    #we let in next_block and previous_block a X and Y value of 0/1/-1. 
                    #And each combination, represents a turn of the snake. 
                    #All is explained in my notebook.
                    if next_block.x == -1 and previous_block.y == -1 or next_block.y == -1 and previous_block.x == -1: 
                        screen.blit(self.body_tl, block_rect)
                    
                    elif next_block.x == -1 and previous_block.y == 1 or next_block.y == 1 and previous_block.x == -1:
                        screen.blit(self.body_bl, block_rect)

                    elif next_block.x == 1 and previous_block.y == 1 or next_block.y == 1 and previous_block.x == 1:
                        screen.blit(self.body_br, block_rect)
                    
                    else: 
                        screen.blit(self.body_tr, block_rect)

    def update_head_graphics(self):
            #Here we catch the direction that the user inputs, and make the snake looks there.
            if main_game.snake.direction == Vector2(1, 0) or main_game.snake.direction == Vector2(0, 0): self.head = self.head_right 
            #If the snake direction is going RIGHT or it is the INITIAL posture.
            elif main_game.snake.direction == Vector2(-1, 0): self.head = self.head_left
            elif main_game.snake.direction == Vector2(0, -1): self.head = self.head_up 
            elif main_game.snake.direction == Vector2(0, 1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1] #We do this to know the direction, the rest of the ante-last element 
        #minus the last element, returns the position on Vector (0,1)up (0,-1)down (1,0)left (-1,0)right. of the ante-last block, 
        #and knowing this, we can know where we have to turn the tail.
        if tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def has_to_move(self):
        if not self.direction == Vector2(0,0) : return True #If the direction isn't 0,0 that means, it has to move.

    def move_snake(self):
        if self.new_block == True: #If there is a new block, then:
            body_copy = self.body[:] #We create a copy of the entire body.
            body_copy.insert(0, body_copy[0] + self.direction) #To the copy, we insert on the first position, a NEW position
            #for the snake head,it gonna be the actual position of the snake head, but adding it the direction (a vector that contains
            #a 1/-1 for x/y and what will do the snake move it).
            self.body = body_copy[:] #Now the real body is the body copy (with a larger snake). 
            self.new_block = False #And there isn't a new block to place. 

        else: #If there isn't a new block, then:
            body_copy = self.body[:-1] #We create a copy of the entire body WITHOUT the LAST body part
            #this because we aren't moving, else we are renovating the positions.
            #So we delete the last part of the snake, and create a new one on the head, so we increase the large of the 
            #snake on the beginning but we diminish the large on the final. Finally it makes the
            #ilussion that the snake is moving.
            body_copy.insert(0, body_copy[0] + self.direction) #Create a new block on the head, adding 1 position like before.
            self.body = body_copy[:] #Now the real body is the body copy.

    def add_block(self): 
        self.new_block = True #Sets new_block boolean to True, to enter on the If in the moving of the snake, and add a new one.

    def play_crunch_sound(self):
        self.crunch_sound.play() #Plays the crunch sound.

class MAIN:
    def __init__(self):
        self.snake = SNAKE() #We create our snake.
        self.fruit = FRUIT() #We create our fruit.
        self.score = 0 #Predeterminates a score of 0.
        self.still_alive = True #Predeterminates if the player stills alive, if the player loses, it changes.
        self.game_over_sound = pygame.mixer.Sound('sounds/game_over_sound.wav') #Imports the game_over_sound.

    def update(self):
        if self.still_alive: #If the player stills alive.
            if self.snake.has_to_move(): #If the snake has to move, move it, and start checking collisions, fails, etc.
                self.snake.move_snake() 
                self.checks()

    def checks(self): 
        #Border fail
        if not 0 <= self.snake.body[0].x < (cell_number) or not 0 <= self.snake.body[0].y < (cell_number):
        #If the head of snake X or Y position ISN'T between 0 and the cell number (if it is OUT the board), Game Over.
            self.game_over_sound.play()
            self.still_alive = False

        #Auto-contact fail
        for block in self.snake.body[1:]: #We iterate every block on the snake, except the head. Every block represents a Vector 
        #(position x and y)if the vector is the same of the vector of the head, then: Game Over.
            if block == self.snake.body[0]: 
                self.game_over_sound.play()
                self.still_alive = False
        
        #Collision snake-fruit
        if self.fruit.pos == self.snake.body[0]: #If the position of the fruit is the same of the head of the snake, then:
            self.fruit.randomize() #Create a new fruit on a random place.
            self.snake.add_block() #Add a new block to the snake.
            self.score +=1 #Adds 1 point to score.
            self.snake.play_crunch_sound() #Plays the sound.

        #Bad fruit spawning
        for block in self.snake.body[1:]: #For each block of the snake, except the head:
            if self.fruit.pos == block: #If the position of the fruit, is equal to each block position:
                self.fruit.randomize() #Respawns the fruit.        

    def draw_game_over(self):
        #Sets the texts.
        go_text = 'Game Over'
        go_score_text = f'Score: {self.score}' 
        press_r_text = 'Press R to restart'
        #Renders the texts and creates the surfaces.
        go_surface = game_font.render(go_text, True, (50,0,100))
        go_score_surface = game_font.render(go_score_text, True, (50,0,100)) 
        press_r_surface = restart_font.render(press_r_text, True, (255,0,100)) 
        #Declares the positions to be placed.
        go_x = int((cell_size * cell_number)//2) 
        go_y = int(((cell_size * cell_number)//2)-10)
        #Creates the rect to place everything. 
        go_rect = go_surface.get_rect(center = (go_x, go_y))
        #Places the texts.
        screen.blit(go_surface, go_rect)
        screen.blit(go_score_surface, go_rect.bottomleft)
        screen.blit(press_r_surface, (go_x - 75, go_y + go_rect.height + go_score_surface.get_height()))

        self.still_alive = False #Sets to false to delete everything in the screen.

    def draw_elements(self): 
        if self.still_alive: #Draw the elements on the screen if the player stills alive.
            self.draw_grass()
            self.fruit.draw_fruit() 
            self.snake.draw_snake()    
            self.draw_score()    
        else: #Else, draw only the game over screen.
            self.draw_game_over()

    def draw_grass(self):
        grass_color = (167,209,61) #Sets a grass color.
        #Here we are gonna travel around every single cell, and paint it. 
        #For this, we are calling the coord of the Y lines of cells to ROW. Each row respresents a VERTICAL position.
        #And the coords of X, are gonna be COL. Each col represents a HORIZONTAL position.

        #So we are multiplying the ROW and the COL, per the cell size, to move per cell measures.
        #ROW 0 represents 25 pixels on Y coord, ROW 1 --> 50 pixels on Y, ROW 2 --> 75 pixels, etc.
        #COL 0 represents 25 pixels on X coord, COL 1 --> 50 pixels on X, COL 2 --> 75 pixels, etc.
       
        #We are painting one cell yes and one cell no. ---> For this, we are painting ONLY if it is an even number, 
        #or if the row number is odd, we are painting the cell if it is odd.
        #(This to move one position the painted cell, else, it will be a vertical lines checkerboard).

        for row in range(cell_number): #For each vertical cell:
            if row % 2 == 0: #If the row is even:
                for col in range(cell_number): #For each horizontal cell in a even row: 
                    if col % 2 == 0: #For painting a cell yes, a cell no.
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size) 
                        #Rect(x,y,w,h) width and height of cell size, and X & Y coords, depends of the ROWS and COLS that we are talking about.                        
                        pygame.draw.rect(screen, grass_color, grass_rect) #Draw it on screen, with a green color, based on grass_rect.
            else: #If the row is odd:
                for col in range(cell_number): #For each horizontal cell in a odd row: 
                    if col % 2 != 0: #For painting a cell no, a cell yes.
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size) #The same of above. 
                        pygame.draw.rect(screen, grass_color, grass_rect) #Draw it on screen, with a green color, based on grass_rect.

    def draw_score(self):
        score_text = 'Score: ' + str(self.score) #We call the text of our score, converting it on STRING.
        score_surface = game_font.render(score_text, True, (51,0,102)) #Creates the surface of the score.
        score_x = int(cell_size * cell_number - 60) #Puts an X coord, -60 to place it far from the border.
        score_y = int(cell_size * cell_number - 610) #Puts and Y coord, -40 to place it far from the border.
        score_rect = score_surface.get_rect(center = (score_x, score_y)) #Creates the rect of the score, to give it a position.
        screen.blit(score_surface, score_rect) #Puts the score on the screen.

main_game = MAIN() #We create an object of the main class.

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #If the player press the close button, it closes the windows and stops the script.
            pygame.quit() #Quit pygame.
            sys.exit() #Quit script.
        if event.type == SCREEN_UPDATE:
            main_game.update() #If there is an user event, update the main (check collision, etc).
        if event.type == pygame.KEYDOWN: #If we detecte a key being pressed:
            #Here we check which key is being pressed and evaluates if the actual direction isn't the contrary,
            # because if the snake is going DOWN on Y and the we make the snake going UP on Y, the snake will collish with itself.
            #Basically, the player cant go up if the snake is going down.
     
            if event.key == pygame.K_UP and main_game.snake.direction != Vector2(0, 1): 
                main_game.snake.direction = Vector2(0, -1) #-1 moves the Y position to up.
            if event.key == pygame.K_DOWN and main_game.snake.direction != Vector2(0, -1):
                main_game.snake.direction = Vector2(0, 1) #1 moves the Y position to down.
            if event.key == pygame.K_RIGHT and main_game.snake.direction != Vector2(-1, 0):
                main_game.snake.direction = Vector2(1, 0) #1 moves the X position to right.
            if event.key == pygame.K_LEFT and (main_game.snake.direction != Vector2(1, 0) and main_game.snake.direction != Vector2(0,0)):
                main_game.snake.direction = Vector2(-1, 0) #-1 moves the X position to left.
                #In the left one we evaluate if the direction isn't 0,0 to don't let the snake go inside itself when the game starts.
            if event.key == pygame.K_r: 
                main_game.__init__() #We set all the values to default, to restart the game.

    screen.fill((175, 215, 70))#We fill all the screen with a light green color.
    main_game.draw_elements() #We constantly draw the elements (snake, apple).
    pygame.display.update() #We constatanly update the displaying screen.
    clock.tick(60) #We set the times that the While True loop can execute in 1 second.