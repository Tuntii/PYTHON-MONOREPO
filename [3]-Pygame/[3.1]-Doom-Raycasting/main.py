import pygame
import math

# Pygame başlangıcı
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doom Tarzı Raycasting")

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Harita (1 = Duvar, 0 = Boşluk)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

TILE_SIZE = 50
MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)

# Oyuncu
player_x = 100
player_y = 100
player_angle = 0
player_speed = 3
fov = math.pi / 4  


def cast_rays():
    for ray in range(0, WIDTH, 2):  

        ray_angle = player_angle - fov / 2 + (ray / WIDTH) * fov

        for depth in range(0, 500, 1):  
            target_x = player_x + depth * math.cos(ray_angle)
            target_y = player_y + depth * math.sin(ray_angle)

            if 0 <= target_x < MAP_WIDTH * TILE_SIZE and 0 <= target_y < MAP_HEIGHT * TILE_SIZE:
                map_x = int(target_x / TILE_SIZE)
                map_y = int(target_y / TILE_SIZE)

                if MAP[map_y][map_x] == 1:
                    color = GRAY if depth < 250 else (100, 100, 100) 
                    wall_height = HEIGHT / (depth + 0.0001)
                    pygame.draw.rect(
                        screen,
                        color,
                        (ray, HEIGHT // 2 - wall_height // 2, 2, wall_height),
                    )
                    break

# Kontroller
def handle_input():
    global player_x, player_y, player_angle

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: 
        player_x += player_speed * math.cos(player_angle)
        player_y += player_speed * math.sin(player_angle)
    if keys[pygame.K_s]:  
        player_x -= player_speed * math.cos(player_angle)
        player_y -= player_speed * math.sin(player_angle)
    if keys[pygame.K_a]:  
        player_angle -= 0.1
    if keys[pygame.K_d]:  
        player_angle += 0.1

    if MAP[int(player_y / TILE_SIZE)][int(player_x / TILE_SIZE)] == 1:
        player_x -= player_speed * math.cos(player_angle)
        player_y -= player_speed * math.sin(player_angle)

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_input()
    cast_rays()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
