#!/usr/bin/env python3
"""SEO helpers: URLs, meta tags, JSON-LD."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Optional

SITE_URL = "https://www.doris-gunsch.eu"
BUSINESS_ID = f"{SITE_URL}/#business"
WEBSITE_ID = f"{SITE_URL}/#website"
LLMS_TXT_URL = f"{SITE_URL}/llms.txt"
LLMS_FULL_URL = f"{SITE_URL}/llms-full.txt"
OG_IMAGE = f"{SITE_URL}/public/doris-web.jpg"
OG_IMAGE_WIDTH = 800
OG_IMAGE_HEIGHT = 682
ORG_NAME_DE = "Doris Gunsch – Psychologische Managementberatung"
ORG_NAME_EN = "Doris Gunsch – Psychological Management Consulting"
FAVICON_VERSION = 3
ASSET_VERSION = 1

# Newtonstraße 3, 49088 Osnabrück
GEO_LATITUDE = 52.2726
GEO_LONGITUDE = 8.0472

LOGO_PRELOAD_PAGES = frozenset({"index.html", "404.html"})
PROFILE_PRELOAD_PAGES = frozenset({"person.html"})


def clean_path(filename: str) -> str:
    """URL path segment without .html (empty string for index)."""
    if filename == "index.html":
        return ""
    if filename.endswith(".html"):
        return filename[:-5]
    return filename


def page_href(filename: str, prefix: str = "") -> str:
    """Relative href for internal navigation (matches Vercel cleanUrls)."""
    path = clean_path(filename)
    if not path:
        return prefix if prefix else "./"
    return f"{prefix}{path}"


def clean_internal_hrefs(content: str) -> str:
    """Rewrite relative .html links in page body to clean URLs."""
    def repl(match: re.Match[str]) -> str:
        href = match.group(1)
        if re.match(r"^(https?:|mailto:|tel:|#|/)", href):
            return match.group(0)
        m = re.match(r"^((?:\.\./)*)?(.*)$", href)
        if not m:
            return match.group(0)
        path_prefix, rest = m.group(1) or "", m.group(2)
        if not rest.endswith(".html"):
            return match.group(0)
        cleaned = clean_path(rest)
        if not cleaned:
            new_href = path_prefix or "./"
        else:
            new_href = f"{path_prefix}{cleaned}"
        return f'href="{new_href}"'

    return re.sub(r'href="([^"]+)"', repl, content)


def absolute_url(filename: str, lang: str) -> str:
    path = clean_path(filename)
    if lang == "en":
        base = f"{SITE_URL}/en"
        return f"{base}/" if not path else f"{base}/{path}"
    return f"{SITE_URL}/" if not path else f"{SITE_URL}/{path}"


def favicon_head(asset: str) -> str:
    query = f"?v={FAVICON_VERSION}"
    return f"""  <link rel="icon" href="{asset}public/favicon.ico{query}" sizes="any">
  <link rel="icon" type="image/png" sizes="48x48" href="{asset}public/favicon-48.png{query}">
  <link rel="icon" type="image/png" sizes="32x32" href="{asset}public/favicon-32.png{query}">
  <link rel="icon" type="image/png" sizes="16x16" href="{asset}public/favicon-16.png{query}">
  <link rel="apple-touch-icon" sizes="180x180" href="{asset}public/apple-touch-icon.png{query}">"""


def canonical_hreflang(filename: str, lang: str, *, include_hreflang: bool = True) -> str:
    canonical = absolute_url(filename, lang)
    if not include_hreflang:
        return f'  <link rel="canonical" href="{canonical}">'

    de_url = absolute_url(filename, "de")
    en_url = absolute_url(filename, "en")
    return f"""  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="de" href="{de_url}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="x-default" href="{de_url}">"""


def llms_head_link() -> str:
    """Machine-readable site summary for LLM crawlers and AI assistants."""
    return f"""  <link rel="alternate" type="text/plain" href="{LLMS_TXT_URL}" title="LLM-readable site summary">
  <link rel="alternate" type="text/plain" href="{LLMS_FULL_URL}" title="LLM-readable full site content">"""


