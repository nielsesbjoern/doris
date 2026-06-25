#!/usr/bin/env python3
"""Wrap page main content with sidebar shell (DE + EN)."""
from pathlib import Path
import html
import re
import sys
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from seo import (  # noqa: E402
    canonical_hreflang,
    llms_head_link,
    favicon_head,
    logo_image,
    open_graph,
    performance_head,
    structured_data,
)
from standorte_data import STANDORTE_META  # noqa: E402

META = {
    "index.html": {
        "page": "home",
        "active": "home",
        "schema": "business",
        "title_de": "Psychologische Managementberatung Osnabrück – Doris Gunsch",
        "title_en": "Psychological Management Consulting Osnabrück – Doris Gunsch",
        "desc_de": "Coaching, Trainings und Prozessbegleitung für Führungskräfte in Veränderungs- und Konfliktsituationen. Büro in Osnabrück, deutschlandweit tätig.",
        "desc_en": "Coaching, training and process facilitation for leaders in change and conflict situations. Based in Osnabrück, working across Germany.",
    },
    "leistungen.html": {
        "page": "leistungen",
        "active": "leistungen",
        "schema": "webpage",
        "title_de": "Leistungen – Coaching, Training & Prozessbegleitung",
        "title_en": "Services – Coaching, Training & Facilitation",
        "desc_de": "Überblick über Coaching, Trainings, Teamentwicklung und Diagnostik für Führungskräfte und Organisationen — psychologisch fundiert und praxisnah.",
        "desc_en": "Overview of coaching, training, team development and diagnostics for leaders and organisations — psychologically grounded and practical.",
    },
    "einsatzgebiete.html": {
        "page": "einsatzgebiete",
        "active": "einsatzgebiete",
        "schema": "webpage",
        "title_de": "Einsatzgebiete – Von Osnabrück deutschlandweit | Doris Gunsch",
        "title_en": "Service Areas – From Osnabrück across Germany | Doris Gunsch",
        "desc_de": "Coaching und Beratung in Osnabrück, bundesweit und hybrid — ausgewählte Einsatzorte in Hamburg, Berlin, Frankfurt, München und weiteren Regionen.",
        "desc_en": "Coaching and consulting in Osnabrück, nationwide and hybrid — selected locations in Hamburg, Berlin, Frankfurt, Munich and other regions.",
    },
    "coaching.html": {
        "page": "leistungen",
        "active": "coaching",
        "schema": "webpage",
        "title_de": "Coaching für Führungskräfte – Personal & Business",
        "title_en": "Executive Coaching – Personal & Business",
        "desc_de": "Personal- und Business-Coaching für Führungskräfte: Klarheit gewinnen, Konflikte lösen, Veränderungen gestalten — vertraulich und zielorientiert.",
        "desc_en": "Personal and business coaching for leaders: gain clarity, resolve conflicts, navigate change — confidential and goal-oriented.",
    },
    "trainings.html": {
        "page": "leistungen",
        "active": "trainings",
        "schema": "webpage",
        "title_de": "Trainings & Seminare für Führungskräfte – Doris Gunsch",
        "title_en": "Leadership Training & Seminars – Doris Gunsch",
        "desc_de": "Praxisnahe Trainings und Seminare zu Führung, Kommunikation und Teamentwicklung — maßgeschneidert für Ihr Unternehmen.",
        "desc_en": "Practical training and seminars on leadership, communication and team development — tailored to your organisation.",
    },
    "team.html": {
        "page": "leistungen",
        "active": "team",
        "schema": "webpage",
        "title_de": "Team- & Prozessbegleitung für Führungskräfte",
        "title_en": "Team & Process Facilitation for Leaders",
        "desc_de": "Begleitung von Teams und Gruppenprozessen in Veränderungsphasen — Moderation, Konfliktklärung und Teamentwicklung.",
        "desc_en": "Facilitation of teams and group processes during change — moderation, conflict resolution and team development.",
    },
    "diagnostik.html": {
        "page": "leistungen",
        "active": "diagnostik",
        "schema": "webpage",
        "title_de": "Diagnostik & Persönlichkeitsprofiling",
        "title_en": "Diagnostics & Personality Profiling",
        "desc_de": "Psychologische Diagnostik und Persönlichkeitsprofiling für Führungskräfte und Teams — fundierte Entscheidungsgrundlagen.",
        "desc_en": "Psychological diagnostics and personality profiling for leaders and teams — sound foundations for decisions.",
    },
    "person.html": {
        "page": "person",
        "active": "person",
        "schema": "person",
        "title_de": "Doris Gunsch – Psychologische Managementberaterin",
        "title_en": "Doris Gunsch – Psychological Management Consultant",
        "desc_de": "Profil, Qualifikation und Berufserfahrung: Doris Gunsch, Psychologin und Managementberaterin mit über 20 Jahren Erfahrung.",
        "desc_en": "Profile, qualifications and experience: Doris Gunsch, psychologist and management consultant with over 20 years of experience.",
    },
    "psi-aktuell.html": {
        "page": "psi",
        "active": "psi",
        "schema": "webpage",
        "title_de": "PSI Weiterbildungen – Doris Gunsch",
        "title_en": "PSI Continuing Education – Doris Gunsch",
        "desc_de": "Aktuelle PSI-Theorie-Seminare und Weiterbildungen — Termine und Informationen von Doris Gunsch.",
        "desc_en": "Current PSI theory seminars and continuing education — dates and information from Doris Gunsch.",
    },
    "referenzen.html": {
        "page": "referenzen",
        "active": "referenzen",
        "schema": "webpage",
        "title_de": "Referenzen & Mandate – Doris Gunsch",
        "title_en": "References & Clients – Doris Gunsch",
        "desc_de": "Ausgewählte Referenzen aus Wirtschaft, Gesundheitswesen und öffentlichem Sektor — Vertrauen durch langjährige Zusammenarbeit.",
        "desc_en": "Selected references from business, healthcare and the public sector — trust built through long-term collaboration.",
    },
    "links.html": {
        "page": "links",
        "active": "links",
        "schema": "webpage",
        "title_de": "Empfohlene Links – Doris Gunsch",
        "title_en": "Recommended Links – Doris Gunsch",
        "desc_de": "Empfehlenswerte Partner, Publikationen und weiterführende Ressourcen rund um Führung und Organisationsentwicklung.",
        "desc_en": "Recommended partners, publications and further resources on leadership and organisational development.",
    },
    "kontakt.html": {
        "page": "kontakt",
        "active": "kontakt",
        "schema": "contact",
        "title_de": "Kontakt & Erstgespräch – Doris Gunsch",
        "title_en": "Contact & Initial Meeting – Doris Gunsch",
        "desc_de": "Kontaktieren Sie Doris Gunsch in Osnabrück: Newtonstraße 3, Telefon +49 (0)541 14496, E-Mail dg@doris-gunsch.eu.",
        "desc_en": "Contact Doris Gunsch in Osnabrück: Newtonstraße 3, phone +49 (0)541 14496, email dg@doris-gunsch.eu.",
    },
    "impressum.html": {
        "page": "legal",
        "active": "legal",
        "legal_page": "impressum",
        "schema": "webpage",
        "title_de": "Impressum – Doris Gunsch",
        "title_en": "Legal Notice – Doris Gunsch",
        "desc_de": "Impressum und Anbieterkennzeichnung — Doris Gunsch, Psychologische Managementberatung, Osnabrück.",
        "desc_en": "Legal notice and provider information — Doris Gunsch, Psychological Management Consulting, Osnabrück.",
    },
    "datenschutz.html": {
        "page": "legal",
        "active": "legal",
        "legal_page": "datenschutz",
        "schema": "webpage",
        "title_de": "Datenschutz – Doris Gunsch",
        "title_en": "Privacy Policy – Doris Gunsch",
        "desc_de": "Datenschutzerklärung der Website doris-gunsch.eu — Informationen zur Verarbeitung personenbezogener Daten.",
        "desc_en": "Privacy policy for doris-gunsch.eu — information on the processing of personal data.",
    },
    "404.html": {
        "page": "error",
        "active": "",
        "schema": "webpage",
        "noindex": True,
        "no_hreflang": True,
        "title_de": "Seite nicht gefunden – Doris Gunsch",
        "title_en": "Page not found – Doris Gunsch",
        "desc_de": "Die angeforderte Seite wurde nicht gefunden. Zurück zur Startseite von Doris Gunsch.",
        "desc_en": "The requested page was not found. Return to the Doris Gunsch homepage.",
    },
}

