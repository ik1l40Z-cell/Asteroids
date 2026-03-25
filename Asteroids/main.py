import pygame
import sys
import constants
import variables
from logger import log_state
from logger import log_event
from circleshape import CircleShape
from player import Player
from shot import Shot
from asteroid import *
from particle import *
from asteroidfield import AsteroidField

def main():
    pygame.init()
    print("Starting Asteroids with pygame version: 2.6.1")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    particles = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteField = AsteroidField()
    pygame.font.init()
    font = pygame.font.SysFont(None, 69)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    while variables.running:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            pass
        screen.fill("black")
        for drawn in drawable:
            drawn.draw(screen)
        updatable.update(dt)
        score_surface = font.render(f"||{variables.score:0{NUMB_OF_ZEROS}}||", False, "white")
        screen.blit(score_surface, (10, 10))
        lives_surface = font.render(f"{variables.lives} UP", False, "white")
        x_pos = SCREEN_WIDTH - lives_surface.get_width() - 10
        screen.blit(lives_surface, (x_pos, 10))
        for obj in asteroids:
            if isinstance(obj, Particle):
                continue
            for shot in shots:
                if obj.collides_with(shot):
                    log_event("asteroid_shot")
                    particles.add(Particle.explode(obj))
                    obj.split()
                    shot.kill()
        for part in particles.sprites():
            if part.duration <= 0:
                part.kill()
        if variables.timer <= 0:
            for asteroid in asteroids:
                if CircleShape.collides_with(player, asteroid):
                    if variables.shield or variables.timer > 0:
                        asteroid.split()
                        particles.add(Particle.explode(asteroid))
                        if variables.shield and variables.timer <= 0:
                            variables.shield = False
                            variables.timer = variables.iFrameTime
                            player.invincible(screen)
                        continue
                    if variables.lives > 0:
                        log_event("player_hit")
                        variables.lives -= 1
                        player.kill()
                        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        variables.timer = variables.iFrameTime
                        player.invincible(screen)
                        variables.shield = True
                    else:
                        log_event("player_killed")
                        print("Game over!")
                        sys.exit()
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
