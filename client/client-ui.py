# This is a placeholder module for UI rendering using pygame.
# You can expand these functions to draw the maze, characters, and scores.

import pygame

def init_screen(width=640, height=480):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Multiplayer PacMan")
    return screen

def render_game(screen, state):
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Render PacMan as a yellow circle (using state data)
    pacman_pos = state.get('pacman_position', [0, 0])
    pygame.draw.circle(screen, (255, 255, 0), (pacman_pos[0]*20, pacman_pos[1]*20), 10)
    
    # Render ghosts as red circles
    ghost_positions = state.get('ghost_positions', [])
    for pos in ghost_positions:
        pygame.draw.circle(screen, (255, 0, 0), (pos[0]*20, pos[1]*20), 10)
    
    pygame.display.flip()
