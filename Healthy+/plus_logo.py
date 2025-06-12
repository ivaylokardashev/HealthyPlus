from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle

class DoublePlus(Widget):
    def __init__(
        self,
        # Голям плюс параметри
        big_width=35,
        big_height=35,
        big_thickness=5,
        big_radius=3.0,
        big_color=(1, 1, 1, 1),

        # Малък плюс параметри
        small_width=22,
        small_height=22,
        small_thickness=3,
        small_radius=2,
        small_color=(0.058, 0.227, 0.212, 1),

        # Позициониране
        size_hint=(None, None),
        size=(43, 43),
        pos_hint=None,
        **kwargs
    ):
        super().__init__(size_hint=size_hint, size=size, pos_hint=pos_hint, **kwargs)

        # Запазване на параметрите
        self.big_width = big_width
        self.big_height = big_height
        self.big_thickness = big_thickness
        self.big_radius = big_radius
        self.big_color = big_color

        self.small_width = small_width
        self.small_height = small_height
        self.small_thickness = small_thickness
        self.small_radius = small_radius
        self.small_color = small_color

        with self.canvas:
            # Голям плюс
            Color(*self.big_color)
            self.h_rect_big = RoundedRectangle()
            self.v_rect_big = RoundedRectangle()

            # Малък плюс
            Color(*self.small_color)
            self.h_rect_small = RoundedRectangle()
            self.v_rect_small = RoundedRectangle()

        self.bind(pos=self.update_rects, size=self.update_rects)

    def update_rects(self, *args):
        # Център на widget-а от pos и size
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2

        # Голям плюс
        bw, bh = self.big_width, self.big_height
        bt = self.big_thickness
        br = self.big_radius

        self.h_rect_big.pos = (cx - bw / 2, cy - bt / 2)
        self.h_rect_big.size = (bw, bt)
        self.h_rect_big.radius = [(br, br)] * 4

        self.v_rect_big.pos = (cx - bt / 2, cy - bh / 2)
        self.v_rect_big.size = (bt, bh)
        self.v_rect_big.radius = [(br, br)] * 4

        # Малък плюс - центриран спрямо големия
        sw = self.small_width
        sh = self.small_height
        st = self.small_thickness
        sr = self.small_radius

        self.h_rect_small.pos = (cx - sw / 2, cy - st / 2)
        self.h_rect_small.size = (sw, st)
        self.h_rect_small.radius = [(sr, sr)] * 4

        self.v_rect_small.pos = (cx - st / 2, cy - sh / 2)
        self.v_rect_small.size = (st, sh)
        self.v_rect_small.radius = [(sr, sr)] * 4