META.update(STANDORTE_META)

SERVICE_SUB_PAGES = ("diagnostik", "team", "trainings", "coaching")

SIDEBAR_KEYS = ["home", "einsatzgebiete", "leistungen", "coaching", "trainings", "team", "diagnostik", "person", "psi", "referenzen", "links"]

LABELS = {
    "de": {
        "nav": "Navigation",
        "home": "Start",
        "einsatzgebiete": "Einsatzgebiete",
        "services": "Leistungen",
        "overview": "Übersicht",
        "coaching": "Coaching",
        "trainings": "Trainings & Seminare",
        "team": "Team & Prozess",
        "diagnostik": "Diagnostik",
        "person": "Zur Person",
        "psi": "PSI Aktuell",
        "referenzen": "Referenzen",
        "links": "Links",
        "impressum": "Impressum",
        "datenschutz": "Datenschutz",
        "contact": "Kontakt",
        "lang": "Sprache",
        "theme_to_dark": "Dunkelmodus aktivieren",
        "menu": "Menü öffnen",
        "logo": "Doris Gunsch – Startseite",
        "footer_nav": "Fußnavigation",
        "back_home": "← Zurück zur Startseite",
        "back_services": "← Zurück zu Leistungen",
        "breadcrumb_aria": "Brotkrumen-Navigation",
        "next_step": "Nächster Schritt",
    },
    "en": {
        "nav": "Navigation",
        "home": "Home",
        "einsatzgebiete": "Service areas",
        "services": "Services",
        "overview": "Overview",
        "coaching": "Coaching",
        "trainings": "Training & Seminars",
        "team": "Team & Process",
        "diagnostik": "Diagnostics",
        "person": "About",
        "psi": "PSI News",
        "referenzen": "References",
        "links": "Links",
        "impressum": "Legal Notice",
        "datenschutz": "Privacy",
        "contact": "Contact",
        "lang": "Language",
        "theme_to_dark": "Switch to dark mode",
        "menu": "Open menu",
        "logo": "Doris Gunsch – Home",
        "footer_nav": "Footer navigation",
        "back_home": "← Back to home",
        "back_services": "← Back to services",
        "breadcrumb_aria": "Breadcrumb navigation",
        "next_step": "Next step",
    },
}

