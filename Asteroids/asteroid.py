import pygame
import random
import constants
from logger import log_event
from circleshape import CircleShape

class Asteroid(CircleShape):
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius)

	def draw(self, screen):
		pygame.draw.circle(screen, "white", self.position, self.radius, constants.LINE_WIDTH)

	def update(self, dt):
		self.position += self.velocity * dt

	def split(self):
		self.kill()
		if self.radius <= constants.ASTEROID_MIN_RADIUS:
			constants.SCORE += 125
			return
		log_event("asteroid_split")
		constants.SCORE += 42
		num = random.uniform(20, 50)
		new_vec1 = self.velocity.rotate(num)
		new_vec2 = self.velocity.rotate(-num)
		new_rad = self.radius - constants.ASTEROID_MIN_RADIUS
		smol_ast1 = Asteroid(self.position.x, self.position.y, new_rad)
		smol_ast2 = Asteroid(self.position.x, self.position.y, new_rad)
		smol_ast1.velocity = new_vec1
		smol_ast2.velocity = new_vec2
