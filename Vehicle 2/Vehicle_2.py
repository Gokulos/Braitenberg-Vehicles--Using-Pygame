import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Braitenberg Vehicle 2 - Single Vehicle")

RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
YELLOW = (255, 255,   0)
FPS    = 60

clock = pygame.time.Clock()

class Circle:
    def __init__(self, position, radius, color):
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)

class Vehicle:
    def __init__(self, position, direction, radius=30, color=RED):
        self.position = pygame.math.Vector2(position)
        self.direction = direction
        self.radius = radius
        self.color = color

        self.speed_scaling = 600
        self.rotation_scaling = 2

        self.sensor_radius = 8
        self.sensor_offset = self.radius + self.sensor_radius
        self.sensor_spacing = 50

        self.sensor_color = GREEN
        self.update_sensors()

    def update_sensors(self):
        forward = pygame.math.Vector2(0, -1).rotate(self.direction)
        right = forward.rotate(-90)
        self.left_sensor_position = self.position + forward * self.sensor_offset - right * (self.sensor_spacing / 2)
        self.right_sensor_position = self.position + forward * self.sensor_offset + right * (self.sensor_spacing / 2)

    def move(self, sun_position):
        forward = pygame.math.Vector2(0, -1).rotate(self.direction)

        ld = self.left_sensor_position.distance_to(sun_position)
        rd = self.right_sensor_position.distance_to(sun_position)

        rs = self.speed_scaling / max(ld, 1)
        ls = self.speed_scaling / max(rd, 1)

        speed = (ls + rs) / 2
        
        rotation = (rs - ls) * self.rotation_scaling * -0.5  # Moving Away from the source

        self.direction += rotation
        forward = pygame.math.Vector2(0, -1).rotate(self.direction)
        self.position += forward * speed

        self.position.x %= WIDTH
        self.position.y %= HEIGHT

        self.update_sensors()

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)
        pygame.draw.circle(surface, self.sensor_color, (int(self.left_sensor_position.x), int(self.left_sensor_position.y)), self.sensor_radius)
        pygame.draw.circle(surface, self.sensor_color, (int(self.right_sensor_position.x), int(self.right_sensor_position.y)), self.sensor_radius)

    def bounce(self):
        self.direction += 90

def check_collision(v, c):
    return v.position.distance_to(c.position) < (v.radius + c.radius)

sun = Circle((WIDTH // 2, HEIGHT // 2), radius=30, color=YELLOW)

# Only one vehicle
x = random.randint(0, WIDTH)
y = random.randint(0, HEIGHT)
direction = random.randint(0, 360)
vehicle = Vehicle((x, y), direction, radius=30, color=(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))

# Main loop
running = True
while running:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    sun.draw(screen)

    # Bounce off the sun
    if check_collision(vehicle, sun):
        vehicle.bounce()

    vehicle.move(sun.position)
    vehicle.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
