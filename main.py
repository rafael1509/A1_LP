import pygame, os, random, json
from datetime import datetime
from game_configs import *

pygame.init()
clock=pygame.time.Clock()
directory = os.path.dirname(os.path.realpath(__file__))


## Variáveis globais
user_name = str
remaining_life = 3
remaining_life2 = 3
points = 0
pointz = 0
date = str
speed = 5
first = True
lands01 = 0
lands02 = 0
lands_group = 0
Background_level = "levelBackground"


########## CLASSES, INSTANCES, GROUPS ########## 

class car(pygame.sprite.Sprite):
    '''
    Essa classe é responsável pelos carros que atuam como obstáculos para o jogador
    '''
    def __init__(self, lane, invert):
        '''
        :param lane: posição em que o carro vai nascer
        :type lane: int
        :param invert: booleano para girar 180º o carro caso ele nasça na contra-mão
        :type invert: bool
        '''
        super().__init__()

        global speed
        
        self.size = (50, 50)
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(directory + "\\sprites\\gray_car.png").convert_alpha(),self.size),180)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.lane = lane

        car_kind = ['gray_car', 'red_truck', 'green_truck', 'gray_truck', 'brown_truck', 'yellow_bus']
        self.image = pygame.image.load(directory + f"\\sprites\\{random.choice(car_kind)}.png").convert_alpha()

        if invert == True:
            self.image = pygame.transform.rotate(self.image, 180)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.lane
        self.rect.y = -100
        
    def move_forward(self):
        
        if self.rect.y < 650:
            self.rect.y += speed
        else:
            self.kill()
        if self.rect.x < 500:
            self.rect.y += round(speed/2)

enemy_car_group = pygame.sprite.Group()


class thing(pygame.sprite.Sprite):
    '''
    Essa classe é responsável pelos objetos que aparecem na pista, como diamantes e vidas extras.
    '''
    def __init__(self, lane, tipo):
        '''
        :param lane: posição em que o carro vai nascer
        :type lane: int  
        :param tipo: "diamond" ou "heart". Necessário identificar o objeto para selecionar o sprite correto
        :type tipo: str      
        '''
        super().__init__()

        if tipo == 'diamond':
            self.image = pygame.image.load(directory + "\\sprites\\diamond.png").convert_alpha()

        else: #heart
            picture = pygame.image.load(directory + "\\sprites\\heart.png")
            picture = pygame.transform.scale(picture, (45, 45))
            self.image = picture.convert_alpha() 

        self.rect = self.image.get_rect()
        self.rect.y = -100
        self.rect.x = lane

    def move_forward(self):
        
        if self.rect.y < 650:
            self.rect.y += speed
        else:
           self.kill()
          
diamond_group = pygame.sprite.Group()
heart_group = pygame.sprite.Group()
            
