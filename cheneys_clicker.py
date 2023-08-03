import pygame, math, random, sys

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()

crunch_sound = pygame.mixer.Sound('sounds/crunch.wav')
click_sound = pygame.mixer.Sound('sounds/click.mp3')
musica = pygame.mixer.Sound('sounds/soundtrack.wav')

crunch_sound.set_volume(0.5)
click_sound.set_volume(0.2)
musica.set_volume(0.3)

font_grande = pygame.font.Font(None, 72)
font = pygame.font.Font(None, 40)

cookie_img = pygame.image.load('imagens/cookie.png')
cookie_img = pygame.transform.scale(cookie_img, (250,250))
cookie_img_start = pygame.transform.scale(cookie_img, (300,300))
backgroundCookie = pygame.transform.scale(cookie_img, (30,30))

wooden_bar = pygame.image.load('imagens/wooden_bar.png')
wooden_bar_r = pygame.image.load('imagens/wooden_bar.png')
upgrades_wooden_bar = pygame.image.load('imagens/upgrades_wooden_bar.png')
upgrades_wooden_bar = pygame.transform.scale(upgrades_wooden_bar, (800, 16))
wooden_background = pygame.image.load('imagens/wooden_background.png')


aluno_img = pygame.image.load('imagens/aluno_img.png')
funcionario_img = pygame.image.load('imagens/funcionario_img.png')
professor_img = pygame.image.load('imagens/professor_img.png')
mrcheney_img = pygame.image.load('imagens/mrcheney_img.png')

aluno_icon = pygame.image.load('imagens/aluno_icon.png')
funcionario_icon = pygame.image.load('imagens/funcionario_icon.png')
professor_icon = pygame.image.load('imagens/professor_icon.png')
mrcheney_icon = pygame.image.load('imagens/mrcheney_icon.png')


background_img = pygame.image.load('imagens/background.png')
background_img = pygame.transform.scale(background_img, (800,750))
building_display_background = pygame.image.load('imagens/building_display_background.png')


class CookieObj:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 250
        self.height = 250
        
        self.animation_state = 0
    def draw(self):
        if self.animation_state > 0:
            cookie_img_scaled = pygame.transform.scale(cookie_img, (int(0.9*self.length), int(0.9*self.height)))
            window.blit(cookie_img_scaled, (cookie_img_scaled.get_rect(  center=(int(self.x + self.length/2), int(self.y + self.height/2))  )))
            self.animation_state -= 1
        else:
            window.blit(cookie_img, (cookie_img.get_rect(  center=(int(self.x + self.length/2), int(self.y + self.height/2))  )))
    def collidepoint(self, point):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(point)
     
class BackgroundCookie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 40
        self.height = 40
        
    def animate(self, list_of_cookies):
        self.y += 5
        if self.y > height:
            list_of_cookies.remove(self)
            
    def draw(self):
        window.blit(backgroundCookie, (self.x, self.y))
     
class CookieDisplayObj:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 100
        self.height = 100
        
        self.score = 0
                
    def draw(self, score, user_cps):
        font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 24)
        small_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 15)
        
        text = font.render('{} cookies'.format(int( format_number(score) )), True, WHITE)
        cps = small_font.render('per second: {}'.format(int( format_number( format_number(user_cps) ))), True, WHITE)
        window.blit( text, (  text.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2)))  ) )
        window.blit( cps, (  cps.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2) + 20))  ) )

class Building:
    def __init__(self, name, x, y, image, icon, base_cost, increase_per_purchase, cps):
        self.x = x
        self.y = y
        self.length = 300
        self.height = 64
        
        self.name = name
        self.image = image
        self.icon = icon
        
        self.quantity = 0
        self.base_cost = base_cost
        self.increase_per_purchase = increase_per_purchase
        self.cps = cps
        
        self.created = 0
    def collidepoint(self, point):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(point)
    def getTotalCost(self):
        return int(self.base_cost * self.increase_per_purchase**(self.quantity))
    
    def draw(self, solid=True):
        
        store_cost_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 17)
        store_quantity_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 36)
        
        icon = self.image
        cost = store_cost_font.render('{}'.format( format_number(self.getTotalCost()) ), True, LIGHT_GREEN)
        quantity = store_quantity_font.render('{}'.format(self.quantity), True, GRAY)
        if solid == False:    
            icon.set_alpha(100)
        else:
            icon.set_alpha(255)
        window.blit(icon, (self.x, self.y))
        window.blit(cost, (self.x + 90, self.y + self.height - 30))
        window.blit(quantity, (self.x + self.length - 40, self.y + 6))
        
    def drawDisplayBox(self):
        building_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 20)
        building_title = building_font.render('{}'.format(self.name), True, WHITE)
        
        description_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 11)
        production = description_font.render('Cada {} produz {:.1f} cookies por segundo'.format(self.name, self.cps), True, WHITE)
        quantity = description_font.render('Você tem {} {}s produzindo {:.1f} cookies por segundo'.format(self.quantity, self.name, self.cps * self.quantity), True, WHITE)
        created = description_font.render('{}s criaram {} cookies até agora'.format(self.name, math.floor(self.created)), True, WHITE)
        
        x_pos = self.x - 30
        y_pos = pygame.mouse.get_pos()[1] - 200
        
        window.blit(building_display_background, (x_pos, y_pos))
        window.blit(self.icon, (x_pos + 3, y_pos + 3))
        window.blit(building_title, (x_pos + 43, y_pos + 3))
        
        '''Description'''
        space_between_lines = 16
        window.blit(production, (x_pos + 10, y_pos + 50))
        window.blit(quantity, (x_pos + 10, y_pos + 50 + space_between_lines*1))
        window.blit(created, (x_pos + 10, y_pos + 50 + space_between_lines*2))

            
