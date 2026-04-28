import math
import random
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt6.QtGui import QPainter, QBrush, QRadialGradient, QColor
from PyQt6.QtWidgets import QWidget

class LavaBlob:
    """Одна тёплая «капля» лавы."""
    def __init__(self, canvas_width, canvas_height):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.hue = random.randint(15, 45)
        self.reset(start_from_bottom=False)

    def reset(self, start_from_bottom=True):
        self.radius = random.randint(30, 70)
        self.base_x = random.uniform(self.radius, self.canvas_width - self.radius)
        if start_from_bottom:
            self.y = self.canvas_height + self.radius * 2
        else:
            self.y = random.uniform(-self.radius * 2, self.canvas_height + self.radius * 2)
        self.speed_y = random.uniform(0.7, 1.3)
        self.wave_amplitude = random.uniform(15, 35)
        self.wave_frequency = random.uniform(0.01, 0.025)
        self.phase = random.uniform(0, 2 * math.pi)
        self.x = self.base_x + self.wave_amplitude * math.sin(self.phase)

    def update(self):
        self.y -= self.speed_y
        self.phase += 0.05
        self.x = self.base_x + self.wave_amplitude * math.sin(self.phase)
        if self.y + self.radius < 0:
            self.y = self.canvas_height + self.radius * 2
            self.base_x = random.uniform(self.radius, self.canvas_width - self.radius)
            self.speed_y = random.uniform(0.7, 1.3)
            self.wave_amplitude = random.uniform(15, 35)
            self.wave_frequency = random.uniform(0.01, 0.025)
            self.phase = random.uniform(0, 2 * math.pi)
            self.hue = random.randint(15, 45)


class LavaBackground(QWidget):
    """Фон с анимированными тёплыми пузырями."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(11, 12, 16))
        self.setPalette(p)

        self.blobs = []
        self.blob_count = 8
        self.flash_intensity = 0.0
        self.flash_decay = 0.9

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(45)

    def resizeEvent(self, event):
        self.blobs.clear()
        w, h = self.width(), self.height()
        if w > 0 and h > 0:
            for _ in range(self.blob_count):
                blob = LavaBlob(w, h)
                blob.reset(start_from_bottom=False)
                self.blobs.append(blob)
        super().resizeEvent(event)

    def animate(self):
        for blob in self.blobs:
            blob.update()
        if self.flash_intensity > 0.01:
            self.flash_intensity *= self.flash_decay
        else:
            self.flash_intensity = 0.0
        self.update()

    def trigger_glow(self):
        self.flash_intensity = 1.0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(11, 12, 16))

        for blob in self.blobs:
            base_center = QColor.fromHsl(blob.hue, 220, 140)
            if self.flash_intensity > 0:
                r = min(255, base_center.red()   + int(80 * self.flash_intensity))
                g = min(255, base_center.green() + int(100 * self.flash_intensity))
                b = min(255, base_center.blue()  + int(50 * self.flash_intensity))
                center = QColor(r, g, b, 255)
            else:
                center = base_center

            gradient = QRadialGradient(QPointF(blob.x, blob.y), blob.radius)
            gradient.setColorAt(0.0, center)
            gradient.setColorAt(0.6, QColor(center.red(), center.green(), center.blue(), 120))
            gradient.setColorAt(1.0, QColor(11, 12, 16, 0))

            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRectF(blob.x - blob.radius, blob.y - blob.radius,
                                       blob.radius * 2, blob.radius * 2))

            glow = QRadialGradient(QPointF(blob.x, blob.y), blob.radius * 1.8)
            glow_color = QColor(center.red(), center.green(), center.blue(), 30)
            glow.setColorAt(0.0, glow_color)
            glow.setColorAt(1.0, QColor(11, 12, 16, 0))
            painter.setBrush(QBrush(glow))
            painter.drawEllipse(QRectF(blob.x - blob.radius * 1.8, blob.y - blob.radius * 1.8,
                                       blob.radius * 3.6, blob.radius * 3.6))

        painter.end()