class player_car(pygame.sprite.Sprite):
    '''
    Essa classe é responsável pelo carro do jogador.
    '''    
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(directory + "\\sprites\\kar.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 400
        
    def moveRight(self, pixels):
        if self.rect.x < 650:
            self.rect.x += pixels
 
    def moveLeft(self, pixels):
        if self.rect.x > 300:
            self.rect.x -= pixels

player_kar = player_car() 
player_car_group = pygame.sprite.Group() 
player_car_group.add(player_kar)

class kar2(pygame.sprite.Sprite):
    '''
    Essa classe é responsável pelo carro do jogador 2 no modo versus.
    '''       
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(directory + "\\sprites\\kar2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 400
        
    def moveRight(self, pixels):
        if self.rect.x < 650:
            self.rect.x += pixels
 
    def moveLeft(self, pixels):
        if self.rect.x > 300:
            self.rect.x -= pixels

player_kar2 = kar2() 
player_car_group2 = pygame.sprite.Group() 
player_car_group2.add(player_kar2)

class landscape(pygame.sprite.Sprite):
    
    global speed, Background_level, lands01, lands02, lands_group
    
    def __init__(self, y):
        super().__init__()
        self.image = pygame.image.load(directory + f"\\sprites\\levelBackground.png").convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect.y = y
        
    def play(self):
        if self.rect.y < 5000:
            self.rect.y += speed
        else:
            self.rect.y = -5000

class landscape2(pygame.sprite.Sprite):
    
    global speed, Background_level
    
    def __init__(self, y):
        super().__init__()
        self.image = pygame.image.load(directory + f"\\sprites\\levelBackground2.png").convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect.y = y
        
    def play(self):
        if self.rect.y < 5000:
            self.rect.y += speed
        else:
            self.rect.y = -5000

class landscape3(pygame.sprite.Sprite):
    
    global speed, Background_level
    
    def __init__(self, y):
        super().__init__()
        self.image = pygame.image.load(directory + f"\\sprites\\levelBackground3.png").convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect.y = y
        
    def play(self):
        if self.rect.y < 2500:
            self.rect.y += speed
        else:
            self.rect.y = -2500
class button():

    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            text = myfont.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        pos = pygame.mouse.get_pos()
        if self.isOver(pos):
            self.color = WHITE
        else:
            self.color = GREY

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
                
        return False    

okBtn = button(RED, 250, 300, 200, 25, "ok")

class InputBox:
    
    COLOR_INACTIVE = BLACK
    COLOR_ACTIVE = WHITE

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = InputBox.COLOR_INACTIVE
        self.text = text
        self.txt_surface = myfont.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    if len(self.text) < 10:
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = myfont.render(self.text, True, self.color)
                
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2) 
    
input_box1 = InputBox(400, 300, 140, 32)  

##### FUNCTIONS #####

##### change scene

def changescn(scn, text="", btnfnc=""):
    
    # ~ continuar haciendo lo mismo que abajo
    global menu_s, enterName_s, mainLoop_s, versusLoop_s, instructions_s, msg_s, scores_s, mapmenu_s
    menu_s = enterName_s = mainLoop_s = instructions_s = msg_s = scores_s = mapmenu_s = False
    
    if scn == "menu":
        menu_s = True
        menu()
    
    elif scn == "enterName":
        enterName_s = True
        enterName()
        
    elif scn == "mainLoop":
        mainLoop_s = True
        mainLoop()
    
    elif scn == "versusLoop":
        versusLoop_s = True
        versusLoop()
        
    elif scn == "instructions":
        instructions_s = True
        instructions()
    
    elif scn == "mapmenu":
        mapmenu_s = True
        mapmenu()
        
    elif scn == "msg":
        msg_s = True
        msg(text,btnfnc)
        
    elif scn == "scores":
        scores_s = True
        scores()
        
##### msg system

msg_s = True
def msg(text,btnfnc):
    
    global msg_s, first
    
    msgOkBtn = button(RED, SCREENWIDTH/2 - 100, SCREENHEIGHT/2, 200, 25, "ok")
    label = pygame.font.SysFont('Lucida Console', 30).render(text, 1, BLACK)
    
    if text == "Game Over!":
        playMusic("stop")
        resetGame()
        first = True
        soundGameOver.play()
    elif text == "O Jogador 2 é o Vencedor!":
        playMusic("stop")
        resetGame()
        first = True
        soundVictory_Versus.play()
    elif text == "O Jogador 1 é o Vencedor!":
        playMusic("stop")
        resetGame()
        first = True
        soundVictory_Versus.play()
        
    while msg_s:
            
        screen.fill(MAGENTA)
        screen.blit(label, (SCREENWIDTH/2 - label.get_width()/2, SCREENHEIGHT/2 - label.get_height()/2 - 50))
        msgOkBtn.draw(screen, BLACK)
        
        ##### UPDATE #####
        
        pygame.display.flip()
        
        ##### EVENTS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type==pygame.QUIT:
                msg_s = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if msgOkBtn.isOver(pos):
                    if text == "Game Over!":
                        playMusic("main")
                    elif text == "O Jogador 2 é o Vencedor!":
                        playMusic("main")
                    elif text == "O Jogador 1 é o Vencedor!":
                        playMusic("main")
    
                    changescn(btnfnc)
                    
            if event.type == pygame.KEYDOWN:
                                
                if event.key==pygame.K_ESCAPE:
                    changescn(btnfnc)

##### change music
def playMusic(music):

    if music == "main":
        pygame.mixer.music.load(directory + "\\sounds\\music.wav")
        pygame.mixer.music.play(-1)
        
    elif music == "engine":
        pygame.mixer.music.load(directory + "\\sounds\\engine.wav")
        pygame.mixer.music.play(-1)
        
    elif music == "stop":
        pygame.mixer.music.stop()
             
            
##### save score
sortedData = []
data = {}
def saveGame():
    
    global sortedData, data, date, points, user_name
    
    with open(directory + "\\save\\" + "scores.txt", "r") as f:
        data = json.load(f)

    # add key to dictthings
    data.update({date:{"name":user_name, "points":points, "remaining_life":remaining_life}} )
    
    # order and clear dict
    sortedData = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True) # ordenar diccionario de diccionarios
    try:
        del data[sortedData[10][0]]

    except IndexError:
        pass

    # save dict
    with open(directory + "\\save\\" + "scores.txt", "w") as f:
        json.dump(data, f)