SERVICE_DETAIL_PAGES = {"coaching.html", "trainings.html", "team.html", "diagnostik.html"}

PAGE_TRAILS = {
    "einsatzgebiete.html": [("home", "index.html"), ("einsatzgebiete", None)],
    "leistungen.html": [("home", "index.html"), ("services", None)],
    "coaching.html": [("home", "index.html"), ("services", "leistungen.html"), ("coaching", None)],
    "trainings.html": [("home", "index.html"), ("services", "leistungen.html"), ("trainings", None)],
    "team.html": [("home", "index.html"), ("services", "leistungen.html"), ("team", None)],
    "diagnostik.html": [("home", "index.html"), ("services", "leistungen.html"), ("diagnostik", None)],
    "person.html": [("home", "index.html"), ("person", None)],
    "psi-aktuell.html": [("home", "index.html"), ("psi", None)],
    "referenzen.html": [("home", "index.html"), ("referenzen", None)],
    "links.html": [("home", "index.html"), ("links", None)],
    "kontakt.html": [("home", "index.html"), ("contact", None)],
    "impressum.html": [("home", "index.html"), ("impressum", None)],
    "datenschutz.html": [("home", "index.html"), ("datenschutz", None)],
}

NEXT_STEP = {
    "coaching.html": {
        "de": {
            "title": "Coaching-Gespräch vereinbaren",
            "text": "Sie möchten Klarheit in einer konkreten Führungssituation? Schreiben Sie mir — wir finden einen passenden Rahmen.",
        },
        "en": {
            "title": "Arrange a coaching conversation",
            "text": "Looking for clarity in a specific leadership situation? Get in touch — we will find a format that fits.",
        },
    },
    "trainings.html": {
        "de": {
            "title": "Training oder Seminar anfragen",
            "text": "Ob kompakter Workshop oder mehrtägiges Seminar — ich stimme Inhalt und Format mit Ihnen ab.",
        },
        "en": {
            "title": "Request training or a seminar",
            "text": "Whether a compact workshop or multi-day seminar — I will align content and format with your needs.",
        },
    },
    "team.html": {
        "de": {
            "title": "Prozessbegleitung anfragen",
            "text": "Steht Ihr Team vor einer Veränderung oder einem Konflikt? Lassen Sie uns besprechen, wie ich Sie begleiten kann.",
        },
        "en": {
            "title": "Request process facilitation",
            "text": "Is your team facing change or conflict? Let us discuss how I can support you.",
        },
    },
    "diagnostik.html": {
        "de": {
            "title": "Diagnostik besprechen",
            "text": "Sie benötigen fundierte Persönlichkeits- oder Teambewertungen? Ich berate Sie zu passenden Verfahren.",
        },
        "en": {
            "title": "Discuss diagnostics",
            "text": "Need sound personality or team assessments? I will advise you on suitable methods.",
        },
    },
}


