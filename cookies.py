import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurar a janela
width, height = 800, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cheney's Clicker")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Carregar imagens
cookie_image = pygame.image.load('cookie.png').convert_alpha()
cookie_image_normal = pygame.transform.scale(cookie_image, (300, 289))
cookie_image_large = pygame.transform.scale(cookie_image, (330, 319))
cookie_image_start = pygame.transform.scale(cookie_image, (400, 400))

background_image = pygame.image.load('background.png').convert()
background_image = pygame.transform.scale(background_image, (width, height))

imagem_upgrade = pygame.image.load('upgrade.png').convert_alpha()
imagem_upgrade = pygame.transform.scale(imagem_upgrade, (30, 30))

# Posição e tamanho do cookie
cookie_rect = cookie_image_normal.get_rect(center=(width / 2, height / 4))
cookinho_img = pygame.transform.scale(cookie_image, (30,29))
cookinho_width = 30
cookinho_height = 29
icone_cookie = pygame.transform.scale(cookie_image, (20,20))

# Fontes para o texto
font_title = pygame.font.Font(None, 72)  # Fonte do título
font = pygame.font.Font(None, 36)
font_custo_upgrade = pygame.font.Font(None, 26)

# Contador de cliques e valor por clique
click_count = 0
value_per_click = 1

# Custo de upgrade
upgrade_cost = 10

# Botão de upgrade
upgrade_button = pygame.Rect(width - 165, 10, 155, 40)
aba = pygame.Rect(0, height/2, width, height/2)
borda = pygame.Rect(0, height/2, width, 25)

# Pulsar cookie
pulse = False

# Estado do jogo
state = "start_screen"

# clock
clock = pygame.time.Clock()

# Classe cookies
class Cookie(pygame.sprite.Sprite):
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width-cookinho_width)
        self.rect.y = random.randint(-100, -cookinho_height)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 4)
    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.top > height or self.rect.right < 0 or self.rect.left > width:
            self.rect.x = random.randint(0, width-cookinho_width)
            self.rect.y = random.randint(-100, -cookinho_height)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(2, 4)
            
# Chuva de cookies
all_cookies = pygame.sprite.Group()
for i in range(20):
    cookie = Cookie(cookinho_img)
    all_cookies.add(cookie)

# Loop principal do jogo
while True:
    clock.tick(60)
    # Desenhar o fundo (mesmo para ambas as telas)
    screen.blit(background_image, (0, 0))
    
    if state == "start_screen":
        # Tela inicial
        title_text = font_title.render("Cheney's Clicker", True, BLACK)
        screen.blit(title_text, (width / 2 - title_text.get_width() / 2, height / 4 - title_text.get_height()))
        screen.blit(cookie_image_start, cookie_image_start.get_rect(center=(width / 2, height / 2)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if cookie_image_start.get_rect(center=(width / 2, height / 2)).collidepoint(event.pos):
                    state = "game"

    elif state == "game":
        # Jogo principal
        all_cookies.update()
        all_cookies.draw(screen)
        
        # Processar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Checar se o clique foi no cookie
                if cookie_rect.collidepoint(event.pos):
                    click_count += value_per_click
                    pulse = True
                # Checar se o clique foi no botão de upgrade
                elif upgrade_button.collidepoint(event.pos) and click_count >= upgrade_cost:
                    value_per_click += 0.2
                    click_count -= upgrade_cost
                    upgrade_cost += 5

        # Desenhar o cookie com pulsação
        if pulse:
            screen.blit(cookie_image_large, cookie_image_large.get_rect(center=(width / 2, height / 4)))
            pulse = False
        else:
            screen.blit(cookie_image_normal, cookie_rect)

        # Desenhar o texto com a contagem de cliques
        text = font.render(f'Cookies: {int(click_count)}', True, WHITE)
        screen.blit(text, (330, 20))
        
        # Aba dos upgrades
        pygame.draw.rect(screen, (1, 15, 20), aba)
        pygame.draw.rect(screen, (19, 92, 112), borda)

        # Desenhar o botão de upgrade
        pygame.draw.rect(screen, (166, 159, 151), upgrade_button, border_radius=4)
        text_upgrade = font.render(f'Upgrade', True, WHITE)
        custo_upgrade = font_custo_upgrade.render(f'{upgrade_cost}', True, WHITE)
        
        # Blit dos textos
        screen.blit(text_upgrade, (width - 155, 20))
        screen.blit(imagem_upgrade, (width - 50, 15))
        screen.blit(custo_upgrade, (width - 135, 60))
        screen.blit(icone_cookie, (width - 160, 58))

    pygame.display.flip()
'Cookie eh bom, ninguem da'