def diamond_action():
    '''
    quando um diamante é pego
    '''
    
    global points, speed
 
    points += 1200
    soundPoints.play()
    speed += 1

def heart_action():
    '''
    quando um coração é pego
    '''
    
    global remaining_life

    if remaining_life < 5:
        remaining_life += 1

    soundPoints.play()

def heart_action2():
    '''
    quando um coração é pego pelo segundo jogador
    '''
    
    global remaining_life2

    if remaining_life2 < 5:
        remaining_life2 += 1

    soundPoints.play()
    
def display_info():
    '''
    mostra informações sobre nome do jogador, vidas restantes, pontuação e velocidade no canto superior direito da tela
    '''
    
    global remaining_life, user_name, points, pointz, speed, player_kar
    if player_kar.rect.x < 500:
        points += 1
        pointz += 2
    else:
        points += 1

    if points % 1000 == 0:
        speed +=1
    
    nome = myfont.render("Nome: " + str(user_name), 1, WHITE, BLACK)
    screen.blit(nome, (590, 20))     
    
    vida = myfont.render("Vidas: " + str(remaining_life), 1, WHITE, BLACK)
    screen.blit(vida, (590, 50))

    pontos = myfont.render("Pontuação: " + str(points+pointz), 1, WHITE, BLACK)
    screen.blit(pontos, (590, 80))

    velocidade = myfont.render("Velocidade: " + str(speed*10)+"Km/h", 1, WHITE, BLACK)
    screen.blit(velocidade, (590, 110))

def display_info_versus():
    '''
    mostra informações sobre os jogadores no modo versus do jogo
    '''
    
    global remaining_life, remaining_life, points, speed

    points += 1
    if points % 400 == 1:
        speed +=1
    
    nome = myfont.render("Jogador 2", 1, WHITE, BLACK)
    screen.blit(nome, (610, 20))     
    
    vida = myfont.render("Vidas: " + str(remaining_life2), 1, WHITE, BLACK)
    screen.blit(vida, (610, 50))

    velocidade = myfont.render("Velocidade: " + str(speed*10)+"Km/h", 1, WHITE, BLACK)
    screen.blit(velocidade, (610, 80))

    nome = myfont.render("Jogador 1", 1, WHITE, BLACK)
    screen.blit(nome, (10, 20))     
    
    vida = myfont.render("Vidas: " + str(remaining_life), 1, WHITE, BLACK)
    screen.blit(vida, (10, 50))

    velocidade = myfont.render("Velocidade: " + str(speed*10)+"Km/h", 1, WHITE, BLACK)
    screen.blit(velocidade, (10, 80))
    

