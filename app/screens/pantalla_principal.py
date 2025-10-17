import os
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.dialog import MDDialog
from app.utils.ui import show_snackbar
import random

from app.data.colores import COLORES
from app.data.rutas import rutas_seguras


consejos_seguridad = [
    {"titulo": "Usa casco", "descripcion": "El casco reduce el riesgo de lesiones graves.", "icono": "bike-helmet"},
    {"titulo": "Respeta las señales", "descripcion": "Obedece semáforos y señales de tránsito.", "icono": "traffic-light"},
    {"titulo": "Mantén tu bici", "descripcion": "Revisa frenos y neumáticos antes de salir.", "icono": "wrench"},
    {"titulo": "Ilumina tu camino", "descripcion": "Usa luces y reflectantes en la noche.", "icono": "flashlight"},
    {"titulo": "Evita distracciones", "descripcion": "No uses el celular mientras pedaleas.", "icono": "cellphone"},
    {"titulo": "Planifica tu ruta", "descripcion": "Elige rutas seguras y conocidas.", "icono": "map-marker"},
]


class PantallaPrincipal(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'principal'

        # Layout principal
        self.main_layout = MDBoxLayout(
            orientation="vertical",
            padding=[dp(16), dp(8), dp(16), dp(8)],
            spacing=dp(12),
            md_bg_color=COLORES['fondo']
        )

        # Toolbar
        self.toolbar = MDTopAppBar(
            title="CiclisApp", elevation=0, md_bg_color=COLORES['principal'], radius=[16, 16, 0, 0]
        )
        self.toolbar.left_action_items = [["arrow-left", lambda x: self.volver_a_login(x)]]
        self.toolbar.right_action_items = [
            ["cog", lambda x: self.abrir_configuracion(x)],
            ["theme-light-dark", lambda x: self.toggle_tema(x)],
        ]

        self.main_layout.add_widget(self.toolbar)

        # Botón para ir al mapa (ejemplo simple)
        self.btn_mapa = MDRaisedButton(
            text="Ver Mapa",
            md_bg_color=COLORES['secundario'],
            font_style="Button",
            elevation=0,
            on_release=self.ir_a_mapa,
        )
        self.main_layout.add_widget(self.btn_mapa)

        self.add_widget(self.main_layout)

    def ir_a_mapa(self, instance):
        if self.manager:
            self.manager.current = 'mapa'

    def toggle_tema(self, instance):
        from kivy.app import App

        app = App.get_running_app()
        if hasattr(app, 'theme_cls'):
            if app.theme_cls.theme_style == "Light":
                app.theme_cls.theme_style = "Dark"
                show_snackbar("Modo nocturno activado")
            else:
                app.theme_cls.theme_style = "Light"
                show_snackbar("Modo claro activado")

    def mostrar_ubicacion(self, instance):
        lat, lon = -38.7359, -72.5904
        try:
            self.mapa.limpiar_todo()
            self.mapa.agregar_marcador(lat, lon, COLORES['exito'], "usuario")
            show_snackbar("Ubicación actual mostrada")
        except Exception:
            show_snackbar("Funcionalidad de mapa no disponible")

    def mostrar_ruta_segura(self, instance):
        ruta_nombre = random.choice(list(rutas_seguras.keys())) if rutas_seguras else None
        if ruta_nombre:
            coordenadas = rutas_seguras[ruta_nombre].get("coordenadas", [])
            try:
                self.mapa.limpiar_todo()
                self.mapa.agregar_ruta(coordenadas, COLORES['principal'])
                if len(coordenadas) >= 2:
                    self.mapa.agregar_marcador(coordenadas[0][0], coordenadas[0][1], COLORES['exito'], "inicio")
                    self.mapa.agregar_marcador(coordenadas[-1][0], coordenadas[-1][1], COLORES['peligro'], "fin")
                show_snackbar(f"Mostrando: {ruta_nombre}")
            except Exception:
                show_snackbar("Funcionalidad de mapa no disponible")
        else:
            show_snackbar("No hay rutas seguras definidas")

    def seleccionar_ruta(self, nombre_ruta):
        info_ruta = rutas_seguras.get(nombre_ruta, {})
        coordenadas = info_ruta.get("coordenadas", [])
        try:
            self.mapa.limpiar_todo()
            self.mapa.agregar_ruta(coordenadas, COLORES['principal'])
            if len(coordenadas) >= 2:
                self.mapa.agregar_marcador(coordenadas[0][0], coordenadas[0][1], COLORES['exito'], "inicio")
                self.mapa.agregar_marcador(coordenadas[-1][0], coordenadas[-1][1], COLORES['peligro'], "fin")
            show_snackbar(f"Ruta seleccionada: {nombre_ruta}")
        except Exception:
            show_snackbar("No se pudo mostrar la ruta")

    def reportar_problema(self, instance):
        lat = random.uniform(-38.75, -38.72)
        lon = random.uniform(-72.61, -72.57)
        tipo = random.choice(["peligro", "reparacion", "obstruccion"])
        try:
            self.mapa.agregar_incidente(lat, lon, tipo)
            tipos_texto = {
                "peligro": "Peligro reportado",
                "reparacion": "Reparación necesaria",
                "obstruccion": "Obstrucción reportada",
            }
            show_snackbar(tipos_texto[tipo])
        except Exception:
            show_snackbar("Reporte simulado (sin mapa)")

    def limpiar_mapa(self, instance):
        try:
            self.mapa.limpiar_todo()
            show_snackbar("Mapa limpiado")
        except Exception:
            show_snackbar("No hay mapa para limpiar")

    def mostrar_consejo_aleatorio(self, instance):
        consejos = [
            "Usa casco siempre que salgas a pedalear.",
            "Respeta las señales de tránsito y cruces peatonales.",
            "Mantén tu bicicleta en buen estado.",
            "Usa luces y reflectantes de noche.",
            "Evita usar el celular mientras conduces.",
            "Planifica tu ruta antes de salir.",
        ]
        consejo = random.choice(consejos)
        try:
            self.label_consejo_aleatorio.text = consejo
        except Exception:
            show_snackbar(consejo)

    def cerrar_sesion(self, instance=None):
        def confirmar_logout(instance):
            try:
                self.manager.current = 'login'
                show_snackbar("Sesión cerrada correctamente")
            except Exception:
                show_snackbar("No se pudo cerrar sesión")
            dialog.dismiss()

        def cancelar_logout(instance):
            dialog.dismiss()

        label_dialog = MDLabel()
        label_dialog.theme_text_color = "Primary"
        label_dialog.text = "¿Estás seguro de que quieres cerrar la sesión?"
        dialog = MDDialog(
            title="Cerrar Sesión",
            content_cls=label_dialog,
            buttons=[
                MDFlatButton(
                    text="CANCELAR",
                    on_release=cancelar_logout,
                    theme_text_color="Custom",
                    text_color=COLORES['texto_secundario'],
                ),
                MDRaisedButton(
                    text="CERRAR SESIÓN",
                    on_release=confirmar_logout,
                    md_bg_color=COLORES['peligro'],
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                ),
            ],
        )
        dialog.open()

    def volver_a_login(self, instance):
        if self.manager is not None and 'login' in self.manager.screen_names:
            self.manager.current = 'login'
        else:
            show_snackbar("No se puede volver atrás.")