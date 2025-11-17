from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem

from kivy_garden.mapview import MapView, MapLayer, MapMarker
from kivy.graphics import Color, Line
from kivy.utils import get_color_from_hex
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.widget import WidgetException
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation

import requests
import platform
import threading

# ============================================================
# CAPA CICLOVÍAS
# ============================================================
class CicloviaLayer(MapLayer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lines = []

    def reposition(self):
        self.draw_lines()

    def draw_lines(self):
        if not self.parent:
            return
        zoom = self.parent.zoom
        self.canvas.clear()

        if not self.lines:
            return

        with self.canvas:
            # Glow
            Color(0, 1, 1, 0.10)
            for segmento in self.lines:
                pts = []
                for lat, lon in segmento:
                    x, y = self.parent.get_window_xy_from(lat, lon, zoom)
                    pts += [x, y]
                if len(pts) >= 4:
                    Line(points=pts, width=3)

            # Azul principal
            Color(0.3, 0.64, 1, 0.9)
            for segmento in self.lines:
                pts = []
                for lat, lon in segmento:
                    x, y = self.parent.get_window_xy_from(lat, lon, zoom)
                    pts += [x, y]
                if len(pts) >= 4:
                    Line(points=pts, width=1.5)

    def set_lines(self, coords):
        self.lines = coords or []
        self.draw_lines()


# ============================================================
# CAPA RUTA
# ============================================================
class RouteLayer(MapLayer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.route_coords = []

    def reposition(self):
        self.draw_route()

    def draw_route(self):
        if not self.parent:
            return
        zoom = self.parent.zoom
        self.canvas.clear()

        if not self.route_coords:
            return

        with self.canvas:
            Color(0, 1, 0.4, 1)
            pts = []
            for lat, lon in self.route_coords:
                x, y = self.parent.get_window_xy_from(lat, lon, zoom)
                pts += [x, y]
            if len(pts) >= 4:
                Line(points=pts, width=2)

    def set_route(self, coords):
        if not coords:
            self.route_coords = []
            self.canvas.clear()
            return
        self.route_coords = coords
        self.draw_route()

    def clear_route(self):
        self.route_coords = []
        self.canvas.clear()


# ============================================================
# PANTALLA PRINCIPAL OPTIMIZADA
# ============================================================
class PantallaMapa(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "pantalla_mapa"

        app = App.get_running_app()
        self.apply_background()

        self.dropdown_menu = None
        self._pending_query = ""
        self._autocomplete_event = None
        
        self.dest_marker = None
        self.user_location_marker = None
        self.user_lat = None
        self.user_lon = None

        # =============================
        # LAYOUT PRINCIPAL
        # =============================
        root = MDBoxLayout(orientation="vertical", spacing=0)

        # ----------------------------
        # BUSCADOR MODERNO (Material Design 3)
        # ----------------------------
        header = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(50),
            padding=(dp(8), dp(8), dp(8), dp(2)),
        )

        self.search_card = MDCard(
            size_hint=(1, None),
            height=dp(48),
            radius=[20, 20, 20, 20],
            elevation=1,
            padding=(dp(8), dp(8)),
            md_bg_color=getattr(app.theme_cls, "surfaceColor", (1, 1, 1, 1)),
        )

        search_row = MDBoxLayout(orientation="horizontal", spacing=dp(6))

        self.search_field = MDTextField(
            hint_text="Buscar destino...",
            size_hint_x=0.82,
            mode="fill",
            line_color_normal=(0, 0, 0, 0),
            line_color_focus=(0, 0, 0, 0),
            hint_text_color=(0.5, 0.5, 0.5, 1),
            pos_hint={"center_y": 0.5},
        )

        self.search_button = MDRaisedButton(
            text="Ir",
            size_hint_x=0.18,
            md_bg_color=app.theme_cls.primary_color,
            elevation=1,
            pos_hint={"center_y": 0.5},
            on_release=self.on_search_press,
        )

        search_row.add_widget(self.search_field)
        search_row.add_widget(self.search_button)
        self.search_card.add_widget(search_row)
        header.add_widget(self.search_card)

        root.add_widget(header)

        # ======================================================
        # MAPA A PANTALLA COMPLETA
        # ======================================================
        map_container = FloatLayout()

        self.mapview = MapView(
            zoom=13,
            lat=-38.7359,
            lon=-72.5904,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            map_source="osm",
        )
        map_container.add_widget(self.mapview)

        # -------------------------------
        # BOTÓN GPS (mejor posición)
        # -------------------------------
        self.location_button = MDFloatingActionButton(
            icon="crosshairs-gps",
            elevation=7,
            md_bg_color=get_color_from_hex("#4CAF50"),
            pos_hint={"right": 0.96, "y": 0.13},
        )
        self.location_button.bind(on_release=self.on_location_press)
        map_container.add_widget(self.location_button)

        # -------------------------------
        # TARJETA DE INSTRUCCIONES
        # -------------------------------
        self.instructions_card = MDCard(
            size_hint=(0.96, None),
            height=0,
            elevation=5,
            radius=[16, 16, 16, 16],
            md_bg_color=getattr(app.theme_cls, "surfaceColor", (1, 1, 1, 1)),
            pos_hint={"center_x": 0.5, "y": 0.02},
            opacity=0,
        )

        box = MDBoxLayout(orientation="vertical", padding=dp(12), spacing=dp(4))

        self.instructions_title = MDLabel(
            text="Indicaciones de ruta",
            font_style="Subtitle2",
            size_hint_y=None,
            height=dp(20),
        )
        self.instructions_label = MDLabel(text="", font_style="Caption", valign="top")

        box.add_widget(self.instructions_title)
        box.add_widget(self.instructions_label)
        self.instructions_card.add_widget(box)

        map_container.add_widget(self.instructions_card)
        root.add_widget(map_container)
        self.add_widget(root)

        # Capas de mapa
        self.ciclovia_layer = CicloviaLayer()
        self.route_layer = RouteLayer()
        self.mapview.add_layer(self.ciclovia_layer, mode="scatter")
        self.mapview.add_layer(self.route_layer, mode="scatter")

        self.apply_map_theme()
        app.theme_cls.bind(theme_style=self.on_theme_change)

        # Cargar ciclovías
        self.obtener_ciclovias()

        # Autocomplete
        self.search_field.bind(text=self.on_text_change)

    # ============================================================
    # TEMA DINÁMICO
    # ============================================================
    def on_theme_change(self, *args):
        app = App.get_running_app()
        self.apply_background()
        self.search_button.md_bg_color = app.theme_cls.primary_color
        self.search_card.md_bg_color = getattr(app.theme_cls, "surfaceColor", (1, 1, 1, 1))
        self.instructions_card.md_bg_color = getattr(app.theme_cls, "surfaceColor", (1, 1, 1, 1))
        self.apply_map_theme()

    def apply_background(self):
        app = App.get_running_app()
        if app.theme_cls.theme_style == "Dark":
            self.md_bg_color = (0.05, 0.05, 0.05, 1)
        else:
            self.md_bg_color = (0.95, 1, 0.95, 1)

    def apply_map_theme(self):
        app = App.get_running_app()
        from kivy_garden.mapview.source import MapSource

        if app.theme_cls.theme_style == "Dark":
            MapSource.providers["carto_dark"] = (
                False, 0, 20,
                "https://cartodb-basemaps-a.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png",
                "CartoDB Dark Matter"
            )
            self.mapview.map_source = "carto_dark"
        else:
            self.mapview.map_source = "osm"

    # ============================================================
    # AUTOCOMPLETE
    # ============================================================
    def on_text_change(self, instance, value):
        value = value.strip()
        if len(value) < 3:
            self._pending_query = ""
            if self.dropdown_menu:
                try:
                    self.dropdown_menu.dismiss()
                except:
                    pass
            return

        self._pending_query = value
        
        if self._autocomplete_event:
            self._autocomplete_event.cancel()

        self._autocomplete_event = Clock.schedule_once(
            self._run_autocomplete_debounced, 0.4
        )

    def _run_autocomplete_debounced(self, dt):
        query = self._pending_query
        if not query:
            return

        threading.Thread(
            target=self._fetch_suggestions_thread, args=(query,), daemon=True
        ).start()

    def _fetch_suggestions_thread(self, query):
        suggestions = self.get_suggestions(query)

        def update(dt):
            if query != self._pending_query:
                return
            self._update_dropdown_menu(suggestions)

        Clock.schedule_once(update)

    def _update_dropdown_menu(self, suggestions):
        if not suggestions:
            if self.dropdown_menu:
                try:
                    self.dropdown_menu.dismiss()
                except:
                    pass
            return

        items = [
            {
                "viewclass": "TwoLineListItem",
                "text": s["name"],
                "secondary_text": s["full_address"],
                "on_release": lambda x=s: self.on_suggestion_select(x),
            }
            for s in suggestions
        ]

        if self.dropdown_menu:
            self.dropdown_menu.items = items
        else:
            self.dropdown_menu = MDDropdownMenu(
                caller=self.search_card,
                items=items,
                width_mult=6,
                max_height=dp(280),
                position="auto",
                ver_growth="down",
            )

        try:
            self.dropdown_menu.open()
        except:
            pass

    def get_suggestions(self, query):
        try:
            url = "https://photon.komoot.io/api/"
            params = {"q": query, "limit": 5}
            r = requests.get(url, params=params, timeout=4)
            data = r.json()

            results = []
            for feature in data.get("features", []):
                props = feature.get("properties", {})
                name = props.get("name")
                if not name:
                    continue

                city = props.get("city", "")
                state = props.get("state", "")
                country = props.get("country", "")
                full_address = ", ".join([x for x in [city, state, country] if x])

                lon, lat = feature["geometry"]["coordinates"]

                results.append(
                    {
                        "name": name,
                        "full_address": full_address,
                        "lat": lat,
                        "lon": lon,
                    }
                )

            return results

        except:
            return []

    def on_suggestion_select(self, sug):
        self.search_field.text = f"{sug['name']}, {sug['full_address']}"
        if self.dropdown_menu:
            try:
                self.dropdown_menu.dismiss()
            except:
                pass
        self.search_with_coords(sug["lat"], sug["lon"])

    # ============================================================
    # GEOCODING / RUTA
    # ============================================================
    def geocode(self, query):
        try:
            r = requests.get("https://photon.komoot.io/api/", params={"q": query, "limit": 1}, timeout=8)
            data = r.json()
            if data.get("features"):
                lon, lat = data["features"][0]["geometry"]["coordinates"]
                return lat, lon
        except:
            pass
        return None

    def obtener_ruta(self, lat_o, lon_o, lat_d, lon_d):
        try:
            url = (
                f"https://router.project-osrm.org/route/v1/bicycle/"
                f"{lon_o},{lat_o};{lon_d},{lat_d}?overview=full&geometries=geojson&steps=true"
            )
            r = requests.get(url, timeout=15)
            data = r.json()

            if data.get("routes"):
                coords = data["routes"][0]["geometry"]["coordinates"]
                route = [(lat, lon) for lon, lat in coords]

                instructions = []
                for leg in data["routes"][0]["legs"]:
                    for step in leg["steps"]:
                        t = step["maneuver"].get("instruction", "")
                        if t:
                            instructions.append(t)

                return route, instructions

        except:
            pass

        return [], []

    def on_search_press(self, instance):
        q = self.search_field.text.strip()
        if not q:
            return

        dest = self.geocode(q)
        if not dest:
            print("Destino no encontrado")
            return

        self.search_with_coords(dest[0], dest[1])

    def search_with_coords(self, lat_d, lon_d):
        lat_o = self.user_lat or self.mapview.lat
        lon_o = self.user_lon or self.mapview.lon

        self.route_layer.clear_route()

        if self.dest_marker:
            self.mapview.remove_marker(self.dest_marker)
            self.dest_marker = None

        route, instructions = self.obtener_ruta(lat_o, lon_o, lat_d, lon_d)

        if not route:
            self.show_instructions([])
            return

        self.route_layer.set_route(route)

        self.dest_marker = MapMarker(lat=lat_d, lon=lon_d)
        self.mapview.add_marker(self.dest_marker)
        self.mapview.center_on(lat_d, lon_d)

        self.show_instructions(instructions)

    # ============================================================
    # PANEL DE INSTRUCCIONES
    # ============================================================
    def show_instructions(self, instructions):
        if not instructions:
            Animation(height=0, opacity=0, d=0.25).start(self.instructions_card)
            self.instructions_label.text = ""
            return

        txt = "\n".join([f"{i+1}. {ins}" for i, ins in enumerate(instructions[:5])])
        self.instructions_label.text = txt

        target_height = min(dp(160), dp(60) + len(instructions) * dp(14))

        Animation(height=target_height, opacity=1, d=0.30).start(self.instructions_card)

    # ============================================================
    # GPS
    # ============================================================
    def on_location_press(self, instance):
        if platform.system() == "Android":
            try:
                from plyer import gps
                gps.configure(on_location=self.on_gps_location, on_status=self.on_gps_status)
                gps.start(minTime=1000, minDistance=1)
            except:
                self.get_location_fallback()
        else:
            self.get_location_fallback()

    def on_gps_location(self, **kwargs):
        self.user_lat = kwargs.get("lat")
        self.user_lon = kwargs.get("lon")
        self.update_user_marker()

    def on_gps_status(self, stype, status):
        print("GPS status:", stype, status)

    def get_location_fallback(self):
        try:
            r = requests.get("http://ip-api.com/json/", timeout=8)
            data = r.json()
            if data.get("status") == "success":
                self.user_lat = data["lat"]
                self.user_lon = data["lon"]
                self.update_user_marker()
        except:
            pass

    def update_user_marker(self):
        if self.user_lat and self.user_lon:
            if self.user_location_marker:
                self.mapview.remove_marker(self.user_location_marker)

            self.user_location_marker = MapMarker(lat=self.user_lat, lon=self.user_lon)
            self.mapview.add_marker(self.user_location_marker)
            self.mapview.center_on(self.user_lat, self.user_lon)

    # ============================================================
    # CICLOVÍAS OSM
    # ============================================================
    def obtener_ciclovias(self):
        query = """
        [out:json][timeout:25];
        (
          way["highway"="cycleway"](around:15000,-38.7359,-72.5904);
          relation["route"="bicycle"](around:15000,-38.7359,-72.5904);
        );
        out geom;
        """

        def fetch():
            try:
                req = requests.get(
                    "https://overpass-api.de/api/interpreter",
                    params={"data": query},
                    timeout=25,
                )
                data = req.json()

                trazos = []
                for el in data.get("elements", []):
                    if "geometry" in el:
                        coords = [(g["lat"], g["lon"]) for g in el["geometry"]]
                        trazos.append(coords)

                Clock.schedule_once(lambda dt: self.ciclovia_layer.set_lines(trazos))

            except Exception as e:
                print("ERROR OSM:", e)

        threading.Thread(target=fetch, daemon=True).start()


