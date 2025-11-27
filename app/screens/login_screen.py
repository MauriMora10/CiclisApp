from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from app.utils.ui import show_snackbar


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'

        # CONTENEDOR PRINCIPAL SIN SCROLL
        container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(24),
            padding=(0, dp(24), 0, dp(24)),
        )

        # ---------------------------------------------------
        # LOGO GRANDE Y 100% CENTRADO
        # ---------------------------------------------------
        logo_path = 'assets/icons/CiclisApp_logo.jpg'

        try:
            logo = Image(
                source=logo_path,
                size_hint=(None, None),
                size=(dp(220), dp(220)),
                allow_stretch=True
            )
        except Exception:
            logo = MDLabel(text='🚲', halign='center', font_style='H2')

        # AnchorLayout → siempre centrado
        logo_anchor = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(1, None),
            height=dp(260)
        )
        logo_anchor.add_widget(logo)

        container.add_widget(logo_anchor)

        # ---------------------------------------------------
        # TARJETA LOGIN
        # ---------------------------------------------------
        card = MDCard(
            orientation="vertical",
            padding=dp(20),
            radius=[20],
            elevation=0,
            size_hint=(None, None),
            size=(dp(320), dp(360)),
            pos_hint={"center_x": 0.5},
        )

        card.add_widget(MDLabel(
            text="Iniciar Sesión",
            font_style="H5",
            halign="center",
            theme_text_color="Primary"
        ))

        self.user_field = MDTextField(
            hint_text="Usuario",
            icon_right="account",
            mode="rectangle",
            size_hint_y=None,
            height=dp(48)
        )

        self.pass_field = MDTextField(
            hint_text="Contraseña",
            password=True,
            icon_right="lock",
            mode="rectangle",
            size_hint_y=None,
            height=dp(48)
        )

        card.add_widget(self.user_field)
        card.add_widget(self.pass_field)

        # ---------------------------------------------------
        # BOTONES
        # ---------------------------------------------------
        btn_box = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(140)
        )

        btn_login = MDRaisedButton(
            text="Ingresar",
            md_bg_color=(0.2, 0.6, 1, 1),
            on_release=self.validar_login,
            size_hint=(1, None),
            height=dp(44)
        )

        btn_register = MDFlatButton(
            text="Registrarse",
            on_release=self.ir_a_registro,
            size_hint=(1, None),
            height=dp(36)
        )

        btn_box.add_widget(btn_login)
        btn_box.add_widget(btn_register)
        card.add_widget(btn_box)

        container.add_widget(card)
        self.add_widget(container)

    # ---------------------------------------------------
    # FUNCIONES
    # ---------------------------------------------------

    def validar_login(self, instance):
        usuario = self.user_field.text.strip()
        contrasena = self.pass_field.text.strip()

        if usuario == "" or contrasena == "":
            show_snackbar("Completa todos los campos")
        else:
            from main import load_users
            users = load_users()
            if usuario in users and users[usuario]["password"] == contrasena:
                show_snackbar(f"¡Bienvenido, {users[usuario]['nombre']}!")
                self.manager.current = 'principal'
            else:
                show_snackbar("Usuario o contraseña incorrectos")

    def ir_a_registro(self, instance):
        self.manager.current = 'registro'

    def ir_a(self, pantalla):
        self.menu.dismiss()
        self.manager.current = pantalla





