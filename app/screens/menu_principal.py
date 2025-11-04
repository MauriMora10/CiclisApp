from kivymd.uix.screen import MDScreen
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class DrawerSeparator(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(1)
        with self.canvas:
            Color(0.9, 0.9, 0.9, 1)
            self._rect = Rectangle(pos=self.pos, size=(self.width, self.height))
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self._rect.pos = (self.x, self.y)
        self._rect.size = (self.width, self.height)
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from app.screens.consejos_screen import ConsejosScreen
from app.screens.sos_screen import WeatherScreen
from app.screens.checklist_screen import ChecklistScreen
from app.screens.pantalla_mapa import PantallaMapa
from app.screens.profile_screen import ProfileScreen
from app.utils.ui import show_snackbar

class MenuPrincipal(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'principal'
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.toolbar import MDTopAppBar
        from kivymd.uix.menu import MDDropdownMenu
        # Usamos MDNavigationLayout para soportar drawer lateral moderno
        nav_layout = MDNavigationLayout()

        # Contenido principal (barra superior + bottom navigation)
        content = MDBoxLayout(orientation='vertical')

        # Barra superior con menú sandwich que abre el drawer
        self.toolbar = MDTopAppBar(title='CiclisApp', elevation=0, left_action_items=[['menu', lambda x: self.nav_drawer.set_state('open')]])
        content.add_widget(self.toolbar)

        # Navegación inferior
        nav = MDBottomNavigation()
        tab_consejos = MDBottomNavigationItem(name='consejos', text='Consejos', icon='shield-check')
        tab_consejos.add_widget(ConsejosScreen())
        nav.add_widget(tab_consejos)
        tab_weather = MDBottomNavigationItem(name='weather', text='Clima', icon='weather-partly-cloudy')
        tab_weather.add_widget(WeatherScreen())
        nav.add_widget(tab_weather)
        tab_checklist = MDBottomNavigationItem(name='checklist', text='Checklist', icon='check')
        tab_checklist.add_widget(ChecklistScreen())
        nav.add_widget(tab_checklist)
        tab_mapa = MDBottomNavigationItem(name='mapa', text='Mapa', icon='map')
        tab_mapa.add_widget(PantallaMapa())
        nav.add_widget(tab_mapa)
        content.add_widget(nav)

        # Drawer lateral
        self.nav_drawer = MDNavigationDrawer()
        # Fijar ancho para evitar que se vea corrido (tamaño razonable para pantallas móviles)
        try:
            self.nav_drawer.size_hint_x = None
            self.nav_drawer.width = dp(280)
        except Exception:
            pass

        # Header del drawer
        header = MDBoxLayout(orientation='horizontal', padding=dp(12), size_hint_y=None, height=dp(120), spacing=dp(12))
        # Avatar circular con iniciales como fallback
        avatar = MDBoxLayout(size_hint=(None, None), size=(dp(64), dp(64)), md_bg_color=(0.1, 0.6, 0.8, 1), radius=[dp(32)])
        avatar_label = MDLabel(text='CT', halign='center', valign='middle', theme_text_color='Custom', text_color=(1,1,1,1))
        avatar.add_widget(avatar_label)

        header_right = MDBoxLayout(orientation='vertical')
        header_right.add_widget(MDLabel(text='CiclisApp', font_style='H6', halign='left'))
        header_right.add_widget(MDLabel(text='Seguridad vial para ciclistas', halign='left', theme_text_color='Secondary', font_style='Caption'))
        header.add_widget(avatar)
        header.add_widget(header_right)

        # Lista de opciones
        drawer_list = MDList()

        def _add_item(text, icon, on_release):
            item = OneLineIconListItem(text=text, on_release=on_release)
            icon_widget = IconLeftWidget(icon=icon)
            item.add_widget(icon_widget)
            drawer_list.add_widget(item)

        _add_item('Perfil de usuario', 'account', lambda x=None: (self.nav_drawer.set_state('close'), self.show_perfil()))
        _add_item('Reportar peligro', 'map-marker-alert', lambda x=None: (self.nav_drawer.set_state('close'), self.ir_a_reporte()))
        _add_item('Ver reportes', 'playlist-check', lambda x=None: (self.nav_drawer.set_state('close'), self.ir_a_lista_reportes()))
        _add_item('Ajustes de la app', 'cog', lambda x=None: (self.nav_drawer.set_state('close'), self.show_ajustes()))
        _add_item('Configuraciones', 'tune', lambda x=None: (self.nav_drawer.set_state('close'), self.show_configuraciones()))
        _add_item('Cerrar sesión', 'logout', lambda x=None: (self.nav_drawer.set_state('close'), self.cerrar_sesion()))

        # Un único contenedor vertical para el drawer (header + separador + lista scrollable)
        from kivy.uix.scrollview import ScrollView as _ScrollView
        drawer_content = MDBoxLayout(orientation='vertical')
        drawer_content.add_widget(header)
        drawer_content.add_widget(DrawerSeparator())
        sv = _ScrollView()
        sv.add_widget(drawer_list)
        drawer_content.add_widget(sv)

        self.nav_drawer.add_widget(drawer_content)

        # MDNavigationLayout requires a ScreenManager as first child
        sm = ScreenManager()
        # envolver el content en una screen del ScreenManager
        from kivymd.uix.screen import MDScreen as _MDScreen
        main_screen = _MDScreen(name='main_content')
        main_screen.add_widget(content)
        sm.add_widget(main_screen)

        nav_layout.add_widget(sm)
        nav_layout.add_widget(self.nav_drawer)
        self.add_widget(nav_layout)

    def open_menu(self, instance):
        # Mantener compatibilidad: abrir drawer si existe
        try:
            self.nav_drawer.set_state('open')
        except Exception:
            pass

    def show_perfil(self):
        try:
            self.nav_drawer.set_state('close')
        except Exception:
            pass
        if self.manager:
            self.manager.current = 'profile'

    def show_ajustes(self):
        try:
            self.nav_drawer.set_state('close')
        except Exception:
            pass
        show_snackbar("Ajustes de la app (próximamente)", allow_on_login=True)

    def show_configuraciones(self):
        try:
            self.nav_drawer.set_state('close')
        except Exception:
            pass
        show_snackbar("Otras configuraciones (próximamente)", allow_on_login=True)

    def ir_a_reporte(self):
        try:
            self.nav_drawer.set_state('close')
        except Exception:
            pass
        if self.manager:
            self.manager.current = 'reporte'

    def ir_a_lista_reportes(self):
        try:
            self.nav_drawer.set_state('close')
        except Exception:
            pass
        if self.manager:
            self.manager.current = 'lista_reportes'

    def cerrar_sesion(self):
        # Navegar a la pantalla de login (si existe en el ScreenManager raíz)
        try:
            # Si este Screen está en un ScreenManager que a su vez está en la app principal
            app_sm = self.manager
            if app_sm:
                app_sm.current = 'login'
        except Exception:
            pass
