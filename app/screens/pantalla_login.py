from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.uix.widget import Widget
from app.data.colores import COLORES
import sys, os

usuarios_db = {
    "admin": {"password": "123", "nombre": "Administrador"},
    "usuario": {"password": "456", "nombre": "Usuario Demo"}
}

class PantallaLogin(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'

        # Fondo principal con scroll
        scroll = MDScrollView()
        layout_principal = MDBoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(24),
            size_hint_y=None,
            height=self.height,
            md_bg_color=COLORES['fondo']
        )
        layout_principal.bind(minimum_height=layout_principal.setter("height"))

        # Título
        layout_principal.add_widget(MDLabel(
            text="🚲 CiclisApp",
            font_style="H3",
            halign="center",
            theme_text_color="Primary"
        ))

        # Tarjeta de login
        card = MDCard(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(20),
            size_hint=(None, None),
            adaptive_height=True,
            width=dp(340),
            pos_hint={"center_x": 0.5},
            elevation=0,
            radius=[20, 20, 20, 20],
            md_bg_color=COLORES['superficie']
        )

        card.add_widget(MDLabel(
            text="Inicia sesión para continuar",
            font_style="Subtitle1",
            halign="center",
            theme_text_color="Secondary"
        ))

        self.input_usuario = MDTextField(
            hint_text="Usuario",
            icon_right="account",
            fill_mode="outline",
            helper_text="Ingresa tu usuario",
            helper_text_mode="on_focus"
        )
        card.add_widget(self.input_usuario)

        self.input_password = MDTextField(
            hint_text="Contraseña",
            password=True,
            icon_right="lock",
            fill_mode="outline",
            helper_text="Ingresa tu contraseña",
            helper_text_mode="on_focus"
        )
        card.add_widget(self.input_password)

        btn_login = MDRaisedButton(
            text="INGRESAR",
            icon="login",
            on_release=self.validar_login,
            md_bg_color=COLORES['principal'],
            text_color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(48),
            elevation=0
        )
        card.add_widget(btn_login)

        btn_demo = MDFlatButton(
            text="MODO DEMO",
            icon="account-eye",
            on_release=self.modo_demo,
            text_color=COLORES['principal'],
            size_hint=(1, None),
            height=dp(48)
        )
        card.add_widget(btn_demo)

        card.add_widget(MDLabel(
            text="Usuarios demo: admin/123, usuario/456",
            font_style="Caption",
            halign="center",
            theme_text_color="Hint"
        ))

        layout_principal.add_widget(card)
        scroll.add_widget(layout_principal)
        self.add_widget(scroll)

    def validar_login(self, instance):
        usuario = self.input_usuario.text.strip()
        password = self.input_password.text.strip()
        if not usuario or not password:
            Snackbar(text="Por favor completa todos los campos").open()
            return
        if usuario in usuarios_db and usuarios_db[usuario]["password"] == password:
            Snackbar(text=f"Bienvenido {usuarios_db[usuario]['nombre']}!").open()
            self.manager.current = 'principal'
        else:
            self.input_usuario.error = True
            self.input_password.error = True
            Snackbar(text="Usuario o contraseña incorrectos").open()

    def modo_demo(self, instance):
        Snackbar(text="Iniciando en modo demostración").open()
        self.manager.current = 'principal'