class Player:
    def __init__(self):
        self.score = 0
        self.click_multiplier = 1
        self.total_cps = 0
    def updateTotalCPS(self, list_of_buildings):
        global timer, n_of_cookies
        
        self.total_cps = 0
        for building in list_of_buildings:
            self.total_cps += building.cps * building.quantity
        '''Updates number of falling cookies'''
        timer = 0
        if self.total_cps > 100000:
            n_of_cookies = 6
        elif self.total_cps > 10000:
            n_of_cookies = 8
        elif self.total_cps > 1000:
            n_of_cookies = 9
        elif self.total_cps > 100:
            n_of_cookies = 10
        elif self.total_cps > 10:
            n_of_cookies = 11
        elif self.total_cps > 0:
            n_of_cookies = 15
        
def format_number(n):
    if n >= 1000000000:
        if (n / 1000000000 )% 1 == 0:
            n = '{:.0f} billion'.format(n / 1000000000)
        else:
            n = '{:.2f} billion'.format(n / 1000000000)
    elif n >= 1000000:
        if (n / 1000000) % 1 == 0:
            n = '{:.0f} million'.format(n / 1000000) 
        else:
            n = '{:.2f} million'.format(n / 1000000)
    return n

def draw():
    global timer
    
    '''Draw background'''
    window.blit(background_img, (0, 0))
    
    '''Draws falling cookies'''
    if timer == n_of_cookies:
        list_of_falling_cookies.append(BackgroundCookie(random.randint(0, width), 0))
        timer = 0
    else:
        timer += 1
    for falling_cookie in list_of_falling_cookies:
        falling_cookie.draw()
        falling_cookie.animate(list_of_falling_cookies)
    
    '''Draws cookie and cookie display'''
    cookie.draw()
    cookie_display.draw(user.score, user.total_cps)
    
    '''Draws clicked cookies'''
    for falling_cookie in list_of_clicked_cookies:
        falling_cookie.animate(list_of_clicked_cookies)
        falling_cookie.draw()
    
    '''Draws wooden bars'''
    window.blit(wooden_background, (0, height/2))
    window.blit(wooden_background, (300 - 40, height/2))
    window.blit(wooden_background, (520, height/2))
    window.blit(wooden_bar, (0, height/2))
    window.blit(wooden_bar_r, (width - 16, height/2))
    window.blit(upgrades_wooden_bar, (0, height/2))
    
    '''Draw Buildings'''
    for building in list_of_buildings:
        if user.score >= building.getTotalCost():
            building.draw(solid=True)
        else:
            building.draw(solid=False)
        
            '''Adds cookies made through building'''
        user.score += building.quantity * building.cps * .01
        building.created += building.quantity * building.cps * .01
        
        '''Draws building stats if mouse hover'''
        if building.collidepoint(pygame.mouse.get_pos()):
            building.drawDisplayBox()

'''----------------------------------------------------------------------------------'''
cookie = CookieObj(275, 80)
cookie_display = CookieDisplayObj(355, 0)

n_of_cookies = -1
list_of_falling_cookies = []
timer = 0

list_of_clicked_cookies = []

'''Buildings'''
store_y = 440
aluno = Building('Aluno', 60, store_y, aluno_img, aluno_icon, base_cost=15, increase_per_purchase=1.15, cps=0.2)
funcionario = Building('Funcionario', 120 + 300*1, store_y, funcionario_img, funcionario_icon, base_cost=100, increase_per_purchase=1.15, cps=2)
professor = Building('Professor', 60, store_y + 64*2, professor_img, professor_icon, base_cost=1100, increase_per_purchase=1.15, cps=23)
mrcheney = Building('MrCheney', 120 + 300*1, store_y + 64*2, mrcheney_img, mrcheney_icon, base_cost=12000, increase_per_purchase=1.15, cps=100)

list_of_buildings = [aluno, funcionario, professor, mrcheney]

user = Player()

width = 800
height = 750

DARK_BLUE = (51, 90, 114)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (0, 255, 0)
GRAY = (155, 155, 155)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cheney Clicker')

main = True
timer = 0
state = 'inicial_screen'

musica.play()
while main == True:

    if state == 'inicial_screen':
        #tela inicial
        title_text = font_grande.render("Cheney's Clicker", True, BLACK)
        comeca = font.render('Clique no cookie para comecar', True, WHITE)

        window.blit(background_img, (0,0))
        window.blit(cookie_img_start, (width/3 - 15, height/4 + 60))
        window.blit(title_text, (width/3 - 65, height/4))
        window.blit(comeca, (width/3 - 78, height - 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if cookie_img_start.get_rect(center=(width / 2, height / 2)).collidepoint(event.pos):
                    click_sound.play()
                    state = "game"
    
    elif state == 'game':
    
        pygame.time.delay(10)
            
        for event in pygame.event.get():
                
            if event.type == pygame.QUIT:
                main = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                '''Click Cookie'''
                if cookie.collidepoint(mouse_pos):
                    user.score += 1 * user.click_multiplier
                    cookie.animation_state = 1
                    crunch_sound.play()
                    '''Draws new falling cookie'''
                    list_of_clicked_cookies.append( BackgroundCookie(pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10) )
                        
                    '''Buy Buildings'''
                for building in list_of_buildings:
                    if building.collidepoint(mouse_pos) and user.score >= building.getTotalCost():
                        click_sound.play()
                            
                        user.score -= building.getTotalCost()
                        building.quantity += 1
                        user.updateTotalCPS(list_of_buildings)
    
        draw()
    pygame.display.update()

pygame.quit()