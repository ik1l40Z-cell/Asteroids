import pygame
import random
from constants import *
from logger import log_event
from circleshape import CircleShape

class Asteroid(CircleShape):
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius)

	def draw(self, screen):
		pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

	def update(self, dt):
		self.position += self.velocity * dt

	def split(self):
		self.kill()
		if self.radius <= ASTEROID_MIN_RADIUS:
			return
		log_event("asteroid_split")
		num = random.uniform(20, 50)
		new_vec1 = self.velocity.rotate(num)
		new_vec2 = self.velocity.rotate(-num)
		new_rad = self.radius - ASTEROID_MIN_RADIUS
		smol_ast1 = Asteroid(self.position.x, self.position.y, new_rad)
		smol_ast2 = Asteroid(self.position.x, self.position.y, new_rad)
		smol_ast1.velocity = new_vec1
		smol_ast2.velocity = new_vec2
