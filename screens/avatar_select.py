# Owner: Arpa
# Shown after pressing Start. The player picks an avatar from data/avatars.py,
# then continues to the store page.

import pygame

import config
import game_state
from components.avatar import draw_avatar
from data.avatars import AVATARS
from screens.base_screen import BaseScreen, MenuButton, draw_text

CARD_W = 170
CARD_H = 190
CARD_GAP = 22
PER_ROW = 4
GRID_TOP = 125


class AvatarSelect(BaseScreen):
    def __init__(self, state):
        super().__init__(state)
        cx = config.WIDTH // 2

        # One card per avatar, in centered rows of PER_ROW
        row_w = PER_ROW * CARD_W + (PER_ROW - 1) * CARD_GAP
        left = cx - row_w // 2
        self.cards = []
        for i, avatar in enumerate(AVATARS):
            col, row = i % PER_ROW, i // PER_ROW
            rect = pygame.Rect(left + col * (CARD_W + CARD_GAP),
                               GRID_TOP + row * (CARD_H + CARD_GAP), CARD_W, CARD_H)
            self.cards.append((rect, avatar))

        self.back = MenuButton("Back", (cx - 150, config.HEIGHT - 50),
                               lambda: state.change_screen(game_state.MENU), size=(220, 60))
        self.go = MenuButton("Let's Shop!", (cx + 150, config.HEIGHT - 50),
                             lambda: state.change_screen(game_state.STORE), size=(220, 60))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, avatar in self.cards:
                if rect.collidepoint(event.pos):
                    self.state.choose_avatar(avatar["id"])
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state.change_screen(game_state.MENU)
        self.back.handle_event(event)
        self.go.handle_event(event)

    def update(self, dt):
        # Can't continue until an avatar is picked
        self.go.enabled = self.state.avatar_id is not None

    def draw(self, surface):
        surface.fill(config.BACKGROUND)
        draw_text(surface, "Choose Your Shopper", config.HEADING_SIZE, (config.WIDTH // 2, 70), config.ACCENT)

        mouse = pygame.mouse.get_pos()
        for rect, avatar in self.cards:
            selected = avatar["id"] == self.state.avatar_id
            pygame.draw.rect(surface, config.CARD, rect, border_radius=14)
            if selected:
                border, width = config.SELECTED, 5
            elif rect.collidepoint(mouse):
                border, width = config.ACCENT, 3
            else:
                border, width = config.CARD_BORDER, 2
            pygame.draw.rect(surface, border, rect, width=width, border_radius=14)
            draw_avatar(surface, avatar, (rect.centerx, rect.centery - 18), size=115)
            draw_text(surface, avatar["name"], config.BODY_SIZE, (rect.centerx, rect.bottom - 22))

        if self.state.avatar_id is None:
            draw_text(surface, "Click a shopper to pick them", config.BODY_SIZE,
                      (config.WIDTH // 2, 548), config.TEXT_MUTED)

        self.back.draw(surface)
        self.go.draw(surface)
