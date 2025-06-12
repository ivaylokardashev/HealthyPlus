from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.metrics import dp  # За density-independent pixels
from kivy.utils import get_color_from_hex  # За по-лесно дефиниране на цветове от хекс
from kivy.uix.floatlayout import FloatLayout  # Добавяме импорт за FloatLayout
from color_overlay import ColorOverlay
from kivy.uix.label import Label

import sqlite3

# --- Дефиниране на списъци със съставки (Примери) ---
HEALTHY_INGREDIENTS = [
    "аскорбинова киселина",
]

UNHEALTHY_INGREDIENTS = [
    "микрокристална целулоза", "магнезиев стеарат", "колоиден безводен силициев диоксид",
]

DANGEROUS_INGREDIENTS = [
    "талк", "e102",
]

# --- Дефиниране на цветове за категориите ---
COLOR_HEALTHY = get_color_from_hex("#4CAF50")  # Зелен (Healthy)
COLOR_UNHEALTHY = get_color_from_hex("#FFC107")  # Жълт (Unhealthy)
COLOR_DANGEROUS = get_color_from_hex("#F44336")  # Червен (Dangerous)
COLOR_UNKNOWN = get_color_from_hex("#9E9E9E")  # Сив (Unknown)


# --- Персонализиран Widget за цветно кръгче ---
class ColoredCircle(Widget):
    def __init__(self, color_rgba, **kwargs):
        super().__init__(**kwargs)
        self.color_rgba = color_rgba
        self.size_hint = (None, None)  # За да се зададе фиксиран размер
        self.size = (dp(16), dp(16))  # Размер на кръгчето

        with self.canvas:
            self.color_instruction = Color(*self.color_rgba)
            # Рисуваме елипса, която е кръг
            self.circle = Ellipse(pos=self.pos, size=self.size)

        # Обновяване позицията и размера на кръгчето, ако се промени уиджета
        self.bind(pos=self.update_circle, size=self.update_circle)

    def update_circle(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size


class ResultScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Основен layout на екрана е FloatLayout
        self.layout = FloatLayout()
        self.add_widget(self.layout)  # Добавяме го към ResultScreen

        overlay = ColorOverlay(size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.layout.add_widget(overlay)
        # Label за името на продукта
        # Позициониран в горната част на FloatLayout-а, центриран хоризонтално
        self.name_label = Label(
            text="Име на продукта:",
            halign="center",
            color=(1, 1, 1, 1),  # <-- Changed to white color (RGBA)
            # font_name="PoppinsBold",  # <-- Changed font style to PoppinsSemiBold
            font_size="25",
            size_hint=(0.9, None),  # Takes 90% of parent's width
            height=dp(50),  # Fixed height
            pos_hint={"center_x": 0.5, "top": 0.95},  # 95% from top, horizontally centered
        )
        self.layout.add_widget(self.name_label)  # Добавяме към новия FloatLayout

        # MDCard за списъка със съставки
        # Позициониран по средата на FloatLayout-а
        self.ingredients_card = MDCard(
            md_bg_color=(0.96, 0.96, 0.96, 0.93),
            radius=[dp(15)],
            elevation=0,
            orientation="vertical",  # MDCard е BoxLayout, така че това е валидно
            padding=dp(10),
            spacing=dp(5),
            size_hint=(0.9, 0.6),  # Заема 90% ширина, 60% височина
            pos_hint={"center_x": 0.5, "center_y": 0.47},
            # Позициониран леко под центъра, за да остави място за бутона отдолу
        )
        self.layout.add_widget(self.ingredients_card)  # Добавяме към новия FloatLayout

        # ScrollView за скролиране на списъка със съставки
        self.scroll_view = MDScrollView()
        self.ingredients_card.add_widget(self.scroll_view)

        # MDBoxLayout, който ще съдържа индивидуалните редове със съставки
        self.ingredients_list_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,  # Важно: За да може ScrollView да скролира
            height=dp(1),  # Начална височина (коригира се динамично в show_result)
            spacing=dp(5),
        )
        self.scroll_view.add_widget(self.ingredients_list_layout)

        self.card_button = MDCard(
            size_hint=(None, None),
            size=(323, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            radius=[12],
            elevation=0,
            md_bg_color=(1, 1, 1, 0.73),  # white 73% opacity background
        )

        # Бутон "Назад"
        # Позициониран в долната част на FloatLayout-а, центриран хоризонтално
        self.back_button = MDFlatButton(
            text="Back",
            theme_text_color="Custom",  # Enable custom color
            text_color=(0.058, 0.227, 0.212, 1),  # Red in RGBA
            font_size="15",
            font_name="PoppinsSemiBold",
            size_hint=(1, 1),  # fill the card
            height="48dp",
            on_release=self.go_back,
        )
        self.card_button.add_widget(self.back_button)
        self.layout.add_widget(self.card_button)  # Добавяме към новия FloatLayout

    def show_result(self, qrcode):
        conn = sqlite3.connect("qr_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, ingredients FROM qr_items WHERE qrcode = ?", (qrcode,))
        result = cursor.fetchone()
        conn.close()

        # Изчистваме предишни резултати
        self.ingredients_list_layout.clear_widgets()
        self.ingredients_list_layout.height = 0  # Ресетваме височината

        if result:
            product_name = result[0]
            ingredients_raw = result[1]

            self.name_label.text = f"{product_name}"

            # Парсваме съставките, разделени с ", "
            ingredients_list = [
                s.strip().lower() for s in ingredients_raw.split(",") if s.strip()
            ]

            # >>> НАСТРОЙКИ ЗА ФИНО ПОЗИЦИОНИРАНЕ НА ТЕКСТА (в dp) <<<
            # Променяйте тези стойности, за да измествате текста спрямо кръгчето.
            #
            # Положителна стойност за text_offset_x_dp измества текста НАДЯСНО.
            # Отрицателна стойност за text_offset_x_dp измества текста НАЛЯВО.
            #
            # Положителна стойност за text_offset_y_dp измества текста НАДОЛУ.
            # Отрицателна стойност за text_offset_y_dp измества текста НАГОРЕ.
            #
            # Пример: dp(0) за без отместване. dp(1) за отместване с 1 пиксел.
            # Експериментирайте с малки стойности (напр. от -5 до 5)
            text_offset_x_dp = dp(-12)  # Хоризонтално изместване на текста (наляво/надясно)
            text_offset_y_dp = dp(12)  # Вертикално изместване на текста (нагоре/надолу)
            # >>> КРАЙ НА НАСТРОЙКИТЕ <<<

            # Добавяме всяка съставка към списъка с класификация
            for ingredient in ingredients_list:
                category_color = COLOR_UNKNOWN  # По подразбиране

                if ingredient in HEALTHY_INGREDIENTS:
                    category_color = COLOR_HEALTHY
                elif ingredient in UNHEALTHY_INGREDIENTS:
                    category_color = COLOR_UNHEALTHY
                elif ingredient in DANGEROUS_INGREDIENTS:
                    category_color = COLOR_DANGEROUS

                # Създаваме ред за всяка съставка
                ingredient_row = MDBoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height=dp(30),  # Фиксирана височина за всеки ред
                )

                # Цветно кръгче
                circle_widget = ColoredCircle(color_rgba=category_color)

                # Обвиваме кръгчето в MDBoxLayout, за да го центрираме вертикално
                circle_container = MDBoxLayout(
                    orientation="vertical",
                    size_hint=(None, 1),  # Заема пълната височина на реда
                    width=dp(30),  # Фиксирана ширина за контейнера на кръгчето
                )
                circle_container.add_widget(circle_widget)

                # Label за текста на съставката
                ingredient_label = MDLabel(
                    text=ingredient.capitalize(),
                    theme_text_color="Primary",
                    font_style="Body2",
                    halign="left",  # Хоризонтално подравняване на текста в неговото пространство
                    valign="middle",  # Вертикално подравняване на текста в неговото пространство
                    size_hint=(1, 1),  # Заема цялото налично пространство
                    # Прилагаме padding директно към MDLabel за фино отместване
                    # padding: [ляво, горе, дясно, долу]
                    padding=[
                        text_offset_x_dp if text_offset_x_dp > 0 else 0,  # Ляв padding (движи текста надясно)
                        text_offset_y_dp,  # Горен padding (движи текста надолу)
                        -text_offset_x_dp if text_offset_x_dp < 0 else 0,  # Десен padding (движи текста наляво)
                        0  # Долен padding
                    ]
                )

                # Ред на добавяне: кръгче отляво, текст отдясно
                ingredient_row.add_widget(circle_container)  # Първо кръгчето (отляво)
                ingredient_row.add_widget(ingredient_label)  # След това лейбъла

                self.ingredients_list_layout.add_widget(ingredient_row)

                self.ingredients_list_layout.height += dp(30) + self.ingredients_list_layout.spacing

        else:
            self.name_label.text = "Продуктът не е намерен."
            self.ingredients_list_layout.clear_widgets()
            self.ingredients_list_layout.height = 0

    def go_back(self, *args):
        self.manager.current = "dashboard"