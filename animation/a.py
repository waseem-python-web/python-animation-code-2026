"""
╔══════════════════════════════════════════╗
║   🎆 ANIMATION APP - Kivy (Python)       ║
║   موبائل اینیمیشن پروگرام               ║
╚══════════════════════════════════════════╝

Installation (Termux / Android):
  pkg install python
  pip install kivy

Run:
  python animation_app.py
"""

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import (
    Color, Ellipse, Line, Rectangle, Triangle
)
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import random
import math

kivy.require('2.0.0')

# ─────────────────────────────────────────
#  MENU SCREEN  (یوزر سے انپٹ لیں)
# ─────────────────────────────────────────
class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        root = FloatLayout()

        # Background
        with root.canvas.before:
            Color(0.05, 0.05, 0.12, 1)
            self.bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(size=self._update_bg, pos=self._update_bg)

        # Title
        title = Label(
            text="✨ اینیمیشن منتخب کریں ✨",
            font_size='26sp',
            bold=True,
            color=(1, 0.9, 0.2, 1),
            size_hint=(1, 0.15),
            pos_hint={'x': 0, 'top': 0.97},
            halign='center'
        )
        root.add_widget(title)

        subtitle = Label(
            text="Animation Select Karen",
            font_size='16sp',
            color=(0.7, 0.7, 1, 1),
            size_hint=(1, 0.08),
            pos_hint={'x': 0, 'top': 0.82},
            halign='center'
        )
        root.add_widget(subtitle)

        # Buttons config
        buttons = [
            {
                'text': '🎆  آتش بازی\n     Fireworks',
                'bg': (0.8, 0.2, 0.1, 1),
                'top': 0.73,
                'screen': 'fireworks'
            },
            {
                'text': '💥  ذرات کا دھماکہ\n     Particle Explosion',
                'bg': (0.1, 0.5, 0.9, 1),
                'top': 0.55,
                'screen': 'particle'
            },
            {
                'text': '⭐  بگ بینگ اثر\n     Big Bang Effect',
                'bg': (0.3, 0.1, 0.7, 1),
                'top': 0.37,
                'screen': 'bigbang'
            },
        ]

        for b in buttons:
            btn = Button(
                text=b['text'],
                font_size='18sp',
                bold=True,
                background_color=b['bg'],
                background_normal='',
                size_hint=(0.78, 0.14),
                pos_hint={'center_x': 0.5, 'top': b['top']},
                halign='center',
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=self._make_go(b['screen']))
            root.add_widget(btn)

        # Footer
        foot = Label(
            text="اسکرین پر واپس جانے کے لیے ← بٹن دبائیں",
            font_size='12sp',
            color=(0.5, 0.5, 0.7, 1),
            size_hint=(1, 0.07),
            pos_hint={'x': 0, 'top': 0.10},
            halign='center'
        )
        root.add_widget(foot)

        self.add_widget(root)

    def _make_go(self, screen_name):
        def go(instance):
            self.manager.current = screen_name
        return go

    def _update_bg(self, *a):
        self.bg.pos = self.children[0].pos
        self.bg.size = self.children[0].size


# ─────────────────────────────────────────
#  BACK BUTTON MIXIN
# ─────────────────────────────────────────
class BackMixin:
    def add_back_button(self, root):
        btn = Button(
            text='← Menu',
            font_size='14sp',
            background_color=(0.2, 0.2, 0.3, 0.9),
            background_normal='',
            size_hint=(0.28, 0.07),
            pos_hint={'x': 0.02, 'top': 0.99},
            color=(1, 1, 1, 1)
        )
        btn.bind(on_press=self._go_menu)
        root.add_widget(btn)

    def _go_menu(self, *a):
        self.manager.current = 'menu'


