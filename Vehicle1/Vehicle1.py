import pygame
import math

pygame.init()

WIDTH, HEIGHT = 720, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Braitenberg Vehicle 1")

font = pygame.font.SysFont("Impact", 15)

clock = pygame.time.Clock()
fps = 60

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Vehicle:
    def __init__(self, position, direction, colour, radius=50):
        self.colour = colour
        self.position = pygame.math.Vector2(position)
        self.direction = direction  # in degrees
        self.radius = radius
        self.initial_position = pygame.math.Vector2(100, 500)

        # Sensor properties
        self.sensor_radius = 15
        self.sensor_offset = self.radius + self.sensor_radius
        self.sensor_color = BLACK
        self.update_sensor_position()

    def update_sensor_position(self):
        self.sensor_position = self.position + pygame.math.Vector2(0, -self.sensor_offset).rotate(self.direction)

    def get_speed(self, sun_position):
        distance = self.sensor_position.distance_to(sun_position) # Euclidean Distace
        if distance < 1:
            distance = 1
        speed = 200 / distance
        return speed, distance

    def move(self, sun_position):
        speed, distance = self.get_speed(sun_position)

        # Display speed and distance
        msg1 = f"Distance to Sun: {distance:.2f}"
        screen.blit(font.render(msg1, True, BLACK), (10, 10))
        msg2 = f"Current Speed: {speed * 10:.2f}"  # multiplied 10 just to make it look better as speeds less than 1 looks weird
        screen.blit(font.render(msg2, True, BLACK), (10, 30))

        vec_direction = pygame.math.Vector2(0, -1).rotate(self.direction)
        self.position += vec_direction * speed

        # For resetting the position after vehicle exits the screen
        if (self.position.x < -self.radius or self.position.x > WIDTH + self.radius or
                self.position.y < -self.radius or self.position.y > HEIGHT + self.radius):
            self.position = self.initial_position.copy()

        self.update_sensor_position()

    def draw(self, surface):
        pygame.draw.circle(surface, self.colour, (int(self.position.x), int(self.position.y)), self.radius)
        pygame.draw.circle(surface, self.sensor_color, (int(self.sensor_position.x), int(self.sensor_position.y)), self.sensor_radius)


# Sun
sun_position = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)

def draw_sun(surface):
    pygame.draw.circle(surface, YELLOW, (int(sun_position.x), int(sun_position.y)), 30)

# Create vehicle
vehicle = Vehicle((100, 500), direction=45, colour=RED)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    draw_sun(screen)
    vehicle.move(sun_position)
    vehicle.draw(screen)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
