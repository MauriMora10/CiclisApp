from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from app.utils.ui import show_snackbar
from datetime import datetime
import os
import json
import platform
if platform.system() == 'Windows':
    import tkinter as tk
    from tkinter import filedialog

FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'reportes_peligro.json')


class ReportePeligro(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'reporte'

        from kivymd.uix.toolbar import MDTopAppBar

        # --- Layout principal ---
        layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(16),
            spacing=dp(12)
        )

        # Barra superior
        self.toolbar = MDTopAppBar(
            title='Reportar peligro',
            left_action_items=[['arrow-left', lambda x: self.volver_principal(x)]],
            elevation=1  # 🔽 sombra reducida
        )
        layout.add_widget(self.toolbar)

        # --- Tarjeta del formulario ---
        card = MDCard(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(16),
            radius=[12, 12, 12, 12],
            elevation=1,  # 🔽 sombra reducida
            pos_hint={'center_x': 0.5},
            size_hint_x=0.95
        )

        # Título
        title_label = MDLabel(
            text='Reportar peligro',
            font_style='H5',
            halign='center',
            theme_text_color='Primary'
        )
        card.add_widget(title_label)

        # Campo: Calle
        self.calle_field = MDTextField(
            hint_text='Calle o zona',
            mode='rectangle'
        )
        card.add_widget(self.calle_field)

        # Campo: Tipo de peligro
        self.tipo_field = MDTextField(
            hint_text='Tipo de peligro (ej: bache, ciclovía)',
            mode='rectangle'
        )
        card.add_widget(self.tipo_field)

        # Campo: Descripción
        self.desc_field = MDTextField(
            hint_text='Descripción (opcional)',
            mode='rectangle',
            multiline=True,
            max_text_length=300
        )
        card.add_widget(self.desc_field)

        # Etiqueta de imagen seleccionada
        self.imagen_label = MDLabel(
            text='Imagen: Ninguna seleccionada',
            halign='left',
            theme_text_color='Secondary',
            font_style='Caption'
        )
        card.add_widget(self.imagen_label)

        # Contenedor para botones de imagen
        image_buttons_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(40)
        )
        self.btn_view_image = MDRectangleFlatIconButton(
            text='Ver imagen',
            icon='eye',
            on_release=self.view_image,
            disabled=True
        )
        self.btn_delete_image = MDRectangleFlatIconButton(
            text='Eliminar',
            icon='delete',
            on_release=self.delete_image,
            disabled=True
        )
        image_buttons_layout.add_widget(self.btn_view_image)
        image_buttons_layout.add_widget(self.btn_delete_image)
        card.add_widget(image_buttons_layout)

        # Botón de selección de imagen
        btn_select_image = MDRectangleFlatIconButton(
            text='Seleccionar imagen',
            icon='image',
            pos_hint={'center_x': 0.5},
            md_bg_color=self.theme_cls.primary_color,
            text_color=(1, 1, 1, 1),
            theme_icon_color="Custom",
            icon_color=(1, 1, 1, 1),
            on_release=self.select_image
        )
        card.add_widget(btn_select_image)

        # Botón de envío
        btn_send = MDRaisedButton(
            text='Enviar reporte',
            pos_hint={'center_x': 0.5},
            elevation=1,  # 🔽 sombra reducida
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.enviar_reporte
        )
        card.add_widget(btn_send)

        layout.add_widget(card)
        self.add_widget(layout)

        self.selected_image_path = None

    # --- Volver a la pantalla principal ---
    def volver_principal(self, instance):
        if self.manager:
            self.manager.current = 'principal'

    # --- Enviar y guardar reporte ---
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
            'imagen': self.selected_image_path if self.selected_image_path else None,
            'fecha': datetime.now().isoformat()
        }

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

            dialog = MDDialog(
                title='Reporte guardado',
                text='Gracias. El reporte fue guardado localmente.'
            )
            dialog.open()

            # Recargar la lista de reportes en la pantalla lista_reportes
            if self.manager:
                lista_screen = self.manager.get_screen('lista_reportes')
                if lista_screen:
                    lista_screen.load_reportes()

            # Limpiar campos
            self.calle_field.text = ''
            self.tipo_field.text = ''
            self.desc_field.text = ''
            self.imagen_label.text = 'Imagen: Ninguna seleccionada'
            self.selected_image_path = None
            self.btn_view_image.disabled = True
            self.btn_delete_image.disabled = True

        except Exception as e:
            show_snackbar(f'Error guardando el reporte: {e}')

    # --- Seleccionar imagen ---
    def select_image(self, instance):
        if platform.system() == 'Windows':
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            file_path = filedialog.askopenfilename(
                title='Seleccionar imagen',
                filetypes=[('Archivos de imagen', '*.png *.jpg *.jpeg *.gif *.bmp')]
            )
            root.destroy()
            if file_path:
                self.selected_image_path = file_path
                self.imagen_label.text = f'Imagen: {os.path.basename(file_path)}'
                self.btn_view_image.disabled = False
                self.btn_delete_image.disabled = False
        else:
            show_snackbar('Esta funcionalidad solo está disponible en Windows')

    # --- Ver imagen ---
    def view_image(self, instance):
        if self.selected_image_path and os.path.exists(self.selected_image_path):
            if platform.system() == 'Windows':
                os.startfile(self.selected_image_path)
            else:
                show_snackbar('Esta funcionalidad solo está disponible en Windows')
        else:
            show_snackbar('No hay imagen seleccionada o el archivo no existe')

    # --- Eliminar imagen ---
    def delete_image(self, instance):
        if self.selected_image_path:
            self.selected_image_path = None
            self.imagen_label.text = 'Imagen: Ninguna seleccionada'
            self.btn_view_image.disabled = True
            self.btn_delete_image.disabled = True
            show_snackbar('Imagen eliminada')
        else:
            show_snackbar('No hay imagen seleccionada')

    # --- Listar reportes guardados ---
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

