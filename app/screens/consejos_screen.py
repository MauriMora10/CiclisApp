from kivy.metrics import dp
from kivy.animation import Animation
import random
import webbrowser

from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDRectangleFlatIconButton
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

# --- Consejos aleatorios ---
CONSEJOS = [
    "Usa casco siempre que salgas a pedalear.",
    "Respeta las señales de tránsito y cruces peatonales.",
    "Mantén tu bicicleta en buen estado.",
    "Usa luces y reflectantes de noche.",
    "Evita usar el celular mientras conduces.",
    "Planifica tu ruta antes de salir.",
]


class ConsejosScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "consejos"

        app = App.get_running_app()
        app.theme_cls.bind(theme_style=self.on_theme_change)

        # === Layout principal ===
        root = MDBoxLayout(orientation="vertical")
        scroll = MDScrollView(do_scroll_x=False)

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(22),
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))

        # ==============================
        # SECCIÓN PRINCIPAL: CONSEJO
        # ==============================
        self.consejo_card = MDCard(
            orientation="vertical",
            padding=(dp(24), dp(20)),
            spacing=dp(14),
            radius=[18, 18, 18, 18],
            elevation=2,
            size_hint=(0.95, None),
            adaptive_height=True,
            pos_hint={"center_x": 0.5},
            md_bg_color=app.theme_cls.bg_normal,
        )

        inner_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            adaptive_height=True,
        )

        inner_box.add_widget(
            MDLabel(
                text="Consejo de Seguridad",
                font_style="H5",
                halign="center",
                theme_text_color="Primary",
            )
        )

        self.label_consejo = MDLabel(
            text=random.choice(CONSEJOS),
            halign="center",
            font_style="Body1",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(40),
        )
        inner_box.add_widget(self.label_consejo)

        # Separador dinámico
        self.divider = Widget(size_hint_y=None, height=dp(1))
        with self.divider.canvas.before:
            self.divider_color = Color(rgba=app.theme_cls.divider_color)
            self.divider_rect = Rectangle(size=self.divider.size, pos=self.divider.pos)
        self.divider.bind(pos=self._update_divider, size=self._update_divider)
        inner_box.add_widget(self.divider)

        # Botón nuevo consejo
        self.btn_nuevo = MDRectangleFlatIconButton(
            text="Nuevo consejo",
            icon="refresh",
            size_hint=(None, None),
            size=(dp(180), dp(44)),
            pos_hint={"center_x": 0.5},
            on_release=self.nuevo_consejo,
            theme_text_color="Custom",
        )
        inner_box.add_widget(self.btn_nuevo)

        self.consejo_card.add_widget(inner_box)
        content.add_widget(self.consejo_card)

        # ==============================
        # SECCIÓN: NOTICIAS
        # ==============================
        content.add_widget(
            MDLabel(
                text="Noticias y Leyes del Ciclismo",
                font_style="H6",
                halign="left",
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(32),
            )
        )

        noticias = [
            {
                "titulo": "Ley de Convivencia Vial",
                "desc": "Cómo protege a los ciclistas en la vía pública.",
                "link": "https://www.mtt.gob.cl/leydeconvivenciavial",
                "icon": "gavel",
            },
            {
                "titulo": "Consejos MTT para ciclistas",
                "desc": "Recomendaciones del Ministerio de Transportes.",
                "link": "https://www.mtt.gob.cl/seguridadvial/ciclistas",
                "icon": "bike",
            },
            {
                "titulo": "Infraestructura ciclista - Noticias",
                "desc": "Actualizaciones de ciclovías y proyectos locales.",
                "link": "https://www.latercera.com/",
                "icon": "newspaper",
            },
        ]

        self.news_cards = []

        for item in noticias:
            card = MDCard(
                orientation="horizontal",
                padding=(dp(14), dp(10)),
                spacing=dp(10),
                size_hint=(0.95, None),
                height=dp(86),
                radius=[14, 14, 14, 14],
                elevation=2,
                pos_hint={"center_x": 0.5},
                md_bg_color=app.theme_cls.bg_normal,
            )

            text_box = MDBoxLayout(
                orientation="vertical",
                spacing=dp(4),
            )
            text_box.add_widget(
                MDLabel(
                    text=item["titulo"],
                    font_style="Subtitle1",
                    theme_text_color="Primary",
                )
            )

            text_box.add_widget(
                MDLabel(
                    text=item["desc"],
                    font_style="Caption",
                    theme_text_color="Secondary",
                )
            )

            icon_btn = MDIconButton(
                icon=item["icon"],
                pos_hint={"center_y": 0.5},
                theme_text_color="Primary",
                on_release=lambda inst, url=item["link"]: webbrowser.open(url),
            )

            card.add_widget(text_box)
            card.add_widget(icon_btn)

            self.news_cards.append(card)
            content.add_widget(card)

        # Botón final
        self.btn_not = MDRaisedButton(
            text="Ver más noticias",
            size_hint=(None, None),
            size=(dp(180), dp(44)),
            pos_hint={"center_x": 0.5},
            elevation=2,
            on_release=lambda x: webbrowser.open("https://www.mtt.gob.cl"),
        )
        content.add_widget(self.btn_not)

        content.add_widget(MDBoxLayout(size_hint_y=None, height=dp(24)))

        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)

        self.apply_theme()

    # ==============
    # CAMBIO DE CONSEJO
    # ==============
    def nuevo_consejo(self, instance):
        new_text = random.choice(CONSEJOS)
        anim = Animation(opacity=0, d=0.15)

        def set_text(*args):
            self.label_consejo.text = new_text

        def fade_in(*args):
            Animation(opacity=1, d=0.25).start(self.label_consejo)

        anim.bind(on_complete=lambda *a: (set_text(), fade_in()))
        anim.start(self.label_consejo)

    # ============
    # THEME APPLY
    # ============
    def apply_theme(self):
        app = App.get_running_app()

        # Card principal
        self.consejo_card.md_bg_color = app.theme_cls.bg_normal

        # Divider dinámico
        self.divider_color.rgba = app.theme_cls.divider_color

        # Botón nuevo consejo
        self.btn_nuevo.md_bg_color = app.theme_cls.primary_color
        self.btn_nuevo.text_color = app.theme_cls.opposite_text_color
        self.btn_nuevo.icon_color = app.theme_cls.opposite_text_color

        # Noticias
        for c in self.news_cards:
            c.md_bg_color = app.theme_cls.bg_normal

        # Botón final
        self.btn_not.md_bg_color = app.theme_cls.primary_color
        self.btn_not.text_color = app.theme_cls.opposite_text_color

    # ============
    # THEME CHANGE
    # ============
    def on_theme_change(self, *args):
        self.apply_theme()

    def _update_divider(self, instance, value):
        self.divider_rect.size = self.divider.size
        self.divider_rect.pos = self.divider.pos
