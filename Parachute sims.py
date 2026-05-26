import pygame
import math

# Init
pygame.init()

WIDTH = 600
HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Parachute Hypothesis Simulator")

font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

# Constants for physics
g = 9.81  # gravity m/s^2
rho = 1.225  # air density kg/m^3

class Parachute:
    def __init__(self, x, y, mass, cd, area, shape, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.cd = cd
        self.area = area
        self.shape = shape
        self.color = color
        self.velocity = 0
        self.time = 0  # time since drop
        self.landed = False

    def update(self, dt):
        if not self.landed:
            drag_force = 0.5 * rho * self.cd * self.area * self.velocity ** 2
            net_force = self.mass * g - drag_force
            acceleration = net_force / self.mass

            self.velocity += acceleration * dt
            self.y += self.velocity * dt
            self.time += dt

            if self.y >= HEIGHT - 50:  # ground level with some margin
                self.y = HEIGHT - 50
                self.landed = True

    def draw(self, screen):
        if self.shape == 'no_parachute':
            pygame.draw.rect(screen, self.color, (self.x - 15, self.y - 15, 30, 30))
        elif self.shape == 'cruciform':
            # vertical rectangle
            pygame.draw.rect(screen, self.color, (self.x - 10, self.y - 30, 20, 60))
            # horizontal rectangle
            pygame.draw.rect(screen, self.color, (self.x - 30, self.y - 10, 60, 20))
        elif self.shape == 'hemisphere':
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 30)
            pygame.draw.rect(screen, BLACK, (self.x - 30, self.y, 60, 30))  # cover bottom half
        elif self.shape == 'annular':
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 30)
            pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 15)
        elif self.shape == 'parafoil':
            points = [
                (self.x - 30, self.y),
                (self.x - 15, self.y - 20),
                (self.x + 15, self.y - 20),
                (self.x + 30, self.y)
            ]
            pygame.draw.polygon(screen, self.color, points)

        # Draw the box/base under the parachute
        pygame.draw.rect(screen, GRAY, (self.x - 15, self.y + 20, 30, 30))

        # Draw descent time text above
        time_text = font.render(f"{self.time:.1f}s", True, WHITE)
        screen.blit(time_text, (self.x - 20, self.y - 60))


def main():
    parachutes = []

    # Parameters for the parachutes
    # mass in kg, cd drag coeff, area in m^2
    parachute_params = [
        (100, 1.05, 0.0, 'no_parachute', (255, 0, 0)),
        (100, 1.87, 1.0, 'cruciform', (0, 150, 255)),
        (100, 1.33, 1.0, 'hemisphere', (0, 200, 0)),
        (100, 1.6, 1.0, 'annular', (255, 165, 0)),
        (100, 2.0, 1.0, 'parafoil', (160, 32, 240))
    ]

    # Initial horizontal positions for parachutes spaced evenly
    start_x_positions = [100, 200, 300, 400, 500]

    # Create parachute objects
    for i, params in enumerate(parachute_params):
        mass, cd, area, shape, color = params
        parachutes.append(Parachute(start_x_positions[i], 50, mass, cd, area, shape, color))

    running = True
    while running:
        dt = clock.tick(60) / 1000  # delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update parachutes
        for p in parachutes:
            p.update(dt)

        # Drawing
        screen.fill(BLACK)

        for p in parachutes:
            p.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
