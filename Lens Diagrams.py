import pygame
import math
import time

pygame.init()
font = pygame.font.SysFont(None, 36)

WIDTH = 800
HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0,0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

speed = 2

class Convex_Lens:
    def __init__(self, focal_length, x, y):
        self.focal = focal_length
        self.x = x
        self.y = y
    
    def draw(self, screen, object_dist, object_h):
         pygame.draw.line(screen, BLUE, (0, self.y), (WIDTH, self.y), 2)
         pygame.draw.ellipse(screen, BLUE, (self.x - 10, self.y - 100, 20, 200), 3)

         obj_x = self.x - object_dist

         pygame.draw.line(screen, RED, (obj_x, self.y), (obj_x, self.y - object_h), 3)

         if object_dist == self.focal:
              return
                
         image_dist = (self.focal * object_dist) / (object_dist - self.focal)

         mag = image_dist / object_dist

         image_hight = object_h * mag

         image_x = self.x + image_dist

         pygame.draw.line(screen, GREEN, (image_x, self.y), (image_x, self.y + image_hight), 3)
         
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Convex Lens Simulator")

lens = Convex_Lens(100, WIDTH//2, HEIGHT//2)

object_distance = 150
object_height = 25


clock = pygame.time.Clock()
running = True
while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            object_distance += speed
        if keys[pygame.K_RIGHT]:
            object_distance -= speed

        if object_distance > 370:
             object_distance = 370
        if object_distance < 15:
             object_distance = 15

        screen.fill(WHITE)
        lens.draw(screen, object_distance, object_height)
        pygame.display.update()
        clock.tick(60)

pygame.quit()



    