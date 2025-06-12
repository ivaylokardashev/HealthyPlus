from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from color_overlay import ColorOverlay
from profile_placer import ProfilePictureCircle
from top_rectangle import SquareWidget
from kivy.metrics import dp


class Dashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        overlay = ColorOverlay(size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        overlay.set_color(0.176, 0.525, 0.498, 1)
        self.layout.add_widget(overlay)

        square = SquareWidget(
            size_hint=(None, None),  # Изключваме автоматичното оразмеряване
            size=(360, 259)  # Задаване на конкретни размери
        )

        top_container = MDBoxLayout(
            orientation='horizontal',
            pos_hint={"center_x": 0.5, "center_y": 1.1},
            height=259,  # Височината на квадрата
            padding=[0, 0, 0, 0]  # Без вътрешен отстъп
        )

        top_container.add_widget(square)
        self.layout.add_widget(top_container)

        profile_image = ProfilePictureCircle(
            size_hint=(None, None),
            size=(dp(120), dp(120)),
            pos_hint={'center_x': 0.5, 'center_y': 0.81},
            circle_color=[1,1,1,1]
        )
        profile_image.set_profile_image('img/blank_profile.jpg')
        self.layout.add_widget(profile_image)

        label = Label(
            text="Welcome Alex!",
            font_name="PoppinsBold",
            font_size='24sp',
            halign='center',
            valign='middle',
            pos_hint={"center_x": 0.5, "center_y": 0.67},
        )
        self.layout.add_widget(label)

        card_button = MDCard(
            size_hint=(None, None),
            size=(323, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[12],
            elevation=0,
            md_bg_color=(1, 1, 1, 0.73),  # white 73% opacity background
        )

        scan_button = MDFlatButton(
            text="Scan QR code",
            theme_text_color="Custom",  # Enable custom color
            text_color=(0.058, 0.227, 0.212, 1),  # Red in RGBA
            size_hint=(1, 1),  # fill the card
            size=(200, 50),
            pos_hint={"center_x": 0.5},
            font_size="15",
            font_name="PoppinsSemiBold",
            on_release=self.go_to_qr_scan
        )

        card_button.add_widget(scan_button)

        self.layout.add_widget(card_button)

    def go_to_qr_scan(self, instance):
        self.manager.current = 'qrread'