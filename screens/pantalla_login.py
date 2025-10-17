# This file has been removed.
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivymd.uix.snackbar import Snackbar
from data.colores import COLORES

usuarios_db = {
    "admin": {"password": "123", "nombre": "Administrador"},
    "usuario": {"password": "456", "nombre": "Usuario Demo"}
}

class PantallaLogin(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        layout_principal = MDBoxLayout(
            orientation="vertical", 
            spacing=dp(30),
            adaptive_height=True,
            md_bg_color=COLORES['fondo']
        )
        layout_principal.add_widget(Widget(size_hint_y=0.2))
        titulo_box = MDBoxLayout(
            orientation="vertical", 
            spacing=dp(10),
            adaptive_height=True,
            size_hint_y=None,
            height=dp(120)
        )
        label_title = MDLabel(
            text="CicloTemuco",
            font_style="H3",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(70)
        )
        titulo_box.add_widget(label_title)
        layout_principal.add_widget(titulo_box)
        card = MDCard(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(20),
            size_hint=(None, None),
            size=(dp(320), dp(380)),
            pos_hint={"center_x": 0.5},
            elevation=0,
            radius=[15, 15, 15, 15],
            md_bg_color=COLORES['superficie']
        )
        label_subtitle = MDLabel(
            text="Inicia sesión para continuar",
            font_style="Subtitle1",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(30)
        )
        card.add_widget(label_subtitle)
        self.input_usuario = MDTextField(
            hint_text="Usuario",
            mode="rectangle",
            icon_right="account",
            size_hint_x=1,
            helper_text="Ingresa tu usuario",
            helper_text_mode="on_focus"
        )
        card.add_widget(self.input_usuario)
        self.input_password = MDTextField(
            hint_text="Contraseña",
            password=True,
            mode="rectangle",
            icon_right="lock",
            size_hint_x=1,
            helper_text="Ingresa tu contraseña",
            helper_text_mode="on_focus"
        )
        card.add_widget(self.input_password)
        btn_login = MDRaisedButton(
            text="INGRESAR",
            on_release=self.validar_login,
            md_bg_color=COLORES['principal'],
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(48),
            elevation=0
        )
        card.add_widget(btn_login)
        btn_demo = MDFlatButton(
            text="MODO DEMO",
            on_release=self.modo_demo,
            theme_text_color="Custom",
            text_color=COLORES['principal'],
            size_hint=(1, None),
            height=dp(48)
        )
        card.add_widget(btn_demo)
        label_help = MDLabel(
            text="Usuarios demo: admin/123, usuario/456",
            font_style="Caption",
            halign="center",
            theme_text_color="Hint",
            size_hint_y=None,
            height=dp(20)
        )
        card.add_widget(label_help)
        layout_principal.add_widget(card)
        layout_principal.add_widget(Widget(size_hint_y=0.3))
        self.add_widget(layout_principal)
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
