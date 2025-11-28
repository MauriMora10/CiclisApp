from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.clock import Clock
from app.utils.ui import show_snackbar
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))
from app.data.colores import COLORES
from app.data.rutas import rutas_seguras
from app.screens.consejos_screen import ConsejosScreen
from app.screens.weather_screen import WeatherScreen
from app.screens.checklist_screen import ChecklistScreen
from app.screens.pantalla_mapa import PantallaMapa
from kivy.app import App

def load_users():
    import json
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    import json
    with open('user_data.json', 'w') as f:
        json.dump(users, f, indent=4)

# Inicializar usuarios si no existen
if not os.path.exists('user_data.json'):
    initial_users = {
        "admin": {"password": "123", "email": "admin@ciclotemuco.cl", "nombre": "Administrador"},
        "usuario": {"password": "456", "email": "maria@email.com", "nombre": "María González"},
        "ciclista": {"password": "789", "email": "carlos@email.com", "nombre": "Carlos Pérez"}
    }
    save_users(initial_users)
else:
    # Asegurar que los usuarios iniciales estén presentes si el archivo existe pero está vacío
    users = load_users()
    if not users:
        users = initial_users
        save_users(users)

class CiclismoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        # Set theme colors for better dark mode support
        self.theme_cls.theme_style = "Light"  # Default to light theme

        from app.screens.login_screen import LoginScreen
        from app.screens.registro_screen import RegistroScreen
        from app.screens.menu_principal import MenuPrincipal
        from app.screens.reporte_peligro import ReportePeligro
        from app.screens.lista_reportes import ListaReportes

        sm = MDScreenManager()
        sm.add_widget(LoginScreen())
        sm.add_widget(RegistroScreen())
        sm.add_widget(MenuPrincipal())
        sm.add_widget(ReportePeligro())
        sm.add_widget(ListaReportes())
        from app.screens.profile_screen import ProfileScreen
        sm.add_widget(ProfileScreen())
        sm.current = 'login'
        return sm

    def on_start(self):
        pass

if __name__ == "__main__":
    app = CiclismoApp()
    app.run()