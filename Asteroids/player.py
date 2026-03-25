import math
import pygame
import variables
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
	def __init__(self, x, y):
		super().__init__(x, y, PLAYER_RADIUS)
		self.PLAYER_RADIUS = PLAYER_RADIUS
		self.rotation = 0
		self.cooldown = 0

	# in the Player class
	def triangle(self):
		forward = pygame.Vector2(0, 1).rotate(self.rotation)
		right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
		a = self.position + forward * self.radius
		b = self.position - forward * self.radius - right
		c = self.position - forward * self.radius + right
		return [a, b, c]

	def draw(self, screen):
		if variables.timer <= 0:
			pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
		else:
			pulse = math.sin(variables.timer * 15)
			fade_value = int(255 * (pulse + 1) / 2)
			pygame.draw.polygon(screen, (fade_value, fade_value, fade_value), self.triangle(), LINE_WIDTH)

	def rotate(self, dt):
		self.rotation += PLAYER_TURN_SPEED * dt

	def move(self, dt):
		unit_vector = pygame.Vector2(0, 1)
		rotated_vector = unit_vector.rotate(self.rotation)
		rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
		self.position += rotated_with_speed_vector

	def shoot(self):
		shot = Shot(self.position.x, self.position.y)
		direction = pygame.Vector2(0, 1).rotate(self.rotation)
		shot.velocity = direction * PLAYER_SHOOT_SPEED

	def invincible(self, screen):
		variables.timer = variables.iFrameTime

	def update(self, dt):
		keys = pygame.key.get_pressed()
		self.cooldown -= dt
		variables.timer -= dt
		if keys[pygame.K_a]:
			self.rotate(-dt)
		if keys[pygame.K_d]:
			self.rotate(dt)
		if keys[pygame.K_s]:
			self.move(-dt)
		if keys[pygame.K_w]:
			self.move(dt)
		if keys[pygame.K_SPACE]:
			if self.cooldown > 0:
				return
			self.shoot()
			self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
