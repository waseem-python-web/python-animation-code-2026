import pygame
import random
import math
import sys

# --- Init ---
pygame.init()
W, H = 400, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Battery Charging")
clock = pygame.time.Clock()

# --- Colors ---
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
DARK    = (15, 15, 25)
RED     = (220, 50, 50)
GREEN   = (50, 220, 80)
YELLOW  = (255, 200, 0)
LGRAY   = (80, 90, 100)
DGRAY   = (30, 35, 45)
CYAN    = (0, 220, 220)

# --- Font ---
try:
    font_big   = pygame.font.SysFont("monospace", 52, bold=True)
    font_small = pygame.font.SysFont("monospace", 22)
    font_tiny  = pygame.font.SysFont("monospace", 16)
except:
    font_big   = pygame.font.Font(None, 52)
    font_small = pygame.font.Font(None, 22)
    font_tiny  = pygame.font.Font(None, 16)

# --- Battery dimensions ---
BAT_X  = 80
BAT_Y  = 120
BAT_W  = 240
BAT_H  = 440
BAT_TIP_W = 60
BAT_TIP_H = 28
BORDER = 8

# Fill area inside battery
FILL_X = BAT_X + BORDER
FILL_Y = BAT_Y + BORDER
FILL_W = BAT_W - BORDER * 2
FILL_H = BAT_H - BORDER * 2

# --- Particles (dots) ---
class Particle:
    def __init__(self, percent):
        self.reset(percent)

    def reset(self, percent):
        self.x = random.uniform(FILL_X + 10, FILL_X + FILL_W - 10)
        self.y = FILL_Y + FILL_H  # start from bottom
        self.size = random.uniform(3, 7)
        self.speed = random.uniform(1.2, 3.0)
        self.alpha = random.randint(160, 255)
        self.color = self._pick_color(percent)
        self.active = True

    def _pick_color(self, percent):
        if percent <= 20:
            return RED
        elif percent <= 60:
            return YELLOW
        else:
            return GREEN

    def update(self, percent):
        self.y -= self.speed
        self.alpha = max(0, self.alpha - 1)
        if self.y < FILL_Y or self.alpha <= 0:
            self.reset(percent)

    def draw(self, surf):
        s = pygame.Surface((int(self.size*2), int(self.size*2)), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, self.alpha),
                           (int(self.size), int(self.size)), int(self.size))
        surf.blit(s, (int(self.x - self.size), int(self.y - self.size)))

# --- Rings / circles inside battery (20 circles = 10 per row × 2 rows) ---
RING_ROWS = 2
RING_COLS = 10
rings = []
for row in range(RING_ROWS):
    for col in range(RING_COLS):
        rx = FILL_X + (FILL_W / RING_COLS) * (col + 0.5)
        ry = FILL_Y + FILL_H - 40 - row * 36
        rings.append({"x": rx, "y": ry, "col": col, "row": row})

# --- State ---
percent    = 0        # 0..100
particles  = [Particle(percent) for _ in range(80)]
frame      = 0
speed_up   = 0.18     # percent increase per frame (~60fps → fills in ~9 sec)

# Lightning bolt symbol
def draw_bolt(surf, cx, cy, size, color):
    pts = [
        (cx + size*0.15, cy - size*0.55),
        (cx - size*0.08, cy + size*0.05),
        (cx + size*0.18, cy + size*0.05),
        (cx - size*0.15, cy + size*0.55),
        (cx + size*0.08, cy - size*0.05),
        (cx - size*0.18, cy - size*0.05),
    ]
    pygame.draw.polygon(surf, color, pts)

def get_fill_color(pct):
    if pct <= 20:
        return RED
    elif pct <= 60:
        r = int(220 - (pct - 20) / 40 * 170)
        g = int(50  + (pct - 20) / 40 * 150)
        return (r, g, 0)
    else:
        r = int(50  - (pct - 60) / 40 * 30)
        g = int(200 + (pct - 60) / 40 * 20)
        return (r, g, 60)