# ─────────────────────────────────────────
#  1. FIREWORKS ANIMATION  🎆
# ─────────────────────────────────────────
class FireworksWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.particles = []
        self.rockets = []
        Clock.schedule_interval(self.update, 1 / 60)
        Clock.schedule_interval(self.launch_rocket, 0.8)

    def launch_rocket(self, dt):
        x = random.uniform(Window.width * 0.15, Window.width * 0.85)
        self.rockets.append({
            'x': x, 'y': 0,
            'vy': random.uniform(12, 18),
            'burst_y': random.uniform(Window.height * 0.45, Window.height * 0.85),
            'color': [random.random(), random.random(), random.random()]
        })

    def burst(self, x, y, color):
        count = random.randint(60, 120)
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 10)
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.6, 1.0),
                'color': [
                    min(1, color[0] + random.uniform(-0.2, 0.2)),
                    min(1, color[1] + random.uniform(-0.2, 0.2)),
                    min(1, color[2] + random.uniform(-0.2, 0.2)),
                ],
                'size': random.uniform(3, 7)
            })

    def update(self, dt):
        # Update rockets
        new_rockets = []
        for r in self.rockets:
            r['y'] += r['vy']
            if r['y'] >= r['burst_y']:
                self.burst(r['x'], r['y'], r['color'])
            else:
                new_rockets.append(r)
        self.rockets = new_rockets

        # Update particles
        alive = []
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] -= 0.18   # gravity
            p['vx'] *= 0.97   # drag
            p['life'] -= 0.018
            if p['life'] > 0:
                alive.append(p)
        self.particles = alive

        self.canvas.clear()
        with self.canvas:
            # Black background
            Color(0, 0, 0.06, 1)
            Rectangle(pos=self.pos, size=self.size)

            # Draw rockets (small white dot moving up)
            for r in self.rockets:
                Color(1, 1, 0.8, 0.9)
                Ellipse(pos=(r['x'] - 3, r['y'] - 3), size=(6, 6))

            # Draw particles
            for p in self.particles:
                Color(p['color'][0], p['color'][1], p['color'][2], p['life'])
                s = p['size'] * p['life']
                Ellipse(pos=(p['x'] - s/2, p['y'] - s/2), size=(s, s))

    def on_touch_down(self, touch):
        color = [random.random(), random.random(), random.random()]
        self.burst(touch.x, touch.y, color)
        return True


class FireworksScreen(BackMixin, Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        fw = FireworksWidget(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        layout.add_widget(fw)

        info = Label(
            text="🎆 آتش بازی - اسکرین چھوئیں!",
            font_size='15sp',
            color=(1, 1, 0.5, 0.85),
            size_hint=(0.6, 0.07),
            pos_hint={'right': 0.99, 'top': 0.99},
            halign='right'
        )
        layout.add_widget(info)
        self.add_back_button(layout)
        self.add_widget(layout)


# ─────────────────────────────────────────
#  2. PARTICLE EXPLOSION  💥
# ─────────────────────────────────────────
class ParticleWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.particles = []
        Clock.schedule_interval(self.update, 1 / 60)

    def explode(self, x, y):
        colors = [
            [1.0, 0.3, 0.1],
            [1.0, 0.8, 0.0],
            [0.2, 0.8, 1.0],
            [0.8, 0.2, 1.0],
            [0.2, 1.0, 0.4],
            [1.0, 0.4, 0.7],
        ]
        for _ in range(150):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 14)
            color = random.choice(colors)
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.7, 1.2),
                'max_life': random.uniform(0.7, 1.2),
                'color': color[:],
                'size': random.uniform(4, 10),
                'trail': []
            })

    def update(self, dt):
        alive = []
        for p in self.particles:
            p['trail'].append((p['x'], p['y']))
            if len(p['trail']) > 6:
                p['trail'].pop(0)
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] -= 0.25
            p['vx'] *= 0.96
            p['life'] -= 0.02
            if p['life'] > 0:
                alive.append(p)
        self.particles = alive

        self.canvas.clear()
        with self.canvas:
            Color(0.02, 0.02, 0.05, 1)
            Rectangle(pos=self.pos, size=self.size)

            for p in self.particles:
                alpha = max(0, p['life'])
                # Trail
                for i, (tx, ty) in enumerate(p['trail']):
                    ta = alpha * (i / len(p['trail'])) * 0.4
                    Color(p['color'][0], p['color'][1], p['color'][2], ta)
                    ts = p['size'] * 0.4
                    Ellipse(pos=(tx - ts/2, ty - ts/2), size=(ts, ts))

                # Main particle
                Color(p['color'][0], p['color'][1], p['color'][2], alpha)
                s = p['size'] * alpha
                Ellipse(pos=(p['x'] - s/2, p['y'] - s/2), size=(s, s))

                # Glow
                Color(p['color'][0], p['color'][1], p['color'][2], alpha * 0.25)
                gs = s * 2.5
                Ellipse(pos=(p['x'] - gs/2, p['y'] - gs/2), size=(gs, gs))

    def on_touch_down(self, touch):
        self.explode(touch.x, touch.y)
        return True