cars_out = diamonds_out = 0 # variáveis criadas para controlar o numero de coisas que nascem
def launch():
    '''
    launch car and things
    '''
    global cars_out, diamonds_out

    lane_list = [300, 350, 400, 450, 500, 550, 600, 650]
    lane = random.choice(lane_list)

    # inverter a imagem do carro caso ele esteja na contra-mão
    invert = False 
    if lane < 500:
        invert = True

    if cars_out < 5:
        enemy_car = car(lane, invert)
        enemy_car_group.add(enemy_car)
        cars_out += 1
        
    elif diamonds_out < 5: # um diamante nasce a cada 5 carros 
        diamond = thing(lane, "diamond")
        diamond_group.add(diamond)
        cars_out = 0
        diamonds_out += 1
    
    else: # um coração nasce a cada 5 diamantes
        heart = thing(lane, "heart")
        heart_group.add(heart)
        cars_out = 0
        diamonds_out = 0

cars_out = diamonds_out = 0 # variáveis criadas para controlar o numero de coisas que nascem
def launch_versus():
    '''
    launch car and things
    '''
    global cars_out, diamonds_out

    lane_list = [300, 350, 400, 450, 500, 550, 600, 650]
    lane = random.choice(lane_list)

    # inverter a imagem do carro caso ele esteja na contra-mão
    invert = False 
    if lane < 500:
        invert = True

    if cars_out < 5:
        enemy_car = car(lane, invert)
        enemy_car_group.add(enemy_car)
        cars_out += 1
    
    else: # um coração nasce a cada 5 diamantes
        heart = thing(lane, "heart")
        heart_group.add(heart)
        cars_out = 0

        
##### Crash
aux = False
def crash(value):
    
    global aux
    global remaining_life

    if value == True and aux == False:
        remaining_life -= 1
        soundCrash.play()

        aux = True
        
    if value == False and aux == True:
        aux = False

    if remaining_life < 1:
        saveGame()
        changescn("msg", text="Game Over!", btnfnc="menu")

aux = False
def crash_versus(value):
    
    global aux
    global remaining_life, remaining_life2
    global versusLoop_s

    if value == True and aux == False:
        remaining_life -= 1
        soundCrash.play()

        aux = True
        
    if value == False and aux == True:
        aux = False

    if remaining_life < 1:
        versusLoop_s = False
        resetGame()
        changescn("msg", text="O Jogador 2 é o Vencedor!", btnfnc="menu")

aux = False
def crash_versus2(value):
    
    global aux
    global remaining_life, remaining_life2
    global versusLoop_s

    if value == True and aux == False:
        remaining_life2 -= 1
        soundCrash.play()

        aux = True
        
    if value == False and aux == True:
        aux = False

    if remaining_life2 < 1:
        versusLoop_s = False
        resetGame()
        changescn("msg", text="O Jogador 1 é o Vencedor!", btnfnc="menu")
        
##### reset game

def resetGame():
    global user_name, remaining_life, remaining_life2, first, points, pointz, date, speed
    
    for i in enemy_car_group:
        i.kill()
        
    for i in diamond_group:
        i.kill()

    for i in heart_group:
        i.kill()
    
    user_name = input_box1.text
    input_box1.text = "" # clear input_box
    input_box1.txt_surface = myfont.render("", True, input_box1.color) # clear input_box 

    input_box1.update
    remaining_life = 3
    remaining_life2 = 3
    points = 0
    pointz = 0
    speed = 5
   
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
        
########## ESCENAS ########## 

##### menu

