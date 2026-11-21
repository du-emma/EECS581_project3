# Shopping cart icon and panel. Contents live on GameState so they survive
# opening/closing the panel and switching between the store and aisle views.

import pygame

import config
from components.button import Button
from data.items import increment_stock
from screens.base_screen import draw_text


ICON_SIZE = 70
ICON_GAP = 12
PANEL_WIDTH = 360
MAX_VISIBLE_ROWS = 6
ROW_HEIGHT = 46
HEADER_HEIGHT = 52
FOOTER_HEIGHT = 70
PANEL_PAD = 16
REMOVE_SIZE = (110, 36)


class ShoppingCart:
    def __init__(self, state, anchor_rect, on_stock_changed=None):
        self.state = state
        self.on_stock_changed = on_stock_changed
        self.icon_rect = pygame.Rect(0, 0, ICON_SIZE, ICON_SIZE)
        self.icon_rect.midright = (anchor_rect.left - ICON_GAP, anchor_rect.centery)
        self.panel_rect = pygame.Rect(0, 0, PANEL_WIDTH, HEADER_HEIGHT + FOOTER_HEIGHT)
        self.scroll = 0
        self._remove_buttons = []
        self.clear_button = Button(
            "Clear Cart",
            (0, 0),
            self._clear_cart,
            size=(200, 44),
        )
        self._layout_panel()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.state.cart_open:
                self.state.close_cart()
                return True
            return False

        if event.type == pygame.MOUSEWHEEL and self.state.cart_open:
            if self.panel_rect.collidepoint(pygame.mouse.get_pos()):
                self._scroll_by(-event.y)
                return True
            return False

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False

        if self.icon_rect.collidepoint(event.pos):
            self.state.toggle_cart()
            return True

        if not self.state.cart_open:
            return False

        self._layout_panel()
        if self.panel_rect.collidepoint(event.pos):
            if self.state.cart:
                self.clear_button.handle_event(event)
                for button in self._remove_buttons:
                    button.handle_event(event)
            return True

        return False

    def draw(self, surface):
        self._draw_icon(surface)
        if self.state.cart_open:
            self._layout_panel()
            self._draw_panel(surface)

    def _draw_icon(self, surface):
        hovering = self.icon_rect.collidepoint(pygame.mouse.get_pos())
        fill = config.SELECTED if self.state.cart_open else config.CARD
        border = config.OUTLINE if hovering or self.state.cart_open else config.CARD_BORDER
        pygame.draw.rect(surface, fill, self.icon_rect, border_radius=12)
        pygame.draw.rect(surface, border, self.icon_rect, width=2, border_radius=12)
        self._draw_cart_glyph(surface, self.icon_rect)

        count = self.state.cart_count()
        if count:
            badge = pygame.Rect(0, 0, 26, 26)
            badge.topright = (self.icon_rect.right + 4, self.icon_rect.top - 4)
            pygame.draw.circle(surface, config.SELECTED, badge.center, 13)
            pygame.draw.circle(surface, config.OUTLINE, badge.center, 13, 2)
            draw_text(surface, str(count), 20, badge.center, config.TEXT)

    @staticmethod
    def _draw_cart_glyph(surface, rect):
        color = config.TEXT
        basket = pygame.Rect(0, 0, 32, 18)
        basket.center = (rect.centerx, rect.centery + 4)
        pygame.draw.lines(
            surface,
            color,
            False,
            [
                (basket.left - 6, basket.top - 10),
                (basket.left - 2, basket.top - 10),
                (basket.left + 2, basket.top),
            ],
            3,
        )
        pygame.draw.rect(surface, color, basket, width=3, border_radius=3)
        pygame.draw.circle(surface, color, (basket.left + 8, basket.bottom + 7), 4)
        pygame.draw.circle(surface, color, (basket.right - 8, basket.bottom + 7), 4)

    def _draw_panel(self, surface):
        pygame.draw.rect(surface, config.CARD, self.panel_rect, border_radius=16)
        pygame.draw.rect(
            surface, config.CARD_BORDER, self.panel_rect, width=3, border_radius=16
        )
        draw_text(
            surface,
            "Shopping Cart",
            28,
            (self.panel_rect.centerx, self.panel_rect.top + 28),
            config.ACCENT,
        )

        items = self.state.cart_items()
        if not items:
            draw_text(
                surface,
                "Your cart is empty",
                24,
                (self.panel_rect.centerx, self.panel_rect.top + 88),
                config.TEXT_MUTED,
            )
            return

        clip = surface.get_clip()
        surface.set_clip(self._list_rect())
        visible = items[self.scroll : self.scroll + MAX_VISIBLE_ROWS]
        for button, entry, row_rect in zip(
            self._remove_buttons, visible, self._row_rects(len(visible))
        ):
            label = f"{str(entry['item_name']).title()} ({entry['quantity']})"
            font = pygame.font.Font(None, 24)
            image = font.render(label, True, config.TEXT)
            max_width = button.rect.left - row_rect.left - 16
            if image.get_width() > max_width > 0:
                image = image.subsurface((0, 0, max_width, image.get_height()))
            surface.blit(image, image.get_rect(midleft=(row_rect.left + 12, row_rect.centery)))
            button.draw(surface)
        surface.set_clip(clip)
        self.clear_button.draw(surface)

    def _layout_panel(self):
        items = self.state.cart_items()
        rows = min(len(items), MAX_VISIBLE_ROWS) if items else 1
        height = HEADER_HEIGHT + rows * ROW_HEIGHT + (FOOTER_HEIGHT if items else 20)
        if not items:
            height = 140
        self.panel_rect.size = (PANEL_WIDTH, height)
        self.panel_rect.topright = (config.WIDTH - 24, self.icon_rect.bottom + 10)
        max_scroll = max(0, len(items) - MAX_VISIBLE_ROWS)
        self.scroll = min(self.scroll, max_scroll)

        self._remove_buttons = []
        if items:
            visible = items[self.scroll : self.scroll + MAX_VISIBLE_ROWS]
            for entry, row_rect in zip(visible, self._row_rects(len(visible))):
                item_id = entry["item_id"]
                button = Button(
                    "Remove",
                    (row_rect.right - 8 - REMOVE_SIZE[0] // 2, row_rect.centery),
                    lambda item_id=item_id: self._remove_one(item_id),
                    size=REMOVE_SIZE,
                )
                self._remove_buttons.append(button)
            self.clear_button.rect.center = (
                self.panel_rect.centerx,
                self.panel_rect.bottom - 32,
            )

    def _list_rect(self):
        items = self.state.cart_items()
        rows = min(len(items), MAX_VISIBLE_ROWS)
        return pygame.Rect(
            self.panel_rect.left + PANEL_PAD,
            self.panel_rect.top + HEADER_HEIGHT,
            self.panel_rect.width - 2 * PANEL_PAD,
            rows * ROW_HEIGHT,
        )

    def _row_rects(self, count):
        list_rect = self._list_rect()
        return [
            pygame.Rect(
                list_rect.left,
                list_rect.top + i * ROW_HEIGHT,
                list_rect.width,
                ROW_HEIGHT,
            )
            for i in range(count)
        ]

    def _scroll_by(self, delta):
        max_scroll = max(0, len(self.state.cart_items()) - MAX_VISIBLE_ROWS)
        self.scroll = max(0, min(self.scroll + delta, max_scroll))

    def _remove_one(self, item_id):
        removed = self.state.remove_from_cart(item_id)
        if removed is None:
            return
        updated = increment_stock(item_id, 1)
        if updated is not None and self.on_stock_changed:
            self.on_stock_changed(item_id, updated["stock_quantity"])

    def _clear_cart(self):
        for entry in self.state.clear_cart():
            updated = increment_stock(entry["item_id"], entry["quantity"])
            if updated is not None and self.on_stock_changed:
                self.on_stock_changed(entry["item_id"], updated["stock_quantity"])
        self.scroll = 0
