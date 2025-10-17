from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from app.utils.ui import show_snackbar
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
import json
import os
from datetime import datetime

FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'reportes_peligro.json')

class ReportePeligro(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'reporte'
        from kivymd.uix.toolbar import MDTopAppBar

        layout = MDBoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))
        # Top bar con botón regresar
        self.toolbar = MDTopAppBar(title='Reportar peligro', left_action_items=[['arrow-left', lambda x: self.volver_principal(x)]])
        layout.add_widget(self.toolbar)
        # Card con formulario para reporte
        card = MDCard(orientation='vertical', padding=dp(12), radius=[12, 12, 12, 12], elevation=0)
        card.add_widget(MDLabel(text='Reportar peligro', font_style='H5', halign='center'))

        self.calle_field = MDTextField(hint_text='Nombre de la calle o zona', mode='rectangle')
        self.tipo_field = MDTextField(hint_text='Tipo de peligro (ej: bache, falta de ciclovía)', mode='rectangle')
        self.desc_field = MDTextField(hint_text='Descripción opcional', mode='rectangle')

        card.add_widget(self.calle_field)
        card.add_widget(self.tipo_field)
        card.add_widget(self.desc_field)

        btn_send = MDRaisedButton(text='Enviar reporte', pos_hint={'center_x': 0.5}, on_release=self.enviar_reporte)
        card.add_widget(btn_send)

        layout.add_widget(card)
        self.add_widget(layout)

    def volver_principal(self, instance):
        if self.manager:
            self.manager.current = 'principal'

    def enviar_reporte(self, instance):
        calle = self.calle_field.text.strip()
        tipo = self.tipo_field.text.strip()
        descripcion = self.desc_field.text.strip()
        if not calle or not tipo:
            show_snackbar('Completa los campos requeridos')
            return
        reporte = {
            'calle': calle,
            'tipo': tipo,
            'descripcion': descripcion,
            'fecha': datetime.now().isoformat()
        }
        # Guardar en JSON
        app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        file_path = os.path.join(app_root, 'reportes_peligro.json')
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
            else:
                data = []
            data.append(reporte)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            dialog = MDDialog(title='Reporte guardado', text='Gracias. El reporte fue guardado localmente.')
            dialog.open()
            # limpiar campos
            self.calle_field.text = ''
            self.tipo_field.text = ''
            self.desc_field.text = ''
        except Exception as e:
            show_snackbar(f'Error guardando el reporte: {e}')

    def listar_reportes(self):
        """Devuelve lista de reportes guardados (si existen)."""
        app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        file_path = os.path.join(app_root, 'reportes_peligro.json')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                except Exception:
                    return []
        return []
