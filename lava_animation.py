from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
import random
import math

class LavaBackground(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blobs = []
        self.flash = 0
        Clock.schedule_interval(self.animate, 1/30.)

    def add_blob(self):
        r = random.randint(20, 50)
        x = random.randint(r, self.width - r) if self.width > 0 else 300
        y = self.height + r if self.height > 0 else 700
        hue = random.randint(15, 45)
        color = (hue/255, random.randint(100,200)/255, random.randint(30,80)/255)
        with self.canvas:
            Color(rgba=(*color, 0.8))
            blob = Ellipse(pos=(x-r, y-r), size=(r*2, r*2))
            self.blobs.append({
                'widget': blob,
                'dx': random.uniform(-0.6, 0.6),
                'dy': -random.uniform(0.8, 2.0),
                'r': r,
                'color': color
            })
        Clock.schedule_once(lambda dt: self.add_blob(), random.uniform(2, 4))

    def animate(self, dt):
        if self.flash > 0:
            self.flash = max(0, self.flash - 0.05)
        for blob in list(self.blobs):
            blob['widget'].pos = (blob['widget'].pos[0] + blob['dx'], blob['widget'].pos[1] + blob['dy'])
            if blob['widget'].pos[1] < -blob['r']*2:
                self.canvas.remove(blob['widget'])
                self.blobs.remove(blob)
                self.add_blob()
        self.update_graphics()

    def trigger_glow(self):
        self.flash = 1.0

    def update_graphics(self):
        if self.width <= 0 or self.height <= 0:
            return
        for blob in self.blobs:
            r, g, b = blob['color']
            if self.flash > 0:
                r = min(1.0, r + 0.3*self.flash)
                g = min(1.0, g + 0.4*self.flash)
                b = min(1.0, b + 0.2*self.flash)
            blob['widget'].color = (r, g, b, 0.8)

    def on_size(self, *args):
        self.canvas.clear()
        self.blobs.clear()
        for _ in range(4):
            self.add_blob()