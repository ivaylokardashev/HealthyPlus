from kivy.core.window import Window
from kivy.config import Config

# **ВАЖНО**: ТЕЗИ РЕДОВЕ ТРЯБВА ДА СА НАЙ-ОТГОРЕ И НАЙ-РАНО!
# Config.set('input', 'provider', 'android') # Ако е за Android, но за Windows често е 'uvc' или 'opencv'
# Config.set('input', 'camera', 'android')   # Ако е за Android, но за Windows често е '0' (за първа камера)
# За Windows, може да опитате:
Config.set('input', 'provider', 'opencv')
Config.set('input', 'camera', '0') # Или номера на камерата ако имате няколко

Window.size = (360, 640)

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from plus_logo import DoublePlus
from color_overlay import ColorOverlay
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from dashboard import Dashboard
from qread_screen import QRReadScreen
from result_screen import ResultScreen


# Добавяне на фон
LabelBase.register(name="PoppinsSemiBold", fn_regular="fonts/Poppins/Poppins-SemiBold.ttf")
LabelBase.register(name="PoppinsBold", fn_regular="fonts/Poppins/Poppins-Bold.ttf")


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Цветен полупрозрачен слой
        overlay = ColorOverlay(size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.layout.add_widget(overlay)

        # Фоново изображение
        bg_image = Image(
            source='img/backgroundIMG1.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(2.25, 1.2),
            pos_hint={"center_x": 0.3, "center_y": 0.55}
        )
        self.layout.add_widget(bg_image)

        self.textLogo = Label(
            text="Healthy",
            font_name="PoppinsBold",
            font_size="42",
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.47, "center_y": 0.66},
        )
        self.layout.add_widget(self.textLogo)

        plus = DoublePlus(
            size_hint=(None, None),
            size=(43, 43),
            pos_hint={"center_x": 0.77, "center_y": 0.66},

            # Голям плюс
            big_width=41,
            big_height=41,
            big_thickness=8,
            big_radius=2.5,
            big_color=(1, 1, 1, 1),

            # Малък плюс
            small_width=32,
            small_height=32,
            small_thickness=3,
            small_radius=1,
            small_color=(0.058, 0.227, 0.212, 1),
        )
        self.layout.add_widget(plus)

        self.info = Label(
            text="Your Pocket Pharmacist",
            font_name="PoppinsSemiBold",
            font_size="21",
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.45},
        )
        self.layout.add_widget(self.info)

        self.info1 = Label(
            text="Healthy+ makes medication\n"
                 "  safety simple. Scan. Learn.\n"
                 "              Stay protected.",
            font_name="PoppinsSemiBold",
            font_size="13",
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.36},
        )
        self.layout.add_widget(self.info1)

        self.card_button = MDCard(
            size_hint=(None, None),
            size=(323, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.12},
            radius=[12],
            elevation=0,
            md_bg_color=(1, 1, 1, 0.73),  # white 73% opacity background
        )

        # Бутон
        self.button = MDFlatButton(
            text="Get Started",
            theme_text_color="Custom",  # Enable custom color
            text_color=(0.058, 0.227, 0.212, 1),
            font_size="15",
            font_name="PoppinsSemiBold",
            size_hint=(1, 1),  # fill the card
            on_release=self.on_button_click
        )
        self.card_button.add_widget(self.button)
        self.layout.add_widget(self.card_button)

    def on_button_click(self, instance):
        self.manager.current = "dashboard"


class MainApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(Dashboard(name="dashboard"))
        sm.add_widget(QRReadScreen(name="qrread"))
        sm.add_widget(ResultScreen(name="result"))
        return sm


MainApp().run()
