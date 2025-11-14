from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivy_garden.mapview import MapView, MapMarker, MapLayer
from kivy.graphics import Color, Line
import requests


class CicloviaLayer(MapLayer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lines = []

    def reposition(self):
        pass

    def set_lines(self, coords):
        self.lines = coords
        self.canvas.clear()
        with self.canvas:
            Color(0, 0.4, 1, 1)  # azul ciclovías
            for line_coords in self.lines:
                points = []
                for lat, lon in line_coords:
                    x, y = self.parent.get_window_xy_from(lat, lon)
                    points += [x, y]
                if len(points) >= 4:
                    Line(points=points, width=1.3)


class PantallaMapa(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'pantalla_mapa'

        # Layout principal vertical
        layout = MDBoxLayout(orientation='vertical')

        # Barra superior con título
        toolbar = MDTopAppBar(
            title="Mapa de Zonas Seguras",
            elevation=4
        )
        layout.add_widget(toolbar)

        # MapView ocupando el resto del espacio
        self.mapview = MapView(
            zoom=13,
            lat=-38.7359,
            lon=-72.5904,
            size_hint=(1, 1)
        )
        layout.add_widget(self.mapview)

        self.add_widget(layout)

        # Capa de ciclovías
        self.ciclovia_layer = CicloviaLayer()
        self.mapview.add_layer(self.ciclovia_layer, mode="scatter")

        # Descargar ciclovías desde OSM
        self.obtener_ciclovias()

    def obtener_ciclovias(self):
        query = """
        [out:json][timeout:25];
        (
          way["highway"="cycleway"](around:15000,-38.7359,-72.5904);
          relation["route"="bicycle"](around:15000,-38.7359,-72.5904);
        );
        out geom;
        """

        try:
            r = requests.get("https://overpass-api.de/api/interpreter", params={"data": query})
            data = r.json()

            trazos = []

            for el in data["elements"]:
                if "geometry" in el:
                    coords = [(g["lat"], g["lon"]) for g in el["geometry"]]
                    trazos.append(coords)

            self.ciclovia_layer.set_lines(trazos)

        except Exception as e:
            print("ERROR OSM:", e)