running = True
while running:
    clock.tick(60)
    frame += 1

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    # Increase percent
    if percent < 100:
        percent = min(100, percent + speed_up)

    pct  = int(percent)
    fcol = get_fill_color(pct)

    # --- Draw background ---
    screen.fill(DARK)

    # subtle grid bg
    for gx in range(0, W, 30):
        pygame.draw.line(screen, (25,28,38), (gx,0),(gx,H))
    for gy in range(0, H, 30):
        pygame.draw.line(screen, (25,28,38), (0,gy),(W,gy))

    # --- Battery tip (top nub) ---
    tip_rect = pygame.Rect(BAT_X + (BAT_W - BAT_TIP_W)//2,
                           BAT_Y - BAT_TIP_H, BAT_TIP_W, BAT_TIP_H)
    pygame.draw.rect(screen, LGRAY, tip_rect, border_radius=6)

    # --- Battery body shadow ---
    shadow = pygame.Rect(BAT_X+6, BAT_Y+8, BAT_W, BAT_H)
    pygame.draw.rect(screen, (8,8,15), shadow, border_radius=18)

    # --- Battery body border ---
    bat_rect = pygame.Rect(BAT_X, BAT_Y, BAT_W, BAT_H)
    pygame.draw.rect(screen, LGRAY, bat_rect, border_radius=18)

    # --- Battery fill ---
    fill_height = int(FILL_H * percent / 100)
    if fill_height > 0:
        fill_rect = pygame.Rect(FILL_X,
                                FILL_Y + FILL_H - fill_height,
                                FILL_W, fill_height)
        pygame.draw.rect(screen, fcol, fill_rect, border_radius=10)

        # Glow effect on fill top
        glow_surf = pygame.Surface((FILL_W, 18), pygame.SRCALPHA)
        glow_surf.fill((255,255,255,35))
        screen.blit(glow_surf, (FILL_X, FILL_Y + FILL_H - fill_height))

    # --- Battery body inner (dark overlay above fill) ---
    empty_h = FILL_H - fill_height
    if empty_h > 0:
        pygame.draw.rect(screen, DGRAY,
                         (FILL_X, FILL_Y, FILL_W, empty_h), border_radius=10)

    # --- Draw 20 ring circles at bottom ---
    for rng in rings:
        rx, ry = int(rng["x"]), int(rng["y"])
        idx = rng["row"] * RING_COLS + rng["col"]
        # how many rings should be lit
        lit_count = int(pct / 5)   # each 5% lights one ring (20 rings total)
        lit = (20 - idx) <= lit_count   # fill from bottom up

        if pct <= 20:
            ring_color = RED if lit else (50, 20, 20)
            border_col = RED if lit else LGRAY
        else:
            ring_color = GREEN if lit else (15, 40, 20)
            border_col = GREEN if lit else LGRAY

        pygame.draw.circle(screen, ring_color, (rx, ry), 10)
        pygame.draw.circle(screen, border_col, (rx, ry), 10, 2)

        # Pulse glow for lit rings
        if lit:
            pulse = int(30 + 20 * math.sin(frame * 0.08 + idx))
            gs = pygame.Surface((28,28), pygame.SRCALPHA)
            pygame.draw.circle(gs, (*border_col, pulse), (14,14), 13)
            screen.blit(gs, (rx-14, ry-14))

    # --- Particles ---
    for p in particles:
        p.update(pct)
        # Only show particles in fill area
        if p.y >= FILL_Y + FILL_H - fill_height:
            p.draw(screen)

    # --- Percent counter in center ---
    count_text = font_big.render(f"{pct}%", True, WHITE)
    cx = W // 2 - count_text.get_width() // 2
    cy = BAT_Y + BAT_H // 2 - count_text.get_height() // 2
    # semi-transparent backdrop
    pad = 14
    bdrop = pygame.Surface((count_text.get_width() + pad*2,
                            count_text.get_height() + pad), pygame.SRCALPHA)
    bdrop.fill((0,0,0,120))
    screen.blit(bdrop, (cx - pad, cy - pad//2))
    screen.blit(count_text, (cx, cy))

    # --- Lightning bolt ---
    if pct < 100:
        bolt_pulse = int(200 + 55 * math.sin(frame * 0.15))
        draw_bolt(screen, W//2, BAT_Y + BAT_H//2 + 38, 28,
                  (*YELLOW[:2], 0, bolt_pulse) if False else YELLOW)
    else:
        # Full — show check
        done_t = font_small.render("FULLY CHARGED!", True, GREEN)
        screen.blit(done_t, (W//2 - done_t.get_width()//2,
                             BAT_Y + BAT_H//2 + 32))

    # --- Status label at top ---
    if pct <= 20:
        status = "LOW BATTERY"
        scol   = RED
    elif pct < 100:
        status = "CHARGING..."
        scol   = YELLOW
    else:
        status = "FULL !"
        scol   = GREEN

    st = font_small.render(status, True, scol)
    screen.blit(st, (W//2 - st.get_width()//2, 60))

    # --- Tip glow ---
    tip_glow = pygame.Surface((BAT_TIP_W+20, BAT_TIP_H+10), pygame.SRCALPHA)
    g_alpha = int(60 + 40 * math.sin(frame * 0.1))
    pygame.draw.rect(tip_glow, (*fcol, g_alpha),
                     (0, 0, BAT_TIP_W+20, BAT_TIP_H+10), border_radius=8)
    screen.blit(tip_glow, (BAT_X + (BAT_W - BAT_TIP_W)//2 - 10,
                           BAT_Y - BAT_TIP_H - 5))

    # --- Bottom label ---
    hint = font_tiny.render("ESC to exit", True, LGRAY)
    screen.blit(hint, (W//2 - hint.get_width()//2, H - 30))

    pygame.display.flip()

pygame.quit()
sys.exit()