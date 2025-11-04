from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.fitimage import FitImage
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from app.utils.ui import show_snackbar
import json
import os

class ProfileScreen(MDScreen):
    """Pantalla de perfil de usuario para CiclisApp."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'profile'
        self.md_bg_color = (0.96, 0.96, 0.96, 1)  # Fondo gris muy claro #F5F5F5

        # Layout principal
        layout = MDBoxLayout(orientation='vertical', padding=[dp(20), dp(60), dp(20), dp(20)], spacing=dp(20))

        # Contenedor para el botón de volver atrás
        back_button_layout = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            padding=[dp(10), dp(10), 0, 0]
        )
        back_button = MDIconButton(
            icon='arrow-left',
            on_release=lambda x: self.go_back(),
            md_bg_color=(0.29, 0.69, 0.31, 1)  # Verde #4CAF50
        )
        back_button_layout.add_widget(back_button)
        layout.add_widget(back_button_layout)

        # Barra superior con menú hamburguesa
        self.toolbar = MDTopAppBar(
            title='Perfil de usuario',
            elevation=0,
            left_action_items=[['menu', lambda x: self.open_nav_drawer()]],
            md_bg_color="#4CAF50"
        )
        layout.add_widget(self.toolbar)

        # Avatar circular
        avatar_layout = MDBoxLayout(size_hint=(None, None), size=(dp(120), dp(120)), pos_hint={'center_x': 0.5})
        self.avatar = FitImage(source='', size_hint=(None, None), size=(dp(120), dp(120)), radius=[dp(60)])
        self.avatar.md_bg_color = (0.2, 0.6, 0.8, 1)  # Color azul por defecto
        avatar_layout.add_widget(self.avatar)
        layout.add_widget(avatar_layout)

        # Ícono de edición en la esquina superior derecha del avatar
        edit_icon = MDIconButton(icon='pencil', pos_hint={'right': 1, 'top': 1}, size_hint=(None, None), size=(dp(40), dp(40)), on_release=self.select_photo)
        avatar_layout.add_widget(edit_icon)

        # FileManager para seleccionar foto
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=['.png', '.jpg', '.jpeg']
        )

        # Botón editar perfil
        edit_profile_button = MDRaisedButton(
            text='Editar perfil',
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            on_release=self.toggle_edit,
            elevation=0,
            md_bg_color=(0.29, 0.69, 0.31, 1),  # Verde #4CAF50
            text_color=(1, 1, 1, 1)
        )
        layout.add_widget(edit_profile_button)

        # Campos de información
        self.name_field = MDTextField(
            hint_text='Nombre completo',
            text='María González',  # Placeholder, integrar con app.user_name
            disabled=True,
            size_hint_x=1,
            font_size='16sp'
        )
        layout.add_widget(self.name_field)

        self.email_field = MDTextField(
            hint_text='Correo electrónico',
            text='maria@email.com',  # Placeholder, integrar con app.user_email
            disabled=True,
            size_hint_x=1,
            font_size='16sp'
        )
        layout.add_widget(self.email_field)

        self.city_field = MDTextField(
            hint_text='Ciudad / Región',
            text='Temuco, Chile',
            disabled=True,
            size_hint_x=1,
            font_size='16sp'
        )
        layout.add_widget(self.city_field)

        self.phone_field = MDTextField(
            hint_text='Teléfono (opcional)',
            text='+56 9 1234 5678',
            disabled=True,
            size_hint_x=1,
            font_size='16sp'
        )
        layout.add_widget(self.phone_field)

        self.reg_date_label = MDLabel(
            text='Fecha de registro: 01/01/2023',
            halign='center',
            theme_text_color='Primary'
        )
        layout.add_widget(self.reg_date_label)

        # Tipo de cuenta
        self.account_type_label = MDLabel(
            text='Cuenta: Gratuita',
            halign='center',
            theme_text_color='Primary'
        )
        layout.add_widget(self.account_type_label)

        # Botón guardar (oculto inicialmente)
        self.save_button = MDRaisedButton(
            text='Guardar cambios',
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            on_release=self.save_profile,
            opacity=0,  # Oculto
            elevation=0,
            md_bg_color=(0.29, 0.69, 0.31, 1),  # Verde #4CAF50
            text_color=(1, 1, 1, 1)
        )
        layout.add_widget(self.save_button)



        self.add_widget(layout)

        self.edit_mode = False
        self.user_data_file = 'user_data.json'
        self.load_user_data()

    def open_nav_drawer(self):
        """Abre el menú lateral."""
        # Navegar al menú principal donde está el nav_drawer
        if self.manager:
            self.manager.current = 'principal'
            # Una vez en principal, abrir el drawer
            try:
                principal_screen = self.manager.get_screen('principal')
                principal_screen.nav_drawer.set_state('open')
            except Exception:
                pass

    def select_photo(self, instance):
        """Abre el file manager para seleccionar foto."""
        self.file_manager.show(os.path.expanduser('~'))

    def exit_manager(self, *args):
        """Cierra el file manager."""
        self.file_manager.close()

    def select_path(self, path):
        """Selecciona la ruta de la imagen."""
        self.avatar.source = path
        self.exit_manager()

    def toggle_edit(self, instance):
        """Activa o desactiva el modo edición."""
        self.edit_mode = not self.edit_mode
        self.name_field.disabled = not self.edit_mode
        self.email_field.disabled = not self.edit_mode
        self.city_field.disabled = not self.edit_mode
        self.phone_field.disabled = not self.edit_mode
        self.save_button.opacity = 1 if self.edit_mode else 0

    def load_user_data(self):
        """Carga los datos del usuario desde JSON."""
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, 'r') as f:
                data = json.load(f)
                self.name_field.text = data.get('nombre', '')
                self.email_field.text = data.get('email', '')
                self.city_field.text = data.get('ciudad', '')
                self.phone_field.text = data.get('telefono', '')
                self.reg_date_label.text = f'Fecha de registro: {data.get("fecha_registro", "")}'
                self.account_type_label.text = f'Cuenta: {data.get("cuenta", "")}'
                if data.get('foto'):
                    self.avatar.source = data['foto']

    def save_profile(self, instance):
        """Guarda los cambios del perfil en JSON."""
        data = {
            'nombre': self.name_field.text,
            'email': self.email_field.text,
            'ciudad': self.city_field.text,
            'telefono': self.phone_field.text,
            'fecha_registro': '01/01/2023',  # Mantener fijo o actualizar
            'cuenta': 'Gratuita',
            'foto': self.avatar.source if self.avatar.source else ''
        }
        with open(self.user_data_file, 'w') as f:
            json.dump(data, f, indent=4)
        show_snackbar("✅ Datos guardados correctamente")
        self.toggle_edit(None)  # Salir del modo edición

    def go_back(self):
        """Vuelve a la pantalla anterior."""
        if self.manager:
            self.manager.current = 'principal'
