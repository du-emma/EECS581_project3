# Owner: Ellie
# One aisle on the store map, labeled with its name.
# Clicking it calls select_aisle(aisle_id) from game_state to open that aisle.

import pygame
import config
 
 
class Aisle:
    def __init__(self, aisle_id, name, rect, game_state):
        self.aisle_id = aisle_id
        self.name = name
        fx, fy, fw, fh = rect  # fractions of the window (see data/aisles.py)
        self.rect = pygame.Rect(int(fx * config.WIDTH), int(fy * config.HEIGHT),
                                int(fw * config.WIDTH), int(fh * config.HEIGHT))
        self.game_state = game_state
        self.font = pygame.font.SysFont(None, config.BODY_SIZE)
 
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.game_state.select_aisle(self.aisle_id)
                return True
        return False
 
    def draw(self, surface):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            return
        pygame.draw.rect(surface, config.SELECTED, self.rect, 4)
        tag = self.font.render(self.name, True, config.TEXT)
        tag_rect = tag.get_rect(midbottom=(self.rect.centerx, self.rect.top - 6))
        pygame.draw.rect(surface, config.CARD, tag_rect.inflate(16, 10))
        pygame.draw.rect(surface, config.OUTLINE, tag_rect.inflate(16, 10), 2)
        surface.blit(tag, tag_rect)
        