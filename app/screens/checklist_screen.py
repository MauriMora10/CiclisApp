from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.selectioncontrol import MDCheckbox
from app.utils.ui import show_snackbar
from kivy.metrics import dp

ITEMS = [
    ("Casco puesto", "bike-helmet"),
    ("Luces encendidas", "flashlight"),
    ("Frenos en buen estado", "car-brake-alert"),
    ("Presión de neumáticos correcta", "car-tire-alert"),
]


class ChecklistScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'checklist'

        layout = MDBoxLayout(orientation="vertical", padding=dp(24), spacing=dp(16))

        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            radius=[20, 20, 20, 20],
            md_bg_color=(0.9, 1, 0.9, 1),
            elevation=0,
        )

        card.add_widget(
            MDLabel(
                text="Checklist de Seguridad",
                font_style="H5",
                halign="center",
                theme_text_color="Primary",
            )
        )

        self.checkboxes = []
        for label, icon in ITEMS:
            row = MDBoxLayout(orientation="horizontal", spacing=dp(8))
            checkbox = MDCheckbox()
            self.checkboxes.append(checkbox)
            row.add_widget(checkbox)
            row.add_widget(
                MDLabel(
                    text=label,
                    font_style="Body1",
                    halign="left",
                    theme_text_color="Secondary",
                )
            )
            card.add_widget(row)

        btn_revisar = MDRaisedButton(
            text="Revisar",
            md_bg_color=(0.2, 0.7, 0.2, 1),
            on_release=self.revisar,
        )
        card.add_widget(btn_revisar)

        layout.add_widget(card)
        self.add_widget(layout)

    def revisar(self, instance):
        if all(cb.active for cb in self.checkboxes):
            show_snackbar("✅ ¡Felicitaciones por seguir los consejos de seguridad!")
        else:
            show_snackbar("⚠ Revisa los puntos pendientes")
