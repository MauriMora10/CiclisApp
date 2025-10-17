from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
import webbrowser

class PantallaMapa(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'mapa'

        # Layout principal
        self.layout = MDBoxLayout(orientation="vertical")

        # Barra superior (sin botón de regresar)
        self.toolbar = MDTopAppBar(
            title="Mapa de Zonas Seguras",
            elevation=0
        )
        self.layout.add_widget(self.toolbar)

        # Scroll para contenido
        scroll = MDScrollView()

        # Contenedor vertical dentro del scroll
        content = MDBoxLayout(orientation="vertical", padding=dp(16), spacing=dp(16), size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))

        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            radius=[20, 20, 20, 20],
            elevation=0,
            size_hint=(1, None),
            adaptive_height=True
        )

        card_content = MDBoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None)
        card_content.bind(minimum_height=card_content.setter("height"))

        card_content.add_widget(MDLabel(
            text="Mapa de Ciclovías Temuco",
            font_style="H6",
            halign="center",
            theme_text_color="Primary"
        ))

        card_content.add_widget(Image(
            source="c:/Users/Mauricio/Desktop/mapa_ciclovias_temuco.png.png",
            allow_stretch=True,
            keep_ratio=True,
            size_hint_y=None,
            height=dp(300)
        ))

        card_content.add_widget(MDRaisedButton(
            text="Abrir mapa interactivo",
            md_bg_color=(0.2, 0.6, 1, 1),
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(dp(200), dp(40)),
            on_release=lambda x: webbrowser.open("https://bicivias.cl/temuco/")
        ))

        card.add_widget(card_content)
        content.add_widget(card)
        scroll.add_widget(content)
        self.layout.add_widget(scroll)
        self.add_widget(self.layout)

    # El método de regreso se eliminó porque la pantalla no muestra el botón de volver