menu_s = bool
def menu():
    
    global data, sortedData, menu_s, firts

    playBtn = button(RED, 400, 240, 200, 25, "PLAY")
    playvsBtn = button(RED, 400, 270, 200, 25, "PLAY VERSUS")
    scoresBtn = button(RED, 400, 300, 200, 25, "SCORES")
    instBtn = button(RED, 400, 330, 200, 25, "INSTRUCTIONS")
    exitBtn = button(RED, 400, 360, 200, 25, "EXIT")
    backBtn = button(RED, 650, 450, 200, 25, "Back")

    with open(directory + "\\save\\" + "scores.txt", "r") as f:
        data = json.load(f)
    sortedData = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True) # ordenar dicionario de dicionarios

    while menu_s:

        ##### RENDER #####
        screen.blit(menu_background, (0, 0))
        playBtn.draw(screen, (0,0,0))
        playvsBtn.draw(screen, (0,0,0))
        scoresBtn.draw(screen, (0,0,0))
        instBtn.draw(screen, (0,0,0))
        exitBtn.draw(screen, (0,0,0))

        if first == False:
        
            backBtn.draw(screen, (0,0,0))

        ##### EVENTOS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() # toma la posicion del mouse
 
            if event.type == pygame.QUIT:
                menu_s = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                ############ control de los botones
                
                if playBtn.isOver(pos):         
                    changescn("enterName")
      
                if instBtn.isOver(pos):
                    changescn("instructions")
                
                if exitBtn.isOver(pos):
                    menu_s = False
                    
                if backBtn.isOver(pos):
                    changescn("mainLoop")
                
                if playvsBtn.isOver(pos):         
                    changescn("versusLoop")
                    
                if scoresBtn.isOver(pos):
                    changescn("scores")
                    
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    menu_s = False
                    


        # Refresh Screen
        pygame.display.flip()

mapmenu_s = bool
def mapmenu():
    
    global data, sortedData, menu_s, firts, Background_level, speed, lands01, lands02, lands_group, screen

    CopacabanaBtn = button(RED, 300, 270, 400, 25, "COPACABANA")
    IpanemaBtn = button(RED, 300, 300, 400, 25, "IPANEMA")
    AvriobrancoBtn = button(RED, 300, 330, 400, 25, "AVENIDA RIO BRANCO")
    backBtn = button(RED, 650, 450, 200, 25, "Back")

    with open(directory + "\\save\\" + "scores.txt", "r") as f:
        data = json.load(f)
    sortedData = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True) # ordenar diccionario de diccionarios

    while mapmenu_s:

        ##### RENDER #####
        screen.blit(menu_background, (0, 0))
        CopacabanaBtn.draw(screen, (0,0,0))
        IpanemaBtn.draw(screen, (0,0,0))
        AvriobrancoBtn.draw(screen, (0,0,0))
        backBtn.draw(screen, (0,0,0))

        if first == False:
        
            backBtn.draw(screen, (0,0,0))

        ##### EVENTOS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
 
            if event.type == pygame.QUIT:
                menu_s = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                ############ control de los botones
                
                if CopacabanaBtn.isOver(pos):
                    landscape(0)
                    lands01 = landscape(-5000) 
                    lands02 = landscape(0) 
                    lands_group = pygame.sprite.Group()
                    lands_group.add(lands01) 
                    lands_group.add(lands02)
                    changescn("mainLoop")
                    
      
                if IpanemaBtn.isOver(pos):
                    landscape2(0)
                    lands01 = landscape2(-5000) 
                    lands02 = landscape2(0) 
                    lands_group = pygame.sprite.Group()
                    lands_group.add(lands01) 
                    lands_group.add(lands02)
                    changescn("mainLoop")
                
                if backBtn.isOver(pos):
                    resetGame()
                    changescn("menu")
                    
                if AvriobrancoBtn.isOver(pos):
                    landscape3(0)
                    lands01 = landscape3(-2500) 
                    lands02 = landscape3(0) 
                    lands_group = pygame.sprite.Group()
                    lands_group.add(lands01) 
                    lands_group.add(lands02)
                    changescn("mainLoop")
                    changescn("mainLoop")
                    
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    menu_s = False               

        # Refresh Screen
        pygame.display.flip()
       
##### scores
   
