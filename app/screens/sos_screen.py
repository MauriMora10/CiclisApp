from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from app.utils.ui import show_snackbar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
import webbrowser
import os
import json
import re

# Intentar usar MDIconButton si está disponible; si no, usaremos MDLabel como fallback
try:
    from kivymd.uix.button import MDIconButton
except Exception:
    MDIconButton = None

# Número familiar por defecto
FAMILIAR = "+56912345678"


class SOSScreen(MDScreen):
    """Pantalla SOS con llamada de emergencia y contacto familiar.

    Funcionalidades:
    - Llamar al 131 con confirmación (intenta abrir marcador via tel:)
    - Copiar número familiar al portapapeles
    - Guardar/leer número de contacto personalizado en `contacto_emergencia.json`
    """

    RED = (211/255, 47/255, 47/255, 1)
    ORANGE = (1.0, 167/255, 38/255, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'sos'
        # Layout principal centrado
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12))

        # Card centrada con ancho reducido
        card = MDCard(orientation='vertical', padding=dp(16), radius=[16, 16, 16, 16], elevation=0, size_hint=(0.95, None), height=dp(420))
        card_box = MDBoxLayout(orientation='vertical', spacing=dp(12), padding=(dp(12), dp(8)))

        # Icono grande SOS: preferir MDIconButton si está disponible
        if MDIconButton:
            try:
                icon = MDIconButton(icon='alert', user_font_size=dp(56), pos_hint={'center_x': 0.5}, md_bg_color=(0,0,0,0))
            except Exception:
                icon = MDLabel(text='🚨', font_size=dp(56), halign='center')
        else:
            icon = MDLabel(text='🚨', font_size=dp(56), halign='center')
        title = MDLabel(text='Emergencia', font_style='H5', halign='center')
        subtitle = MDLabel(text='Accesos rápidos', halign='center', theme_text_color='Secondary')
        card_box.add_widget(icon)
        card_box.add_widget(title)
        card_box.add_widget(subtitle)

        # Contenedor de botones grandes (vertical)
        botones_box = MDBoxLayout(orientation='vertical', spacing=dp(12), size_hint_y=None)

        self.btn_llamar = MDRaisedButton(text='Llamar al 131', md_bg_color=self.RED, size_hint=(1, None), height=dp(64), on_release=lambda x: self.confirmar_llamada('131'))
        self.btn_llamar.md_bg_color = self.RED
        botones_box.add_widget(self.btn_llamar)

        self.btn_copiar_familiar = MDRaisedButton(text='Copiar número familiar', md_bg_color=self.ORANGE, size_hint=(1, None), height=dp(56), on_release=self.copiar_familiar)
        botones_box.add_widget(self.btn_copiar_familiar)

        card_box.add_widget(botones_box)

        # Campo para número de contacto personal
        self.contact_field = MDTextField(hint_text='Número de contacto de emergencia', helper_text='Formato: +569XXXXXXXX', helper_text_mode='on_focus', size_hint_x=1)
        card_box.add_widget(self.contact_field)

        # Botones para guardar y copiar contacto guardado (en línea)
        actions = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(48))
        btn_guardar = MDRaisedButton(text='Guardar', size_hint_x=0.5, on_release=self.guardar_contacto)
        btn_copiar_guardado = MDRaisedButton(text='Copiar guardado', size_hint_x=0.5, on_release=self.copiar_contacto_guardado)
        actions.add_widget(btn_guardar)
        actions.add_widget(btn_copiar_guardado)
        card_box.add_widget(actions)

        card.add_widget(card_box)
        layout.add_widget(card)
        self.add_widget(layout)

        # Cargar contacto si existe
        self.cargar_contacto()

    def show_snackbar(self, mensaje: str):
        """Helper: muestra un MDSnackbar con un MDLabel interno."""
        # Delegar al helper centralizado
        try:
            show_snackbar(mensaje)
        except Exception:
            # Silenciar si algo falla aquí
            pass

    def get_storage_path(self):
        app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        return os.path.join(app_root, 'contacto_emergencia.json')

    def cargar_contacto(self):
        path = self.get_storage_path()
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                numero = data.get('contacto', '')
                if numero:
                    self.contact_field.text = numero
            except Exception:
                # No mostrar error intrusivo; dejar campo vacío
                pass

    def guardar_contacto(self, instance):
        numero = (self.contact_field.text or '').strip()
        if not numero:
            self.show_snackbar('Ingrese un número antes de guardar')
            return
        # Validar formato del número (acepta + y entre 7 y 15 dígitos)
        if not self.validar_numero(numero):
            self.show_snackbar('Número inválido. Use formato +569XXXXXXXX o solo dígitos (7-15 cifras)')
            return
        path = self.get_storage_path()
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({'contacto': numero}, f, ensure_ascii=False, indent=2)
            self.show_snackbar('Contacto guardado')
        except Exception as e:
            self.show_snackbar(f'Error guardando contacto: {e}')

    def copiar_contacto_guardado(self, instance):
        numero = (self.contact_field.text or '').strip()
        if not numero:
            self.show_snackbar('No hay contacto guardado para copiar')
            return
        if not self.validar_numero(numero):
            self.show_snackbar('El contacto guardado tiene formato inválido')
            return
        Clipboard.copy(numero)
        self.show_snackbar('Número de contacto copiado al portapapeles')

    def validar_numero(self, numero: str) -> bool:
        """Valida que el número tenga entre 7 y 15 dígitos, opcionalmente con prefijo +."""
        if not numero:
            return False
        # Eliminar espacios y guiones
        n = re.sub(r"[\s\-]", "", numero)
        # Coincidir + opcional seguido de 7-15 dígitos
        return bool(re.fullmatch(r"\+?\d{7,15}", n))

    def copiar_familiar(self, instance):
        Clipboard.copy(FAMILIAR)
        self.show_snackbar('Número de emergencia copiado al portapapeles')

    def confirmar_llamada(self, numero):
        # Mostrar diálogo de confirmación antes de intentar abrir el marcador
        def _cancel(instance):
            dialog.dismiss()

        def _call(instance):
            dialog.dismiss()
            self.realizar_llamada(numero)

        dialog = MDDialog(title='Confirmar llamada', text=f'¿Deseas llamar a emergencias ({numero})?', size_hint=(0.8, None), height=dp(180), buttons=[MDFlatButton(text='Cancelar', on_release=_cancel), MDRaisedButton(text='Llamar', on_release=_call)])
        dialog.open()

    def realizar_llamada(self, numero):
        # Intentamos abrir el marcador; en escritorio esto puede no funcionar, en Android debería abrir la app de teléfono
        try:
            url = f'tel:{numero}'
            webbrowser.open(url)
            self.show_snackbar('Abriendo marcador...')
        except Exception as e:
            self.show_snackbar(f'No se pudo iniciar la llamada: {e}')