def performance_head(asset: str, filename: str = "index.html") -> str:
    """Preload LCP assets and self-hosted fonts — avoids render-blocking Google Fonts."""
    v = ASSET_VERSION
    parts: list[str] = []

    if filename in LOGO_PRELOAD_PAGES:
        parts.append(
            f'  <link rel="preload" href="{asset}public/doris-logo-400.webp" '
            f'as="image" type="image/webp" fetchpriority="high">'
        )
    if filename in PROFILE_PRELOAD_PAGES:
        parts.append(
            f'  <link rel="preload" href="{asset}public/doris-web-600.webp" '
            f'as="image" type="image/webp">'
        )

    parts.extend(
        [
            f'  <link rel="preload" href="{asset}public/fonts/inter-latin-400.woff2" '
            f'as="font" type="font/woff2" crossorigin>',
            f'  <link rel="preload" href="{asset}public/fonts/cormorant-garamond-latin-400.woff2" '
            f'as="font" type="font/woff2" crossorigin>',
            f'  <link rel="preload" href="{asset}css/styles.css?v={v}" as="style">',
            f'  <link rel="stylesheet" href="{asset}css/fonts.css?v={v}">',
            f'  <link rel="stylesheet" href="{asset}css/styles.css?v={v}">',
        ]
    )
    return "\n".join(parts)


def logo_image(asset: str, *, label: str, fetchpriority: str = "auto") -> str:
    alt = html.escape(label, quote=True)
    priority_attr = (
        f'\n              fetchpriority="{fetchpriority}"'
        if fetchpriority in ("high", "low", "auto")
        else ""
    )
    return f"""          <picture>
            <source
              srcset="{asset}public/doris-logo-280.webp 280w, {asset}public/doris-logo-400.webp 400w"
              sizes="(max-width: 640px) 200px, 280px"
              type="image/webp">
            <img
              src="{asset}public/doris-logo-400.png"
              srcset="{asset}public/doris-logo-280.png 280w, {asset}public/doris-logo-400.png 400w"
              sizes="(max-width: 640px) 200px, 280px"
              alt="{alt}"
              width="400"
              height="223"
              decoding="async"{priority_attr}>
          </picture>"""


def profile_image(asset: str, alt: str, *, lazy: bool = True) -> str:
    loading = ' loading="lazy"' if lazy else ""
    alt_esc = html.escape(alt, quote=True)
    return f"""            <picture>
              <source srcset="{asset}public/doris-web-600.webp" type="image/webp">
              <img
                src="{asset}public/doris-web-600.jpg"
                alt="{alt_esc}"
                class="profile-photo"
                width="600"
                height="511"
                decoding="async"{loading}>
            </picture>"""


def open_graph(filename: str, lang: str, title: str, description: str) -> str:
    url = absolute_url(filename, lang)
    locale = "de_DE" if lang == "de" else "en_GB"
    alt_locale = "en_GB" if lang == "de" else "de_DE"
    t = html.escape(title, quote=True)
    d = html.escape(description, quote=True)
    return f"""  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="{OG_IMAGE_WIDTH}">
  <meta property="og:image:height" content="{OG_IMAGE_HEIGHT}">
  <meta property="og:image:alt" content="Doris Gunsch">
  <meta property="og:locale" content="{locale}">
  <meta property="og:locale:alternate" content="{alt_locale}">
  <meta property="og:site_name" content="Doris Gunsch">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{OG_IMAGE}">"""


def _json_ld(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return f'  <script type="application/ld+json">\n{payload}\n  </script>'


def _business_entity(lang: str) -> dict:
    name = ORG_NAME_DE if lang == "de" else ORG_NAME_EN
    return {
        "@type": "ProfessionalService",
        "@id": BUSINESS_ID,
        "name": name,
        "url": SITE_URL if lang == "de" else f"{SITE_URL}/en/",
        "image": OG_IMAGE,
        "telephone": "+49-541-14496",
        "email": "dg@doris-gunsch.eu",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Newtonstraße 3",
            "postalCode": "49088",
            "addressLocality": "Osnabrück",
            "addressCountry": "DE",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": GEO_LATITUDE,
            "longitude": GEO_LONGITUDE,
        },
        "areaServed": ["Germany", "Austria", "Switzerland"],
        "knowsAbout": [
            "Executive coaching",
            "Leadership development",
            "Organizational psychology",
            "Team development",
            "Change management",
        ],
    }