scores_s = bool
def scores():

    global data

    tag = "NAME".ljust(10) + "POINTS".center(10) + "DATE".rjust(10)

    if len(sortedData) > 0:
        place0 = str(data[(sortedData[0][0])]["name"].ljust(10) + str(data[(sortedData[0][0])]["points"]).center(10) + str(sortedData[0][0]).rjust(25))
    else:
        place0 = "Empty"
        
    if len(sortedData) > 1:
        place1 = str(data[(sortedData[1][0])]["name"].ljust(10) + str(data[(sortedData[1][0])]["points"]).center(10) + str(sortedData[1][0]).rjust(25))
    else:
        place1 = "Empty"
        
    if len(sortedData) > 2:
        place2 = str(data[(sortedData[2][0])]["name"].ljust(10) + str(data[(sortedData[2][0])]["points"]).center(10) + str(sortedData[2][0]).rjust(25))
    else:
        place2 = "Empty"
        
    if len(sortedData) > 3:
        place3 = str(data[(sortedData[3][0])]["name"].ljust(10) + str(data[(sortedData[3][0])]["points"]).center(10) + str(sortedData[3][0]).rjust(25))
    else:
        place3 = "Empty"
        
    if len(sortedData) > 4:
        place4 = str(data[(sortedData[4][0])]["name"].ljust(10) + str(data[(sortedData[4][0])]["points"]).center(10) + str(sortedData[4][0]).rjust(25))
    else:
        place4 = "Empty"
        
    if len(sortedData) > 5:
        place5 = str(data[(sortedData[5][0])]["name"].ljust(10) + str(data[(sortedData[5][0])]["points"]).center(10) + str(sortedData[5][0]).rjust(25))
    else:
        place5 = "Empty"
        
    if len(sortedData) > 6:
        place6 = str(data[(sortedData[6][0])]["name"].ljust(10) + str(data[(sortedData[6][0])]["points"]).center(10) + str(sortedData[6][0]).rjust(25))
    else:
        place6 = "Empty"  

    if len(sortedData) > 7:
        place7 = str(data[(sortedData[7][0])]["name"].ljust(10) + str(data[(sortedData[7][0])]["points"]).center(10) + str(sortedData[7][0]).rjust(25))
    else:
        place7 = "Empty"
        
    if len(sortedData) > 8:
        place8 = str(data[(sortedData[8][0])]["name"].ljust(10) + str(data[(sortedData[8][0])]["points"]).center(10) + str(sortedData[8][0]).rjust(25))
    else:
        place8 = "Empty"
        
    if len(sortedData) > 9:
        place9 = str(data[(sortedData[9][0])]["name"].ljust(10) + str(data[(sortedData[9][0])]["points"]).center(10) + str(sortedData[9][0]).rjust(25))
    else:
        place9 = "Empty"

    scoresOk = button(RED, 150, 450, 200, 25, "Back")
    scoresClear = button(RED, 450, 450, 200, 25, "Clear Score")
    scoresTitle = myfont.render("SCORES - TOP10", 1, WHITE, BLUE)
    tag2 = myfont.render(tag, 1, WHITE, BLUE)
    score0 = myfont.render(place0, 1, WHITE)
    score1 = myfont.render(place1, 1, WHITE)
    score2 = myfont.render(place2, 1, WHITE)
    score3 = myfont.render(place3, 1, WHITE)
    score4 = myfont.render(place4, 1, WHITE)
    score5 = myfont.render(place5, 1, WHITE)
    score6 = myfont.render(place6, 1, WHITE)
    score7 = myfont.render(place7, 1, WHITE)
    score8 = myfont.render(place8, 1, WHITE)
    score9 = myfont.render(place9, 1, WHITE)

    global scores_s
    while scores_s:

        ##### RENDER #####
        screen.fill(MAGENTA)
        
        pygame.draw.rect(screen,BLACK,(90,20,600,400))
        
        screen.blit(scoresTitle, (100, 30))
        screen.blit(tag2, (100, 80))
        screen.blit(score0, (100, 120))
        screen.blit(score1, (100, 150))
        screen.blit(score2, (100, 180))
        screen.blit(score3, (100, 210))
        screen.blit(score4, (100, 240))
        screen.blit(score5, (100, 270))
        screen.blit(score6, (100, 300))
        screen.blit(score7, (100, 330))
        screen.blit(score8, (100, 360))
        screen.blit(score9, (100, 390))
        
        scoresOk.draw(screen, (0,0,0))
        scoresClear.draw(screen, (0,0,0))

        ##### EVENTS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
 
            if event.type == pygame.QUIT:
                scores_s = False
                
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    changescn("menu")

            if event.type == pygame.MOUSEBUTTONDOWN:          
                if scoresOk.isOver(pos):
                    changescn("menu")
                    
                elif scoresClear.isOver(pos):
                    clearScores()

        # Refresh Screen
        pygame.display.flip()
        
