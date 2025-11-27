from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.fitimage import FitImage
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout

from app.utils.ui import show_snackbar

import json
import os


class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "profile"

        # Layout principal
        main_layout = MDBoxLayout(orientation="vertical")

        # Toolbar superior
        self.toolbar = MDTopAppBar(
            title="Mi Perfil",
            elevation=0,
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            md_bg_color=(0.2, 0.6, 0.3, 1),
        )
        main_layout.add_widget(self.toolbar)

        # ScrollView para contenido
        scroll = MDScrollView(do_scroll_x=False)
        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(16),
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))

        # ============================================================
        # TARJETA DE FOTO DE PERFIL
        # ============================================================
        avatar_card = MDCard(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(16),
            radius=[dp(16), dp(16), dp(16), dp(16)],
            elevation=1,
            size_hint=(1, None),
            adaptive_height=True,
            pos_hint={"center_x": 0.5},
        )

        # Título de la sección
        avatar_card.add_widget(
            MDLabel(
                text="Foto de Perfil",
                font_style="H6",
                halign="center",
                theme_text_color="Primary",
            )
        )

        # Contenedor para avatar
        avatar_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(16),
            size_hint_y=None,
            adaptive_height=True,
        )

        # Avatar centrado
        avatar_box = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(120),
            spacing=dp(8),
        )

        self.avatar = FitImage(
            source="",
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            radius=[dp(50)],
            pos_hint={"center_x": 0.5},
        )
        avatar_box.add_widget(self.avatar)

        # Botón de cambiar foto
        change_photo_btn = MDRaisedButton(
            text="Cambiar Foto",
            icon="camera",
            md_bg_color=(0.2, 0.6, 0.3, 1),
            size_hint=(None, None),
            size=(dp(140), dp(36)),
            elevation=1,
            pos_hint={"center_x": 0.5},
            on_release=self.select_photo,
        )
        avatar_box.add_widget(change_photo_btn)

        avatar_container.add_widget(avatar_box)
        avatar_card.add_widget(avatar_container)
        content.add_widget(avatar_card)

        # ============================================================
        # TARJETA DE INFORMACIÓN PERSONAL
        # ============================================================
        info_card = MDCard(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(16),
            radius=[dp(16), dp(16), dp(16), dp(16)],
            elevation=1,
            size_hint=(1, None),
            adaptive_height=True,
            pos_hint={"center_x": 0.5},
        )

        # Título de la sección
        info_card.add_widget(
            MDLabel(
                text="Información Personal",
                font_style="H6",
                halign="center",
                theme_text_color="Primary",
            )
        )

        # Campos de información
        self.name_field = MDTextField(
            hint_text="Nombre completo",
            mode="rectangle",
            disabled=True,
        )
        info_card.add_widget(self.name_field)

        self.email_field = MDTextField(
            hint_text="Correo electrónico",
            mode="rectangle",
            disabled=True,
        )
        info_card.add_widget(self.email_field)

        self.city_field = MDTextField(
            hint_text="Ciudad / Región",
            mode="rectangle",
            disabled=True,
        )
        info_card.add_widget(self.city_field)

        self.phone_field = MDTextField(
            hint_text="Teléfono",
            mode="rectangle",
            disabled=True,
        )
        info_card.add_widget(self.phone_field)

        # Información adicional
        self.reg_date_label = MDLabel(
            text="Fecha de registro: --",
            halign="left",
            theme_text_color="Secondary",
            font_style="Caption",
        )
        info_card.add_widget(self.reg_date_label)

        self.account_type_label = MDLabel(
            text="Cuenta: --",
            halign="left",
            theme_text_color="Secondary",
            font_style="Caption",
        )
        info_card.add_widget(self.account_type_label)

        content.add_widget(info_card)

        # ============================================================
        # BOTONES DE ACCIÓN
        # ============================================================
        actions_card = MDCard(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(12),
            radius=[dp(16), dp(16), dp(16), dp(16)],
            elevation=1,
            size_hint=(1, None),
            height=dp(120),
            pos_hint={"center_x": 0.5},
        )

        self.edit_button = MDRaisedButton(
            text="Editar Perfil",
            md_bg_color=(0.2, 0.6, 0.3, 1),
            size_hint=(1, None),
            height=dp(44),
            elevation=1,
            on_release=self.toggle_edit,
        )
        actions_card.add_widget(self.edit_button)

        self.save_button = MDRaisedButton(
            text="Guardar Cambios",
            md_bg_color=(0.2, 0.6, 0.3, 1),
            size_hint=(1, None),
            height=dp(44),
            elevation=1,
            disabled=True,
            opacity=0,
            on_release=self.save_profile,
        )
        actions_card.add_widget(self.save_button)

        content.add_widget(actions_card)

        # Espacio final
        content.add_widget(MDBoxLayout(size_hint_y=None, height=dp(20)))

        scroll.add_widget(content)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

        # Sistema archivos
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=[".png", ".jpg", ".jpeg"]
        )

        self.user_data_file = "user_data.json"
        self.edit_mode = False
        self.load_user_data()

    # =======================================================================
    # NAVEGACIÓN
    # =======================================================================
    def go_back(self):
        self.manager.current = "principal"

    # =======================================================================
    # FOTO
    # =======================================================================
    def select_photo(self, instance):
        self.file_manager.show(os.path.expanduser("~"))

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.avatar.source = path
        self.exit_manager()

    # =======================================================================
    # EDICIÓN / GUARDADO
    # =======================================================================
    def toggle_edit(self, instance):
        self.edit_mode = not self.edit_mode
        for field in (self.name_field, self.email_field, self.city_field, self.phone_field):
            field.disabled = not self.edit_mode

        self.save_button.disabled = not self.edit_mode
        self.save_button.opacity = 1 if self.edit_mode else 0

    def load_user_data(self):
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, "r") as f:
                data = json.load(f)
                self.name_field.text = data.get("nombre", "")
                self.email_field.text = data.get("email", "")
                self.city_field.text = data.get("ciudad", "")
                self.phone_field.text = data.get("telefono", "")
                self.reg_date_label.text = f"Fecha de registro: {data.get('fecha_registro', '--')}"
                self.account_type_label.text = f"Cuenta: {data.get('cuenta', '--')}"
                if data.get("foto"):
                    self.avatar.source = data["foto"]

    def save_profile(self, instance):
        data = {
            "nombre": self.name_field.text,
            "email": self.email_field.text,
            "ciudad": self.city_field.text,
            "telefono": self.phone_field.text,
            "foto": self.avatar.source,
        }

        with open(self.user_data_file, "w") as f:
            json.dump(data, f, indent=4)

        show_snackbar("✔ Perfil actualizado correctamente")
        self.toggle_edit(None)

