from kivy.metrics import dp
from kivy.animation import Animation
import webbrowser
from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.scrollview import MDScrollView


# -------------------------------------------------------
# CONSEJOS (texto + imagen con nombres REALES)
# -------------------------------------------------------
CONSEJOS = [
    ("Usa casco siempre que salgas a pedalear.", "casco.png"),
    ("Mantén tu celular con batería suficiente.", "comunicacion.png"),
    ("Revisa frenos y luces antes de salir.", "revision.png"),
    ("Respeta las señales de tránsito.", "senales.png"),
    ("Usa ropa visible y reflectante.", "visibilidad.png"),
    ("Evita ciclovías en mal estado.", "vial.png"),
]


class ConsejosScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "consejos"

        app = App.get_running_app()

        root = MDBoxLayout(orientation="vertical")
        scroll = MDScrollView(do_scroll_x=False)

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(26),
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))

        # -------------------------------------------------------
        # CONSEJO DEL DÍA — MDCard + CARRUSEL
        # -------------------------------------------------------
        self.consejo_card = MDCard(
            orientation="vertical",
            padding=(dp(24), dp(20)),
            spacing=dp(18),
            radius=[24, 24, 24, 24],
            elevation=1,
            size_hint=(0.96, None),
            adaptive_height=True,
            pos_hint={"center_x": 0.5},
        )

        header_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            adaptive_height=True,
        )

        header_box.add_widget(
            MDIconButton(
                icon="shield-check",
                theme_text_color="Primary",
                icon_size=dp(36),
                pos_hint={"center_x": 0.5},
            )
        )

        header_box.add_widget(
            MDLabel(
                text="Consejo de Seguridad",
                font_style="H5",
                halign="center",
                theme_text_color="Primary",
            )
        )

        # -------------------------------------------------------
        # CARRUSEL
        # -------------------------------------------------------
        self.carousel = Carousel(direction="right", size_hint_y=None, height=dp(260))

        for texto, img in CONSEJOS:
            slide = MDBoxLayout(
                orientation="vertical",
                padding=dp(10),
                spacing=dp(10),
            )

            slide.add_widget(
                Image(
                    source=f"assets/consejos/{img}",
                    allow_stretch=True,
                    keep_ratio=True,
                    size_hint=(1, 0.75),
                )
            )

            slide.add_widget(
                MDLabel(
                    text=texto,
                    halign="center",
                    font_style="Body1",
                    theme_text_color="Primary",
                    size_hint_y=None,
                    height=dp(40),
                )
            )

            self.carousel.add_widget(slide)

        header_box.add_widget(self.carousel)

        # Botón cambiar consejo
        self.btn_nuevo = MDRaisedButton(
            text="Nuevo consejo",
            icon="refresh",
            size_hint=(None, None),
            size=(dp(180), dp(46)),
            elevation=1,
            pos_hint={"center_x": 0.5},
            on_release=self.nuevo_consejo,
        )

        header_box.add_widget(self.btn_nuevo)
        self.consejo_card.add_widget(header_box)
        content.add_widget(self.consejo_card)

        # -------------------------------------------------------
        # SECCIÓN NOTICIAS
        # -------------------------------------------------------
        content.add_widget(
            MDLabel(
                text="Noticias y Leyes del Ciclismo",
                font_style="H6",
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(32),
            )
        )

        noticias = [
            {
                "titulo": "Ley de Convivencia Vial",
                "desc": "Cómo protege a los ciclistas en la vía pública.",
                "link": "https://www.conaset.cl/ciclistas/",
                "icon": "gavel",
            },
            {
                "titulo": "Consejos MTT para ciclistas",
                "desc": "Recomendaciones del Ministerio de Transportes.",
                "link": "https://www.conaset.cl/ciclistas-decretos/",
                "icon": "bike",
            },
            {
                "titulo": "Infraestructura ciclista - Noticias",
                "desc": "Actualizaciones de ciclovías y proyectos locales.",
                "link": "https://www.conaset.cl/condiciones-de-gestion-y-seguridad-de-transito-de-las-ciclovias/",
                "icon": "newspaper",
            },
        ]

        for item in noticias:
            card = MDCard(
                orientation="horizontal",
                padding=(dp(16), dp(12)),
                spacing=dp(14),
                size_hint=(0.96, None),
                height=dp(86),
                radius=[22, 22, 22, 22],
                elevation=1,
                pos_hint={"center_x": 0.5},
            )

            text_box = MDBoxLayout(orientation="vertical", spacing=dp(3))
            text_box.add_widget(
                MDLabel(
                    text=item["titulo"],
                    theme_text_color="Primary",
                    font_style="Subtitle1",
                )
            )
            text_box.add_widget(
                MDLabel(
                    text=item["desc"],
                    theme_text_color="Secondary",
                    font_style="Caption",
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
            content.add_widget(card)

        # ESPACIO FINAL
        content.add_widget(MDBoxLayout(size_hint_y=None, height=dp(30)))

        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)

    # -------------------------------------------------------
    # NUEVO CONSEJO — Carrusel funcional con animación
    # -------------------------------------------------------
    def nuevo_consejo(self, instance):
        fade_out = Animation(opacity=0, d=0.15)
        fade_in = Animation(opacity=1, d=0.25)

        def next_slide(*args):
            self.carousel.load_next(mode="next")
            fade_in.start(self.carousel)

        fade_out.bind(on_complete=next_slide)
        fade_out.start(self.carousel)
