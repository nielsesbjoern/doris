#!/usr/bin/env python3
"""Generate DACH map SVG from Natural Earth data."""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    "master/geojson/ne_50m_admin_0_countries.geojson"
)

# name, lon, lat, home, label_side (-1 left / 1 right / 0 centered below), label_dx, label_dy
CITIES = [
    ("Osnabrück", 8.0472, 52.2799, True, 0, 0, 28),
    ("Hamburg", 9.9937, 53.5511, False, 1, 10, -2),
    ("Berlin", 13.4050, 52.5200, False, -1, -10, 0),
    ("Hannover", 9.7320, 52.3759, False, 1, 10, 0),
    ("Bremen", 8.8017, 53.0793, False, -1, -10, 0),
    ("Düsseldorf", 6.7735, 51.2277, False, 1, 10, 0),
    ("Köln", 6.9603, 50.9375, False, 1, 10, 0),
    ("Frankfurt", 8.6821, 50.1109, False, 1, 10, 0),
    ("Stuttgart", 9.1829, 48.7758, False, 1, 10, 0),
    ("München", 11.5820, 48.1351, False, -1, -10, 0),
    ("Zürich", 8.5417, 47.3769, False, 0, 0, 14),
]

RING_CITIES = {"Berlin", "Hamburg", "München", "Frankfurt"}

WIDTH = 520
HEIGHT = 620
PAD_LEFT = 62
PAD_RIGHT = 62
PAD_TOP = 46
PAD_BOTTOM = 58
MIN_LON, MAX_LON = 5.4, 17.3
MIN_LAT, MAX_LAT = 45.4, 55.3


def build_svg(aria_label: str) -> str:
    with urllib.request.urlopen(URL, timeout=60) as response:
        data = json.load(response)

    features = [
        feature
        for feature in data["features"]
        if feature["properties"].get("ISO_A3") in {"DEU", "AUT", "CHE"}
    ]

    def project(lon, lat):
        x = PAD_LEFT + (lon - MIN_LON) / (MAX_LON - MIN_LON) * (WIDTH - PAD_LEFT - PAD_RIGHT)
        y = PAD_TOP + (MAX_LAT - lat) / (MAX_LAT - MIN_LAT) * (HEIGHT - PAD_TOP - PAD_BOTTOM)
        return round(x, 2), round(y, 2)

    def ring_to_path(coords, step=1):
        coords = coords[::step]
        parts = []
        for index, (lon, lat) in enumerate(coords):
            x, y = project(lon, lat)
            parts.append(("M" if index == 0 else "L") + f"{x:.2f},{y:.2f}")
        return "".join(parts) + "Z"

    lines = [
        f'<svg class="map-dach-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="{aria_label}">',
        "  <title>Einsatzgebiet Doris Gunsch</title>",
        '  <g class="map-countries">',
    ]

    steps = {"DEU": 3, "AUT": 2, "CHE": 2}
    for feature in sorted(features, key=lambda item: item["properties"]["ISO_A3"]):
        iso = feature["properties"]["ISO_A3"]
        geometry = feature["geometry"]
        polygons = (
            [geometry["coordinates"]]
            if geometry["type"] == "Polygon"
            else geometry["coordinates"]
        )
        for polygon in polygons:
            lines.append(f'    <path class="map-country" d="{ring_to_path(polygon[0], steps.get(iso, 2))}"/>')

    lines.append("  </g>")
    lines.append('  <g class="map-cities">')

    for name, lon, lat, home, side, tdx, tdy in CITIES:
        x, y = project(lon, lat)
        if home:
            lines.append(f'    <circle class="map-ring map-ring--home" cx="{x}" cy="{y}" r="10"/>')
            lines.append(f'    <circle class="map-ring map-ring--soft" cx="{x}" cy="{y}" r="16"/>')
            lines.append(f'    <circle class="map-dot map-dot--home" cx="{x}" cy="{y}" r="4.5"/>')
        else:
            if name in RING_CITIES:
                lines.append(f'    <circle class="map-ring" cx="{x}" cy="{y}" r="8"/>')
            lines.append(f'    <circle class="map-dot" cx="{x}" cy="{y}" r="3.5"/>')

        if side == 0:
            anchor = "middle"
            tx, ty = x, round(y + tdy, 2)
        else:
            anchor = "end" if side < 0 else "start"
            tx, ty = round(x + tdx, 2), round(y + tdy, 2)
        label_class = "map-label map-label--home" if home else "map-label"
        lines.append(
            f'    <text class="{label_class}" x="{tx}" y="{ty}" text-anchor="{anchor}">{name}</text>'
        )

    lines.append("  </g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def main():
    svg = build_svg("Karte DACH-Raum mit Einsatzorten")
    (ROOT / "assets" / "map-dach.svg").write_text(svg, encoding="utf-8")
    print("Wrote assets/map-dach.svg")


if __name__ == "__main__":
    main()
