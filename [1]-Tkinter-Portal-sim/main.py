import pygame
import pymunk
import pymunk.pygame_util
import math

# Pygame başlangıç ayarları
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
space = pymunk.Space()
space.gravity = (0, 900)

# Portal ve top özellikleri
PORTAL_RADIUS = 40
PORTAL_PAIR = [(200, 300), (600, 300)]  # Portal koordinatları
BALL_RADIUS = 15
BALL_MASS = 1

# Portal mekanikleri için yardımcı fonksiyonlar
def teleport_ball(ball_body, portal_entry, portal_exit):
    # Konumu ve hızı yeniden ayarla
    relative_position = ball_body.position - portal_entry
    new_position = portal_exit + relative_position
    angle_offset = math.atan2(
        portal_exit[1] - portal_entry[1], portal_exit[0] - portal_entry[0]
    )
    velocity_magnitude = ball_body.velocity.length
    new_velocity = pymunk.Vec2d(
        velocity_magnitude * math.cos(angle_offset),
        velocity_magnitude * math.sin(angle_offset),
    )
    ball_body.position = new_position
    ball_body.velocity = new_velocity

# Top yaratma fonksiyonu
def create_ball(space, position):
    body = pymunk.Body(BALL_MASS, pymunk.moment_for_circle(BALL_MASS, 0, BALL_RADIUS))
    body.position = position
    shape = pymunk.Circle(body, BALL_RADIUS)
    shape.elasticity = 0.9
    shape.friction = 0.5
    space.add(body, shape)
    return body

# Portalları çizme fonksiyonu
def draw_portals():
    for portal in PORTAL_PAIR:
        pygame.draw.circle(screen, (0, 255, 0), portal, PORTAL_RADIUS, 2)

# Topu çizme fonksiyonu
def draw_ball(ball_body):
    pygame.draw.circle(screen, (255, 0, 0), ball_body.position, BALL_RADIUS)

# Top yarat
ball_body = create_ball(space, (100, 100))

# Simülasyon döngüsü
running = True
while running:
    screen.fill((0, 0, 0))
    draw_portals()
    draw_ball(ball_body)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Topun portal ile çarpışma durumunu kontrol et
# Topun portal ile çarpışma durumunu kontrol et
    for portal_entry, portal_exit in zip(PORTAL_PAIR, reversed(PORTAL_PAIR)):
        portal_entry_vec = pymunk.Vec2d(*portal_entry)  # Tuple -> Vec2d
        distance_to_portal = ball_body.position.get_distance(portal_entry_vec)
        if distance_to_portal < PORTAL_RADIUS:
            teleport_ball(ball_body, portal_entry_vec, pymunk.Vec2d(*portal_exit))


    # Fizik simülasyonu
    space.step(1 / 60.0)

    # Ekranı güncelle
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
