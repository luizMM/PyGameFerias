import pygame
import sys
import random
import math

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
cookie_image = pygame.image.load('imagens/cookie.png').convert_alpha()
cookie_image_normal = pygame.transform.scale(cookie_image, (300, 289))
cookie_image_large = pygame.transform.scale(cookie_image, (330, 319))
cookie_image_start = pygame.transform.scale(cookie_image, (400, 400))

background_image = pygame.image.load('imagens/background.png').convert()
background_image = pygame.transform.scale(background_image, (width, height))

imagem_upgrade = pygame.image.load('imagens/upgrade.png').convert_alpha()
imagem_upgrade = pygame.transform.scale(imagem_upgrade, (30, 30))

aluno = pygame.image.load('imagens/aluno.png').convert_alpha()
aluno = pygame.transform.scale(aluno, (100,100))

fundo_aba = pygame.image.load('imagens/fundo_aba_upgrades.png').convert_alpha()
fundo_aba = pygame.transform.scale(fundo_aba, (width+300, height))

borda_botao = pygame.image.load('imagens/borda botao.png').convert_alpha()
borda_botao = pygame.transform.scale(borda_botao, (250, 75))

borda = pygame.image.load('imagens/borda2.png').convert_alpha()
borda = pygame.transform.scale(borda, (width, 60))

funcionario = pygame.image.load('imagens/funcionario.png').convert_alpha()
funcionario = pygame.transform.scale(funcionario, (115,115))

building_display_background = pygame.image.load('imagens/building_display_background.png')

# Posição e tamanho do cookie
cookie_rect = cookie_image_normal.get_rect(center=(width / 2, height / 4))
<<<<<<< HEAD
cookinho_img = pygame.transform.scale(cookie_image, (30, 29))
cookinho_width = 30
cookinho_height = 29
icone_cookie = pygame.transform.scale(cookie_image, (20, 20))
=======
cookinho_img = pygame.transform.scale(cookie_image, (30,30))
cookinho_width = 30
cookinho_height = 29
icone_cookie = pygame.transform.scale(cookie_image, (25,25))
>>>>>>> 466b892ebbd7b865b58a7b1d6676471e4f734e29

# Fontes para o texto
font_title = pygame.font.Font(None, 72)  # Fonte do título
font = pygame.font.Font(None, 36)
font_custo_upgrade = pygame.font.Font(None, 30)
font_quant = pygame.font.Font(None, 80)

# Contador de cliques e valor por clique
click_count = 0
value_per_click = 1
funcionarios = 0
alunos = 0

# Custo de upgrade
<<<<<<< HEAD
upgrade_costs = [10, 20, 30, 40]

# Botões de upgrade
upgrade_buttons = [
    pygame.Rect(width - 165, 10 + i * 60, 155, 40) for i in range(4)
]
=======
upgrade_cost = 10
super_upgrade_cost = 100

# Botão de upgrade
upgrade_button_x = 70
upgrade_button_y = height/2 + 55

upgrade_button = pygame.Rect(upgrade_button_x, upgrade_button_y, 250, 75)
super_upgrade_button = pygame.Rect(450, height/2 + 55, 300, 75)

#aba = pygame.Rect(0, height/2, width, height/2)
#borda = pygame.Rect(0, height/2, width, 25)
>>>>>>> 466b892ebbd7b865b58a7b1d6676471e4f734e29

# Pulsar cookie
pulse = False

# Estado do jogo
state = "start_screen"

# clock
clock = pygame.time.Clock()

# Classe cookies
class Cookie(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - cookinho_width)
        self.rect.y = random.randint(-100, -cookinho_height)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 4)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > height or self.rect.right < 0 or self.rect.left > width:
            self.rect.x = random.randint(0, width - cookinho_width)
            self.rect.y = random.randint(-100, -cookinho_height)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(2, 4)


# Chuva de cookies
all_cookies = pygame.sprite.Group()
for i in range(30):
    cookie = Cookie(cookinho_img)
    all_cookies.add(cookie)

#caixa_aluno = CaixaLateral(upgrade_button, 'Aluno', 70, height/2 + 55, aluno, aluno, base_cost=10, increase_per_purchase=1.15, cps=0)
#caixa_funcionario = CaixaLateral()

