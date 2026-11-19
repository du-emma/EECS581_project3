# Owner: Ellie, Emma
# One shelf row used by aisle_view. Slots hold DB item dicts (name, price, stock).

import pygame
import config

OUT_OF_STOCK = (200, 40, 40)
HOVER_BORDER = (45, 45, 90)       # darker outline while hovered
CLICK_FILL = (255, 255, 255)      # brief flash fill on click
CLICK_FLASH_SECONDS = 0.18


class Shelf:
    def __init__(self, x, y, width, slots=5, slot_h=90):
        self.x, self.y = x, y
        self.gap = int(width * 0.03)
        self.slot_w = (width - self.gap * (slots - 1)) // slots
        self.slot_h = slot_h
        self.items = [None] * slots  # None = empty; else item dict from the DB
        self.width = width
        self.name_font = pygame.font.SysFont(None, 22)
        self.meta_font = pygame.font.SysFont(None, 18)
        self._flash_remaining = [0.0] * slots

    def slot_rect(self, i):
        return pygame.Rect(
            self.x + i * (self.slot_w + self.gap),
            self.y,
            self.slot_w,
            self.slot_h,
        )

    def place_items(self, items):
        """Fill slots left-to-right; leftover slots stay empty."""
        self.items = [None] * len(self.items)
        self._flash_remaining = [0.0] * len(self.items)
        for i, item in enumerate(items[: len(self.items)]):
            self.items[i] = item

    def item_at_pos(self, pos):
        """Return (item, slot_index) under pos, or (None, None)."""
        for i, item in enumerate(self.items):
            if item is not None and self.slot_rect(i).collidepoint(pos):
                return item, i
        return None, None

    def flash_slot(self, index):
        if 0 <= index < len(self._flash_remaining):
            self._flash_remaining[index] = CLICK_FLASH_SECONDS

    def update(self, dt):
        for i, remaining in enumerate(self._flash_remaining):
            if remaining > 0:
                self._flash_remaining[i] = max(0.0, remaining - dt)

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        for i, item in enumerate(self.items):
            rect = self.slot_rect(i)
            hovering = item is not None and rect.collidepoint(mouse)
            flashing = self._flash_remaining[i] > 0
            out_of_stock = item is not None and item.get("stock_quantity", 0) <= 0

            fill = CLICK_FILL if flashing else config.CARD
            pygame.draw.rect(surface, fill, rect, border_radius=6)

            if out_of_stock:
                border, width = OUT_OF_STOCK, 4
            elif hovering or flashing:
                border, width = HOVER_BORDER, 5
            else:
                border, width = config.CARD_BORDER, 3
            pygame.draw.rect(surface, border, rect, width, border_radius=6)

            if item is not None:
                self._draw_item(surface, rect, item)
        pygame.draw.rect(
            surface,
            config.FLOOR,
            (self.x - 12, self.y + self.slot_h + 6, self.width + 24, 12),
            border_radius=4,
        )

    def _draw_item(self, surface, rect, item):
        name = str(item.get("item_name", "?")).title()
        price = float(item.get("price", 0))
        stock = int(item.get("stock_quantity", 0))
        stock_color = OUT_OF_STOCK if stock <= 0 else config.TEXT_MUTED

        name_img = self.name_font.render(name, True, config.TEXT)
        price_img = self.meta_font.render(f"${price:.2f}", True, config.ACCENT)
        stock_img = self.meta_font.render(f"Stock: {stock}", True, stock_color)

        pad = 8
        y = rect.top + pad
        for img in (name_img, price_img, stock_img):
            clipped = img
            if img.get_width() > rect.width - 2 * pad:
                clipped = img.subsurface((0, 0, rect.width - 2 * pad, img.get_height()))
            surface.blit(clipped, clipped.get_rect(midtop=(rect.centerx, y)))
            y += img.get_height() + 4
