#!/usr/bin/env python3
"""Generate interactive DACH map SVG from Natural Earth data."""
import html
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from standorte_data import MAP_CITIES, REACH_DESCRIPTIONS  # noqa: E402

URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    "master/geojson/ne_50m_admin_0_countries.geojson"
)

WIDTH = 520
HEIGHT = 620
PAD_LEFT = 62
PAD_RIGHT = 62
PAD_TOP = 46
PAD_BOTTOM = 58
MIN_LON, MAX_LON = 5.4, 17.3
MIN_LAT, MAX_LAT = 45.4, 55.3

DEFAULT_HIT_R = 15
DENSE_LINK_HIT_R = 12


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


def city_aria_label(city: dict) -> str:
    name = city["name_de"]
    slug = city.get("slug")
    if slug and slug in REACH_DESCRIPTIONS:
        return f"{name} — {REACH_DESCRIPTIONS[slug]['de']}"
    return name


def label_position(x, y, side, tdx, tdy):
    if side == 0:
        return "middle", x, round(y + tdy, 2)
    anchor = "end" if side < 0 else "start"
    return anchor, round(x + tdx, 2), round(y + tdy, 2)


def hit_radius(city: dict) -> int:
    if "hit_r" in city:
        return city["hit_r"]
    if not city["link"]:
        return 13
    if city.get("slug") in {"duesseldorf", "hannover"}:
        return DENSE_LINK_HIT_R
    return DEFAULT_HIT_R


def render_city_group(city: dict) -> list[str]:
    x, y = project(city["lon"], city["lat"])
    name = city["name_de"]
    slug = city.get("slug")
    data_slug = slug or ""
    side = city["label_side"]
    anchor, tx, ty = label_position(x, y, side, city["label_dx"], city["label_dy"])
    label_class = "map-label map-label--home" if city["home"] else "map-label"
    aria = html.escape(city_aria_label(city), quote=True)
    hit_r = hit_radius(city)

    marker_lines = []
    if city["home"]:
        marker_lines.extend(
            [
                f'    <circle class="map-ring map-ring--home" cx="{x}" cy="{y}" r="10"/>',
                f'    <circle class="map-ring map-ring--soft" cx="{x}" cy="{y}" r="16"/>',
                f'    <circle class="map-dot map-dot--home" cx="{x}" cy="{y}" r="4.5"/>',
            ]
        )
    else:
        if city["ring"]:
            marker_lines.append(f'    <circle class="map-ring" cx="{x}" cy="{y}" r="8"/>')
        marker_lines.append(f'    <circle class="map-dot" cx="{x}" cy="{y}" r="3.5"/>')
    marker_lines.append(
        f'    <text class="{label_class}" x="{tx}" y="{ty}" text-anchor="{anchor}">{html.escape(name)}</text>'
    )
    marker_lines.append(f'    <circle class="map-city-hit" cx="{x}" cy="{y}" r="{hit_r}"/>')
    marker_body = "\n".join(marker_lines)

    if city["link"] and slug:
        return [
            f'    <a class="map-city map-city--link" data-slug="{data_slug}" '
            f'href="standorte/{slug}" role="listitem" aria-label="{aria}">',
            marker_body,
            "    </a>",
        ]

    nolink_slug = data_slug or name.lower().replace("ü", "ue").replace("ö", "oe")
    return [
        f'    <g class="map-city map-city--nolink" data-slug="{nolink_slug}" role="listitem">',
        marker_body,
        "    </g>",
    ]


def render_city_markers() -> list[str]:
    linked = [city for city in MAP_CITIES if city["link"] and city.get("slug")]
    visual_only = [city for city in MAP_CITIES if not city["link"] or not city.get("slug")]

    lines = ['  <g class="map-cities" role="list">']
    for city in linked:
        lines.extend(render_city_group(city))
    for city in visual_only:
        lines.extend(render_city_group(city))
    lines.append("  </g>")
    return lines


def build_svg(aria_label: str) -> str:
    with urllib.request.urlopen(URL, timeout=60) as response:
        data = json.load(response)

    features = [
        feature
        for feature in data["features"]
        if feature["properties"].get("ISO_A3") in {"DEU", "AUT", "CHE"}
    ]

    lines = [
        f'<svg class="map-dach-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'role="group" aria-label="{html.escape(aria_label, quote=True)}">',
        "  <title>Einsatzgebiet Doris Gunsch</title>",
        '  <g class="map-countries" aria-hidden="true">',
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
            lines.append(
                f'    <path class="map-country" d="{ring_to_path(polygon[0], steps.get(iso, 2))}"/>'
            )

    lines.append("  </g>")
    lines.extend(render_city_markers())
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def main():
    svg = build_svg("Karte DACH-Raum mit Einsatzorten")
    (ROOT / "assets" / "map-dach.svg").write_text(svg, encoding="utf-8")
    print("Wrote assets/map-dach.svg")


if __name__ == "__main__":
    main()
