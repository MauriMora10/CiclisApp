from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from app.utils.ui import show_snackbar
from kivy.uix.image import Image
from kivy.metrics import dp

class RegistroScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'registro'

        scroll = MDScrollView()
        container = MDBoxLayout(orientation="vertical", spacing=dp(24), padding=dp(24), size_hint_y=None)
        container.bind(minimum_height=container.setter("height"))

        # Logo centrado
        logo_path = 'assets/icons/CiclisApp_logo.jpg'
        try:
            logo = Image(source=logo_path, size_hint=(None, None), size=(dp(160), dp(160)), allow_stretch=True)
        except Exception:
            logo = MDLabel(text='🚲', halign='center', font_style='H3')
        logo_box = MDBoxLayout(size_hint=(1, None), height=dp(180), pos_hint={"center_x": 0.5})
        logo_box.add_widget(logo)
        container.add_widget(logo_box)

        # Tarjeta centrada
        card = MDCard(orientation="vertical", padding=dp(20), radius=[20], elevation=0,
                      size_hint=(None, None), size=(dp(320), dp(360)), pos_hint={"center_x": 0.5})
        card.add_widget(MDLabel(text="Registro de Usuario", font_style="H6", halign="center", theme_text_color="Primary"))

        self.user_field = MDTextField(hint_text="Usuario", icon_right="account", mode="rectangle",
                                      size_hint_y=None, height=dp(48))
        self.email_field = MDTextField(hint_text="Email", icon_right="email", mode="rectangle",
                                       size_hint_y=None, height=dp(48))
        self.pass_field = MDTextField(hint_text="Contraseña", password=True, icon_right="lock", mode="rectangle",
                                      size_hint_y=None, height=dp(48))
        card.add_widget(self.user_field)
        card.add_widget(self.email_field)
        card.add_widget(self.pass_field)

        # Botones
        btn_box = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint=(1, None), height=dp(100))
        btn_registrar = MDRaisedButton(text="Registrar", md_bg_color=(0.2, 0.7, 0.2, 1), on_release=self.validar_registro,
                                       size_hint=(1, None), height=dp(44))
        btn_volver = MDFlatButton(text="Volver", on_release=self.volver_login,
                                  size_hint=(1, None), height=dp(36))
        btn_box.add_widget(btn_registrar)
        btn_box.add_widget(btn_volver)
        card.add_widget(btn_box)

        container.add_widget(card)
        scroll.add_widget(container)
        self.add_widget(scroll)

    def validar_registro(self, instance):
        usuario = self.user_field.text.strip()
        email = self.email_field.text.strip()
        contrasena = self.pass_field.text.strip()

        from kivymd.uix.label import MDLabel
        if usuario == "" or email == "" or contrasena == "":
            show_snackbar("Completa todos los campos")
        elif "@" not in email or "." not in email:
            show_snackbar("Email inválido")
        else:
            show_snackbar("¡Registro exitoso! Ahora puedes iniciar sesión.")
            self.manager.current = 'login'

    def volver_login(self, instance):
        self.manager.current = 'login'