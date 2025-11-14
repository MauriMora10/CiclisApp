# Dependencias necesarias:
# pip install requests

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
import requests

class WeatherScreen(MDScreen):
    """Pantalla de clima para ciclistas con autodetección de ciudad y diseño limpio."""

    API_KEY = "e93a5bdb07a04dca86d908749275ce5b"  # API key de OpenWeatherMap
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'weather'

        # Fondo con degradado suave (azul claro)
        with self.canvas.before:
            Color(0.8, 0.9, 1, 1)  # Azul claro superior
            self.rect1 = Rectangle(size=self.size, pos=self.pos)
            Color(1, 1, 1, 1)  # Blanco inferior
            self.rect2 = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Layout principal centrado
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint=(1, 1))

        # Tarjeta centrada para información del clima
        self.weather_card = MDCard(
            size_hint=(0.9, None),
            height=dp(220),
            pos_hint={'center_x': 0.5},
            elevation=1,  # Sombra mínima
            radius=[dp(20), dp(20), dp(20), dp(20)],
            md_bg_color=(1, 1, 1, 0.95)
        )

        card_layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        # Etiqueta de ciudad
        self.city_label = MDLabel(
            text='Ciudad: Cargando...',
            halign='center',
            font_style='H5',
            theme_text_color='Primary'
        )
        card_layout.add_widget(self.city_label)

        # Etiqueta de temperatura actual
        self.temp_label = MDLabel(
            text='Temperatura: Cargando...',
            halign='center',
            font_style='H4',
            theme_text_color='Primary'
        )
        card_layout.add_widget(self.temp_label)

        # Etiqueta de temperatura mínima y máxima
        self.temp_min_max_label = MDLabel(
            text='Mín/Máx: Cargando...',
            halign='center',
            font_style='Body1',
            theme_text_color='Secondary'
        )
        card_layout.add_widget(self.temp_min_max_label)

        # Etiqueta de descripción
        self.desc_label = MDLabel(
            text='Descripción: Cargando...',
            halign='center',
            font_style='Body1',
            theme_text_color='Secondary'
        )
        card_layout.add_widget(self.desc_label)

        # Ícono del clima (emoji)
        self.weather_icon = MDLabel(
            text='🌤️',
            halign='center',
            font_style='H4'
        )
        card_layout.add_widget(self.weather_icon)

        self.weather_card.add_widget(card_layout)
        layout.add_widget(self.weather_card)

        # Botón para actualizar clima (debajo del card)
        update_button = MDRaisedButton(
            text='Actualizar clima',
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            md_bg_color="#43A047",
            on_release=self.update_weather
        )
        layout.add_widget(update_button)

        self.add_widget(layout)

        # Detección automática de ciudad al iniciar
        self.detect_city()
        # Actualización automática cada 10 minutos
        Clock.schedule_interval(self.update_weather, 600)

    def _update_rect(self, instance, value):
        """Actualiza el degradado del fondo."""
        self.rect1.size = self.size
        self.rect1.pos = self.pos
        self.rect2.size = (self.width, self.height / 2)
        self.rect2.pos = (self.x, self.y + self.height / 2)

    def detect_city(self):
        """Detecta la ciudad automáticamente usando ipapi.co."""
        try:
            response = requests.get("https://ipapi.co/json/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.current_city = data.get('city', 'Temuco')
            else:
                self.current_city = 'Temuco'
        except Exception:
            self.current_city = 'Temuco'
        # Actualizar clima con la ciudad detectada
        self.update_weather()

    def update_weather(self, dt=None):
        """Actualiza los datos del clima desde OpenWeatherMap."""
        city = self.current_city

        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API_KEY}&units=metric&lang=es"
            response = requests.get(url, timeout=10)
            data = response.json()

            if response.status_code == 200:
                city_name = data['name']
                temp = data['main']['temp']
                temp_min = data['main']['temp_min']
                temp_max = data['main']['temp_max']
                desc = data['weather'][0]['description'].capitalize()
                icon_code = data['weather'][0]['icon']

                self.city_label.text = f'Ciudad: {city_name}'
                self.temp_label.text = f'Temperatura: {temp}°C'
                self.temp_min_max_label.text = f'Mín/Máx: {temp_min}°C / {temp_max}°C'
                self.desc_label.text = f'Descripción: {desc}'
                self.weather_icon.text = self.get_weather_emoji(icon_code)
            elif response.status_code == 401:
                self.show_message('API Key inválida. Verifica tu clave de OpenWeatherMap.')
            elif response.status_code == 404:
                self.show_message('Ciudad no encontrada.')
            else:
                self.show_message(f'Error: {data.get("message", "Error desconocido")}')

        except requests.exceptions.RequestException as e:
            self.show_message('Error de conexión. Verifica tu internet.')
        except Exception as e:
            self.show_message(f'Error al obtener clima: {str(e)}')

    def get_weather_emoji(self, icon_code):
        """Devuelve un emoji basado en el código de ícono de OpenWeatherMap."""
        icon_map = {
            '01d': '☀️',  # clear sky day
            '01n': '🌙',  # clear sky night
            '02d': '⛅',  # few clouds day
            '02n': '☁️',  # few clouds night
            '03d': '☁️',  # scattered clouds
            '03n': '☁️',
            '04d': '☁️',  # broken clouds
            '04n': '☁️',
            '09d': '🌦️',  # shower rain
            '09n': '🌦️',
            '10d': '🌧️',  # rain
            '10n': '🌧️',
            '11d': '⛈️',  # thunderstorm
            '11n': '⛈️',
            '13d': '❄️',  # snow
            '13n': '❄️',
            '50d': '🌫️',  # mist
            '50n': '🌫️'
        }
        return icon_map.get(icon_code, '🌤️')

    def show_message(self, message):
        """Muestra un mensaje usando snackbar o print para debug."""
        try:
            from app.utils.ui import show_snackbar
            show_snackbar(message, duration=3.0)
        except ImportError:
            print(message)  # Fallback si no hay snackbar
