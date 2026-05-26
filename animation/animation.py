
import math
import random


from kivy.config import Config

# मोबाइल साइज़ (TikTok जैसा पोर्ट्रेट मोड)
Config.set('graphics', 'width', '360')   # या '480'
Config.set('graphics', 'height', '640')  # या '800'
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'window_state', 'visible')



import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import (
    Color, Ellipse, Line, Rectangle,
    Bezier, Triangle, Mesh, RoundedRectangle
)
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.widget import Widget

kivy.require('2.0.0')

# ═══════════════════════════════════════════
#  SHARED UTILITIES
# ═══════════════════════════════════════════

def lerp(a, b, t):
    return a + (b - a) * t

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def draw_bg(canvas, widget, r, g, b):
    with canvas:
        Color(r, g, b, 1)
        Rectangle(pos=widget.pos, size=widget.size)

class BackButton(Button):
    def __init__(self, manager, **kw):
        super().__init__(
            text='← Menu',
            font_size='13sp',
            background_color=(0.15, 0.15, 0.25, 0.92),
            background_normal='',
            size_hint=(0.26, 0.065),
            pos_hint={'x': 0.02, 'top': 0.985},
            color=(0.9, 0.9, 1, 1),
            **kw
        )
        self._manager = manager
        self.bind(on_press=self._go)

    def _go(self, *a):
        self._manager.current = 'menu'


# ═══════════════════════════════════════════
#  MENU SCREEN
# ═══════════════════════════════════════════

ANIMALS = [
    ('🦋', 'تتلی اڑنا',       'Butterfly Flutter', 'butterfly'),
    ('🐠', 'مچھلی کا تالاب',  'Fish Aquarium',     'fish'),
    ('🐦', 'پرندوں کا جھنڈ', 'Bird Flock',         'birds'),
    ('🦁', 'شیر کی دہاڑ',    'Lion Roar',          'lion'),
    ('🐍', 'سانپ کا رینگنا', 'Snake Crawl',         'snake'),
    ('🦈', 'شارک کا شکار',   'Shark Hunt',          'shark'),
    ('🐝', 'مکھیوں کا جھنڈ', 'Bee Swarm',          'bees'),
    ('🦊', 'لومڑی کا چلنا',  'Fox Walk',            'fox'),
    ('🌊', 'ڈولفن کی چھلانگ','Dolphin Jump',        'dolphin'),
]

BTN_COLORS = [
    (0.72, 0.25, 0.62),
    (0.15, 0.52, 0.72),
    (0.18, 0.62, 0.42),
    (0.78, 0.42, 0.12),
    (0.28, 0.55, 0.22),
    (0.62, 0.18, 0.28),
    (0.72, 0.62, 0.08),
    (0.42, 0.22, 0.72),
    (0.12, 0.52, 0.62),
]

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        root = FloatLayout()

        with root.canvas.before:
            Color(0.06, 0.06, 0.14, 1)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(size=self._upd, pos=self._upd)

        title = Label(
            text='🐾 جانوروں کی اینیمیشن 🐾',
            font_size='22sp', bold=True,
            color=(1, 0.92, 0.35, 1),
            size_hint=(1, None), height=50,
            pos_hint={'x': 0, 'top': 0.985},
            halign='center'
        )
        root.add_widget(title)

        sub = Label(
            text='Animal Animations — Select One',
            font_size='14sp',
            color=(0.65, 0.75, 1, 1),
            size_hint=(1, None), height=30,
            pos_hint={'x': 0, 'top': 0.925},
            halign='center'
        )
        root.add_widget(sub)

        scroll = ScrollView(
            size_hint=(1, 0.84),
            pos_hint={'x': 0, 'y': 0.02}
        )
        grid = GridLayout(
            cols=1,
            spacing=10,
            padding=[18, 10],
            size_hint_y=None
        )
        grid.bind(minimum_height=grid.setter('height'))

        for i, (emoji, urdu, eng, screen) in enumerate(ANIMALS):
            c = BTN_COLORS[i]
            btn = Button(
                text=f'{emoji}  {urdu}\n     {eng}',
                font_size='17sp',
                bold=True,
                background_color=(c[0], c[1], c[2], 1),
                background_normal='',
                size_hint_y=None,
                height=72,
                halign='left',
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=self._make_cb(screen))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        root.add_widget(scroll)
        self.add_widget(root)

    def _make_cb(self, s):
        def cb(inst):
            self.manager.current = s
        return cb

    def _upd(self, inst, val):
        self._bg.pos = inst.pos
        self._bg.size = inst.size


# ═══════════════════════════════════════════
#  1. BUTTERFLY FLUTTER  🦋
# ═══════════════════════════════════════════

class ButterflyWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.butterflies = []
        self.flowers = []
        Clock.schedule_once(self._init, 0.1)
        Clock.schedule_interval(self.update, 1/60)

    def _init(self, dt):
        W, H = Window.width, Window.height
        for _ in range(6):
            self.butterflies.append(self._new_butterfly())
        for _ in range(8):
            self.flowers.append({
                'x': random.uniform(30, W-30),
                'y': random.uniform(20, H*0.35),
                'r': random.uniform(12, 22),
                'color': random.choice([
                    [1,.3,.5],[1,.8,.2],[.5,1,.3],[.3,.6,1],[.9,.4,1]
                ])
            })

    def _new_butterfly(self):
        W, H = Window.width, Window.height
        angle = random.uniform(0, 2*math.pi)
        return {
            'x': random.uniform(60, W-60),
            'y': random.uniform(H*0.3, H*0.95),
            'vx': math.cos(angle)*1.2,
            'vy': math.sin(angle)*0.8,
            'wing_t': random.uniform(0, math.pi*2),
            'wing_speed': random.uniform(3.5, 6.0),
            'size': random.uniform(18, 32),
            'color': random.choice([
                [0.9,0.3,0.8],[0.2,0.7,1.0],[1.0,0.6,0.1],
                [0.3,0.9,0.5],[0.9,0.9,0.2],[0.6,0.3,1.0]
            ]),
            'target_x': random.uniform(60, W-60),
            'target_y': random.uniform(H*0.3, H*0.95),
            'target_timer': random.uniform(60, 150),
        }

    def update(self, dt):
        W, H = Window.width, Window.height
        for b in self.butterflies:
            b['wing_t'] += dt * b['wing_speed']
            b['target_timer'] -= 1
            if b['target_timer'] <= 0:
                b['target_x'] = random.uniform(60, W-60)
                b['target_y'] = random.uniform(H*0.3, H*0.95)
                b['target_timer'] = random.uniform(80, 180)

            dx = b['target_x'] - b['x']
            dy = b['target_y'] - b['y']
            dist = math.sqrt(dx*dx + dy*dy) + 0.001
            b['vx'] = lerp(b['vx'], dx/dist * 2.0, 0.03)
            b['vy'] = lerp(b['vy'], dy/dist * 1.5, 0.03)
            b['x'] += b['vx']
            b['y'] += b['vy']
            b['x'] = clamp(b['x'], 40, W-40)
            b['y'] = clamp(b['y'], 60, H-60)

        self.canvas.clear()
        with self.canvas:
            # Sky gradient (simulate)
            Color(0.45, 0.72, 0.98, 1)
            Rectangle(pos=(0, H*0.5), size=(W, H*0.5))
            Color(0.55, 0.82, 0.55, 1)
            Rectangle(pos=(0, 0), size=(W, H*0.5))

            # Ground
            Color(0.35, 0.62, 0.28, 1)
            Rectangle(pos=(0, 0), size=(W, H*0.28))

            # Flowers
            for fl in self.flowers:
                # stem
                Color(0.2, 0.55, 0.2, 1)
                Line(points=[fl['x'], 0, fl['x'], fl['y']], width=2)
                # petals
                for ang in range(0, 360, 45):
                    rad = math.radians(ang)
                    px = fl['x'] + math.cos(rad)*fl['r']
                    py = fl['y'] + math.sin(rad)*fl['r']
                    Color(fl['color'][0], fl['color'][1], fl['color'][2], 0.9)
                    Ellipse(pos=(px-fl['r']*0.55, py-fl['r']*0.55),
                            size=(fl['r']*1.1, fl['r']*1.1))
                # center
                Color(1, 0.92, 0.1, 1)
                cr = fl['r']*0.55
                Ellipse(pos=(fl['x']-cr, fl['y']-cr), size=(cr*2, cr*2))

            # Butterflies
            for b in self.butterflies:
                wing_open = abs(math.sin(b['wing_t']))
                s = b['size']
                c = b['color']
                cx, cy = b['x'], b['y']

                # Upper wings
                Color(c[0], c[1], c[2], 0.88)
                # left upper wing
                lw = s * wing_open * 1.3
                Ellipse(pos=(cx - lw - s*0.1, cy), size=(lw, s*0.95))
                # right upper wing
                Ellipse(pos=(cx + s*0.1, cy), size=(lw, s*0.95))

                # Lower wings (smaller)
                Color(c[0]*0.8, c[1]*0.8, c[2]*0.5, 0.82)
                llw = s * wing_open * 0.85
                Ellipse(pos=(cx - llw - s*0.1, cy - s*0.75), size=(llw, s*0.72))
                Ellipse(pos=(cx + s*0.1, cy - s*0.75), size=(llw, s*0.72))

                # Wing pattern dots
                Color(1, 1, 1, 0.55)
                for sign in [-1, 1]:
                    dot_x = cx + sign*(s*0.3 + lw*0.4)
                    dot_y = cy + s*0.4
                    Ellipse(pos=(dot_x-3, dot_y-3), size=(6, 6))

                # Body
                Color(0.15, 0.08, 0.02, 1)
                Line(points=[cx, cy-s, cx, cy+s*0.5], width=2.5)

                # Antennae
                Color(0.1, 0.1, 0.1, 0.9)
                Line(points=[cx, cy+s*0.5,
                              cx - s*0.4, cy + s*1.0], width=1.2)
                Line(points=[cx, cy+s*0.5,
                              cx + s*0.4, cy + s*1.0], width=1.2)
                # Antenna tips
                Color(c[0], c[1], c[2], 1)
                Ellipse(pos=(cx - s*0.4 - 3, cy + s*1.0 - 3), size=(6,6))
                Ellipse(pos=(cx + s*0.4 - 3, cy + s*1.0 - 3), size=(6,6))

    def on_touch_down(self, touch):
        for b in self.butterflies:
            b['target_x'] = touch.x + random.uniform(-40, 40)
            b['target_y'] = touch.y + random.uniform(-40, 40)
        return True


class ButterflyScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        layout.add_widget(ButterflyWidget())
        layout.add_widget(Label(
            text='🦋 اسکرین چھوئیں تتلیاں آئیں!',
            font_size='13sp', color=(0.1,0.1,0.1,0.85),
            size_hint=(0.6, 0.06),
            pos_hint={'right':0.99,'top':0.985}, halign='right'))
        layout.add_widget(BackButton(self.manager if hasattr(self,'manager') else None))
        self.layout = layout
        self.add_widget(layout)

    def on_enter(self):
        for w in self.layout.children:
            if isinstance(w, BackButton):
                w._manager = self.manager


# ═══════════════════════════════════════════
#  2. FISH AQUARIUM  🐠
# ═══════════════════════════════════════════

class FishWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.fish = []
        self.bubbles = []
        self.plants = []
        self.bubble_timer = 0
        Clock.schedule_once(self._init, 0.1)
        Clock.schedule_interval(self.update, 1/60)

    def _init(self, dt):
        W, H = Window.width, Window.height
        fish_colors = [
            [1.0, 0.45, 0.1],  # orange
            [0.2, 0.7, 1.0],   # blue
            [0.9, 0.15, 0.3],  # red
            [0.3, 0.9, 0.5],   # green
            [0.9, 0.8, 0.1],   # yellow
            [0.8, 0.3, 0.9],   # purple
            [0.1, 0.8, 0.8],   # cyan
        ]
        for i in range(9):
            c = fish_colors[i % len(fish_colors)]
            self.fish.append({
                'x': random.uniform(60, W-60),
                'y': random.uniform(H*0.15, H*0.80),
                'vx': random.choice([-1,1]) * random.uniform(1.2, 2.5),
                'vy': random.uniform(-0.3, 0.3),
                'size': random.uniform(18, 35),
                'color': c,
                'tail_t': random.uniform(0, math.pi*2),
                'wobble': random.uniform(2,4),
            })
        for _ in range(6):
            self.plants.append({
                'x': random.uniform(20, W-20),
                'h': random.uniform(H*0.12, H*0.28),
                'sway': random.uniform(0, math.pi*2),
                'color': random.choice([
                    [0.1,0.6,0.2],[0.2,0.72,0.35],[0.05,0.5,0.45]
                ])
            })

    def update(self, dt):
        W, H = Window.width, Window.height
        self.bubble_timer += dt
        if self.bubble_timer > 0.35:
            self.bubble_timer = 0
            self.bubbles.append({
                'x': random.uniform(20, W-20),
                'y': random.uniform(20, H*0.12),
                'vy': random.uniform(0.8, 2.0),
                'r': random.uniform(4, 10),
                'alpha': 0.7
            })

        new_b = []
        for b in self.bubbles:
            b['y'] += b['vy']
            b['alpha'] -= 0.006
            if b['y'] < H*0.92 and b['alpha'] > 0:
                new_b.append(b)
        self.bubbles = new_b

        for f in self.fish:
            f['tail_t'] += dt * f['wobble']
            f['x'] += f['vx']
            f['y'] += math.sin(f['tail_t']*0.4) * 0.5

            if f['x'] < 40:
                f['vx'] = abs(f['vx'])
            if f['x'] > W - 40:
                f['vx'] = -abs(f['vx'])
            f['y'] = clamp(f['y'], H*0.12, H*0.88)

        for p in self.plants:
            p['sway'] += dt * 0.8

        self.canvas.clear()
        with self.canvas:
            # Water background layers
            Color(0.04, 0.18, 0.42, 1)
            Rectangle(pos=(0,0), size=(W, H))
            Color(0.06, 0.25, 0.55, 0.6)
            Rectangle(pos=(0, H*0.4), size=(W, H*0.6))
            Color(0.08, 0.32, 0.68, 0.3)
            Rectangle(pos=(0, H*0.65), size=(W, H*0.35))

            # Sand bottom
            Color(0.72, 0.62, 0.38, 1)
            Rectangle(pos=(0, 0), size=(W, H*0.1))
            Color(0.65, 0.55, 0.30, 1)
            Rectangle(pos=(0, 0), size=(W, H*0.07))

            # Plants
            for p in self.plants:
                sway = math.sin(p['sway']) * 8
                Color(p['color'][0], p['color'][1], p['color'][2], 0.9)
                segs = 5
                for seg in range(segs):
                    t = seg / segs
                    t2 = (seg+1) / segs
                    x1 = p['x'] + sway * t * t
                    y1 = H*0.07 + p['h'] * t
                    x2 = p['x'] + sway * t2 * t2
                    y2 = H*0.07 + p['h'] * t2
                    Line(points=[x1, y1, x2, y2], width=3.5 - seg*0.4)
                # leaf tips
                tip_x = p['x'] + sway
                tip_y = H*0.07 + p['h']
                Color(p['color'][0]*1.2, p['color'][1]*1.1, p['color'][2], 0.9)
                Ellipse(pos=(tip_x-8, tip_y-5), size=(16, 10))

            # Bubbles
            for b in self.bubbles:
                Color(0.8, 0.92, 1.0, b['alpha'] * 0.5)
                Ellipse(pos=(b['x']-b['r'], b['y']-b['r']),
                        size=(b['r']*2, b['y']*2 if False else b['r']*2))
                Color(1, 1, 1, b['alpha'] * 0.7)
                Line(circle=(b['x'], b['y'], b['r']), width=1.2)
                # highlight
                Color(1,1,1, b['alpha']*0.5)
                sr = b['r']*0.3
                Ellipse(pos=(b['x']-b['r']*0.5-sr, b['y']+b['r']*0.25-sr),
                        size=(sr*2, sr*2))

            # Fish
            for f in self.fish:
                tail_wave = math.sin(f['tail_t']) * 8
                s = f['size']
                cx, cy = f['x'], f['y']
                c = f['color']
                facing = 1 if f['vx'] > 0 else -1

                # Shadow
                Color(0,0,0,0.18)
                Ellipse(pos=(cx - s*1.1, cy - s*0.35), size=(s*2.2, s*0.6))

                # Tail fin
                Color(c[0]*0.75, c[1]*0.75, c[2]*0.75, 0.9)
                tx = cx - facing * s * 0.9
                Line(points=[
                    tx, cy,
                    tx - facing*s*0.7, cy + s*0.55 + tail_wave*0.5,
                    tx - facing*s*0.7, cy - s*0.55 - tail_wave*0.5,
                    tx, cy
                ], width=1.2)

                # Body
                Color(c[0], c[1], c[2], 1)
                Ellipse(pos=(cx - s, cy - s*0.45), size=(s*2, s*0.9))

                # Belly (lighter)
                Color(min(1,c[0]+0.3), min(1,c[1]+0.3), min(1,c[2]+0.3), 0.5)
                Ellipse(pos=(cx - s*0.7, cy - s*0.3), size=(s*1.3, s*0.5))

                # Dorsal fin
                Color(c[0]*0.8, c[1]*0.8, c[2]*0.6, 0.85)
                Line(points=[
                    cx - s*0.2, cy + s*0.45,
                    cx + facing*s*0.2, cy + s*0.9,
                    cx + facing*s*0.55, cy + s*0.45,
                ], width=1.5)

                # Eye
                Color(0.95, 0.95, 0.95, 1)
                ex = cx + facing * s * 0.55
                Ellipse(pos=(ex - s*0.18, cy - s*0.15), size=(s*0.36, s*0.36))
                Color(0.05, 0.05, 0.05, 1)
                Ellipse(pos=(ex - s*0.1 + facing*s*0.05, cy - s*0.1),
                        size=(s*0.2, s*0.2))
                Color(1,1,1,0.9)
                Ellipse(pos=(ex + facing*s*0.06, cy + s*0.03), size=(s*0.08,s*0.08))

                # Stripe pattern
                Color(c[0]*0.65, c[1]*0.65, c[2]*0.65, 0.5)
                for stripe in range(2):
                    sx = cx + facing * (s * 0.1 - stripe * s * 0.45)
                    Line(points=[sx, cy + s*0.42, sx, cy - s*0.42], width=1.8)

            # Water surface shimmer
            Color(0.6, 0.85, 1.0, 0.18)
            Rectangle(pos=(0, H*0.88), size=(W, H*0.12))
            Color(1, 1, 1, 0.08)
            for i in range(0, int(W), 35):
                Line(points=[i, H*0.92, i+20, H*0.94, i+35, H*0.92], width=1.5)

    def on_touch_down(self, touch):
        for f in self.fish:
            f['vx'] = lerp(f['vx'], (touch.x - f['x']) * 0.04, 0.4)
            f['vy'] = lerp(f['vy'], (touch.y - f['y']) * 0.02, 0.3)
        return True


class FishScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        layout.add_widget(FishWidget())
        layout.add_widget(Label(
            text='🐠 چھوئیں مچھلیاں آئیں!',
            font_size='13sp', color=(0.8,0.95,1,0.9),
            size_hint=(0.55,0.06),
            pos_hint={'right':0.99,'top':0.985}, halign='right'))
        layout.add_widget(BackButton(None))
        self.layout = layout
        self.add_widget(layout)

    def on_enter(self):
        for w in self.layout.children:
            if isinstance(w, BackButton):
                w._manager = self.manager


# ═══════════════════════════════════════════
#  3. BIRD FLOCK  🐦
# ═══════════════════════════════════════════

class BirdFlockWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.birds = []
        self.clouds = []
        self.t = 0
        Clock.schedule_once(self._init, 0.1)
        Clock.schedule_interval(self.update, 1/60)

    def _init(self, dt):
        W, H = Window.width, Window.height
        cx, cy = W/2, H*0.65
        for i in range(22):
            angle = random.uniform(0, 2*math.pi)
            dist = random.uniform(10, 80)
            self.birds.append({
                'x': cx + math.cos(angle)*dist,
                'y': cy + math.sin(angle)*dist*0.5,
                'vx': random.uniform(-1.5, 1.5),
                'vy': random.uniform(-0.5, 0.5),
                'wing_t': random.uniform(0, math.pi*2),
                'size': random.uniform(6, 12),
            })
        for _ in range(5):
            self.clouds.append({
                'x': random.uniform(0, W),
                'y': random.uniform(H*0.6, H*0.9),
                'w': random.uniform(60, 130),
                'speed': random.uniform(0.2, 0.5),
            })

    def _separation(self, i):
        b = self.birds[i]
        sx, sy = 0, 0
        for j, other in enumerate(self.birds):
            if i == j: continue
            dx = b['x'] - other['x']
            dy = b['y'] - other['y']
            d = math.sqrt(dx*dx + dy*dy) + 0.001
            if d < 28:
                sx += dx / d
                sy += dy / d
        return sx, sy

    def _alignment(self, i):
        ax, ay, count = 0, 0, 0
        b = self.birds[i]
        for j, other in enumerate(self.birds):
            if i == j: continue
            dx = b['x'] - other['x']
            dy = b['y'] - other['y']
            if math.sqrt(dx*dx+dy*dy) < 70:
                ax += other['vx']
                ay += other['vy']
                count += 1
        if count:
            ax /= count; ay /= count
        return ax, ay

    def _cohesion(self, i):
        cx, cy, count = 0, 0, 0
        b = self.birds[i]
        for j, other in enumerate(self.birds):
            if i == j: continue
            dx = b['x'] - other['x']
            dy = b['y'] - other['y']
            if math.sqrt(dx*dx+dy*dy) < 100:
                cx += other['x']
                cy += other['y']
                count += 1
        if count:
            cx /= count; cy /= count
            return (cx - b['x'])*0.005, (cy - b['y'])*0.005
        return 0, 0

    def update(self, dt):
        W, H = Window.width, Window.height
        self.t += dt

        for cloud in self.clouds:
            cloud['x'] -= cloud['speed']
            if cloud['x'] < -cloud['w']:
                cloud['x'] = W + cloud['w']

        for i, b in enumerate(self.birds):
            b['wing_t'] += dt * 4.5

            sx, sy = self._separation(i)
            ax, ay = self._alignment(i)
            cx2, cy2 = self._cohesion(i)

            b['vx'] += sx*0.12 + ax*0.05 + cx2
            b['vy'] += sy*0.12 + ay*0.05 + cy2

            speed = math.sqrt(b['vx']**2 + b['vy']**2) + 0.001
            max_spd = 2.8
            if speed > max_spd:
                b['vx'] = b['vx']/speed * max_spd
                b['vy'] = b['vy']/speed * max_spd

            b['x'] += b['vx']
            b['y'] += b['vy']

            if b['x'] < 0: b['x'] = W
            if b['x'] > W: b['x'] = 0
            if b['y'] < H*0.3: b['y'] = H*0.3; b['vy'] = abs(b['vy'])
            if b['y'] > H-20: b['y'] = H-20; b['vy'] = -abs(b['vy'])

        self.canvas.clear()
        with self.canvas:
            # Sky
            Color(0.53, 0.78, 0.98, 1)
            Rectangle(pos=(0, H*0.25), size=(W, H*0.75))
            # Horizon glow
            Color(1.0, 0.88, 0.55, 0.45)
            Rectangle(pos=(0, H*0.25), size=(W, H*0.2))
            # Ground
            Color(0.38, 0.62, 0.25, 1)
            Rectangle(pos=(0,0), size=(W, H*0.3))
            # Hills
            Color(0.30, 0.55, 0.20, 1)
            for hx in [0, W*0.35, W*0.7]:
                Line(circle=(hx, H*0.26, H*0.14), width=H*0.14)

            # Clouds
            for cl in self.clouds:
                Color(1, 1, 1, 0.88)
                for off in [(-cl['w']*0.3, cl['w']*0.18),
                             (0, cl['w']*0.25),
                             (cl['w']*0.3, cl['w']*0.2),
                             (cl['w']*0.55, cl['w']*0.15)]:
                    Ellipse(pos=(cl['x']+off[0]-off[1],
                                 cl['y']-off[1]),
                            size=(off[1]*2, off[1]*2))

            # Birds (boid flocking)
            for b in self.birds:
                s = b['size']
                wing = math.sin(b['wing_t']) * s * 0.9
                cx3, cy3 = b['x'], b['y']
                angle = math.atan2(b['vy'], b['vx'])

                Color(0.12, 0.08, 0.05, 0.9)
                # Left wing
                lx = cx3 - math.cos(angle+math.pi/2)*s*0.5
                ly = cy3 - math.sin(angle+math.pi/2)*s*0.5
                Line(points=[lx, ly,
                              lx - math.cos(angle+math.pi/2)*s*1.5,
                              ly - math.sin(angle+math.pi/2)*s*1.5 + wing],
                     width=1.8)
                # Right wing
                rx = cx3 + math.cos(angle+math.pi/2)*s*0.5
                ry = cy3 + math.sin(angle+math.pi/2)*s*0.5
                Line(points=[rx, ry,
                              rx + math.cos(angle+math.pi/2)*s*1.5,
                              ry + math.sin(angle+math.pi/2)*s*1.5 + wing],
                     width=1.8)
                # Body
                Line(points=[cx3 - math.cos(angle)*s,
                              cy3 - math.sin(angle)*s,
                              cx3 + math.cos(angle)*s,
                              cy3 + math.sin(angle)*s],
                     width=2.2)

    def on_touch_down(self, touch):
        W, H = Window.width, Window.height
        for b in self.birds:
            dx = touch.x - b['x']
            dy = touch.y - b['y']
            dist = math.sqrt(dx*dx+dy*dy)+0.001
            b['vx'] += dx/dist * 2
            b['vy'] += dy/dist * 1.5
        return True


class BirdScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        layout.add_widget(BirdFlockWidget())
        layout.add_widget(Label(
            text='🐦 چھوئیں پرندے آئیں!',
            font_size='13sp', color=(0.1,0.1,0.4,0.85),
            size_hint=(0.55,0.06),
            pos_hint={'right':0.99,'top':0.985}, halign='right'))
        layout.add_widget(BackButton(None))
        self.layout = layout
        self.add_widget(layout)

    def on_enter(self):
        for w in self.layout.children:
            if isinstance(w, BackButton):
                w._manager = self.manager


# ═══════════════════════════════════════════
#  4. LION ROAR  🦁
# ═══════════════════════════════════════════

class LionWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.roar_rings = []
        self.particles = []
        self.roar_t = 0
        self.is_roaring = False
        self.idle_t = 0
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self._auto_roar, 3.5)

    def _auto_roar(self, dt):
        self.start_roar()

    def start_roar(self):
        if self.is_roaring: return
        self.is_roaring = True
        self.roar_t = 0
        W, H = Window.width, Window.height
        for _ in range(60):
            angle = random.uniform(-math.pi*0.6, -math.pi*0.2) + math.pi
            speed = random.uniform(2, 7)
            self.particles.append({
                'x': W/2, 'y': H*0.52,
                'vx': math.cos(angle)*speed,
                'vy': math.sin(angle)*speed + random.uniform(1,3),
                'life': random.uniform(0.5, 1.0),
                'size': random.uniform(3,8),
                'color': random.choice([
                    [1,.85,.1],[1,.6,.1],[0.9,.9,.9],[1,1,1]
                ])
            })

    def update(self, dt):
        W, H = Window.width, Window.height
        self.idle_t += dt

        if self.is_roaring:
            self.roar_t += dt
            if self.roar_t % 0.12 < dt:
                self.roar_rings.append({
                    'r': 5, 'max_r': W*0.7,
                    'alpha': 0.7,
                    'cx': W/2, 'cy': H*0.52
                })
            if self.roar_t > 1.8:
                self.is_roaring = False

        new_rings = []
        for ring in self.roar_rings:
            ring['r'] += 5
            ring['alpha'] -= 0.018
            if ring['alpha'] > 0 and ring['r'] < ring['max_r']:
                new_rings.append(ring)
        self.roar_rings = new_rings

        alive = []
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] -= 0.15
            p['life'] -= 0.022
            if p['life'] > 0: alive.append(p)
        self.particles = alive

        self.canvas.clear()
        with self.canvas:
            # Savanna background
            Color(0.85, 0.62, 0.25, 1)
            Rectangle(pos=(0,0), size=(W,H))
            # Sky
            Color(0.92, 0.72, 0.38, 1)
            Rectangle(pos=(0, H*0.5), size=(W, H*0.5))
            # Sun
            Color(1.0, 0.88, 0.2, 0.9)
            Ellipse(pos=(W*0.78-30, H*0.82-30), size=(60,60))
            # Ground
            Color(0.72, 0.48, 0.15, 1)
            Rectangle(pos=(0,0), size=(W, H*0.22))
            # Grass patches
            Color(0.55, 0.72, 0.18, 0.6)
            for gx in range(0, int(W), 22):
                gh = random.uniform(8, 20)
                Line(points=[gx, H*0.22, gx+3, H*0.22+gh], width=1.5)

            # Roar rings
            for ring in self.roar_rings:
                Color(1.0, 0.75, 0.1, ring['alpha'])
                Line(circle=(ring['cx'], ring['cy'], ring['r']), width=2.2)
                Color(1.0, 0.95, 0.5, ring['alpha']*0.3)
                Line(circle=(ring['cx'], ring['cy'], ring['r']*0.8), width=1.2)

            # Particles (breath/roar effect)
            for p in self.particles:
                Color(p['color'][0], p['color'][1], p['color'][2], p['life'])
                s = p['size'] * p['life']
                Ellipse(pos=(p['x']-s/2, p['y']-s/2), size=(s,s))

            # ── LION BODY ──
            lx, ly = W/2, H*0.35
            mane_r = H*0.16

            # Mane (outer)
            Color(0.52, 0.28, 0.05, 1)
            Ellipse(pos=(lx - mane_r, ly - mane_r*0.85), size=(mane_r*2, mane_r*1.85))
            # Mane inner
            Color(0.72, 0.42, 0.10, 1)
            inner_r = mane_r * 0.82
            Ellipse(pos=(lx-inner_r, ly-inner_r*0.78), size=(inner_r*2, inner_r*1.6))

            # Face
            Color(0.92, 0.72, 0.38, 1)
            face_r = mane_r * 0.65
            Ellipse(pos=(lx-face_r, ly-face_r*0.8), size=(face_r*2, face_r*1.65))

            # Forehead lighter
            Color(1.0, 0.82, 0.48, 0.7)
            Ellipse(pos=(lx-face_r*0.55, ly+face_r*0.1), size=(face_r*1.1, face_r*0.7))

            # Ears
            ear_y = ly + face_r * 0.85
            for ex in [lx - face_r*0.72, lx + face_r*0.72]:
                Color(0.72, 0.42, 0.10, 1)
                Ellipse(pos=(ex-14, ear_y-14), size=(28,28))
                Color(0.92, 0.68, 0.42, 1)
                Ellipse(pos=(ex-8, ear_y-8), size=(16,16))

            # Eyes
            roar_squint = 0.6 if self.is_roaring else 1.0
            for ex2, ey2 in [(lx-face_r*0.32, ly+face_r*0.2),
                             (lx+face_r*0.32, ly+face_r*0.2)]:
                Color(0.95,0.88,0.35,1)
                Ellipse(pos=(ex2-11, ey2-11*roar_squint),
                        size=(22, 22*roar_squint))
                Color(0.1,0.08,0.0,1)
                Ellipse(pos=(ex2-6, ey2-6*roar_squint),
                        size=(12, 12*roar_squint))
                Color(1,1,1,0.9)
                Ellipse(pos=(ex2+2, ey2+2), size=(5,5))

            # Nose
            Color(0.72, 0.35, 0.28, 1)
            Ellipse(pos=(lx-10, ly-face_r*0.08), size=(20,14))
            # Nostrils
            Color(0.42, 0.18, 0.12, 1)
            Ellipse(pos=(lx-8, ly-face_r*0.05), size=(6,5))
            Ellipse(pos=(lx+3, ly-face_r*0.05), size=(6,5))

            # Mouth (open if roaring)
            Color(0.42, 0.18, 0.12, 1)
            if self.is_roaring:
                mouth_open = abs(math.sin(self.roar_t * 8)) * face_r*0.45 + face_r*0.2
                Line(points=[lx-face_r*0.22, ly-face_r*0.18,
                              lx, ly-face_r*0.18 - mouth_open,
                              lx+face_r*0.22, ly-face_r*0.18], width=2.5)
                # Teeth
                Color(0.96, 0.96, 0.96, 1)
                for tx, ty in [(lx-face_r*0.18, ly-face_r*0.18),
                               (lx+face_r*0.18, ly-face_r*0.18)]:
                    Line(points=[tx, ty, tx, ty - mouth_open*0.6], width=3)
                # Tongue
                Color(0.9, 0.25, 0.35, 1)
                Ellipse(pos=(lx-face_r*0.18, ly-face_r*0.18-mouth_open+5),
                        size=(face_r*0.36, mouth_open*0.5))
            else:
                Line(points=[lx-face_r*0.22, ly-face_r*0.18,
                              lx, ly-face_r*0.22,
                              lx+face_r*0.22, ly-face_r*0.18], width=2)

            # Whiskers
            Color(0.95, 0.92, 0.82, 0.9)
            for wx, wy, wdx in [
                (lx-face_r*0.1, ly-face_r*0.02, -face_r*0.7),
                (lx-face_r*0.1, ly-face_r*0.08, -face_r*0.65),
                (lx+face_r*0.1, ly-face_r*0.02, face_r*0.7),
                (lx+face_r*0.1, ly-face_r*0.08, face_r*0.65),
            ]:
                Line(points=[wx, wy, wx+wdx, wy], width=1.2)

            # Body
            Color(0.88, 0.68, 0.35, 1)
            Ellipse(pos=(lx-mane_r*0.72, ly-mane_r*1.45),
                    size=(mane_r*1.45, mane_r*1.5))
            # Legs
            for lleg_x in [lx-mane_r*0.42, lx-mane_r*0.12,
                            lx+mane_r*0.12, lx+mane_r*0.42]:
                Color(0.85, 0.65, 0.32, 1)
                Rectangle(pos=(lleg_x-9, ly-mane_r*1.7), size=(18, mane_r*0.5))
                # Paws
                Color(0.92, 0.72, 0.38, 1)
                Ellipse(pos=(lleg_x-11, ly-mane_r*1.85), size=(22,14))

            # Tail
            Color(0.82, 0.58, 0.22, 1)
            tail_wave2 = math.sin(self.idle_t * 1.5) * 20
            Line(points=[lx+mane_r*0.72, ly-mane_r*0.9,
                          lx+mane_r*1.2, ly-mane_r*1.4+tail_wave2,
                          lx+mane_r*1.0, ly-mane_r*1.8+tail_wave2], width=4)
            # Tail tuft
            Color(0.45, 0.22, 0.04, 1)
            Ellipse(pos=(lx+mane_r*0.85, ly-mane_r*1.92+tail_wave2),
                    size=(22,22))

            # "TAP TO ROAR" hint
            if not self.is_roaring:
                Color(0.1,0.1,0.1,0.5)
                Label  # hint drawn as label in layout

    def on_touch_down(self, touch):
        self.start_roar()
        return True


class LionScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        layout.add_widget(LionWidget())
        layout.add_widget(Label(
            text='🦁 چھوئیں شیر دہاڑے!',
            font_size='13sp', color=(0.6,0.3,0.05,0.9),
            size_hint=(0.55,0.06),
            pos_hint={'right':0.99,'top':0.985}, halign='right'))
        layout.add_widget(BackButton(None))
        self.layout = layout
        self.add_widget(layout)

    def on_enter(self):
        for w in self.layout.children:
            if isinstance(w, BackButton):
                w._manager = self.manager


# ═══════════════════════════════════════════
#  5. SNAKE CRAWL  🐍
# ═══════════════════════════════════════════

class SnakeWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.segments = []
        self.target_x = 0
        self.target_y = 0
        self.t = 0
        Clock.schedule_once(self._init, 0.1)
        Clock.schedule_interval(self.update, 1/60)

    def _init(self, dt):
        W, H = Window.width, Window.height
        self.target_x = W/2
        self.target_y = H/2
        for i in range(35):
            self.segments.append({'x': W/2 - i*8, 'y': H/2})

    def update(self, dt):
        W, H = Window.width, Window.height
        self.t += dt

        # Head follows target
        head = self.segments[0]
        dx = self.target_x - head['x']
        dy = self.target_y - head['y']
        dist = math.sqrt(dx*dx + dy*dy) + 0.001
        speed = min(dist * 0.08, 4.5)
        head['x'] += dx/dist * speed
        head['y'] += dy/dist * speed

        # Each segment follows previous
        for i in range(1, len(self.segments)):
            prev = self.segments[i-1]
            curr = self.segments[i]
            dx2 = prev['x'] - curr['x']
            dy2 = prev['y'] - curr['y']
            d = math.sqrt(dx2*dx2 + dy2*dy2) + 0.001
            seg_len = 9
            if d > seg_len:
                curr['x'] = prev['x'] - dx2/d * seg_len
                curr['y'] = prev['y'] - dy2/d * seg_len

        # Auto wander
        if random.random() < 0.015:
            self.target_x = random.uniform(50, W-50)
            self.target_y = random.uniform(50, H-50)

        self.canvas.clear()
        with self.canvas:
            # Jungle background
            Color(0.08, 0.22, 0.08, 1)
            Rectangle(pos=(0,0), size=(W,H))
            # Light patches
            for i in range(4):
                lx = W * (0.15 + i*0.22)
                Color(0.15, 0.38, 0.12, 0.4)
                Ellipse(pos=(lx-40, H*0.3-40), size=(80,80))

            # Leaves / foliage
            Color(0.12, 0.45, 0.15, 0.7)
            for i in range(0, int(W), 28):
                lh = random.uniform(H*0.05, H*0.18)
                Line(points=[i, H, i+7, H-lh, i+14, H], width=8)
            for i in range(0, int(W), 28):
                lh = random.uniform(H*0.05, H*0.18)
                Line(points=[i, 0, i+7, lh, i+14, 0], width=8)

            # Ground
            Color(0.12, 0.28, 0.08, 1)
            Rectangle(pos=(0,0), size=(W, H*0.08))

            n = len(self.segments)
            for i in range(n-1, -1, -1):
                seg = self.segments[i]
                t_frac = i / (n-1)
                thickness = lerp(22, 8, t_frac)
                # Color gradient green->dark
                r = lerp(0.15, 0.05, t_frac)
                g = lerp(0.68, 0.38, t_frac)
                b2 = lerp(0.12, 0.05, t_frac)

                # Scale pattern
                if i % 3 == 0:
                    scale_c = 0.08
                    Color(r+scale_c, g+scale_c*0.5, b2, 0.85)
                else:
                    Color(r, g, b2, 0.9)

                Ellipse(pos=(seg['x']-thickness/2,
                              seg['y']-thickness/2),
                        size=(thickness, thickness))

                # Belly
                if i > 2:
                    belly_w = thickness * 0.5
                    Color(0.65, 0.78, 0.25, 0.55)
                    Ellipse(pos=(seg['x']-belly_w/2,
                                  seg['y']-belly_w/2),
                            size=(belly_w, belly_w))

            # Head
            hd = self.segments[0]
            Color(0.18, 0.72, 0.15, 1)
            Ellipse(pos=(hd['x']-14, hd['y']-10), size=(28, 22))
            # Snout
            Color(0.25, 0.80, 0.22, 1)
            Ellipse(pos=(hd['x']-10, hd['y']-7), size=(20, 16))
            # Eyes
            for ex, ey in [(hd['x']-5, hd['y']+4), (hd['x']+5, hd['y']+4)]:
                Color(0.9, 0.85, 0.1, 1)
                Ellipse(pos=(ex-4, ey-4), size=(8,8))
                Color(0.05,0.05,0.05,1)
                Ellipse(pos=(ex-2, ey-2), size=(4,4))
            # Tongue
            tongue_flick = abs(math.sin(self.t * 8))
            if tongue_flick > 0.3:
                head_dx = self.segments[1]['x'] - hd['x']
                head_dy = self.segments[1]['y'] - hd['y']
                ha = math.atan2(-head_dy, -head_dx)
                Color(0.92, 0.12, 0.22, 1)
                tx = hd['x'] + math.cos(ha)*14
                ty = hd['y'] + math.sin(ha)*14
                Line(points=[hd['x'], hd['y'], tx, ty], width=1.8)
                fork_len = 7
                Line(points=[tx, ty,
                              tx + math.cos(ha+0.4)*fork_len,
                              ty + math.sin(ha+0.4)*fork_len], width=1.5)
                Line(points=[tx, ty,
                              tx + math.cos(ha-0.4)*fork_len,
                              ty + math.sin(ha-0.4)*fork_len], width=1.5)

    def on_touch_down(self, touch):
        self.target_x = touch.x
        self.target_y = touch.y
        return True

    def on_touch_move(self, touch):
        self.target_x = touch.x
        self.target_y = touch.y
        return True


class SnakeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        layout.add_widget(SnakeWidget())
        layout.add_widget(Label(
            text='🐍 چھوئیں سانپ پیچھا کرے!',
            font_size='13sp', color=(0.5,1,0.3,0.85),
            size_hint=(0.6,0.06),
            pos_hint={'right':0.99,'top':0.985}, halign='right'))
        layout.add_widget(BackButton(None))
        self.layout = layout
        self.add_widget(layout)

    def on_enter(self):
        for w in self.layout.children:
            if isinstance(w, BackButton):
                w._manager = self.manager


# ═══════════════════════════════════════════
#  6. SHARK HUNT  🦈
# ═══════════════════════════════════════════

class SharkWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.shark = {}
        self.small_fish = []
        self.bubbles = []
        self.eaten_flash = 0
        self.t = 0
        Clock.schedule_once(self._init, 0.1)
        Clock.schedule_interval(self.update, 1/60)

    def _init(self, dt):
        W, H = Window.width, Window.height
        self.shark = {
            'x': W/2, 'y': H/2,
            'vx': 2.0, 'vy': 0.2,
            'target_idx': 0,
            'fin_t': 0,
        }
        for _ in range(12):
            self.small_fish.append(self._new_fish())

    def _new_fish(self):
        W, H = Window.width, Window.height
        return {
            'x': random.uniform(30, W-30),
            'y': random.uniform(H*0.1, H*0.9),
            'vx': random.choice([-1,1])*random.uniform(0.8,1.8),
            'vy': random.uniform(-0.2,0.2),
            'size': random.uniform(8,16),
            'color': random.choice([
                [1,.6,.1],[0.2,.8,.8],[1,.9,.2],[0.5,1,.3]
            ]),
            'tail_t': random.uniform(0,6)
        }

    def update(self, dt):
        W, H = Window.width, Window.height
        self.t += dt
        sh = self.shark
        sh['fin_t'] += dt * 2

        # Shark target nearest fish
        if self.small_fish:
            nearest = min(self.small_fish,
                key=lambda f: (f['x']-sh['x'])**2+(f['y']-sh['y'])**2)
            dx = nearest['x'] - sh['x']
            dy = nearest['y'] - sh['y']
            dist = math.sqrt(dx*dx + dy*dy) + 0.001

            sh['vx'] = lerp(sh['vx'], dx/dist*3.5, 0.04)
            sh['vy'] = lerp(sh['vy'], dy/dist*3.0, 0.04)

            # Eat fish
            if dist < 28:
                self.small_fish.remove(nearest)
                self.eaten_flash = 1.0
                self.small_fish.append(self._new_fish())
                for _ in range(20):
                    ang = random.uniform(0, 2*math.pi)
                    spd = random.uniform(1,4)
                    self.bubbles.append({
                        'x': sh['x'], 'y': sh['y'],
                        'vx': math.cos(ang)*spd,
                        'vy': math.sin(ang)*spd + 1,
                        'r': random.uniform(3,8),
                        'alpha': 0.8
                    })

        sh['x'] = clamp(sh['x'] + sh['vx'], 40, W-40)
        sh['y'] = clamp(sh['y'] + sh['vy'], 40, H-40)
        if sh['x'] <= 40 or sh['x'] >= W-40: sh['vx'] *= -1
        if sh['y'] <= 40 or sh['y'] >= H-40: sh['vy'] *= -1

        if self.eaten_flash > 0:
            self.eaten_flash -= 0.05

        for f in self.small_fish:
            f['tail_t'] += dt * 4
            f['x'] += f['vx']
            f['y'] += f['vy']
            f['x'] = clamp(f['x'], 20, W-20)
            f['y'] = clamp(f['y'], 20, H-20)
            if f['x'] <= 20 or f['x'] >= W-20: f['vx'] *= -1

        alive_b = []
        for b in self.bubbles:
            b['x'] += b['vx']
            b['y'] += b['vy']
            b['alpha'] -= 0.02
            if b['alpha'] > 0: alive_b.append(b)
        self.bubbles = alive_b

        self.canvas.clear()
        with self.canvas:
            # Deep ocean
            Color(0.02, 0.12, 0.35, 1)
            Rectangle(pos=(0,0), size=(W,H))
            Color(0.03, 0.18, 0.48, 0.6)
            Rectangle(pos=(0, H*0.5), size=(W, H*0.5))

            # Light rays from surface
            Color(0.4, 0.65, 0.9, 0.08)
            for ray in range(5):
                rx = W * (0.1 + ray*0.2)
                Line(points=[rx-20, H, rx+40, H*0.3,
                              rx+70, H*0.3, rx+20, H], width=1)

            # Sand
            Color(0.6, 0.5, 0.28, 1)
            Rectangle(pos=(0,0), size=(W, H*0.08))

            # Bubbles
            for b in self.bubbles:
                Color(0.7, 0.88, 1, b['alpha']*0.6)
                Line(circle=(b['x'], b['y'], b['r']), width=1.2)

            # Flash on eat
            if self.eaten_flash > 0:
                Color(1, 0.85, 0.1, self.eaten_flash*0.3)
                Rectangle(pos=(0,0), size=(W,H))

            # Small fish
            for f in self.small_fish:
                tail = math.sin(f['tail_t']) * 5
                s = f['size']
                cx3, cy3 = f['x'], f['y']
                c = f['color']
                facing = 1 if f['vx'] > 0 else -1
                Color(c[0], c[1], c[2], 0.92)
                Ellipse(pos=(cx3-s, cy3-s*0.4), size=(s*2, s*0.8))
                Color(c[0]*0.7, c[1]*0.7, c[2]*0.7)
                tx2 = cx3 - facing*s
                Line(points=[tx2, cy3,
                              tx2-facing*s*0.5, cy3+s*0.45+tail*0.3,
                              tx2-facing*s*0.5, cy3-s*0.45-tail*0.3,
                              tx2, cy3], width=1)
                Color(0.9, 0.9, 0.9,1)
                Ellipse(pos=(cx3+facing*s*0.4-4, cy3-3), size=(7,7))
                Color(0.05,0.05,0.05,1)
                Ellipse(pos=(cx3+facing*s*0.4-2, cy3-2), size=(4,4))

            # ── SHARK ──
            sh2 = self.shark
            sx, sy = sh2['x'], sh2['y']
            speed_mag = math.sqrt(sh2['vx']**2 + sh2['vy']**2) + 0.001
            sa = math.atan2(sh2['vy'], sh2['vx'])
            shark_len = 70

            # Shadow
            Color(0,0,0,0.2)
            Ellipse(pos=(sx-shark_len*0.55, sy-12), size=(shark_len*1.1, 24))

            # Body
            Color(0.45, 0.55, 0.62, 1)
            cos_a, sin_a = math.cos(sa), math.sin(sa)
            for seg in range(10):
                t2 = seg/9
                bx = sx - cos_a * shark_len * t2
                by = sy - sin_a * shark_len * t2
                bw = lerp(22, 5, t2)
                Color(0.45, 0.55, 0.62, 0.92)
                Ellipse(pos=(bx-bw/2, by-bw/2*0.7), size=(bw, bw*0.7))

            # Belly
            Color(0.88, 0.90, 0.92, 0.6)
            for seg in range(8):
                t2 = seg/7
                bx = sx - cos_a * shark_len * 0.1 - cos_a * shark_len*0.6*t2
                by = sy - sin_a * shark_len * 0.1 - sin_a * shark_len*0.6*t2
                bw = lerp(12, 3, t2)
                Ellipse(pos=(bx-bw/2, by-bw/3), size=(bw, bw*0.5))

            # Dorsal fin
            fin_wave = math.sin(sh2['fin_t']) * 3
            Color(0.35, 0.42, 0.52, 1)
            perp_x = -sin_a
            perp_y = cos_a
            fin_base1_x = sx - cos_a*shark_len*0.25 + perp_x*12
            fin_base1_y = sy - sin_a*shark_len*0.25 + perp_y*12
            fin_base2_x = sx - cos_a*shark_len*0.48 + perp_x*12
            fin_base2_y = sy - sin_a*shark_len*0.48 + perp_y*12
            fin_tip_x = sx - cos_a*shark_len*0.35 + perp_x*36 + fin_wave
            fin_tip_y = sy - sin_a*shark_len*0.35 + perp_y*36
            Line(points=[fin_base1_x, fin_base1_y,
                          fin_tip_x, fin_tip_y,
                          fin_base2_x, fin_base2_y,
                          fin_base1_x, fin_base1_y], width=2)

            # Pectoral fin
            Color(0.38, 0.48, 0.56, 1)
            pf_x = sx - cos_a*shark_len*0.3 - perp_x*12
            pf_y = sy - sin_a*shark_len*0.3 - perp_y*12
            Line(points=[pf_x, pf_y,
                          pf_x - perp_x*24 - cos_a*16,
                          pf_y - perp_y*24 - sin_a*16,
                          pf_x - cos_a*14, pf_y - sin_a*14,
                          pf_x, pf_y], width=2)

            # Tail
            Color(0.35, 0.45, 0.52, 1)
            tail_x = sx - cos_a*shark_len
            tail_y = sy - sin_a*shark_len
            tail_wave3 = math.sin(sh2['fin_t']*2) * 14
            Line(points=[tail_x, tail_y,
                          tail_x - cos_a*20 + perp_x*22 + tail_wave3,
                          tail_y - sin_a*20 + perp_y*22,
                          tail_x - cos_a*20 - perp_x*22 - tail_wave3,
                          tail_y - sin_a*20 - perp_y*22,
                          tail_x, tail_y], width=2)

            # Eye
            Color(0.95, 0.95, 0.85, 1)
            eye_x = sx + cos_a*shark_len*0.42 + perp_x*7
            eye_y = sy + sin_a*shark_len*0.42 + perp_y*7
            Ellipse(pos=(eye_x-7, eye_y-7), size=(14,14))
            Color(0.0,0.0,0.0,1)
            Ellipse(pos=(eye_x-4, eye_y-4), size=(8,8))

            # Teeth / mouth
            Color(0.32, 0.40, 0.48, 1)
            mouth_x = sx + cos_a*shark_len*0.52
            mouth_y = sy + sin_a*shark_len*0.52
            Line(circle=(mouth_x, mouth_y, 14), width=2)
            Color(0.95,0.92,0.88,1)
            for ti in range(6):
                ta2 = math.radians(ti*30)
                Line(points=[mouth_x + math.cos(ta2)*9,
                              mouth_y + math.sin(ta2)*9,
                              mouth_x + math.cos(ta2)*14,
                              mouth_y + math.sin(ta2)*14], width=2)

            # Stripes
            Color(0,0,0,0.12)
            for seg in range(3):
                t2 = 0.2 + seg*0.15
                bx = sx - cos_a*shark_len*t2
                by = sy - sin_a*shark_len*t2
                bw = lerp(22, 5, t2)
                Line(points=[bx + perp_x*bw*0.6, by + perp_y*bw*0.6,
                              bx - perp_x*bw*0.6, by - perp_y*bw*0.6], width=1.5)

    def on_touch_down(self, touch):
        self.shark['vx'] = (touch.x - self.shark['x']) * 0.08
        self.shark['vy'] = (touch.y - self.shark['y']) * 0.08
        return True


class SharkScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        layout.add_widget(SharkWidget())
        layout.add_widget(Label(
            text='🦈 شارک مچھلیوں کا شکار کرے!',
            font_size='13sp', color=(0.6,0.85,1,0.9),
            size_hint=(0.65,0.06),
            pos_hint={'right':0.99,'top':0.985}, halign='right'))
        layout.add_widget(BackButton(None))
        self.layout = layout
        self.add_widget(layout)

    def on_enter(self):
        for w in self.layout.children:
            if isinstance(w, BackButton):
                w._manager = self.manager


# ═══════════════════════════════════════════
#  7. BEE SWARM  🐝
# ═══════════════════════════════════════════

class BeeWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.bees = []
        self.hive_x = 0
        self.hive_y = 0
        self.honey_drops = []
        self.t = 0
        Clock.schedule_once(self._init, 0.1)
        Clock.schedule_interval(self.update, 1/60)

    def _init(self, dt):
        W, H = Window.width, Window.height
        self.hive_x = W * 0.82
        self.hive_y = H * 0.78
        for i in range(28):
            angle = random.uniform(0, 2*math.pi)
            r = random.uniform(10, 60)
            self.bees.append({
                'x': self.hive_x + math.cos(angle)*r,
                'y': self.hive_y + math.sin(angle)*r,
                'vx': math.cos(angle+math.pi/2)*2,
                'vy': math.sin(angle+math.pi/2)*2,
                'wing_t': random.uniform(0, math.pi*2),
                'orbit_r': random.uniform(40, 180),
                'orbit_speed': random.uniform(0.8, 2.0),
                'orbit_angle': random.uniform(0, math.pi*2),
                'patrol': random.random() < 0.4,
                'patrol_x': random.uniform(50, W-50),
                'patrol_y': random.uniform(50, H-50),
                'patrol_timer': random.uniform(60,180),
            })

    def update(self, dt):
        W, H = Window.width, Window.height
        self.t += dt

        if random.random() < 0.03:
            self.honey_drops.append({
                'x': self.hive_x + random.uniform(-20,20),
                'y': self.hive_y - 20,
                'vy': -random.uniform(0.5, 1.5),
                'alpha': 0.85, 'r': random.uniform(4,8)
            })

        alive_h = []
        for h in self.honey_drops:
            h['y'] += h['vy']
            h['vy'] -= 0.04
            if h['y'] > self.hive_y - 60:
                h['vy'] = abs(h['vy']) * 0.6
            h['alpha'] -= 0.005
            if h['alpha'] > 0: alive_h.append(h)
        self.honey_drops = alive_h

        for b in self.bees:
            b['wing_t'] += dt * 18
            b['orbit_angle'] += dt * b['orbit_speed']
            b['patrol_timer'] -= 1

            if b['patrol']:
                if b['patrol_timer'] <= 0:
                    b['patrol_x'] = random.uniform(50, W-50)
                    b['patrol_y'] = random.uniform(50, H-50)
                    b['patrol_timer'] = random.uniform(80,200)
                tx = b['patrol_x']
                ty = b['patrol_y']
            else:
                tx = (self.hive_x + math.cos(b['orbit_angle'])*b['orbit_r'])
                ty = (self.hive_y + math.sin(b['orbit_angle'])*b['orbit_r']*0.5)

            dx = tx - b['x']
            dy = ty - b['y']
            dist = math.sqrt(dx*dx+dy*dy) + 0.001
            b['vx'] = lerp(b['vx'], dx/dist*2.8, 0.07)
            b['vy'] = lerp(b['vy'], dy/dist*2.8, 0.07)

            # Separation
            for other in self.bees:
                if other is b: continue
                odx = b['x'] - other['x']
                ody = b['y'] - other['y']
                od = math.sqrt(odx*odx+ody*ody)+0.001
                if od < 18:
                    b['vx'] += odx/od * 0.8
                    b['vy'] += ody/od * 0.8

            b['x'] = clamp(b['x'] + b['vx'], 20, W-20)
            b['y'] = clamp(b['y'] + b['vy'], 20, H-20)

        self.canvas.clear()
        with self.canvas:
            # Sky
            Color(0.55, 0.82, 0.40, 1)
            Rectangle(pos=(0,0), size=(W,H))
            # Clouds
            Color(1,1,1,0.7)
            for cx3, cy3 in [(W*0.2, H*0.88),(W*0.6,H*0.82),(W*0.85,H*0.9)]:
                for off in [(-25,18),(0,22),(25,18),(45,15)]:
                    Ellipse(pos=(cx3+off[0]-off[1], cy3-off[1]),
                            size=(off[1]*2, off[1]*2))

            # Flowers
            flower_pos = [(W*0.15,H*0.18),(W*0.35,H*0.12),(W*0.55,H*0.20),
                          (W*0.72,H*0.15),(W*0.08,H*0.25),(W*0.90,H*0.22)]
            for fx2, fy2 in flower_pos:
                Color(0.2, 0.6, 0.15, 1)
                Line(points=[fx2, 0, fx2+5, fy2-10, fx2, fy2], width=3)
                for pa in range(0,360,60):
                    pr = math.radians(pa)
                    Color(random.choice([[1,.3,.5],[1,.8,.2],[.8,.3,1]]))
                    px2 = fx2 + math.cos(pr)*14
                    py2 = fy2 + math.sin(pr)*14
                    Ellipse(pos=(px2-8,py2-8), size=(16,16))
                Color(1,.92,.1,1)
                Ellipse(pos=(fx2-8, fy2-8), size=(16,16))

            # Hive
            hx, hy = self.hive_x, self.hive_y
            Color(0.72, 0.45, 0.08, 1)
            Ellipse(pos=(hx-32, hy-38), size=(64, 75))
            Color(0.88, 0.62, 0.12, 1)
            Ellipse(pos=(hx-26, hy-30), size=(52, 60))
            # Hive lines
            Color(0.55, 0.32, 0.04, 0.7)
            for hi in range(4):
                Line(points=[hx-26, hy-30+hi*14, hx+26, hy-30+hi*14], width=1.5)
            # Entrance
            Color(0.3, 0.15, 0.02, 1)
            Ellipse(pos=(hx-10, hy-35), size=(20, 10))

            # Honey drops
            for h in self.honey_drops:
                Color(0.98, 0.72, 0.05, h['alpha'])
                Ellipse(pos=(h['x']-h['r'], h['y']-h['r']),
                        size=(h['r']*2, h['r']*2))

            # Bees
            for b in self.bees:
                bx2, by2 = b['x'], b['y']
                vx2, vy2 = b['vx'], b['vy']
                ba = math.atan2(vy2, vx2)
                wing_alpha = abs(math.sin(b['wing_t']))

                # Wings
                Color(0.85, 0.95, 1.0, wing_alpha * 0.72)
                for wsign in [-1, 1]:
                    perp = ba + math.pi/2
                    wx = bx2 + math.cos(perp)*wsign*7
                    wy = by2 + math.sin(perp)*wsign*7
                    Ellipse(pos=(wx-7, wy-4), size=(14, 8))

                # Body (striped)
                Color(0.98, 0.82, 0.05, 1)
                Ellipse(pos=(bx2-7, by2-5), size=(14,10))
                Color(0.12, 0.08, 0.02, 1)
                for si2 in range(3):
                    stripe_x = bx2 - 5 + si2*3.5
                    Line(points=[stripe_x, by2-4, stripe_x, by2+4], width=1.8)

                # Head
                Color(0.98, 0.78, 0.05, 1)
                head_x = bx2 + math.cos(ba)*8
                head_y = by2 + math.sin(ba)*8
                Ellipse(pos=(head_x-4, head_y-4), size=(8,8))
                Color(0.05,0.05,0.05,1)
                Ellipse(pos=(head_x-2, head_y-2), size=(4,4))

                # Stinger
                Color(0.25, 0.15, 0.02, 1)
                tail_x = bx2 - math.cos(ba)*8
                tail_y = by2 - math.sin(ba)*8
                Line(points=[bx2-math.cos(ba)*6, by2-math.sin(ba)*6,
                              tail_x, tail_y], width=2)

    def on_touch_down(self, touch):
        for b in self.bees:
            b['patrol'] = True
            b['patrol_x'] = touch.x + random.uniform(-30,30)
            b['patrol_y'] = touch.y + random.uniform(-30,30)
            b['patrol_timer'] = 120
        return True


class BeeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        layout.add_widget(BeeWidget())
        layout.add_widget(Label(
            text='🐝 چھوئیں مکھیاں آئیں!',
            font_size='13sp', color=(0.2,0.2,0.05,0.85),
            size_hint=(0.55,0.06),
            pos_hint={'right':0.99,'top':0.985}, halign='right'))
        layout.add_widget(BackButton(None))
        self.layout = layout
        self.add_widget(layout)

    def on_enter(self):
        for w in self.layout.children:
            if isinstance(w, BackButton):
                w._manager = self.manager


# ═══════════════════════════════════════════
#  8. FOX WALK  🦊
# ═══════════════════════════════════════════

class FoxWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.fox_x = 0
        self.fox_y = 0
        self.fox_dir = 1
        self.walk_t = 0
        self.speed = 1.8
        self.target_x = 0
        self.stars = []
        self.leaves = []
        self.t = 0
        Clock.schedule_once(self._init, 0.1)
        Clock.schedule_interval(self.update, 1/60)

    def _init(self, dt):
        W, H = Window.width, Window.height
        self.fox_x = W * 0.2
        self.fox_y = H * 0.32
        self.target_x = W * 0.8
        for _ in range(30):
            self.stars.append({
                'x': random.uniform(0, W),
                'y': random.uniform(H*0.45, H),
                'r': random.uniform(1,3),
                'twinkle': random.uniform(0, math.pi*2)
            })
        for _ in range(12):
            self.leaves.append({
                'x': random.uniform(0, W),
                'y': random.uniform(H*0.3, H*0.38),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.2, 0.2),
                'r': random.uniform(4,9),
                'rot': random.uniform(0, math.pi*2),
                'color': random.choice([
                    [0.85,0.42,0.08],[0.92,0.68,0.05],[0.75,0.28,0.05]
                ])
            })

    def update(self, dt):
        W, H = Window.width, Window.height
        self.t += dt
        self.walk_t += dt * 4.5

        dx = self.target_x - self.fox_x
        if abs(dx) > 5:
            self.fox_x += self.fox_dir * self.speed
            self.fox_dir = 1 if dx > 0 else -1
        else:
            self.target_x = W * 0.8 if self.fox_x < W*0.5 else W * 0.15

        for star in self.stars:
            star['twinkle'] += dt * 2.5
        for leaf in self.leaves:
            leaf['x'] += leaf['vx']
            leaf['rot'] += 0.03
            if leaf['x'] < 0 or leaf['x'] > W:
                leaf['vx'] *= -1

        self.canvas.clear()
        with self.canvas:
            # Night sky
            Color(0.04, 0.04, 0.18, 1)
            Rectangle(pos=(0,0), size=(W,H))

            # Moon
            Color(0.98, 0.95, 0.82, 1)
            Ellipse(pos=(W*0.82-28, H*0.82-28), size=(56,56))
            Color(0.04, 0.04, 0.18, 1)
            Ellipse(pos=(W*0.82-20, H*0.82-28), size=(48,56))

            # Stars
            for s2 in self.stars:
                alpha = abs(math.sin(s2['twinkle'])) * 0.7 + 0.3
                Color(1, 0.95, 0.8, alpha)
                Ellipse(pos=(s2['x']-s2['r'], s2['y']-s2['r']),
                        size=(s2['r']*2, s2['r']*2))

            # Ground
            Color(0.15, 0.32, 0.10, 1)
            Rectangle(pos=(0,0), size=(W, H*0.32))
            # Path
            Color(0.35, 0.28, 0.18, 0.6)
            Rectangle(pos=(0, H*0.22), size=(W, H*0.10))

            # Trees
            for tx2 in [W*0.08, W*0.28, W*0.55, W*0.75, W*0.92]:
                Color(0.18, 0.10, 0.04, 1)
                Rectangle(pos=(tx2-6, H*0.32), size=(12, H*0.18))
                Color(0.08, 0.28, 0.08, 1)
                Ellipse(pos=(tx2-22, H*0.48), size=(44, H*0.18))
                Color(0.10, 0.38, 0.10, 0.7)
                Ellipse(pos=(tx2-16, H*0.54), size=(32, H*0.12))

            # Leaves
            for lf in self.leaves:
                Color(lf['color'][0], lf['color'][1], lf['color'][2], 0.8)
                Ellipse(pos=(lf['x']-lf['r'], lf['y']-lf['r']),
                        size=(lf['r']*2, lf['r']*1.5))

            # ── FOX ──
            fx2 = self.fox_x
            fy2 = self.fox_y
            fd = self.fox_dir
            wt = self.walk_t

            # Leg animation
            leg_swing = math.sin(wt) * 10
            leg_swing2 = math.sin(wt + math.pi) * 10

            # Tail
            tail_wave4 = math.sin(self.t * 2) * 15
            tail_pts = []
            for ti2 in range(10):
                t3 = ti2/9
                tx3 = fx2 - fd*25 - fd*t3*40
                ty3 = fy2 + 18 - t3*35 + math.sin(t3*math.pi)*tail_wave4
                tail_pts.extend([tx3, ty3])
            Color(0.88, 0.48, 0.08, 1)
            Line(points=tail_pts, width=8)
            Color(0.95, 0.92, 0.88, 1)
            tail_tip_x = fx2 - fd*65
            tail_tip_y = fy2 - 15 + tail_wave4
            Ellipse(pos=(tail_tip_x-10, tail_tip_y-8), size=(20,16))

            # Body
            Color(0.88, 0.48, 0.08, 1)
            Ellipse(pos=(fx2-28, fy2-18), size=(56, 36))
            # Belly
            Color(0.96, 0.82, 0.65, 0.8)
            Ellipse(pos=(fx2-18, fy2-14), size=(36, 24))

            # Legs (animated)
            Color(0.82, 0.40, 0.06, 1)
            for lx2, lsw in [(fx2-12, leg_swing), (fx2+8, leg_swing2),
                              (fx2-8, leg_swing2), (fx2+12, leg_swing)]:
                Line(points=[lx2, fy2-16, lx2+lsw*0.4, fy2-38], width=5)
                # Paw
                Color(0.72, 0.32, 0.05, 1)
                Ellipse(pos=(lx2+lsw*0.4-5, fy2-44), size=(10,8))
                Color(0.82, 0.40, 0.06, 1)

            # Head
            Color(0.88, 0.48, 0.08, 1)
            Ellipse(pos=(fx2+fd*18-18, fy2+4), size=(36, 30))
            # Snout
            Color(0.96, 0.72, 0.52, 1)
            Ellipse(pos=(fx2+fd*32-10, fy2+6), size=(20, 16))
            # Nose
            Color(0.15, 0.08, 0.08, 1)
            Ellipse(pos=(fx2+fd*40-4, fy2+12), size=(8,6))
            # Eye
            Color(0.95, 0.82, 0.12, 1)
            Ellipse(pos=(fx2+fd*28-5, fy2+18), size=(10,10))
            Color(0.05,0.02,0.02,1)
            Ellipse(pos=(fx2+fd*28-3, fy2+20), size=(6,6))
            Color(1,1,1,0.9)
            Ellipse(pos=(fx2+fd*29, fy2+23), size=(3,3))

            # Ears
            Color(0.88, 0.48, 0.08, 1)
            for ear_x in [fx2+fd*24, fx2+fd*34]:
                Line(points=[ear_x, fy2+32,
                              ear_x + fd*5, fy2+52,
                              ear_x + fd*14, fy2+32,
                              ear_x, fy2+32], width=2)
            Color(0.88, 0.28, 0.28, 0.7)
            for ear_x in [fx2+fd*25, fx2+fd*35]:
                Line(points=[ear_x, fy2+33,
                              ear_x + fd*5, fy2+47,
                              ear_x + fd*12, fy2+33], width=1.5)

            # Breath puff (night air)
            if abs(math.sin(self.t*1.2)) > 0.7:
                Color(1,1,1,0.25)
                puff_x = fx2 + fd*50
                puff_y = fy2 + 15
                Ellipse(pos=(puff_x-6, puff_y-6), size=(12,12))
                Ellipse(pos=(puff_x+fd*6-4, puff_y+2), size=(8,8))

    def on_touch_down(self, touch):
        self.target_x = touch.x
        return True


class FoxScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        layout.add_widget(FoxWidget())
        layout.add_widget(Label(
            text='🦊 چھوئیں لومڑی آئے!',
            font_size='13sp', color=(1,0.7,0.2,0.9),
            size_hint=(0.55,0.06),
            pos_hint={'right':0.99,'top':0.985}, halign='right'))
        layout.add_widget(BackButton(None))
        self.layout = layout
        self.add_widget(layout)

    def on_enter(self):
        for w in self.layout.children:
            if isinstance(w, BackButton):
                w._manager = self.manager


# ═══════════════════════════════════════════
#  9. DOLPHIN JUMP  🌊
# ═══════════════════════════════════════════

class DolphinWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.dolphins = []
        self.splashes = []
        self.waves = []
        self.t = 0
        Clock.schedule_once(self._init, 0.1)
        Clock.schedule_interval(self.update, 1/60)

    def _init(self, dt):
        W, H = Window.width, Window.height
        water_y = H * 0.42
        for i in range(3):
            x_start = W * (0.15 + i*0.32)
            phase = i * math.pi * 0.67
            self.dolphins.append({
                'x': x_start,
                'base_x': x_start,
                'y': water_y,
                'phase': phase,
                'arc_h': H * random.uniform(0.22, 0.38),
                'arc_w': W * random.uniform(0.22, 0.35),
                'speed': random.uniform(0.8, 1.3),
                'above_water': False,
                'splash_done': False,
                'size': random.uniform(28, 40),
                'color': random.choice([
                    [0.38, 0.62, 0.88],
                    [0.28, 0.72, 0.82],
                    [0.42, 0.55, 0.98]
                ])
            })
        for i in range(20):
            self.waves.append({
                'x': random.uniform(0, W),
                'y': H * random.uniform(0.38, 0.52),
                'amp': random.uniform(4, 12),
                'freq': random.uniform(0.015, 0.04),
                'phase': random.uniform(0, math.pi*2),
                'speed': random.uniform(0.3, 0.8),
                'alpha': random.uniform(0.08, 0.22),
            })

    def _make_splash(self, x, y):
        for _ in range(25):
            ang = random.uniform(math.pi*0.1, math.pi*0.9)
            spd = random.uniform(1, 6)
            self.splashes.append({
                'x': x, 'y': y,
                'vx': math.cos(ang)*spd,
                'vy': math.sin(ang)*spd,
                'life': random.uniform(0.5,1.0),
                'r': random.uniform(2,6)
            })

    def update(self, dt):
        W, H = Window.width, Window.height
        self.t += dt
        water_y = H * 0.42

        for d in self.dolphins:
            d['phase'] += dt * d['speed']
            sin_v = math.sin(d['phase'])

            d['x'] = d['base_x'] + math.cos(d['phase']) * d['arc_w'] * 0.5
            d['y'] = water_y + sin_v * d['arc_h']

            was_above = d['above_water']
            d['above_water'] = d['y'] > water_y + 10

            if was_above and not d['above_water']:
                if not d['splash_done']:
                    self._make_splash(d['x'], water_y)
                    d['splash_done'] = True
            elif d['above_water']:
                d['splash_done'] = False

            d['x'] = clamp(d['x'], 30, W-30)

        alive_s = []
        for s in self.splashes:
            s['x'] += s['vx']
            s['y'] += s['vy']
            s['vy'] -= 0.2
            s['life'] -= 0.025
            if s['life'] > 0: alive_s.append(s)
        self.splashes = alive_s

        for wv in self.waves:
            wv['phase'] += dt * wv['speed']

        self.canvas.clear()
        with self.canvas:
            # Sky
            Color(0.48, 0.72, 0.98, 1)
            Rectangle(pos=(0, water_y-20), size=(W, H-water_y+20))
            Color(0.72, 0.88, 1.0, 0.5)
            Rectangle(pos=(0, water_y+H*0.1), size=(W, H*0.4))

            # Sun
            Color(1.0, 0.95, 0.5, 1)
            Ellipse(pos=(W*0.12-22, H*0.82-22), size=(44,44))
            Color(1.0, 0.92, 0.4, 0.25)
            Ellipse(pos=(W*0.12-36, H*0.82-36), size=(72,72))

            # Clouds
            Color(1,1,1,0.82)
            for clx, cly in [(W*0.35, H*0.76),(W*0.65,H*0.82),(W*0.88,H*0.75)]:
                for off in [(-20,14),(0,18),(20,14),(38,12)]:
                    Ellipse(pos=(clx+off[0]-off[1], cly-off[1]),
                            size=(off[1]*2,off[1]*2))

            # Deep ocean
            Color(0.04, 0.22, 0.58, 1)
            Rectangle(pos=(0, 0), size=(W, water_y))
            Color(0.05, 0.28, 0.68, 0.7)
            Rectangle(pos=(0, water_y*0.3), size=(W, water_y*0.7))
            Color(0.08, 0.38, 0.78, 0.35)
            Rectangle(pos=(0, water_y*0.6), size=(W, water_y*0.4))

            # Wave lines
            for wv in self.waves:
                Color(0.55, 0.78, 1.0, wv['alpha'])
                pts = []
                for wx2 in range(0, int(W)+10, 8):
                    wy2 = wv['y'] + wv['amp'] * math.sin(wx2*wv['freq'] + wv['phase'])
                    pts.extend([float(wx2), float(wy2)])
                if len(pts) >= 4:
                    Line(points=pts, width=1.5)

            # Water surface
            Color(0.35, 0.65, 0.92, 0.85)
            surface_pts = []
            for sx2 in range(0, int(W)+5, 5):
                sy2 = water_y + 4*math.sin(sx2*0.025 + self.t*1.8)
                surface_pts.extend([float(sx2), float(sy2)])
            if len(surface_pts) >= 4:
                Line(points=surface_pts, width=3)

            # Splashes
            for s in self.splashes:
                Color(0.7, 0.88, 1.0, s['life']*0.8)
                Ellipse(pos=(s['x']-s['r'], s['y']-s['r']),
                        size=(s['r']*2, s['r']*2))

            # Dolphins (draw above-water ones last)
            draw_order = sorted(self.dolphins, key=lambda d: 0 if d['above_water'] else -1)
            for d in draw_order:
                dx2, dy2 = d['x'], d['y']
                s2 = d['size']
                c = d['color']
                # Angle from velocity direction
                angle = math.atan2(math.cos(d['phase']) * d['arc_h'],
                                   -math.sin(d['phase']) * d['arc_w'] * 0.5)
                cos_a2 = math.cos(angle)
                sin_a2 = math.sin(angle)
                perp2_x = -sin_a2
                perp2_y = cos_a2

                # Shadow in water
                if not d['above_water']:
                    Color(0,0,0.2,0.18)
                    Ellipse(pos=(dx2-s2*1.2, dy2-s2*0.3), size=(s2*2.4, s2*0.5))

                # Body
                Color(c[0], c[1], c[2], 0.95)
                body_len = s2*2.0
                for seg in range(12):
                    t4 = seg/11
                    bx3 = dx2 - cos_a2*body_len*t4
                    by3 = dy2 - sin_a2*body_len*t4
                    bw3 = lerp(s2*0.55, s2*0.12, t4)
                    Ellipse(pos=(bx3-bw3, by3-bw3*0.7),
                            size=(bw3*2, bw3*1.4))

                # Belly
                Color(0.88, 0.92, 0.96, 0.65)
                for seg in range(10):
                    t4 = seg/9
                    bx3 = dx2 - cos_a2*body_len*0.05 - cos_a2*body_len*0.7*t4
                    by3 = dy2 - sin_a2*body_len*0.05 - sin_a2*body_len*0.7*t4
                    bw3 = lerp(s2*0.28, s2*0.06, t4)
                    Ellipse(pos=(bx3-bw3, by3-bw3*0.5),
                            size=(bw3*2, bw3))

                # Dorsal fin
                Color(c[0]*0.82, c[1]*0.82, c[2]*0.82, 0.9)
                fin_bx = dx2 - cos_a2*body_len*0.32
                fin_by = dy2 - sin_a2*body_len*0.32
                Line(points=[fin_bx + perp2_x*s2*0.55, fin_by + perp2_y*s2*0.55,
                              fin_bx + perp2_x*s2*1.2, fin_by + perp2_y*s2*1.2,
                              fin_bx - cos_a2*s2*0.4 + perp2_x*s2*0.55,
                              fin_by - sin_a2*s2*0.4 + perp2_y*s2*0.55,
                              fin_bx + perp2_x*s2*0.55, fin_by + perp2_y*s2*0.55],
                     width=1.8)

                # Flippers
                Color(c[0]*0.78, c[1]*0.78, c[2]*0.78, 0.85)
                fl_bx = dx2 - cos_a2*body_len*0.45
                fl_by = dy2 - sin_a2*body_len*0.45
                for fl_sign in [1, -1]:
                    Line(points=[fl_bx, fl_by,
                                  fl_bx + fl_sign*perp2_x*s2*0.8 - cos_a2*s2*0.5,
                                  fl_by + fl_sign*perp2_y*s2*0.8 - sin_a2*s2*0.5,
                                  fl_bx - cos_a2*s2*0.6, fl_by - sin_a2*s2*0.6,
                                  fl_bx, fl_by], width=1.5)

                # Tail flukes
                Color(c[0]*0.75, c[1]*0.75, c[2]*0.75, 0.9)
                tail_x2 = dx2 - cos_a2*body_len
                tail_y2 = dy2 - sin_a2*body_len
                fluke_wave = math.sin(d['phase']*2) * s2*0.35
                Line(points=[tail_x2, tail_y2,
                              tail_x2 + perp2_x*s2*0.7 + fluke_wave,
                              tail_y2 + perp2_y*s2*0.7,
                              tail_x2 - cos_a2*s2*0.5, tail_y2 - sin_a2*s2*0.5,
                              tail_x2 - perp2_x*s2*0.7 - fluke_wave,
                              tail_y2 - perp2_y*s2*0.7,
                              tail_x2, tail_y2], width=2)

                # Beak/snout
                Color(c[0]*1.05, c[1]*1.05, c[2]*1.05, 0.9)
                beak_x = dx2 + cos_a2*s2*0.65
                beak_y = dy2 + sin_a2*s2*0.65
                Line(points=[dx2 + cos_a2*s2*0.5 + perp2_x*s2*0.2,
                              dy2 + sin_a2*s2*0.5 + perp2_y*s2*0.2,
                              beak_x + cos_a2*s2*0.5, beak_y + sin_a2*s2*0.5,
                              dx2 + cos_a2*s2*0.5 - perp2_x*s2*0.2,
                              dy2 + sin_a2*s2*0.5 - perp2_y*s2*0.2],
                     width=2.5)

                # Smile line
                Color(0.15, 0.15, 0.35, 0.5)
                Line(points=[dx2 + cos_a2*s2*0.38 + perp2_x*s2*0.1,
                              dy2 + sin_a2*s2*0.38 + perp2_y*s2*0.1,
                              dx2 + cos_a2*s2*0.52,
                              dy2 + sin_a2*s2*0.52 - sin_a2*s2*0.05,
                              dx2 + cos_a2*s2*0.38 - perp2_x*s2*0.1,
                              dy2 + sin_a2*s2*0.38 - perp2_y*s2*0.1], width=1.5)

                # Eye
                Color(0.05, 0.05, 0.1, 1)
                eye2_x = dx2 + cos_a2*s2*0.38 + perp2_x*s2*0.3
                eye2_y = dy2 + sin_a2*s2*0.38 + perp2_y*s2*0.3
                Ellipse(pos=(eye2_x-s2*0.1, eye2_y-s2*0.1),
                        size=(s2*0.2, s2*0.2))
                Color(1,1,1,0.9)
                Ellipse(pos=(eye2_x, eye2_y+s2*0.04), size=(s2*0.07,s2*0.07))

                # Water droplets when above
                if d['above_water']:
                    for di2 in range(3):
                        drop_t = (self.t + di2*0.3) % 0.9
                        drop_x = dx2 + perp2_x * s2 * (0.3 + di2*0.2) * math.sin(drop_t*3.5)
                        drop_y = dy2 - drop_t * s2 * 1.2
                        Color(0.6, 0.85, 1.0, 1-drop_t)
                        Ellipse(pos=(drop_x-3, drop_y-5), size=(6,8))

    def on_touch_down(self, touch):
        W, H = Window.width, Window.height
        for d in self.dolphins:
            d['base_x'] = touch.x + random.uniform(-W*0.1, W*0.1)
            d['base_x'] = clamp(d['base_x'], 40, W-40)
        return True


class DolphinScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        layout.add_widget(DolphinWidget())
        layout.add_widget(Label(
            text='🌊 چھوئیں ڈولفن آئے!',
            font_size='13sp', color=(0.2,0.5,0.9,0.9),
            size_hint=(0.55,0.06),
            pos_hint={'right':0.99,'top':0.985}, halign='right'))
        layout.add_widget(BackButton(None))
        self.layout = layout
        self.add_widget(layout)

    def on_enter(self):
        for w in self.layout.children:
            if isinstance(w, BackButton):
                w._manager = self.manager


# ═══════════════════════════════════════════
#  APP ENTRY POINT
# ═══════════════════════════════════════════

class AnimalApp(App):
    def build(self):
        Window.clearcolor = (0.06, 0.06, 0.14, 1)
        sm = ScreenManager(transition=SlideTransition(duration=0.3))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ButterflyScreen(name='butterfly'))
        sm.add_widget(FishScreen(name='fish'))
        sm.add_widget(BirdScreen(name='birds'))
        sm.add_widget(LionScreen(name='lion'))
        sm.add_widget(SnakeScreen(name='snake'))
        sm.add_widget(SharkScreen(name='shark'))
        sm.add_widget(BeeScreen(name='bees'))
        sm.add_widget(FoxScreen(name='fox'))
        sm.add_widget(DolphinScreen(name='dolphin'))
        sm.current = 'menu'
        return sm


if __name__ == '__main__':
    AnimalApp().run()