def business_schema(lang: str) -> str:
    """Canonical organisation entity and WebSite — homepage only."""
    website = {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "name": "Doris Gunsch",
        "url": SITE_URL if lang == "de" else f"{SITE_URL}/en/",
        "inLanguage": ["de", "en"],
        "publisher": {"@id": BUSINESS_ID},
    }
    data = {
        "@context": "https://schema.org",
        "@graph": [_business_entity(lang), website],
    }
    return _json_ld(data)


def contact_page_schema(lang: str, filename: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "name": "Kontakt" if lang == "de" else "Contact",
        "url": absolute_url(filename, lang),
        "inLanguage": lang,
        "mainEntity": {"@id": BUSINESS_ID},
        "isPartOf": {
            "@type": "WebSite",
            "@id": WEBSITE_ID,
        },
    }
    return _json_ld(data)


def person_schema(lang: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Doris Gunsch",
        "jobTitle": (
            "Psychologische Managementberaterin"
            if lang == "de"
            else "Psychological Management Consultant"
        ),
        "url": absolute_url("person.html", lang),
        "image": OG_IMAGE,
        "email": "dg@doris-gunsch.eu",
        "telephone": "+49-541-14496",
        "worksFor": {"@id": BUSINESS_ID},
        "knowsAbout": [
            "Psychology",
            "Executive coaching",
            "Leadership",
            "Organizational development",
        ],
        "alumniOf": {
            "@type": "CollegeOrUniversity",
            "name": "Universität Osnabrück",
        },
    }
    return _json_ld(data)


def web_page_schema(filename: str, lang: str, title: str, description: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": absolute_url(filename, lang),
        "inLanguage": lang,
        "isPartOf": {
            "@type": "WebSite",
            "@id": WEBSITE_ID,
        },
    }
    return _json_ld(data)


def _faq_entities(faq: list[tuple[str, str]]) -> list[dict]:
    return [
        {
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {"@type": "Answer", "text": answer},
        }
        for question, answer in faq
    ]


def city_location_schema(
    lang: str,
    city: str,
    filename: str,
    title: str,
    description: str,
    *,
    faq: Optional[list[tuple[str, str]]] = None,
) -> str:
    """Location landing page — references canonical business, no duplicate entity."""
    url = absolute_url(filename, lang)
    service_name = (
        f"Coaching und Prozessbegleitung in {city}"
        if lang == "de"
        else f"Coaching and facilitation in {city}"
    )
    graph: list[dict] = [
        {
            "@type": "WebPage",
            "name": title,
            "description": description,
            "url": url,
            "inLanguage": lang,
            "about": {"@type": "City", "name": city},
            "provider": {"@id": BUSINESS_ID},
            "isPartOf": {
                "@type": "WebSite",
                "@id": WEBSITE_ID,
            },
        },
        {
            "@type": "Service",
            "name": service_name,
            "description": description,
            "url": url,
            "areaServed": {"@type": "City", "name": city},
            "provider": {"@id": BUSINESS_ID},
        },
    ]
    if faq:
        graph.append(
            {
                "@type": "FAQPage",
                "url": url,
                "inLanguage": lang,
                "mainEntity": _faq_entities(faq),
            }
        )
    data = {"@context": "https://schema.org", "@graph": graph}
    return _json_ld(data)


def _standort_slug(filename: str) -> Optional[str]:
    if filename.startswith("standorte/") and filename.endswith(".html"):
        return filename[len("standorte/") : -len(".html")]
    return None


def structured_data(
    filename: str,
    lang: str,
    title: str,
    description: str,
    schema: str,
    *,
    city: Optional[str] = None,
) -> str:
    if schema == "business":
        return business_schema(lang)
    if schema == "contact":
        return contact_page_schema(lang, filename)
    if schema == "city_location" and city:
        from standorte_data import CITIES

        slug = _standort_slug(filename)
        faq = CITIES[slug][lang].get("faq") if slug and slug in CITIES else None
        return city_location_schema(
            lang, city, filename, title, description, faq=faq
        )
    if schema == "person":
        return person_schema(lang)
    if schema == "webpage":
        return web_page_schema(filename, lang, title, description)
    return ""


def file_lastmod(path: Path) -> str:
    if path.exists():
        from datetime import datetime, timezone

        mtime = path.stat().st_mtime
        return datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%d")
    from datetime import date

    return date.today().isoformat()
