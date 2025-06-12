from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class ColorOverlay(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # Запазваме препратка към Color, за да можем да го променим по-късно
            self.color_instruction = Color(0.058, 0.227, 0.212, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def set_color(self, r, g, b, a=1):
        """Променя цвета на слоя. Стойности от 0 до 1."""
        self.color_instruction.r = r
        self.color_instruction.g = g
        self.color_instruction.b = b
        self.color_instruction.a = a