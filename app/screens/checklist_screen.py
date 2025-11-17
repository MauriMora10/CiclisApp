from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.button import MDIconButton
from kivymd.uix.scrollview import MDScrollView

from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.app import App

try:
    from plyer import vibrator
except:
    vibrator = None


ITEMS = [
    ("Casco puesto", "shield-check"),
    ("Luces encendidas", "lightbulb-on"),
    ("Frenos en buen estado", "bike"),
    ("Presión de neumáticos correcta", "car-tire-alert"),
]


class ChecklistScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "checklist"

        # ============= TEMA DINÁMICO =============
        app = App.get_running_app()
        app.theme_cls.bind(theme_style=self.on_theme_change)

        self.store = JsonStore("checklist_data.json")

        # Fondo dinámico según tema
        self.update_background()

        # ----------- SCROLLVIEW (contenido completo) -----------
        scroll = MDScrollView(size_hint=(1, 1))

        container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=[dp(20), dp(20), dp(20), dp(40)],
            size_hint_y=None,
            adaptive_height=True,
        )

        # ----------- CARD PRINCIPAL -----------
        self.card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(20),
            radius=[28, 28, 28, 28],
            elevation=3,
            size_hint=(1, None),
            adaptive_height=True
        )
        self.update_card_color()

        # TÍTULO
        title = MDLabel(
            text="Checklist de Seguridad",
            font_style="H5",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(40),
        )
        self.card.add_widget(title)

        # ----------- ITEMS LISTA -----------
        self.items_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(18),
            adaptive_height=True
        )

        self.checkboxes = []

        for text, icon in ITEMS:

            row = MDBoxLayout(
                orientation="horizontal",
                spacing=dp(12),
                size_hint_y=None,
                height=dp(48),
            )

            checkbox = MDCheckbox(size_hint=(None, None), size=(dp(28), dp(28)))
            checkbox.bind(active=self.on_checkbox_active)
            self.checkboxes.append(checkbox)

            icon_widget = MDIconButton(
                icon=icon,
                icon_size=dp(26),
                theme_text_color="Custom",
                text_color=get_color_from_hex("#43A047"),
            )

            label = MDLabel(
                text=text,
                font_style="Body1",
                theme_text_color="Primary",
                halign="left"
            )

            row.add_widget(checkbox)
            row.add_widget(icon_widget)
            row.add_widget(label)

            self.items_layout.add_widget(row)

        self.card.add_widget(self.items_layout)

        # ----------- PROGRESO -----------

        self.progress_label = MDLabel(
            text="Progreso: 0%",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20),
        )
        self.card.add_widget(self.progress_label)

        self.progress_bar = MDProgressBar(
            value=0,
            max=100,
            color=get_color_from_hex("#43A047"),
            size_hint_y=None,
            height=dp(8)
        )
        self.card.add_widget(self.progress_bar)

        # ----------- BOTONES -----------
        buttons_row = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(52),
        )

        self.btn_revisar = MDRaisedButton(
            text="Revisar",
            size_hint=(1, 1),
            md_bg_color=app.theme_cls.primary_color,
            on_release=self.revisar,
        )

        self.btn_toggle = MDFlatButton(
            text="Seleccionar todo",
            size_hint=(1, 1),
            text_color=get_color_from_hex("#1E88E5"),
            on_release=self.toggle_all,
        )

        buttons_row.add_widget(self.btn_revisar)
        buttons_row.add_widget(self.btn_toggle)

        self.card.add_widget(buttons_row)

        container.add_widget(self.card)
        scroll.add_widget(container)
        self.add_widget(scroll)

        # Cargar estado guardado
        Clock.schedule_once(lambda dt: self.cargar_estado())

    # =========================================================
    # ----------- TEMA DINÁMICO (LIGHT/DARK) -----------------
    # =========================================================
    def update_background(self):
        app = App.get_running_app()
        if app.theme_cls.theme_style == "Dark":
            self.md_bg_color = (0.05, 0.05, 0.05, 1)  # negro puro suave
        else:
            self.md_bg_color = get_color_from_hex("#E8FDE8")

    def update_card_color(self):
        app = App.get_running_app()
        if app.theme_cls.theme_style == "Dark":
            self.card.md_bg_color = (0.15, 0.15, 0.15, 1)  # gris oscuro Material 3
        else:
            self.card.md_bg_color = (1, 1, 1, 1)

    def on_theme_change(self, *args):
        self.update_background()
        self.update_card_color()

        # Ajustar botón según tema
        app = App.get_running_app()
        self.btn_revisar.md_bg_color = app.theme_cls.primary_color

        # refrescar colores de labels dinámicamente
        for child in self.walk():
            if isinstance(child, MDLabel):
                if child.theme_text_color == "Primary":
                    child.text_color = (1, 1, 1, 0.87) if app.theme_cls.theme_style == "Dark" else (0.1, 0.1, 0.1, 1)
                elif child.theme_text_color == "Secondary":
                    child.text_color = (1, 1, 1, 0.6) if app.theme_cls.theme_style == "Dark" else (0.4, 0.4, 0.4, 1)

    # =========================================================
    # ------------------- LÓGICA CHECKLIST --------------------
    # =========================================================

    def on_checkbox_active(self, *args):
        self.actualizar_progreso()
        self.guardar_estado()

    def guardar_estado(self):
        self.store.put("checklist", **{str(i): cb.active for i, cb in enumerate(self.checkboxes)})

    def cargar_estado(self):
        if self.store.exists("checklist"):
            data = self.store.get("checklist")
            for i, cb in enumerate(self.checkboxes):
                cb.active = data.get(str(i), False)
        self.actualizar_progreso()

    def toggle_all(self, *args):
        all_checked = all(cb.active for cb in self.checkboxes)
        for cb in self.checkboxes:
            cb.active = not all_checked

        self.btn_toggle.text = "Deseleccionar todo" if not all_checked else "Seleccionar todo"

        self.actualizar_progreso()
        self.guardar_estado()

    def actualizar_progreso(self):
        total = len(self.checkboxes)
        done = sum(cb.active for cb in self.checkboxes)
        pct = int((done / total) * 100)

        self.progress_label.text = f"Progreso: {pct}%"
        self.progress_bar.value = pct

        if pct == 100:
            Animation(md_bg_color=(0.8, 1, 0.8, 1), duration=0.3).start(self.card)
            if vibrator:
                try:
                    vibrator.vibrate(0.1)
                except:
                    pass

    def revisar(self, *args):
        from app.utils.ui import show_snackbar

        if all(cb.active for cb in self.checkboxes):
            show_snackbar("✨ ¡Checklist completado con éxito!")
        else:
            show_snackbar("⚠ Revisa los puntos pendientes")

        self.actualizar_progreso()
        self.guardar_estado()
