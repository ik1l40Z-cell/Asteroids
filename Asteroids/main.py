import pygame
import sys
import constants
from logger import log_state
from logger import log_event
from circleshape import CircleShape
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    pygame.init()
    print("Starting Asteroids with pygame version: 2.6.1")
    print(f"Screen width: {constants.SCREEN_WIDTH}")
    print(f"Screen height: {constants.SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteField = AsteroidField()
    pygame.font.init()
    font = pygame.font.SysFont(None, 69)
    player = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            pass
        screen.fill("black")
        for drawn in drawable:
            drawn.draw(screen)
        updatable.update(dt)
        score_surface = font.render(f"Score: {constants.SCORE}", False, "white")
        screen.blit(score_surface, (10, 10))
        lives_surface = font.render(f"Lives: {constants.LIVES}", False, "white")
        x_pos = constants.SCREEN_WIDTH - lives_surface.get_width() - 10
        screen.blit(lives_surface, (x_pos, 10))
        for asteroid in asteroids:
            for shot in shots:
                if CircleShape.collides_with(shot, asteroid):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
        for asteroid in asteroids:
            if CircleShape.collides_with(player, asteroid) and constants.LIVES <= 0:
                log_event("player_killed")
                print("Game over!")
                sys.exit()
            elif CircleShape.collides_with(player, asteroid):
                log_event("player_hit")
                constants.LIVES -= 1
                player.kill()
                player = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