def nav_prefix(filename: str) -> str:
    return "../" * filename.count("/")


def content_asset(lang: str, filename: str) -> str:
    return "../" * (filename.count("/") + (1 if lang == "en" else 0))


def home_href(filename: str) -> str:
    return nav_prefix(filename) + "index.html"


def strip_wrapped_artifacts(content: str) -> str:
    """Remove shell blocks preserved inside extracted <main> content."""
    patterns = [
        r'^\s*<nav class="breadcrumbs-wrap[^>]*>.*?</nav>\s*',
        r'^\s*<div class="container page-back">\s*.*?\s*</div>\s*',
    ]
    for pattern in patterns:
        prev = None
        while prev != content:
            prev = content
            content = re.sub(pattern, "", content, count=1, flags=re.DOTALL)

    content = re.sub(
        r'\s*<aside class="container page-next-step">\s*.*?\s*</aside>\s*$',
        "",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'\s*<details class="home-standorte">.*?</details>\s*',
        "\n        <!-- HOME_STANDORTE -->\n",
        content,
        count=1,
        flags=re.DOTALL,
    )
    return content


def breadcrumbs(lang: str, filename: str, asset: str, meta: Optional[dict] = None) -> str:
    meta = meta or META.get(filename, {})
    custom_label = meta.get("breadcrumb_" + lang)
    if custom_label:
        L = LABELS[lang]
        return f"""      <nav class="breadcrumbs-wrap container" aria-label="{L["breadcrumb_aria"]}">
        <ol class="breadcrumbs">
        <li class="breadcrumbs__item"><a href="{home_href(filename)}">{L["home"]}</a></li>
        <li class="breadcrumbs__item" aria-current="page">{custom_label}</li>
        </ol>
      </nav>
"""

    trail = PAGE_TRAILS.get(filename)
    if not trail:
        return ""

    L = LABELS[lang]
    items = []
    for label_key, href in trail:
        label = L[label_key]
        if href:
            items.append(
                f'        <li class="breadcrumbs__item">'
                f'<a href="{nav_prefix(filename)}{href}">{label}</a></li>'
            )
        else:
            items.append(
                f'        <li class="breadcrumbs__item" aria-current="page">{label}</li>'
            )

    return f"""      <nav class="breadcrumbs-wrap container" aria-label="{L["breadcrumb_aria"]}">
        <ol class="breadcrumbs">
{chr(10).join(items)}
        </ol>
      </nav>
"""


