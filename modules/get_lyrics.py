import pygame, os, random, json
from datetime import datetime
from game_configs import *

pygame.init()
clock=pygame.time.Clock()
directory = os.path.dirname(os.path.realpath(__file__))


### VARIÁVEIS GLOBAIS ###
user_name = str
remaining_life = 3
remaining_life2 = 3
points = 0
pointz = 0
extra_point = 0
date = str
speed = 5
first = True
lands01 = 0
lands02 = 0
lands_group = 0
Background_level = "levelBackground"


### CLASSES ### 

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
    '''
    Essa classe é responsável pela paisagem de Copacabana, renderizando e movendo a imagem 
    '''       
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
    '''
    Essa classe é responsável pela paisagem de Ipanema, renderizando e movendo a imagem 
    '''    
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
    '''
    Essa classe é responsável pela paisagem da Avenida Rio Branco, renderizando e movendo a imagem 
    '''   
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
    '''
    Essa classe é responsável pelos botões. Clicar e executar as ações conforme o necessário.
    '''
    def __init__(self, color, x, y, width, height, text=''):
        '''
        :param color: cor do botão. As cores estão definidas no módulo game_configs.py.
        :type color: str
        :param x: posição no eixo x
        :type x: int
        :param y: posição no eixo y
        :type y: int
        :param width: largura do botão
        :type width: int
        :param height: altura do botão
        :type height: int
        :param text: string indicando qual o tipo do botão: "ok", "play", "play versus", "instructions", "exit, "back", "clear scores", "copacabana", "ipanema", "rio branco"
        :type text: str
        '''
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw_button(self,janela,outline=None):
        '''
        Função responsável por desenhar o butão na tela

        :param janela: é a janela do jogo. Definida em 'pygame.display.set_mode(size)' nas game_configs
        :type janela: class 'pygame.Surface'
        :param outline: qual a cor da borda (cores já definidas: RED, GREEN, BLUE, GREY, WHITE, BLACK, MAGENTA)
        :type outline: tuple
        '''
        if outline:
            pygame.draw.rect(janela, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(janela, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            text = myfont.render(self.text, 1, (0,0,0))
            janela.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        pos = pygame.mouse.get_pos()
        if self.is_over(pos):
            self.color = WHITE
        else:
            self.color = GREY

    def is_over(self, pos):
        '''
        verifica se o mouse está em cima do botão

        :param pos: posição atual do mouse
        :type pos: tuple
        '''
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False    

okBtn = button(RED, 250, 300, 200, 25, "ok")

class input_text:
    '''
    Classe responsável pela caixa de input que recolhe o nome do usuário
    '''
    inactive_color = BLACK
    active_color = WHITE

    def __init__(self, x, y, w, h, text=''):
        '''
        :param x: posição da caixa no eixo x
        :type x: int
        :param y: posição da caixa no eixo y
        :type y: int
        :param w: largura da caixa
        :type w: int
        :param h: altura da caixa
        :type h: int       
        :param text: texto escrito na caixa
        :type text: str
        '''
        self.rect = pygame.Rect(x, y, w, h)
        self.color = input_text.inactive_color
        self.text = text
        self.txt_surface = myfont.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        '''
        Função responsável por lidar com o evento ao ocorrer uma interação com a caixa de input

        :param event: qual o evento que ocorreu
        :type event: class 'Event'
        '''
        if event.type == pygame.MOUSEBUTTONDOWN: # Se o usuário clicou na caixa de input
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
                
            self.color = input_text.active_color if self.active else input_text.inactive_color # Mudar a cor da caixa
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
        '''
        Atualiza o tamanho da caixa conforme o tamanho do texto
        '''
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw_input(self, screen):
        '''
        Mostra qual é o input na caixa de input

        :param screen: é a janela do jogo. Definida em 'pygame.display.set_mode(size)' nas game_configs
        :type screen: class 'pygame.Surface'
        '''
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2) 
    
input_box = input_text(400, 300, 140, 32)  


### FUNÇÕES ###

def changescn(scn, text="", btnfnc=""):
    '''
    Responsável por mudar a cena atual.

    :param scn: id da cena atual. Possíveis id's: 'menu', 'enter_name', 'main_loop', 'versus_loop', 'instructions', 'map_menu', 'msg', 'scores'.
    :type scn: str
    '''
    
    # variáveis criadas para auxiliar quando uma cena está acontecendo. Quando True, ela passa a ser executada.
    global menu_s, enter_name_s, main_loop_s, versus_loop_s, instructions_s, msg_s, scores_s, map_menu_s
    menu_s = enter_name_s = main_loop_s = instructions_s = msg_s = scores_s = map_menu_s = False
    
    if scn == "menu":
        menu_s = True
        menu()
    
    elif scn == "enter_name":
        enter_name_s = True
        enter_name()
        
    elif scn == "main_loop":
        main_loop_s = True
        main_loop()
    
    elif scn == "versus_loop":
        versus_loop_s = True
        versus_loop()
        
    elif scn == "instructions":
        instructions_s = True
        instructions()
    
    elif scn == "map_menu":
        map_menu_s = True
        map_menu()
        
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
        play_music("stop")
        reset_game()
        first = True
        sound_gameover.play()
    elif text == "O Jogador 2 é o Vencedor!":
        play_music("stop")
        reset_game()
        first = True
        sound_victory_versus.play()
    elif text == "O Jogador 1 é o Vencedor!":
        play_music("stop")
        reset_game()
        first = True
        sound_victory_versus.play()
        
    while msg_s:
            
        screen.fill(MAGENTA)
        screen.blit(label, (SCREENWIDTH/2 - label.get_width()/2, SCREENHEIGHT/2 - label.get_height()/2 - 50))
        msgOkBtn.draw_button(screen, BLACK)
        
        ##### UPDATE #####
        
        pygame.display.flip()
        
        ##### EVENTS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type==pygame.QUIT:
                msg_s = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if msgOkBtn.is_over(pos):
                    if text == "Game Over!" or text == "O Jogador 2 é o Vencedor!" or text == "O Jogador 1 é o Vencedor!":
                        play_music("main")
                    changescn(btnfnc)
                    
            if event.type == pygame.KEYDOWN:
                                
                if event.key==pygame.K_ESCAPE:
                    changescn(btnfnc)


def play_music(music):

    if music == "main":
        pygame.mixer.music.load(directory + "\\sounds\\music.wav")
        pygame.mixer.music.play(-1)
        
    elif music == "engine":
        pygame.mixer.music.load(directory + "\\sounds\\engine.wav")
        pygame.mixer.music.play(-1)
        
    elif music == "stop":
        pygame.mixer.music.stop()
             
            
sorted_data = []
data = {}
def save_game():
    '''
    Salva a pontuação em "Scores"
    '''
    global sorted_data, data, date, points, user_name
    
    with open(directory + "\\save\\" + "scores.txt", "r") as f:
        data = json.load(f)

    data.update({date:{"name":user_name, "points":points, "remaining_life":remaining_life}} )
    
    sorted_data = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True) # ordenar diccionario de diccionarios
    try:
        del data[sorted_data[10][0]]
    except IndexError:
        pass

    with open(directory + "\\save\\" + "scores.txt", "w") as f:
        json.dump(data, f)