def clearScores():
    
    global data, sortedData
    data.clear()
    sortedData.clear()
    
    with open(directory + "\\save\\" + "scores.txt", "w") as f:
        json.dump(data, f)

    changescn("scores")
    
##### instructions

instructions_s = bool
def instructions():
    
    global instructions_s
    
    backBtn = button(RED, 550, 450, 200, 25, "Back")

    label0 = myfont.render("Instructions (DEIXAR BONITO E EM PORTUGUÊS):", 1, WHITE, BLUE)
    label1 = myfont.render("- Drive through the higway and dont crash", 1, WHITE, BLUE)
    label2 = myfont.render("- Use A and D keys to move your car", 1, WHITE, BLUE)
    label3 = myfont.render("- Catch all the diamonds you can to earn EXTRA points", 1, WHITE, BLUE)
    
    while instructions_s:
        
        ##### RENDER #####
        screen.fill(MAGENTA)
        
        pygame.draw.rect(screen,BLACK,(25,20,750,400))
        
        screen.blit(label0, (30, 30))
        screen.blit(label1, (100, 100))
        screen.blit(label2, (100, 150))
        screen.blit(label3, (100, 250))

  
        backBtn.draw(screen, (0,0,0))
        
        ##### ACTUALIZACION #####
        
        pygame.display.flip()
        
        ##### EVENTOS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if backBtn.isOver(pos):
                    changescn("menu")
                    
            if event.type == pygame.QUIT:
                instructions_s = False
                
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: #Pressing the esc Key will quit the game
                    changescn("menu")

##### enter name

enterName_s = False
def enterName():

    global enterName_s, user_text, first, remaining_life, speed
    
    enterOkBtn = button(RED, 400, 350, 200, 25, "OK")
    enterBackBtn = button(RED, 650, 450, 200, 25, "Back")

    labelEnterName = myfont.render("Enter user name:", 1, BLACK)

    while enterName_s:

        ##### RENDER #####
        
        screen.blit(menu_background, (0, 0)) 
        enterOkBtn.draw(screen, (0,0,0)) 
        enterBackBtn.draw(screen, (0,0,0))

        screen.blit(labelEnterName, (400, 270))  
        
        input_box1.update()
        input_box1.draw(screen) 

        ##### EVENTOS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            input_box1.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                ############ control de los botones
                
                if enterOkBtn.isOver(pos):
                    
                    if input_box1.text == "":
                        changescn("msg", text="You have to enter name", btnfnc="enterName")
                    
                    elif input_box1.text == "INVINCIBLE":
                        first = False
                        resetGame()
                        remaining_life += 97
                        changescn("mapmenu")
                    
                    elif input_box1.text == "I AM SPEED":
                        first = False
                        resetGame()
                        speed += 10
                        changescn("mapmenu")

                    elif input_box1.text == "ROCKETMAN":
                        first = False
                        resetGame()
                        speed += 995
                        changescn("mapmenu") 
                            
                    else:
                        first = False
                        resetGame()
                        changescn("mapmenu")
         
                if enterBackBtn.isOver(pos):
                    changescn("menu")
            
            if event.type==pygame.QUIT:
                enterName_s = False
                
            if event.type == pygame.KEYDOWN:                
                if event.key==pygame.K_ESCAPE:
                    changescn("menu")
      
        ###########################

        # Refresh Screen
        pygame.display.flip()