def page_back(lang: str, filename: str, _asset: str) -> str:
    L = LABELS[lang]
    nav = nav_prefix(filename)
    if filename in SERVICE_DETAIL_PAGES:
        href = f"{nav}leistungen.html"
        label = L["back_services"]
    else:
        href = home_href(filename)
        label = L["back_home"]
    return f"""      <div class="container page-back">
        <a href="{href}" class="btn btn-secondary btn-back">{label}</a>
      </div>
"""


def next_step_block(lang: str, filename: str, _asset: str = "") -> str:
    step = NEXT_STEP.get(filename, {}).get(lang)
    if not step:
        return ""

    L = LABELS[lang]
    nav = nav_prefix(filename)
    return f"""      <aside class="container page-next-step">
        <div class="card card--lead page-next-step__card">
          <p class="eyebrow">{L["next_step"]}</p>
          <h2 class="page-next-step__title">{step["title"]}</h2>
          <p class="page-next-step__text">{step["text"]}</p>
          <a href="{nav}kontakt.html" class="btn btn-primary">{L["contact"]}</a>
        </div>
      </aside>
"""


def extract_main(html: str) -> str:
    start_tag = html.rfind("<main")
    if start_tag != -1:
        content_start = html.find(">", start_tag) + 1
        end_tag = html.rfind("</main>")
        if end_tag > content_start:
            content = html[content_start:end_tag].strip()
            if content.lstrip().startswith("<!DOCTYPE"):
                return extract_main(content)
            return content

    m = re.search(r'<div class="container legal-page">(.*)</div>\s*</main>', html, re.DOTALL)
    if m:
        return f'    <div class="container legal-page">{m.group(1).strip()}\n    </div>'
    return ""


def active_class(key: str, active: str) -> str:
    return ' is-active' if key == active else ""


