# Owner: Ellie
# One empty shelf, used by aisle_view. Items get placed on shelves in a later sprint.

import pygame
import config
 
 
class Shelf:
    def __init__(self, x, y, width, slots=5, slot_h=90):
        self.x, self.y = x, y
        self.gap = int(width * 0.03)
        self.slot_w = (width - self.gap * (slots - 1)) // slots
        self.slot_h = slot_h
        self.items = [None] * slots  # None = empty slot; fill with items later
        self.width = width
 
    def slot_rect(self, i):
        return pygame.Rect(self.x + i * (self.slot_w + self.gap), self.y,
                           self.slot_w, self.slot_h)
 
    def draw(self, surface):
        for i, item in enumerate(self.items):
            rect = self.slot_rect(i)
            if item is None:
                pygame.draw.rect(surface, config.CARD, rect, border_radius=6)
                pygame.draw.rect(surface, config.CARD_BORDER, rect, 3, border_radius=6)
            # Add in later sprint: else, draw the item's image at rect
        pygame.draw.rect(surface, config.FLOOR,
                         (self.x - 12, self.y + self.slot_h + 6, self.width + 24, 12),
                         border_radius=4)
 