# Owner: Jana
#  Grocery order checklist
# Draws the active order as a checklist: one row per item with a completion
# mark, the item name, and collected/required quantity. Reads everything from
# GameState (order from R9, collected amounts derived from the cart in R11).
#
# HudPlaceholders draws it on top of the clipboard art automatically.
# To use it elsewhere:
#     self.checklist = Checklist()
#     self.checklist.draw(surface, self.state, (20, 20))          # white card
#     self.checklist.draw_in_rect(surface, self.state, some_rect) # fit a rect

import pygame

import config


def checklist_rows(state):
    """Pure data for the checklist (easy to test without a window)."""
    return [
        {
            "item_id": r["item_id"],
            "name": r["item_name"].title(),
            "required": r["required_quantity"],
            "collected": r["collected_quantity"],
            "complete": r["complete"],
            "text": f'{r["item_name"].title()}  {r["collected_quantity"]}/{r["required_quantity"]}',
        }
        for r in state.order_progress()
    ]


def checklist_summary(state):
    rows = state.order_progress()
    done = sum(1 for r in rows if r["complete"])
    return f"{done} of {len(rows)} items complete"


class Checklist:
    # (left, top, right, bottom) margins as fractions of the target rect
    CLIPBOARD_INSET = (0.13, 0.17, 0.13, 0.09)
    CARD_INSET = (0.05, 0.05, 0.05, 0.04)

    def __init__(self, width=300):
        self.width = width
        self._fonts = {}

    def _font(self, size):
        size = max(10, int(size))
        if size not in self._fonts:
            self._fonts[size] = pygame.font.Font(None, size)
        return self._fonts[size]

    def height_for(self, state):
        return 90 + len(state.order_items) * 40 + 36

    def draw(self, surface, state, topleft):
        """Standalone white card."""
        panel = pygame.Rect(topleft, (self.width, self.height_for(state)))
        pygame.draw.rect(surface, config.CARD, panel, border_radius=12)
        pygame.draw.rect(surface, config.CARD_BORDER, panel, 3, border_radius=12)
        self.draw_in_rect(surface, state, panel, self.CARD_INSET)

    def draw_in_rect(self, surface, state, rect, inset=None):
        """Lay the checklist out inside rect (e.g. the clipboard image)."""
        l, t, r, b = inset or self.CLIPBOARD_INSET
        area = pygame.Rect(
            rect.left + int(rect.width * l), rect.top + int(rect.height * t),
            int(rect.width * (1 - l - r)), int(rect.height * (1 - t - b)),
        )
        rows = checklist_rows(state)
        n = len(rows)

        title_h = min(34, area.height * 0.13)
        footer_h = min(26, area.height * 0.09)
        row_h = min(40.0, (area.height - title_h - footer_h) / max(n, 1))

        title = self._fit("Grocery List", area.width, title_h * 0.95)
        surface.blit(title, (area.left, area.top))

        y = area.top + title_h + 4
        for row in rows:
            self._draw_row(surface, row, area.left, y, area.width, row_h)
            y += row_h

        if n:
            summary = self._fit(checklist_summary(state), area.width,
                                footer_h * 0.85, config.TEXT_MUTED)
            surface.blit(summary, (area.left, min(y + 2, area.bottom - summary.get_height())))

    def draw_compact(self, surface, state, rect):
        """Horizontal strip of chips (check + name + collected/required).

        For screens with no room for the clipboard (e.g. the aisle view).
        """
        rows = checklist_rows(state)
        if not rows:
            return
        pygame.draw.rect(surface, config.CARD, rect, border_radius=12)
        pygame.draw.rect(surface, config.CARD_BORDER, rect, 3, border_radius=12)
        label = self._fit("Order", 70, rect.height * 0.34, config.ACCENT)
        pad = 14
        surface.blit(label, (rect.left + pad, rect.centery - label.get_height() // 2))
        left = rect.left + pad * 2 + label.get_width()
        chip_w = (rect.right - pad - left) / len(rows)
        for i, row in enumerate(rows):
            self._draw_row(surface, row, int(left + i * chip_w), rect.top,
                           int(chip_w) - 14, rect.height, font_size=28, radius=12, inline_qty=True)

    def _fit(self, text, max_width, size, color=None):
        """Render text, shrinking the font until it fits max_width."""
        color = color or config.TEXT
        size = int(size)
        while True:
            img = self._font(size).render(text, True, color)
            if img.get_width() <= max_width or size <= 12:
                return img
            size -= 2

    def _draw_row(self, surface, row, x, y, width, row_h, font_size=None, radius=None, inline_qty=False):
        cy = int(y + row_h / 2)
        radius = radius or max(6, int(row_h * 0.3))
        center = (x + radius, cy)
        if row["complete"]:
            pygame.draw.circle(surface, config.ACCENT, center, radius)
            k = radius / 12
            pygame.draw.lines(surface, config.BUTTON_TEXT, False, [
                (center[0] - 6 * k, center[1]),
                (center[0] - 2 * k, center[1] + 5 * k),
                (center[0] + 6 * k, center[1] - 5 * k),
            ], max(2, int(3 * k)))
            color = config.TEXT_MUTED
        else:
            pygame.draw.circle(surface, config.ACCENT, center, radius, 2)
            color = config.TEXT

        font_size = font_size or row_h * 0.7
        qty = self._font(font_size).render(f'{row["collected"]}/{row["required"]}', True, color)
        name_x = x + radius * 2 + 8
        name = self._fit(row["name"], width - (name_x - x) - qty.get_width() - 8,
                         font_size, color)
        surface.blit(name, (name_x, cy - name.get_height() // 2))
        if row["complete"]:
            pygame.draw.line(surface, color, (name_x, cy),
                             (name_x + name.get_width(), cy), 2)
        qty_x = (name_x + name.get_width() + 8) if inline_qty else (x + width - qty.get_width())
        surface.blit(qty, (qty_x, cy - qty.get_height() // 2))