class ParticleScreen(BackMixin, Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        pw = ParticleWidget(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        layout.add_widget(pw)

        info = Label(
            text="💥 اسکرین پر کہیں بھی چھوئیں!",
            font_size='15sp',
            color=(1, 0.6, 0.2, 0.9),
            size_hint=(0.6, 0.07),
            pos_hint={'right': 0.99, 'top': 0.99},
            halign='right'
        )
        layout.add_widget(info)
        self.add_back_button(layout)
        self.add_widget(layout)


# ─────────────────────────────────────────
#  3. BIG BANG EFFECT  ⭐
# ─────────────────────────────────────────
class BigBangWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.stars = []
        self.ring_radius = 0
        self.ring_life = 0
        self.bang_x = 0
        self.bang_y = 0
        self.flash = 0
        Clock.schedule_interval(self.update, 1 / 60)
        # Auto-bang at start
        Clock.schedule_once(self._auto_bang, 0.5)
        Clock.schedule_interval(self._auto_bang, 3.5)

    def _auto_bang(self, dt):
        cx = random.uniform(Window.width * 0.25, Window.width * 0.75)
        cy = random.uniform(Window.height * 0.25, Window.height * 0.75)
        self.big_bang(cx, cy)

    def big_bang(self, x, y):
        self.bang_x = x
        self.bang_y = y
        self.ring_radius = 0
        self.ring_life = 1.0
        self.flash = 1.0
        # Clear old stars & add new burst
        self.stars = []
        for _ in range(200):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 16)
            dist = random.uniform(0, 5)
            hue = random.choice([
                [1.0, 0.9, 0.5],   # yellow-white
                [0.6, 0.8, 1.0],   # blue-white
                [1.0, 0.5, 0.2],   # orange
                [0.8, 0.5, 1.0],   # purple
                [1.0, 1.0, 1.0],   # white
            ])
            self.stars.append({
                'x': x + math.cos(angle) * dist,
                'y': y + math.sin(angle) * dist,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.8, 1.5),
                'size': random.uniform(1.5, 6),
                'color': hue[:],
                'twinkle': random.uniform(0, math.pi)
            })

    def update(self, dt):
        # Update stars
        alive = []
        for s in self.stars:
            s['x'] += s['vx']
            s['y'] += s['vy']
            s['vx'] *= 0.985
            s['vy'] *= 0.985
            s['vy'] -= 0.05
            s['life'] -= 0.012
            s['twinkle'] += 0.15
            if s['life'] > 0:
                alive.append(s)
        self.stars = alive

        # Ring
        if self.ring_life > 0:
            self.ring_radius += 8
            self.ring_life -= 0.025

        # Flash
        if self.flash > 0:
            self.flash -= 0.06

        self.canvas.clear()
        with self.canvas:
            # Deep space background
            Color(0.0, 0.0, 0.08, 1)
            Rectangle(pos=self.pos, size=self.size)

            # Flash effect
            if self.flash > 0:
                Color(1, 0.95, 0.8, self.flash * 0.6)
                s = self.flash * max(Window.width, Window.height) * 2
                Color(1, 1, 0.9, self.flash * 0.35)
                Ellipse(pos=(self.bang_x - s/2, self.bang_y - s/2),
                        size=(s, s))

            # Expanding ring
            if self.ring_life > 0:
                Color(0.9, 0.7, 0.3, self.ring_life * 0.7)
                r = self.ring_radius
                Line(circle=(self.bang_x, self.bang_y, r), width=2.5)
                Color(0.6, 0.4, 1.0, self.ring_life * 0.4)
                Line(circle=(self.bang_x, self.bang_y, r * 0.75), width=1.5)

            # Stars
            for s in self.stars:
                tw = abs(math.sin(s['twinkle'])) * 0.5 + 0.5
                alpha = s['life'] * tw
                Color(s['color'][0], s['color'][1], s['color'][2], alpha)
                sz = s['size'] * s['life']
                Ellipse(pos=(s['x'] - sz/2, s['y'] - sz/2),
                        size=(sz, sz))
                # Star glow
                Color(s['color'][0], s['color'][1], s['color'][2],
                      alpha * 0.2)
                gsz = sz * 3
                Ellipse(pos=(s['x'] - gsz/2, s['y'] - gsz/2),
                        size=(gsz, gsz))

    def on_touch_down(self, touch):
        self.big_bang(touch.x, touch.y)
        return True


class BigBangScreen(BackMixin, Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        bb = BigBangWidget(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        layout.add_widget(bb)

        info = Label(
            text="⭐ بگ بینگ - چھوئیں یا انتظار کریں!",
            font_size='15sp',
            color=(0.8, 0.7, 1.0, 0.9),
            size_hint=(0.7, 0.07),
            pos_hint={'right': 0.99, 'top': 0.99},
            halign='right'
        )
        layout.add_widget(info)
        self.add_back_button(layout)
        self.add_widget(layout)


# ─────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────
class AnimationApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.12, 1)
        sm = ScreenManager(transition=FadeTransition(duration=0.4))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(FireworksScreen(name='fireworks'))
        sm.add_widget(ParticleScreen(name='particle'))
        sm.add_widget(BigBangScreen(name='bigbang'))
        sm.current = 'menu'
        return sm


if __name__ == '__main__':
    AnimationApp().run()