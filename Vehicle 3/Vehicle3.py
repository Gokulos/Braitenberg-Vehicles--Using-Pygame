import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
ORANGE =  (244, 196, 48)
BROWN = (150, 75, 0)
BLUE = (0,0,255)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
YELLOW = (255, 255,   0)
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
FPS    = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vehicle 2")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Impact", 19)


inhibition = True
Cross_connection = False

class Circle:
    def __init__(self, position, radius, color):
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color,
                           (int(self.position.x), int(self.position.y)),
                           self.radius)

class Vehicle:
    def __init__(self, position, direction, radius=30, color=GREEN):
        self.position = pygame.math.Vector2(position)
        self.direction = direction
        self.radius = radius
        self.color = color
        self.speed_scaling = 600
        self.rotation_scaling = 2

        self.sensor_radius = 8
        self.sensor_offset = self.radius + self.sensor_radius
        self.sensor_spacing = 50

        self.speed_scaling = 100
        self.rotation_scaling = 5

        
        self.sensor_radius = 10
        self.sensor_offset = self.radius + self.sensor_radius
        
        self.sensor_spacing = 50
         
        self.left_sensor_position = (
            self.position
            + pygame.math.Vector2(0, -self.sensor_spacing)
            + pygame.math.Vector2(1, -self.sensor_spacing)
        )

        self.right_sensor_position = (
            self.position
            + pygame.math.Vector2(0, -self.sensor_spacing)
            + pygame.math.Vector2(1, self.sensor_spacing)
        )

        self.sensor_color = BLUE

    def draw(self, surface):
        pygame.draw.circle(surface, self.color,
                           (int(self.position.x), int(self.position.y)),
                           self.radius)
        pygame.draw.circle(surface, self.sensor_color,
                           (int(self.left_sensor_position.x), int(self.left_sensor_position.y)),
                           self.sensor_radius)
        pygame.draw.circle(surface, self.sensor_color,
                           (int(self.right_sensor_position.x), int(self.right_sensor_position.y)),
                           self.sensor_radius)

    

    def move(self, sun_position):
        forward = pygame.math.Vector2(0, -1).rotate(self.direction)
        right = forward.rotate(-90)
        ld = self.left_sensor_position.distance_to(sun_position)
        rd = self.right_sensor_position.distance_to(sun_position)

        ls = self.speed_scaling * (1 / ld)
        rs = self.speed_scaling * (1 / rd)

        speed = (ls + rs) / 2
        if inhibition:
            speed = 1 - speed

        rotation = (rs - ls) * self.rotation_scaling * -1
        if Cross_connection:
            rotation = -rotation

        self.direction += rotation
        direction_vector = pygame.math.Vector2(0, -1).rotate(self.direction)
        self.position += direction_vector * speed
        self.position.x %= WIDTH
        self.position.y %= HEIGHT

        self.left_sensor_position = (
            self.position
            + forward * self.sensor_offset
            - right * (self.sensor_spacing / 2)
        )

        self.right_sensor_position = (
            self.position
            + forward * self.sensor_offset
            + right * (self.sensor_spacing / 2)
        )
        
        text = f"ld: {ld:.4f}"
        text += f"\nRd: {rd:.4f}"
        text += f"\nspd: {speed:.4f}"
        text_surface = font.render(text, True, BROWN)
        screen.blit(text_surface, (10, 10))

sun = Circle((WIDTH // 2, HEIGHT // 2), radius=40, color=ORANGE)
vehicle = Vehicle((100, 100), direction=45)

running = True
while running:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    sun.draw(screen)
    vehicle.move(sun.position)
    vehicle.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