# Loop principal do jogo
while True:
    clock.tick(60)

    mouse_x, mouse_y = pygame.mouse.get_pos()

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
<<<<<<< HEAD
                # Checar se o clique foi em um dos botões de upgrade
                for i, upgrade_button in enumerate(upgrade_buttons):
                    if upgrade_button.collidepoint(event.pos) and click_count >= upgrade_costs[i]:
                        value_per_click += 0.2
                        click_count -= upgrade_costs[i]
                        upgrade_costs[i] += 5
=======
                # Checar se o clique foi no botão de upgrade
                elif upgrade_button.collidepoint(event.pos) and click_count >= upgrade_cost:
                    value_per_click += 0.2
                    click_count -= upgrade_cost
                    upgrade_cost += 5
                    alunos += 1

                # Checar se o clique foi no botão super upgrade
                elif super_upgrade_button.collidepoint(event.pos) and click_count >= super_upgrade_cost:
                    value_per_click += 2
                    click_count -= super_upgrade_cost
                    super_upgrade_cost += 100
                    funcionarios += 1
>>>>>>> 466b892ebbd7b865b58a7b1d6676471e4f734e29

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
<<<<<<< HEAD
        aba = pygame.Rect(0, height / 2, width, height / 2)
        borda = pygame.Rect(0, height / 2, width, 25)
        pygame.draw.rect(screen, (1, 15, 20), aba)
        pygame.draw.rect(screen, (19, 92, 112), borda)

        # Desenhar os botões de upgrade
        for i, upgrade_button in enumerate(upgrade_buttons):
            pygame.draw.rect(screen, (166, 159, 151), upgrade_button, border_radius=4)
            text_upgrade = font.render(f'Upgrade', True, WHITE)
            custo_upgrade = font_custo_upgrade.render(f'{upgrade_costs[i]}', True, WHITE)

            # Blit dos textos
            screen.blit(text_upgrade, (upgrade_button.x + 5, upgrade_button.y + 10))
            screen.blit(imagem_upgrade, (upgrade_button.x + 110, upgrade_button.y + 5))
            screen.blit(custo_upgrade, (upgrade_button.x - 25, upgrade_button.y + 40))
            screen.blit(icone_cookie, (upgrade_button.x - 50, upgrade_button.y + 38))
=======
        #pygame.draw.rect(screen, (19, 92, 112), borda)

        # Blit do da aba e fundo da aba upgrades
        screen.blit(fundo_aba, (-140, height/2))
        screen.blit(borda, (0, height/2 - 40))

        # Desenhar o botão de upgrade
        pygame.draw.rect(screen, (166, 159, 151), upgrade_button, border_radius=4)
        text_upgrade = font.render(f'Aluno', True, WHITE)
        custo_upgrade = font_custo_upgrade.render(f'{upgrade_cost}', True, WHITE)

        pygame.draw.rect(screen, (166, 159, 151), super_upgrade_button, border_radius=4)
        text_super_upgrade = font.render(f'Funcionario', True, WHITE)
        custo_super_upgrade = font_custo_upgrade.render(f'{super_upgrade_cost}', True, WHITE)

        n_alunos = font_quant.render(f'{alunos}', True, (84, 84, 84))
        screen.blit(n_alunos, (260, height/2 + 55))
        n_funcionarios = font_quant.render(f'{funcionarios}', True, (84, 84, 84))
        screen.blit(n_funcionarios, (690, height/2 + 55))
        
        # Blit dos textos
        #screen.blit(borda_botao, (70, height/2 + 55))
        screen.blit(text_upgrade, (160, height/2 + 68))
        screen.blit(aluno, (65, height/2 + 40))
        screen.blit(custo_upgrade, (70+120, height/2 + 100))
        screen.blit(icone_cookie, (40+120, height/2 + 96))

        screen.blit(text_super_upgrade, (525, height/2 + 68))
        screen.blit(funcionario, (435, height/2 + 30))
        screen.blit(custo_super_upgrade, (555, height/2 + 100))
        screen.blit(icone_cookie, (525, height/2 + 96))
>>>>>>> 466b892ebbd7b865b58a7b1d6676471e4f734e29

        if mouse_x == upgrade_button.x or mouse_y == upgrade_button.y:
            screen.blit(building_display_background, (mouse_x, mouse_y))
        

    pygame.display.flip()
