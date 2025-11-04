from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from kivy.metrics import dp
import requests

class WeatherScreen(MDScreen):
    """Pantalla de clima para ciclistas, mostrando el clima actual desde OpenWeatherMap."""

    API_KEY = "tu_api_key_aquí"  # Reemplaza con tu API key real de OpenWeatherMap

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'weather'
        self.md_bg_color = (0.8, 0.9, 1, 1)  # Fondo azul claro

        # Layout principal
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        # Campo para ingresar ciudad
        self.city_field = MDTextField(
            hint_text='Ingresa la ciudad',
            text='Temuco',  # Ciudad por defecto
            size_hint_x=1
        )
        layout.add_widget(self.city_field)

        # Etiquetas para mostrar datos del clima
        self.city_label = MDLabel(text='Ciudad: Cargando...', halign='center', font_style='H5')
        layout.add_widget(self.city_label)

        self.temp_label = MDLabel(text='Temperatura: Cargando...', halign='center', font_style='H4')
        layout.add_widget(self.temp_label)

        self.desc_label = MDLabel(text='Descripción: Cargando...', halign='center', font_style='Body1')
        layout.add_widget(self.desc_label)

        # Ícono o emoji del clima
        self.weather_icon = MDLabel(text='🌤️', font_size=dp(80), halign='center')
        layout.add_widget(self.weather_icon)

        # Botón para actualizar
        update_button = MDRaisedButton(
            text='Actualizar clima',
            size_hint=(1, None),
            height=dp(50),
            on_release=self.update_weather
        )
        layout.add_widget(update_button)

        self.add_widget(layout)

        # Actualizar automáticamente cada 10 minutos (600 segundos)
        Clock.schedule_interval(self.update_weather, 600)
        # Actualizar al iniciar
        self.update_weather()

    def update_weather(self, dt=None):
        """Actualiza los datos del clima desde la API."""
        city = self.city_field.text.strip()
        if not city:
            self.show_message('Ingresa una ciudad válida')
            return

        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API_KEY}&units=metric&lang=es"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                city_name = data['name']
                temp = data['main']['temp']
                desc = data['weather'][0]['description'].capitalize()
                icon_code = data['weather'][0]['icon']

                self.city_label.text = f'Ciudad: {city_name}'
                self.temp_label.text = f'Temperatura: {temp}°C'
                self.desc_label.text = f'Descripción: {desc}'
                self.weather_icon.text = self.get_weather_emoji(icon_code)

                self.show_message('🌦️ Datos meteorológicos actualizados')
            else:
                self.show_message(f'Error: {data.get("message", "Ciudad no encontrada")}')

        except Exception as e:
            self.show_message(f'Error al obtener clima: {str(e)}')

    def get_weather_emoji(self, icon_code):
        """Devuelve un emoji basado en el código de ícono de OpenWeatherMap."""
        # Mapeo simple de íconos a emojis
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
        """Muestra un mensaje (puedes integrar con snackbar si tienes)."""
        print(message)  # Para debug, reemplaza con snackbar si tienes