def sidebar(lang, active, prefix="", legal_page=None):
    L = LABELS[lang]
    p = prefix
    keys = {
        "home": f'{p}index.html',
        "einsatzgebiete": f'{p}einsatzgebiete.html',
        "leistungen": f'{p}leistungen.html',
        "coaching": f'{p}coaching.html',
        "trainings": f'{p}trainings.html',
        "team": f'{p}team.html',
        "diagnostik": f'{p}diagnostik.html',
        "person": f'{p}person.html',
        "psi": f'{p}psi-aktuell.html',
        "referenzen": f'{p}referenzen.html',
        "links": f'{p}links.html',
    }
    emphasis_keys = {"einsatzgebiete", "person", "psi", "referenzen", "links"}

    def a(k, label, extra=""):
        emph = " sidebar-link--emphasis" if k in emphasis_keys else ""
        return f'          <a href="{keys[k]}" class="sidebar-link{active_class(k, active)}{emph}{extra}">{label}</a>'

    services_open = active == "leistungen" or active in SERVICE_SUB_PAGES
    dropdown_state = " sidebar-dropdown--active" if services_open else ""
    open_attr = " open" if services_open else ""
    overview_active = active_class("leistungen", active)
    imp_cls = ' class="is-active"' if legal_page == "impressum" else ""
    ds_cls = ' class="is-active"' if legal_page == "datenschutz" else ""
    kontakt_active = ' is-active' if active == "kontakt" else ""
    return f'''  <aside class="site-sidebar" id="site-sidebar" aria-label="{L["nav"]}">
    <nav class="sidebar-nav">
      {a("home", L["home"])}
      {a("einsatzgebiete", L["einsatzgebiete"])}
      <details class="sidebar-dropdown{dropdown_state}"{open_attr}>
        <summary class="sidebar-dropdown__summary">
          <a href="{keys["leistungen"]}" class="sidebar-link sidebar-link--emphasis sidebar-dropdown__link{overview_active}">{L["overview"]}</a>
          <span class="sidebar-dropdown__toggle" aria-hidden="true">
            <svg class="sidebar-dropdown__chevron" viewBox="0 0 10 6"><path d="M1 1l4 4 4-4"></path></svg>
          </span>
        </summary>
        <div class="sidebar-dropdown__panel">
          {a("diagnostik", L["diagnostik"], " sidebar-link--sub")}
          {a("team", L["team"], " sidebar-link--sub")}
          {a("trainings", L["trainings"], " sidebar-link--sub")}
          {a("coaching", L["coaching"], " sidebar-link--sub")}
        </div>
      </details>
      {a("person", L["person"])}
      {a("psi", L["psi"])}
      {a("referenzen", L["referenzen"])}
      {a("links", L["links"])}
    </nav>
    <div class="sidebar-footer">
      <a href="{p}kontakt.html" class="btn btn-primary btn-header{kontakt_active}">{L["contact"]}</a>
      <div class="sidebar-lang" role="group" aria-label="{L["lang"]}">
        <button type="button" class="sidebar-lang__btn" data-lang="de" aria-pressed="false">DE</button>
        <button type="button" class="sidebar-lang__btn" data-lang="en" aria-pressed="false">EN</button>
      </div>
    </div>
    <div class="sidebar-legal">
      <a href="{p}impressum.html"{imp_cls}>{L["impressum"]}</a>
      <a href="{p}datenschutz.html"{ds_cls}>{L["datenschutz"]}</a>
    </div>
  </aside>'''


def lang_switcher_html(L: dict) -> str:
    return f"""            <div class="lang-switcher" id="lang-switcher">
              <button type="button" class="lang-switcher__trigger" id="lang-switcher-trigger" aria-haspopup="listbox" aria-expanded="false" aria-controls="lang-switcher-menu" aria-label="{L["lang"]}">
                <span class="lang-switcher__current">DE</span>
                <svg class="lang-switcher__chevron" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4"></path></svg>
              </button>
              <ul class="lang-switcher__menu" id="lang-switcher-menu" role="listbox" aria-label="{L["lang"]}">
                <li role="presentation">
                  <button type="button" class="lang-switcher__option" role="option" data-lang="de">DE</button>
                </li>
                <li role="presentation">
                  <button type="button" class="lang-switcher__option" role="option" data-lang="en">EN</button>
                </li>
              </ul>
            </div>"""


