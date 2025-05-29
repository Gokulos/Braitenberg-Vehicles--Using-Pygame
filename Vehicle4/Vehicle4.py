import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 900, 650
ORANGE = (244, 196, 48)
BROWN = (150, 75, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
FPS = 60
WHITE = (255, 255, 255)


THRESHOLD_SPEED = 4
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vehicle 4")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Impact", 16)


def non_linear_Gauss_func(distance, peak_distance, max_speed):
    sigma = peak_distance / 2
    return max_speed * math.exp(-((distance - peak_distance) ** 2) / (2 * sigma ** 2))


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
    def __init__(self, position, direction, radius=20, color=GREEN, use_threshold = False):
        self.position = pygame.math.Vector2(position)
        self.direction = direction
        self.radius = radius
        self.color = color
        self.use_threshold = use_threshold
        self.sensor_radius = 7
        self.sensor_offset = self.radius + self.sensor_radius + 5
        self.sensor_spacing = 40

        self.sensor_color = BLUE

        self.max_speed = 4.5
        self.rotation_scaling = 3

        self.update_sensors()

    def update_sensors(self):
        forward = pygame.math.Vector2(0, -1).rotate(self.direction)
        right = forward.rotate(-90)
        self.left_sensor_position = self.position + forward * self.sensor_offset - right * (self.sensor_spacing / 2)
        self.right_sensor_position = self.position + forward * self.sensor_offset + right * (self.sensor_spacing / 2)

    def move(self, sun1_pos, sun2_pos, debug_y_offset=10):
        # Compute distances from sensors to each sun
            
        ld1 = self.left_sensor_position.distance_to(sun1_pos)
        ld2 = self.left_sensor_position.distance_to(sun2_pos)
        ld = min(ld1, ld2)

        rd1 = self.right_sensor_position.distance_to(sun1_pos)
        rd2 = self.right_sensor_position.distance_to(sun2_pos)
        rd = min(rd1, rd2)

        peak_distance = 150
        max_speed = self.max_speed
            
        ls = non_linear_Gauss_func(rd, peak_distance, max_speed)
        rs = non_linear_Gauss_func(ld, peak_distance, max_speed) 

        speed = (ls + rs) / 2
        rotation = (rs - ls) * self.rotation_scaling

        if self.use_threshold == True:
            if speed <= THRESHOLD_SPEED:
                self.update_sensors()
                return

        self.direction += rotation
        forward = pygame.math.Vector2(0, -1).rotate(self.direction)
        self.position += forward * speed

        self.position.x %= WIDTH
        self.position.y %= HEIGHT

        self.update_sensors()

        lines = [
            f"Ldist1: {ld1:.2f}  Ldist2: {ld2:.2f}",
            f"Rdist1: {rd1:.2f}  Rdist2: {rd2:.2f}",
            f"Lspeed: {ls:.2f}  Rspeed: {rs:.2f}",
            f"Speed: {speed:.2f}  Rot: {rotation:.2f}"
        ]
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, BROWN)
            screen.blit(text_surface, (10, debug_y_offset + i * 18))

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

use_threshold = False
sun1 = Circle((WIDTH // 3, HEIGHT // 2), radius=30, color=ORANGE)
sun2 = Circle((WIDTH // 1.5, HEIGHT // 1.5), radius=30, color=ORANGE)
vehicle_4a = Vehicle((100, 100), direction=45, use_threshold=False)

vehicle_4b_not_moving = Vehicle((100, 200), direction=45, color=RED, use_threshold=True)

mid_x = (sun1.position.x + sun2.position.x) / 2
mid_y = (sun1.position.y + sun2.position.y) / 2
vehicle_4b_near_moving = Vehicle((mid_x, mid_y), direction=0, color=RED, use_threshold=True)


running = True
while running:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    sun1.draw(screen)
    sun2.draw(screen)
    vehicle_4a.move(sun1.position, sun2.position, debug_y_offset=10)
    vehicle_4a.draw(screen)
    
    vehicle_4b_not_moving.move(sun1.position, sun2.position, debug_y_offset=90)
    vehicle_4b_not_moving.draw(screen)
    
    vehicle_4b_near_moving.move(sun1.position, sun2.position, debug_y_offset=170)
    vehicle_4b_near_moving.draw(screen)


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
