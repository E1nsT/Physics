import pygame 
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (81, 81, 252)
RED = (181, 52, 9)
GRAY = (99, 97, 97)
DIRTY_YELLOW = (150, 137, 72)
DIRTY_GRAY = (214, 197, 178)
DARK_GRAY = (79, 78, 77)
DARK_YELLOW = (143, 101, 37)
LIGHT_BLUE = (117, 193, 199)
DARK_BLUE = (66, 139, 212)
FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  
    TIMESTEP = 3600 * 24 

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.sun = False
        self.distance_to_sun = 0

        self.orbit = []
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * Planet.SCALE + WIDTH / 2
        y = self.y * Planet.SCALE + HEIGHT / 2

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = Planet.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * Planet.TIMESTEP
        self.y_vel += total_fy / self.mass * Planet.TIMESTEP

        self.x += self.x_vel * Planet.TIMESTEP
        self.y += self.y_vel * Planet.TIMESTEP
        self.orbit.append((self.x, self.y))

    @staticmethod    
    def kuiper_belt(num_objects):
        kuiper_belt = []
        for _ in range(num_objects): 
            distance = random.uniform(30 * Planet.AU, 50 * Planet.AU) 
            angle = random.uniform(0, 2 * math.pi)
            x = distance * math.cos(angle)
            y = distance * math.sin(angle)
            radius = random.randint(1, 4)
            mass = random.uniform(1e22, 1e23)
            kuiper_object = Planet(x, y, radius, GRAY, mass)
            orbit_speed = math.sqrt(Planet.G * 1.98892e30 / distance) 
            kuiper_object.x_vel = - orbit_speed * math.sin(angle)
            kuiper_object.y_vel = orbit_speed * math.cos(angle)
            kuiper_belt.append(kuiper_object)
        return kuiper_belt
    
    @staticmethod    
    def asteroid(num_objects, sun):
        asteroid = []
        for _ in range(num_objects): 
            distance = random.uniform(2.1 * Planet.AU, 3.3 * Planet.AU) 
            angle = random.uniform(0, 2 * math.pi)
            x = distance * math.cos(angle)
            y = distance * math.sin(angle)
            radius = random.randint(1, 3)
            mass = random.uniform(1e22, 1e23)
            asteroids_object = Planet(x, y, radius, GRAY, mass)
            orbit_speed = math.sqrt(Planet.G * sun.mass / distance) 
            asteroids_object.x_vel = - orbit_speed * math.sin(angle)
            asteroids_object.y_vel = orbit_speed * math.cos(angle)
            asteroid.append(asteroids_object)
        return asteroid

    
def main():
    run = True
    clock = pygame.time.Clock()
    scale_factor = 50 / Planet.AU  

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, GRAY, 0.330 * 10**24)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, DIRTY_YELLOW, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(5.2 * Planet.AU, 0, 20, DIRTY_GRAY, 1.898 * 10**27)
    jupiter.y_vel = -13.07 * 1000 

    saturn = Planet(9.59 * Planet.AU, 0, 24, DARK_YELLOW, 5.6834 * 10**26) 
    saturn.y_vel = -9.68 * 1000
    
    uranus = Planet(19 * Planet.AU, 0, 28, LIGHT_BLUE, 2.5362 * 10**20)
    uranus.y_vel = -5.43 * 1000

    neptune = Planet(30 * Planet.AU, 0, 32, DARK_BLUE, 2.4622 * 10**20)
    neptune.y_vel = -6.80 * 1000 
    
    kuiper_belt_objects = Planet.kuiper_belt(100)
    asteroid_belt_objects = Planet.asteroid(100, sun)

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, neptune, uranus] + kuiper_belt_objects + asteroid_belt_objects

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: 
                    scale_factor *= 1.1
                if event.button == 5: 
                    scale_factor /= 1.1

        Planet.SCALE = scale_factor 

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()