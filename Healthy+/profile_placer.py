from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse
from kivy.properties import StringProperty, NumericProperty, ListProperty


class ProfilePictureCircle(FloatLayout):
    profile_image_source = StringProperty('C:/Users/User/PycharmProjects/Healthy+/img/blank_profile.jpg')  # Път до снимката
    circle_color = ListProperty([1, 1, 1, 1])  # Цвят на кръга/фона, ако няма снимка или за фон
    border_width = NumericProperty(0)  # Ширина на рамката
    border_color_rgba = ListProperty([0, 0, 0, 1])  # Цвят на рамката (черен по подразбиране)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Инициализираме графичните инструкции веднъж при създаването на уиджета
        with self.canvas:
            # Първо рисуваме рамката (ако има такава), за да е под основния кръг
            self.border_color_instruction = Color(*self.border_color_rgba)
            self.border_ellipse = Ellipse(pos=self.pos, size=self.size)

            # След това рисуваме основния кръг/снимка
            self.color_instruction = Color(*self.circle_color)
            # Важно: Ellipse ще се оразмерява спрямо self.pos и self.size на този уиджет
            self.circle_ellipse = Ellipse(pos=self.pos, size=self.size,
                                          source=self.profile_image_source)

        # Свързваме промените в позицията и размера на самия уиджет
        # с метода, който ще актуализира графичните инструкции
        self.bind(pos=self.update_circle, size=self.update_circle)

        # Свързваме промените в свойствата, които контролират изображението и цветовете
        self.bind(profile_image_source=self.update_image_source)
        self.bind(circle_color=self.update_circle_color)
        self.bind(border_width=self.update_border, border_color_rgba=self.update_border_color)

    def update_circle(self, *args):
        # Актуализираме позицията и размера на основния кръг
        # Ако има рамка, намаляваме размера и изместваме позицията, за да има място за нея
        self.circle_ellipse.pos = (self.pos[0] + self.border_width, self.pos[1] + self.border_width)
        self.circle_ellipse.size = (self.size[0] - 2 * self.border_width, self.size[1] - 2 * self.border_width)

        # Актуализираме позицията и размера на рамката
        self.border_ellipse.pos = self.pos
        self.border_ellipse.size = self.size

    def update_image_source(self, instance, value):
        # Тази функция се извиква автоматично, когато profile_image_source се промени
        self.circle_ellipse.source = value

    def update_circle_color(self, instance, value):
        # Актуализираме цвета на основния кръг
        self.color_instruction.rgba = value

    def update_border(self, instance, value):
        # Актуализираме ширината на рамката и преизчисляваме размера на вътрешния кръг
        # Трябва да извикаме update_circle, за да се преизчислят позицията и размера
        self.update_circle()

    def update_border_color(self, instance, value):
        # Актуализираме цвета на рамката
        self.border_color_instruction.rgba = value

    # Публични методи за лесен достъп
    def set_profile_image(self, image_path):
        """Метод за удобно задаване на пътя до профилната снимка."""
        self.profile_image_source = image_path

    def set_circle_color(self, rgba_list):
        """Метод за удобно задаване на цвета на основния кръг."""
        self.circle_color = rgba_list

    def set_border(self, width, rgba_list):
        """Метод за удобно задаване на рамка."""
        self.border_width = width
        self.border_color_rgba = rgba_list