def diamond_action():
    '''
    quando um diamante é pego
    '''
    
    global points, speed
 
    points += 1200
    sound_points.play()

def heart_action():
    '''
    quando um coração é pego
    '''
    
    global remaining_life

    if remaining_life < 5:
        remaining_life += 1

    sound_points.play()

def heart_action2():
    '''
    quando um coração é pego pelo segundo jogador
    '''
    
    global remaining_life2

    if remaining_life2 < 5:
        remaining_life2 += 1

    sound_points.play()
    

def display_info():
    '''
    mostra informações sobre nome do jogador, vidas restantes, pontuação e velocidade no canto superior direito da tela
    '''
    
    global remaining_life, user_name, points, pointz, speed, player_kar, extra_point
    if player_kar.rect.x < 500:
        points += 1
        pointz += 2
        extra_point +=2 
    else:
        points += 1
        extra_point = 0

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

    extra = myfont.render("Bônus: " + str(extra_point), 1, GREEN, BLACK)
    if player_kar.rect.x < 500:
        screen.blit(extra, (590, 140))
    

cars_out = diamonds_out = 0 # variáveis criadas para controlar o numero de coisas que nascem
def launch():
    '''
    lançar carros, corações e diamantes no mapa de forma aleatória
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


aux = False
def crash(value):
    
    global aux
    global remaining_life

    if value == True and aux == False:
        remaining_life -= 1
        sound_crash.play()

        aux = True
        
    if value == False and aux == True:
        aux = False

    if remaining_life < 1:
        save_game()
        changescn("msg", text="Game Over!", btnfnc="menu")

aux = False
def crash_versus(value):
    '''
    Quando o jogador 1 perde no modo versus
    '''
    global aux
    global remaining_life, remaining_life2
    global versus_loop_s

    if value == True and aux == False:
        remaining_life -= 1
        sound_crash.play()

        aux = True
        
    if value == False and aux == True:
        aux = False

    if remaining_life < 1:
        versus_loop_s = False
        reset_game()
        changescn("msg", text="O Jogador 2 é o Vencedor!", btnfnc="menu")

aux = False
def crash_versus2(value):
    '''
    Quando o jogador 2 perde no modo versus
    '''    
    global aux
    global remaining_life, remaining_life2
    global versus_loop_s

    if value == True and aux == False:
        remaining_life2 -= 1
        sound_crash.play()

        aux = True
        
    if value == False and aux == True:
        aux = False

    if remaining_life2 < 1:
        versus_loop_s = False
        reset_game()
        changescn("msg", text="O Jogador 1 é o Vencedor!", btnfnc="menu")
        

def reset_game():
    '''
    Redefine as variáveis quando o jogador perde
    '''
    global user_name, remaining_life, remaining_life2, points, pointz, date, speed
    
    for i in enemy_car_group:
        i.kill()
        
    for i in diamond_group:
        i.kill()

    for i in heart_group:
        i.kill()
    
    user_name = input_box.text
    input_box.text = "" # clear input_box
    input_box.txt_surface = myfont.render("", True, input_box.color) # clear input_box 

    remaining_life = 3
    remaining_life2 = 3
    points = 0
    pointz = 0
    speed = 5
   
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")


menu_s = bool
def menu():
    '''
    Responsável pelos menus do jogo. 
    '''
    global data, sorted_data, menu_s

    playBtn = button(RED, 400, 240, 200, 25, "PLAY")
    playvsBtn = button(RED, 400, 270, 200, 25, "PLAY VERSUS")
    scoresBtn = button(RED, 400, 300, 200, 25, "SCORES")
    instBtn = button(RED, 400, 330, 200, 25, "INSTRUCTIONS")
    exitBtn = button(RED, 400, 360, 200, 25, "EXIT")
    backBtn = button(RED, 650, 450, 200, 25, "Back")

    with open(directory + "\\save\\" + "scores.txt", "r") as f:
        data = json.load(f)
    sorted_data = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True) # ordenar dicionario de dicionarios

    while menu_s:

        # renderizar os botões e backgrounds
        screen.blit(menu_background, (0, 0))
        playBtn.draw_button(screen, (0,0,0))
        playvsBtn.draw_button(screen, (0,0,0))
        scoresBtn.draw_button(screen, (0,0,0))
        instBtn.draw_button(screen, (0,0,0))
        exitBtn.draw_button(screen, (0,0,0))

        if first == False:
            backBtn.draw_button(screen, (0,0,0))

        # cuida dos eventos referentes às trocas de menus
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() # pega a posição do mouse
            if event.type == pygame.QUIT:
                menu_s = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # controlar os botões                
                if playBtn.is_over(pos):         
                    changescn("enter_name")     
                if instBtn.is_over(pos):
                    changescn("instructions")                
                if exitBtn.is_over(pos):
                    menu_s = False                    
                if backBtn.is_over(pos):
                    changescn("main_loop")               
                if playvsBtn.is_over(pos):         
                    changescn("versus_loop")                    
                if scoresBtn.is_over(pos):
                    changescn("scores")
                    
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    menu_s = False
                    
        # Refresh Screen
        pygame.display.flip()

map_menu_s = bool
def map_menu():
    '''
    Responsável pelo menu da escolha dos mapas 
    '''    
    global data, sorted_data, menu_s, lands01, lands02, lands_group, screen

    CopacabanaBtn = button(RED, 300, 270, 400, 25, "COPACABANA")
    IpanemaBtn = button(RED, 300, 300, 400, 25, "IPANEMA")
    AvriobrancoBtn = button(RED, 300, 330, 400, 25, "AVENIDA RIO BRANCO")
    backBtn = button(RED, 650, 450, 200, 25, "Back")

    while map_menu_s:

        # renderizar os botões e backgrounds
        screen.blit(menu_background, (0, 0))
        CopacabanaBtn.draw_button(screen, (0,0,0))
        IpanemaBtn.draw_button(screen, (0,0,0))
        AvriobrancoBtn.draw_button(screen, (0,0,0))
        backBtn.draw_button(screen, (0,0,0))

        if first == False:
            backBtn.draw_button(screen, (0,0,0))

        # cuida dos eventos referentes às trocas de menus
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() # pega a posição do mouse
 
            if event.type == pygame.QUIT:
                menu_s = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # controlar os botões
                if CopacabanaBtn.is_over(pos):
                    landscape(0)
                    lands01 = landscape(-5000) 
                    lands02 = landscape(0) 
                    lands_group = pygame.sprite.Group()
                    lands_group.add(lands01) 
                    lands_group.add(lands02)
                    changescn("main_loop")
     
                if IpanemaBtn.is_over(pos):
                    landscape2(0)
                    lands01 = landscape2(-5000) 
                    lands02 = landscape2(0) 
                    lands_group = pygame.sprite.Group()
                    lands_group.add(lands01) 
                    lands_group.add(lands02)
                    changescn("main_loop")
                
                if backBtn.is_over(pos):
                    reset_game()
                    changescn("menu")
                    
                if AvriobrancoBtn.is_over(pos):
                    landscape3(0)
                    lands01 = landscape3(-2500) 
                    lands02 = landscape3(0) 
                    lands_group = pygame.sprite.Group()
                    lands_group.add(lands01) 
                    lands_group.add(lands02)
                    changescn("main_loop")
                    changescn("main_loop")
                    
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    menu_s = False               

        # Refresh Screen
        pygame.display.flip()
       

scores_s = bool
def scores():
    '''
    Responsável pelo menu das pontuações
    '''
    global data
    
    tag = "NAME".ljust(10) + "POINTS".center(10) + "DATE".rjust(10)

    if len(sorted_data) > 0:
        place0 = str(data[(sorted_data[0][0])]["name"].ljust(10) + str(data[(sorted_data[0][0])]["points"]).center(10) + str(sorted_data[0][0]).rjust(25))
    else:
        place0 = "-"
        
    if len(sorted_data) > 1:
        place1 = str(data[(sorted_data[1][0])]["name"].ljust(10) + str(data[(sorted_data[1][0])]["points"]).center(10) + str(sorted_data[1][0]).rjust(25))
    else:
        place1 = "-"
        
    if len(sorted_data) > 2:
        place2 = str(data[(sorted_data[2][0])]["name"].ljust(10) + str(data[(sorted_data[2][0])]["points"]).center(10) + str(sorted_data[2][0]).rjust(25))
    else:
        place2 = "-"
        
    if len(sorted_data) > 3:
        place3 = str(data[(sorted_data[3][0])]["name"].ljust(10) + str(data[(sorted_data[3][0])]["points"]).center(10) + str(sorted_data[3][0]).rjust(25))
    else:
        place3 = "-"
        
    if len(sorted_data) > 4:
        place4 = str(data[(sorted_data[4][0])]["name"].ljust(10) + str(data[(sorted_data[4][0])]["points"]).center(10) + str(sorted_data[4][0]).rjust(25))
    else:
        place4 = "-"


    scoresOk = button(RED, 150, 450, 200, 25, "Back")
    scoresClear = button(RED, 450, 450, 200, 25, "Clear Score")
    scoresTitle = myfont.render("SCORES - TOP 5", 1, WHITE, BLUE)
    tag2 = myfont.render(tag, 1, WHITE, BLUE)
    score0 = myfont.render(place0, 1, WHITE)
    score1 = myfont.render(place1, 1, WHITE)
    score2 = myfont.render(place2, 1, WHITE)
    score3 = myfont.render(place3, 1, WHITE)
    score4 = myfont.render(place4, 1, WHITE)

    global scores_s
    while scores_s:

        # renderizar os botões e backgrounds
        screen.fill(MAGENTA)
        pygame.draw.rect(screen,BLACK,(90,20,600,400))
        screen.blit(scoresTitle, (100, 30))
        screen.blit(tag2, (100, 80))
        screen.blit(score0, (100, 120))
        screen.blit(score1, (100, 150))
        screen.blit(score2, (100, 180))
        screen.blit(score3, (100, 210))
        screen.blit(score4, (100, 240))
        scoresOk.draw_button(screen, (0,0,0))
        scoresClear.draw_button(screen, (0,0,0))

        # cuida dos eventos referentes às trocas de menus
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
 
            if event.type == pygame.QUIT:
                scores_s = False
                
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    changescn("menu")

            if event.type == pygame.MOUSEBUTTONDOWN:          
                if scoresOk.is_over(pos):
                    changescn("menu")
                    
                elif scoresClear.is_over(pos):
                    clear_scores()

        # Refresh Screen
        pygame.display.flip()
        
def clear_scores():
    '''
    Responsável por resetar as scores salvas
    '''    
    global data, sorted_data
    data.clear()
    sorted_data.clear()
    
    with open(directory + "\\save\\" + "scores.txt", "w") as f:
        json.dump(data, f)

    changescn("scores")
    

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

  
        backBtn.draw_button(screen, (0,0,0))
        
        ##### ACTUALIZACION #####
        
        pygame.display.flip()
        
        ##### EVENTOS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if backBtn.is_over(pos):
                    changescn("menu")
                    
            if event.type == pygame.QUIT:
                instructions_s = False
                
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: #Pressing the esc Key will quit the game
                    changescn("menu")


enter_name_s = False
def enter_name():
    '''
    Responsável pela tela onde coloca o jogador coloca seu user name. 
    '''
    global enter_name_s, first, remaining_life, speed
    
    enterOkBtn = button(RED, 400, 350, 200, 25, "OK")
    enterBackBtn = button(RED, 650, 450, 200, 25, "Back")
    labelenter_name = myfont.render("Enter user name:", 1, BLACK)

    while enter_name_s:

        # renderizar os botões e backgrounds
        screen.blit(menu_background, (0, 0)) 
        enterOkBtn.draw_button(screen, (0,0,0)) 
        enterBackBtn.draw_button(screen, (0,0,0))
        screen.blit(labelenter_name, (400, 270))  
        input_box.update()
        input_box.draw_input(screen)

        # cuida dos eventos referentes às trocas de menus        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            input_box.handle_event(event)
            
            # controlar os botões
            if event.type == pygame.MOUSEBUTTONDOWN:

                if enterOkBtn.is_over(pos):
                    if input_box.text == "":
                        changescn("msg", text="You have to enter name", btnfnc="enter_name")
                    
                    elif input_box.text == "INVINCIBLE": # easter egg
                        first = False
                        reset_game()
                        remaining_life += 97
                        changescn("map_menu")
                    
                    elif input_box.text == "I AM SPEED": # easter egg
                        first = False
                        reset_game()
                        speed += 10
                        changescn("map_menu")

                    elif input_box.text == "ROCKETMAN": # easter egg
                        first = False
                        reset_game()
                        speed += 995
                        changescn("map_menu") 
                            
                    else:
                        first = False
                        reset_game()
                        changescn("map_menu")
         
                if enterBackBtn.is_over(pos):
                    changescn("menu")
            
            if event.type==pygame.QUIT:
                enter_name_s = False
                
            if event.type == pygame.KEYDOWN:                
                if event.key==pygame.K_ESCAPE:
                    changescn("menu")

        # Refresh Screen
        pygame.display.flip()


count_time = 0
main_loop_s = bool
def main_loop():
    '''
    Responsável por garantir que o jogo funcione em um loop, chamando as funções necessárias sempre que for necessário
    '''
    global main_loop_s, count_time
    
    play_music("engine")

    while main_loop_s:

        # controlar launch de itens
        count_time += 1
        if count_time > 10:
            count_time = 0
            launch()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop_s = False
 
        # resonder quando teclas forem pressionadas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_kar.moveLeft(5)
        if keys[pygame.K_d]:
            player_kar.moveRight(5)         
        if keys[pygame.K_ESCAPE]:
            save_game()
            play_music("main")
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
        
        # colisão entre o carro do jogador e carros inimigos
        car_collision_list = pygame.sprite.spritecollide(player_kar, enemy_car_group,False,pygame.sprite.collide_mask)
        
        if car_collision_list:
            crash(True)
        else:
            crash(False)

        # colisão entre o carro do jogador e diamantes
        diamond_collision = pygame.sprite.spritecollide(player_kar, diamond_group,True,pygame.sprite.collide_mask)
        
        if diamond_collision:
            diamond_action()

        # colisão entre o carro do jogador e corações
        heart_collision = pygame.sprite.spritecollide(player_kar ,heart_group,True,pygame.sprite.collide_mask)
        if heart_collision:
            heart_action()

        #Refresh Screen
        pygame.display.flip()
        clock.tick(60)
        

count_time = 0
versus_loop_s = bool
def versus_loop():

    global main_loop_s, count_time
    
    play_music("engine")
    
    while versus_loop_s:

        # controlar launch de itens
        count_time += 1
        if count_time > 10:
            count_time = 0
            launch()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                versus_loop_s = False
 
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
            reset_game()    
            play_music("main")
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

play_music("main")
menu()
pygame.quit()
