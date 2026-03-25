from constants import *
import pygame
import random
from asteroid import Asteroid

class Particle(Asteroid):
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius)
		self.duration = PARTICLES_LIFESPAN

	def draw(self, screen):
		# A "fading" draw
		color_value = max(5, min(255, int(255 * (self.duration))))
		pygame.draw.circle(
			screen,
			(color_value, color_value, color_value),
			self.position,
			self.radius,
			LINE_WIDTH)

	def update(self, dt):
		self.position += (self.velocity * dt)
		self.duration -= dt

	def split(self):
		pass

	def explode(self):
		frags_parts = pygame.sprite.Group()
		particleRad = self.radius / PARTICLE_RAD_DIVIDER
		count = 0
		part_num = random.uniform(HALF_NUMB_PARTS_MIN, HALF_NUMB_PARTS_MAX)
		while count <= part_num:
			count += 1
			nbRan = random.uniform(0, 360)
			particleVariad = random.uniform(
				particleRad * PARTICLE_VARIAD_MIN,
				particleRad * PARTICLE_VARIAD_MAX)
			part_vec1 = self.velocity.rotate(nbRan)
			part_vec2 = self.velocity.rotate(-nbRan)
			part_ast1 = Particle(self.position.x, self.position.y, particleVariad)
			part_ast2 = Particle(self.position.x, self.position.y, particleVariad)
			part_ast1.velocity = part_vec1
			part_ast2.velocity = part_vec2
			frags_parts.add(part_ast1)
			frags_parts.add(part_ast2)
			return frags_parts
