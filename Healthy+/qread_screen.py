from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.spinner import MDSpinner
from kivy_garden.zbarcam import ZBarCam
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.stencilview import StencilView
from kivy.animation import Animation
from kivy.logger import Logger
from kivymd.uix.label import MDLabel


# Creates a square overlay where the QR code should be placed
class FocusOverlay(StencilView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.redraw, size=self.redraw)

    def redraw(self, *args):
        self.canvas.clear()
        with self.canvas:
            cx, cy = self.center
            w, h = 250, 250
            x_hole = cx - w / 2
            y_hole = cy - h / 2

            Color(0, 0, 0, 0.6)
            Rectangle(pos=(0, y_hole + h), size=(self.width, self.height - (y_hole + h)))
            Rectangle(pos=(0, 0), size=(self.width, y_hole))
            Rectangle(pos=(0, y_hole), size=(x_hole, h))
            Rectangle(pos=(x_hole + w, y_hole), size=(self.width - (x_hole + w), h))

            Color(1, 1, 1, 1)
            Line(rectangle=(x_hole, y_hole, w, h), width=2, cap='round')


class QRReadScreen(Screen):
    # Class variable for the single ZBarCam instance
    _zbarcam_instance = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout(
            size_hint=(1, 1),
        )
        self.add_widget(self.layout)

        self.spinner = MDSpinner(
            size_hint=(None, None),
            size=(64, 64),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            active=True
        )
        self.layout.add_widget(self.spinner)

        self.error_label = MDLabel(
            text='',
            halign='center',
            valign='center',
            font_style='H6',
            color=(1, 0, 0, 1),
            size_hint=(0.8, None),
            height='96dp',
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            opacity=0
        )
        self.layout.add_widget(self.error_label)

        self.overlay = None
        self.scanning = False

    def on_enter(self):
        Logger.info("QRReadScreen: Entering screen. Preparing camera.")
        self.scanning = True
        self.spinner.opacity = 1
        self.spinner.active = True
        self.error_label.opacity = 0

        Clock.schedule_once(self.start_camera_after_delay, 0.5)

    def start_camera_after_delay(self, dt):
        if not self.scanning:
            Logger.info("QRReadScreen: Camera startup interrupted (screen left).")
            return

        if QRReadScreen._zbarcam_instance is None:
            Logger.info("QRReadScreen: Creating new ZBarCam instance (first start).")
            try:
                QRReadScreen._zbarcam_instance = ZBarCam(size_hint=(1, 1), pos=(0, 0),)
                self.ids['xcamera'] = QRReadScreen._zbarcam_instance
            except Exception as e:
                Logger.exception("QRReadScreen: Failed to create ZBarCam instance: %s", e)
                self.error_label.text = ("Failed to start camera.\n"
                                         "Please check if the camera is in use by another app,\n"
                                         "privacy settings, or drivers.")
                self.error_label.opacity = 1
                self.spinner.active = False
                self.spinner.opacity = 0
                self.scanning = False
                return
        else:
            Logger.info("QRReadScreen: Using existing ZBarCam instance.")
            self.ids['xcamera'] = QRReadScreen._zbarcam_instance

        # Bind the on_symbols function every time to ensure it's active
        # Unbind first to avoid duplicates if already bound
        QRReadScreen._zbarcam_instance.unbind(symbols=self.on_symbols)
        QRReadScreen._zbarcam_instance.bind(symbols=self.on_symbols)

        # Add ZBarCam to the layout if it's not already there
        if QRReadScreen._zbarcam_instance.parent is None:
            self.layout.add_widget(QRReadScreen._zbarcam_instance, index=0)
            Logger.info("QRReadScreen: ZBarCam added to layout.")
        else:
            Logger.info("QRReadScreen: ZBarCam is already in the layout.")

        if self.overlay is None:
            self.overlay = FocusOverlay(size_hint=(1, 1), pos=(0, 0))
            self.layout.add_widget(self.overlay)
            Logger.info("QRReadScreen: FocusOverlay successfully added.")
        self.overlay.opacity = 0

        Animation(opacity=1, duration=0.5).start(QRReadScreen._zbarcam_instance)
        Animation(opacity=1, duration=0.5).start(self.overlay)

        spinner_anim = Animation(opacity=0, duration=0.5)
        spinner_anim.bind(on_complete=lambda animation, widget: setattr(widget, 'active', False))
        spinner_anim.start(self.spinner)

    def on_symbols(self, instance, symbols):
        if not self.scanning:
            return

        if symbols:
            try:
                qr_text = symbols[0].data.decode("utf-8")
                Logger.info(f"QRReadScreen: Scanned QR code: {qr_text}")
            except Exception as e:
                Logger.error(f"QRReadScreen: Error decoding QR: {e}")
                self.error_label.text = "Error decoding QR code."
                self.error_label.opacity = 1
                return

            self.scanning = False
            self.hide_camera_for_reuse()

            # --- CHANGE STARTS HERE ---
            # Send the scanned symbols to the ResultScreen
            if self.manager and self.manager.has_screen("result"):  # Target 'result' screen
                result_screen = self.manager.get_screen("result")
                if hasattr(result_screen, 'show_result'):
                    result_screen.show_result(qr_text)
                else:
                    Logger.warning("QRReadScreen: ResultScreen does not have a show_result method.")
                self.manager.current = "result"  # Go to 'result' screen
            else:
                Logger.error("QRReadScreen: ResultScreen not found or manager not set.")
            # --- CHANGE ENDS HERE ---

    def hide_camera_for_reuse(self):
        Logger.info("QRReadScreen: Hiding camera for reuse.")

        if QRReadScreen._zbarcam_instance:
            if QRReadScreen._zbarcam_instance.parent:
                QRReadScreen._zbarcam_instance.parent.remove_widget(QRReadScreen._zbarcam_instance)
                Logger.info("QRReadScreen: ZBarCam removed from layout (hidden).")

            try:
                Logger.info("QRReadScreen: Attempting to call _real_stop() on ZBarCam (hidden).")
                if hasattr(QRReadScreen._zbarcam_instance, '_real_stop') and callable(
                        QRReadScreen._zbarcam_instance._real_stop):
                    QRReadScreen._zbarcam_instance._real_stop()
                    Logger.info("QRReadScreen: _real_stop() successfully called (hidden).")

                Logger.info("QRReadScreen: Attempting to call _camera.release() on ZBarCam (hidden).")
                if hasattr(QRReadScreen._zbarcam_instance, '_camera') and \
                        hasattr(QRReadScreen._zbarcam_instance._camera, 'release') and \
                        callable(QRReadScreen._zbarcam_instance._camera.release):
                    QRReadScreen._zbarcam_instance._camera.release()
                    Logger.info("QRReadScreen: _camera.release() successfully called (hidden).")

            except Exception as e:
                Logger.error(f"QRReadScreen: Error explicitly stopping camera when hiding: {e}")

            QRReadScreen._zbarcam_instance.unbind(symbols=self.on_symbols)
            Logger.info("QRReadScreen: ZBarCam unbinded.")

        if self.overlay:
            if self.overlay.parent:
                self.layout.remove_widget(self.overlay)
            self.overlay = None
            Logger.info("QRReadScreen: FocusOverlay removed.")

        self.spinner.opacity = 0
        self.spinner.active = False
        self.error_label.opacity = 0
        Logger.info("QRReadScreen: Spinner and error hidden.")
        Logger.info("QRReadScreen: Camera hiding complete (for reuse).")

    def on_leave(self):
        Logger.info("QRReadScreen: Leaving screen. Hiding camera.")
        self.scanning = False
        self.hide_camera_for_reuse()