def build_page(lang: str, filename: str, main_content: str, out_path: Path):
    meta = META[filename]
    L = LABELS[lang]
    active = meta["active"]
    is_en = lang == "en"
    nav = nav_prefix(filename)
    asset = content_asset(lang, filename)
    home_link = home_href(filename)
    active_kontakt = ' is-active' if active == "kontakt" else ""
    scroll_progress = """      <div class="header-scroll-progress" aria-hidden="true">
        <span class="header-scroll-progress__fill"></span>
      </div>"""
    raw_title = meta["title_" + lang]
    raw_desc = meta["desc_" + lang]
    city = meta.get("city_" + lang)
    title = html.escape(raw_title, quote=True)
    description = html.escape(raw_desc, quote=True)
    seo_head = f"""{canonical_hreflang(filename, lang, include_hreflang=not meta.get("no_hreflang"))}
{llms_head_link()}
{open_graph(filename, lang, raw_title, raw_desc)}
{structured_data(filename, lang, raw_title, raw_desc, meta.get("schema", "webpage"), city=city)}"""
    robots_meta = '  <meta name="robots" content="noindex, follow">\n' if meta.get("noindex") else ""
    page_nav = ""
    page_footer = ""
    if filename not in ("index.html", "404.html"):
        page_nav = page_back(lang, filename, asset)
        page_footer = next_step_block(lang, filename, asset)

    logo_label = L["logo"]
    page_html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script>
    (function () {{
      var saved = localStorage.getItem('dg-theme');
      var theme = saved === 'dark' || saved === 'light'
        ? saved
        : (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.setAttribute('data-theme', theme);
    }})();
  </script>
{robots_meta}  <title>{title}</title>
  <meta name="description" content="{description}">
{performance_head(asset)}
{favicon_head(asset)}
{seo_head}
</head>
<body data-page="{meta["page"]}">

<div class="site-shell">
  <div class="sidebar-overlay" aria-hidden="true"></div>

  <div class="site-content">
    <header class="site-header" id="top">
      <div class="container header-inner">
        <a href="{home_link}" class="logo" aria-label="{logo_label}">
{logo_image(asset, label="Doris Gunsch")}
        </a>
        <div class="header-right">
          <div class="header-controls">
            <a href="{nav}kontakt.html" class="btn btn-primary btn-header{active_kontakt}">{L["contact"]}</a>
{lang_switcher_html(L)}
            <button type="button" class="theme-toggle" id="theme-toggle" aria-pressed="false" aria-label="{L["theme_to_dark"]}">
              <svg class="theme-icon theme-icon--sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"></path></svg>
              <svg class="theme-icon theme-icon--moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 14.5A8.5 8.5 0 0 1 9.5 3 7 7 0 1 0 21 14.5z"></path></svg>
            </button>
          </div>
          <button type="button" class="sidebar-toggle" aria-label="{L["menu"]}" aria-expanded="false" aria-controls="site-sidebar">
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </div>
{scroll_progress}
    </header>

    <main>
{page_nav}{main_content}
{page_footer}    </main>

    <footer class="site-footer">
      <div class="container footer-inner">
        <p class="footer-brand">Doris Gunsch</p>
        <p class="footer-tagline">{"Psychologische Managementberatung" if lang == "de" else "Psychological Management Consulting"}</p>
        <nav aria-label="{L["footer_nav"]}">
          <ul>
            <li><a href="{nav}kontakt.html">{L["contact"]}</a></li>
            <li><a href="{nav}leistungen.html">{"Leistungen" if lang == "de" else "Services"}</a></li>
            <li><a href="{nav}person.html">{"Zur Person" if lang == "de" else "About"}</a></li>
            <li><a href="{nav}impressum.html">{L["impressum"]}</a></li>
            <li><a href="{nav}datenschutz.html">{L["datenschutz"]}</a></li>
          </ul>
        </nav>
        <p class="footer-copy">&copy; <span id="year"></span> Doris Gunsch</p>
      </div>
    </footer>
  </div>
{sidebar(lang, active, nav, meta.get("legal_page"))}
</div>

  <script src="{asset}js/site.js"></script>
</body>
</html>
'''
    out_path.write_text(page_html, encoding="utf-8")


def main():
    en_dir = ROOT / "en"
    en_dir.mkdir(exist_ok=True)

    for filename in META:
        de_src = ROOT / filename
        if de_src.exists():
            content = strip_wrapped_artifacts(extract_main(de_src.read_text(encoding="utf-8")))
            build_page("de", filename, content, de_src)

        if filename == "404.html":
            continue

        en_fragment = en_dir / filename
        if en_fragment.exists():
            content = strip_wrapped_artifacts(extract_main(en_fragment.read_text(encoding="utf-8")))
            if filename in ("impressum.html", "datenschutz.html") and "legal-page" not in content:
                content = f'    <div class="container legal-page">\n{content}\n    </div>'
            build_page("en", filename, content, en_fragment)

    page_count = sum(
        1
        for f in META
        if (ROOT / f).exists() and (f == "404.html" or (en_dir / f).exists())
    )
    print("Wrapped", page_count, "pages (DE + EN)")


if __name__ == "__main__":
    main()