##### main loop
count_time = 0
mainLoop_s = bool
def mainLoop():

    global mainLoop_s, first, count_time, size, speed
    
    playMusic("engine")
    
    while mainLoop_s:

        # controlar launch de itens
        count_time += 1
        if count_time > 10:
            count_time = 0
            launch()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainLoop_s = False
 
        # resonder quando teclas forem pressionadas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_kar.moveLeft(5)
        if keys[pygame.K_d]:
            player_kar.moveRight(5)         
        if keys[pygame.K_ESCAPE]:
            saveGame()
            playMusic("main")
            changescn("menu")

        # rederizar telas
        lands_group.draw(screen)
        enemy_car_group.draw(screen)
        player_car_group.draw(screen)        
        diamond_group.draw(screen)
        heart_group.draw(screen)

        # mostrar informações no canto superior direto da tela
        display_info()
        

        lands01.play()
        lands02.play()
        
        # garantir que tudo se mova no mapa
        for car in enemy_car_group:
            car.move_forward()
        for diamond in diamond_group:
           diamond.move_forward()
        for heart in heart_group:
           heart.move_forward()

        ##### COLISIONS #####
        
        # car and enemies
        car_collision_list = pygame.sprite.spritecollide(player_kar, enemy_car_group,False,pygame.sprite.collide_mask)
        
        if car_collision_list:
            crash(True)
        else:
            crash(False)

        # car and diamond
        diamond_collision = pygame.sprite.spritecollide(player_kar, diamond_group,True,pygame.sprite.collide_mask)
        
        if diamond_collision:
            diamond_action()

        # car and heart
        heart_collision = pygame.sprite.spritecollide(player_kar ,heart_group,True,pygame.sprite.collide_mask)
        if heart_collision:
            heart_action()

        #Refresh Screen
        
        pygame.display.flip()
        clock.tick(60) # This method should be called once per frame // aprox 16 - 17 fps
        
##### versus loop
count_time = 0
versusLoop_s = bool
def versusLoop():

    global versusLoop_s, first, count_time, size, speed
    
    playMusic("engine")
    
    while versusLoop_s:

        # controlar launch de itens
        count_time += 1
        if count_time > 10:
            count_time = 0
            launch()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                versusLoop_s = False
 
        # resonder quando teclas forem pressionadas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_kar.moveLeft(5)
        if keys[pygame.K_d]:
            player_kar.moveRight(5)
        if keys[pygame.K_LEFT]:
            player_kar2.moveLeft(5)
        if keys[pygame.K_RIGHT]:
            player_kar2.moveRight(5)
        if keys[pygame.K_ESCAPE]:
            resetGame()    
            playMusic("main")
            changescn("menu")


        # rederizar telas
        lands_group.draw(screen)
        enemy_car_group.draw(screen)
        player_car_group.draw(screen)
        player_car_group2.draw(screen)         
        heart_group.draw(screen)

        # mostrar informações no canto superior direto da tela
        display_info_versus()
        

        lands01.play()
        lands02.play()
        
        # garantir que tudo se mova no mapa
        for car in enemy_car_group:
            car.move_forward()
        for heart in heart_group:
           heart.move_forward()

        ##### COLISIONS #####
        
        # car and enemies
        car_collision_list = pygame.sprite.spritecollide(player_kar, enemy_car_group,False,pygame.sprite.collide_mask)
        car_collision_list2 = pygame.sprite.spritecollide(player_kar2, enemy_car_group,False,pygame.sprite.collide_mask)
        
        if car_collision_list:
            crash_versus(True)
        elif car_collision_list2:
            crash_versus2(True)
        else:
            crash_versus(False)
            crash_versus2(False)

        # car and heart
        heart_collision = pygame.sprite.spritecollide(player_kar ,heart_group,True,pygame.sprite.collide_mask)
        heart_collision2 = pygame.sprite.spritecollide(player_kar2 ,heart_group,True,pygame.sprite.collide_mask)

        if heart_collision:
            heart_action()
        elif heart_collision2:
            heart_action2()

        #Refresh Screen
        
        pygame.display.flip()
        clock.tick(60)

#################################################################

playMusic("main")
menu()
pygame.quit()
