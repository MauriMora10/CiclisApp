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
from app.screens.sos_screen import WeatherScreen
from app.screens.checklist_screen import ChecklistScreen
from app.screens.pantalla_mapa import PantallaMapa

consejos_seguridad = [
    {"titulo": "Uso del casco", "descripcion": "Usa casco siempre - reduce 85% el riesgo de lesiones", "icono": "shield-check"},
    {"titulo": "Revisión técnica", "descripcion": "Revisa frenos y luces antes de salir", "icono": "tools"},
    {"titulo": "Señales de tránsito", "descripcion": "Respeta las señales de tránsito", "icono": "traffic-light"},
    {"titulo": "Visibilidad", "descripcion": "Usa ropa reflectante y colores brillantes", "icono": "lightbulb"},
    {"titulo": "Comunicación", "descripcion": "Mantén tu celular con batería suficiente", "icono": "cellphone"},
    {"titulo": "Estado de vías", "descripcion": "Evita ciclovías en mal estado", "icono": "road-variant"},
    {"titulo": "Iluminación nocturna", "descripcion": "Usa luces intermitentes en la noche", "icono": "flashlight"},
    {"titulo": "Distancia segura", "descripcion": "Mantén distancia segura de vehículos", "icono": "car"},
    {"titulo": "Hidratación", "descripcion": "Hidrátate cada 15-20 minutos", "icono": "water"},
    {"titulo": "Neumáticos", "descripcion": "Revisa la presión de neumáticos", "icono": "tire"},
    {"titulo": "Concentración", "descripcion": "No uses audífonos mientras manejas", "icono": "headphones-off"},
    {"titulo": "Planificación", "descripcion": "Planifica tu ruta antes de salir", "icono": "map"}
]

estadisticas_usuario = {
    "distancia_total": 245.7,
    "tiempo_total": 890,  # en minutos
    "rutas_completadas": 18,
    "incidentes_reportados": 5,
    "calorias_quemadas": 3240,
    "co2_ahorrado": 12.3,  # kg
    "velocidad_promedio": 16.5,
    "mejor_tiempo": 42
}

usuarios_db = {
    "admin": {"password": "123", "nombre": "Administrador", "email": "admin@ciclotemuco.cl"},
    "usuario": {"password": "456", "nombre": "María González", "email": "maria@email.com"},
    "ciclista": {"password": "789", "nombre": "Carlos Pérez", "email": "carlos@email.com"}
}

class CiclismoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
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
        Clock.schedule_once(self.mostrar_bienvenida, 1)

    def mostrar_bienvenida(self, *args):
        # Mostrar snackbar en la parte inferior con mayor duración para asegurar visibilidad
        try:
            show_snackbar("Bienvenido a CiclisApp!", duration=4.0, pos_hint={'center_x': 0.5, 'y': 0.02})
        except Exception:
            show_snackbar("Bienvenido a CiclisApp!", duration=3.0)

if __name__ == "__main__":
    app = CiclismoApp()
    app.run()