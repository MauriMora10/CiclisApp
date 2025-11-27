# Dependencias:
# pip install requests

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.app import App
from kivy.uix.image import AsyncImage
import requests


class WeatherScreen(MDScreen):
    """Pantalla de clima con soporte completo para Modo Oscuro."""

    API_KEY = "e93a5bdb07a04dca86d908749275ce5b"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "weather"

        app = App.get_running_app()
        app.theme_cls.bind(theme_style=self.on_theme_change)

        # Fondo por defecto (Modo Claro)
        self.update_background()

        # ---------- LAYOUT PRINCIPAL ----------
        self.main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(20)
        )

        # Card centrada
        from kivy.uix.anchorlayout import AnchorLayout
        card_container = AnchorLayout(anchor_x="center", anchor_y="center", size_hint=(1, 0.8))

        self.weather_card = MDCard(
            size_hint=(0.9, None),
            height=dp(400),
            radius=[28, 28, 28, 28],
            elevation=1,
        )

        self.update_card_color()  # color dinámico según tema

        card_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(15),
        )

        # Etiquetas
        self.city_label = MDLabel(
            text="Ciudad: Cargando...",
            halign="center",
            font_style="H6",
            theme_text_color="Primary",
        )

        self.temp_label = MDLabel(
            text="Temperatura: Cargando...",
            halign="center",
            font_style="H4",
            theme_text_color="Primary",
        )

        self.temp_min_max_label = MDLabel(
            text="Mín/Máx: Cargando...",
            halign="center",
            font_style="Body1",
            theme_text_color="Secondary",
        )

        self.desc_label = MDLabel(
            text="Descripción: Cargando...",
            halign="center",
            font_style="Body1",
            theme_text_color="Secondary",
        )

        # Icono centrado
        icon_container = AnchorLayout(anchor_x="center", anchor_y="center", size_hint_y=None, height=dp(120))
        self.weather_icon = AsyncImage(
            source="http://openweathermap.org/img/wn/01d@2x.png",
            size_hint=(None, None),
            size=(dp(100), dp(100)),
        )
        icon_container.add_widget(self.weather_icon)

        # Agregar al card
        for widget in [
            self.city_label,
            self.temp_label,
            self.temp_min_max_label,
            self.desc_label,
            icon_container,
        ]:
            card_layout.add_widget(widget)

        self.weather_card.add_widget(card_layout)
        card_container.add_widget(self.weather_card)
        self.main_layout.add_widget(card_container)

        # Botón actualizar
        self.update_button = MDRaisedButton(
            text="Actualizar clima",
            size_hint=(0.9, None),
            height=dp(48),
            pos_hint={"center_x": 0.5},
            on_release=self.update_weather,
        )
        self.update_button.md_bg_color = app.theme_cls.primary_color
        self.main_layout.add_widget(self.update_button)

        self.add_widget(self.main_layout)

        # Cargar datos iniciales para Temuco
        self.update_weather()
        Clock.schedule_interval(self.update_weather, 600)

    # =============================================================
    # TEMAS
    # =============================================================
    def update_background(self):
        """Fondo dinámico según tema."""
        app = App.get_running_app()

        if app.theme_cls.theme_style == "Dark":
            self.md_bg_color = (0.05, 0.05, 0.05, 1)  # negro casi puro
        else:
            self.md_bg_color = (0.91, 0.945, 0.992, 1)  # azul claro

    def update_card_color(self):
        """Color dinámico de la tarjeta."""
        app = App.get_running_app()

        if app.theme_cls.theme_style == "Dark":
            # Material 3 dark surfaces
            self.weather_card.md_bg_color = (0.15, 0.15, 0.15, 1)
        else:
            self.weather_card.md_bg_color = (1, 1, 1, 1)

    def on_theme_change(self, *args):
        """Cuando se cambia entre Light/Dark."""
        app = App.get_running_app()

        self.update_background()
        self.update_card_color()

        # Botón primario
        self.update_button.md_bg_color = app.theme_cls.primary_color

        # Refrescar texto de labels (Primary / Secondary)
        for widget in self.walk():
            if isinstance(widget, MDLabel):
                if widget.theme_text_color in ("Primary", "Secondary"):
                    widget.theme_text_color = "Primary"  # forzar refresh
                    widget.theme_text_color = "Secondary" if "Mín/Máx" in widget.text else "Primary"

    # =============================================================
    # API CLIMA
    # =============================================================


    def update_weather(self, dt=None):
        try:
            # Ciudad fija: Temuco
            url = f"http://api.openweathermap.org/data/2.5/weather?q=Temuco&appid={self.API_KEY}&units=metric&lang=es"
            resp = requests.get(url, timeout=10)
            data = resp.json()

            if resp.status_code == 200:
                self.city_label.text = f"Ciudad: {data['name']}"
                self.temp_label.text = f"Temperatura: {data['main']['temp']}°C"
                self.temp_min_max_label.text = (
                    f"Mín/Máx: {data['main']['temp_min']}°C / {data['main']['temp_max']}°C"
                )
                desc = data["weather"][0]["description"].capitalize()
                icon_code = data["weather"][0]["icon"]

                self.desc_label.text = f"Descripción: {desc}"
                self.weather_icon.source = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

            elif resp.status_code == 404:
                self.show_message("Ciudad no encontrada.")
            else:
                self.show_message(data.get("message", "Error desconocido."))

        except Exception:
            self.show_message("Error de conexión.")
            # Fallback para Temuco si la API falla
            self.city_label.text = "Ciudad: Temuco"
            self.temp_label.text = "Temperatura: N/A"
            self.temp_min_max_label.text = "Mín/Máx: N/A"
            self.desc_label.text = "Descripción: Sin conexión"
            self.weather_icon.source = "http://openweathermap.org/img/wn/01d@2x.png"

    # =============================================================
    # ICONOS
    # =============================================================

    def show_message(self, msg):
        try:
            from app.utils.ui import show_snackbar
            show_snackbar(msg, duration=3)
        except:
            print(msg)


