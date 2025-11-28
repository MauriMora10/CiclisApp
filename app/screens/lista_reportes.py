from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivymd.uix.fitimage import FitImage
from kivy.metrics import dp
import json
import os


class ListaReportes(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "lista_reportes"

        # ------------------------------------------------------------
        # LAYOUT PRINCIPAL
        # ------------------------------------------------------------
        main = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=[0, 0, 0, 0],
        )

        # ------------------------------------------------------------
        # HEADER
        # ------------------------------------------------------------
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(85),
            md_bg_color=(0.2, 0.6, 0.3, 1),
            padding=[dp(10), dp(10)],
            radius=[0, 0, dp(28), dp(28)],
        )

        back = MDIconButton(
            icon="arrow-left",
            icon_color=(1, 1, 1, 1),
            on_release=lambda x: self.go_back(),
        )
        header.add_widget(back)

        header.add_widget(
            MDLabel(
                text="Reportes guardados",
                halign="left",
                font_style="H6",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                padding=[0, dp(22), 0, 0],
            )
        )
        main.add_widget(header)

        # ------------------------------------------------------------
        # SCROLL + CONTENEDOR
        # ------------------------------------------------------------
        scroll = MDScrollView()
        container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=[dp(16), dp(16)],
            size_hint_y=None,
        )
        container.bind(minimum_height=container.setter("height"))

        # ------------------------------------------------------------
        # CARD DE FILTRO
        # ------------------------------------------------------------
        filtros_card = MDCard(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10),
            radius=[dp(10)],
            elevation=1,
            size_hint=(1, None),
            adaptive_height=True,
            md_bg_color=(1, 1, 1, 1),
        )

        filtros_card.add_widget(
            MDLabel(
                text="Filtrar reportes",
                font_style="Body1",
                theme_text_color="Primary",
                halign="left",
            )
        )

        self.tipo_field = MDTextField(
            hint_text="Tipo de peligro",
            mode="rectangle",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(30),
        )
        filtros_card.add_widget(self.tipo_field)

        self.fecha_field = MDTextField(
            hint_text="Fecha (YYYY-MM-DD)",
            mode="rectangle",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(30),
        )
        filtros_card.add_widget(self.fecha_field)

        acciones = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(36),
        )

        acciones.add_widget(
            MDRaisedButton(
                text="Filtrar",
                md_bg_color=(0.2, 0.6, 0.3, 1),
                elevation=1,
                on_release=self.filtrar_reportes,
                size_hint_y=None,
                height=dp(32),
                font_style="Caption",
            )
        )

        acciones.add_widget(
            MDRaisedButton(
                text="Exportar",
                md_bg_color=(0.1, 0.4, 1, 1),
                elevation=1,
                on_release=self.exportar_reportes,
                size_hint_y=None,
                height=dp(32),
                font_style="Caption",
            )
        )

        acciones.add_widget(
            MDRaisedButton(
                text="Borrar",
                md_bg_color=(1, 0.2, 0.2, 1),
                elevation=1,
                on_release=self.borrar_filtros,
                size_hint_y=None,
                height=dp(32),
                font_style="Caption",
            )
        )

        filtros_card.add_widget(acciones)
        container.add_widget(filtros_card)

        # ------------------------------------------------------------
        # TITULO REPORTES
        # ------------------------------------------------------------
        container.add_widget(
            MDLabel(
                text="Reportes registrados",
                font_style="H6",
                theme_text_color="Primary",
                halign="left",
            )
        )

        # ------------------------------------------------------------
        # LISTA DE REPORTES (FUNCIONAL)
        # ------------------------------------------------------------
        self.reportes_list = MDList(
            spacing=dp(14),
            size_hint_y=None,
        )
        self.reportes_list.bind(minimum_height=self.reportes_list.setter("height"))

        container.add_widget(self.reportes_list)
        scroll.add_widget(container)
        main.add_widget(scroll)
        self.add_widget(main)

        # Cargar reportes al iniciar
        self.cargar_reportes()

    # ------------------------------------------------------------
    # CARGA DEL JSON (CORREGIDA)
    # ------------------------------------------------------------
    def cargar_reportes(self):
        self.reportes_list.clear_widgets()

        json_path = os.path.join(os.getcwd(), "app", "reportes_peligro.json")

        if not os.path.exists(json_path):
            print("⚠ No existe:", json_path)
            return

        with open(json_path, "r", encoding="utf-8") as f:
            datos = json.load(f)

        if not datos:
            print("⚠ JSON vacío")
            return

        for reporte in datos:
            card = self._crear_card_reporte(reporte)
            self.reportes_list.add_widget(card)

    # ------------------------------------------------------------
    # COMPATIBILIDAD — EVITA EL ERROR:
    # 'ListaReportes' object has no attribute 'load_reportes'
    # ------------------------------------------------------------
    def load_reportes(self):
        """Alias para compatibilidad con pantallas antiguas."""
        self.cargar_reportes()

    # ------------------------------------------------------------
    # CARD INDIVIDUAL (FUNCIONA + MUESTRA IMAGEN)
    # ------------------------------------------------------------
    def _crear_card_reporte(self, reporte):

        card = MDCard(
            elevation=1,
            radius=[dp(16)],
            padding=dp(16),
            size_hint_x=1,
            adaptive_height=True,
            md_bg_color=(1, 1, 1, 1),
        )

        row = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(100),
        )

        col = MDBoxLayout(
            orientation="vertical",
            spacing=dp(6),
            size_hint_x=0.7,
        )

        col.add_widget(
            MDLabel(
                text=f"{reporte.get('calle', 'Sin calle')} - {reporte.get('tipo', 'Sin tipo')}",
                font_style="Subtitle1",
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(22),
            )
        )

        col.add_widget(
            MDLabel(
                text=f"Fecha: {reporte.get('fecha', '--')}",
                font_style="Caption",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(18),
            )
        )

        col.add_widget(
            MDLabel(
                text=reporte.get("descripcion", "--"),
                font_style="Body2",
                theme_text_color="Secondary",
                shorten=True,
                max_lines=2,
            )
        )

        row.add_widget(col)

        # -------------------------
        # IMAGEN DEL REPORTE (FUNCIONAL)
        # -------------------------
        img_path = reporte.get("imagen", "")
        full_img_path = img_path if img_path else ""

        if img_path and os.path.exists(full_img_path):
            img_src = full_img_path
        else:
            img_src = "assets/icons/no_image.png"

        img = FitImage(
            source=img_src,
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            radius=[dp(12)],
        )

        row.add_widget(img)
        card.add_widget(row)

        return card

    # ------------------------------------------------------------
    # LOGICA ORIGINAL
    # ------------------------------------------------------------
    def filtrar_reportes(self, instance):
        pass

    def exportar_reportes(self, instance):
        pass

    def borrar_filtros(self, instance):
        self.tipo_field.text = ""
        self.fecha_field.text = ""
        self.cargar_reportes()

    def go_back(self):
        self.manager.current = "principal"