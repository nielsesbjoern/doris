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
    ASSET_VERSION,
    clean_internal_hrefs,
    canonical_hreflang,
    llms_head_link,
    favicon_head,
    logo_image,
    open_graph,
    page_href,
    performance_head,
    structured_data,
    wizard_href,
    wizard_href_for_page,
)
from contact_config import FORMSPREE_ENDPOINT  # noqa: E402
from standorte_data import STANDORTE_META  # noqa: E402
from psi_bridge_data import TEXT as PSI_TEXT  # noqa: E402

META = {
    "index.html": {
        "page": "home",
        "active": "home",
        "schema": "business",
        "title_de": "Psychologische Managementberatung Osnabrück – Doris Gunsch",
        "title_en": "Psychological Management Consulting Osnabrück – Doris Gunsch",
        "desc_de": "Coaching, Trainings und Prozessbegleitung für Führungskräfte in Veränderungs- und Konfliktsituationen. Büro in Osnabrück, im gesamten DACH-Raum tätig.",
        "desc_en": "Coaching, training and process facilitation for leaders in change and conflict situations. Based in Osnabrück, working across the DACH region.",
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
        "title_de": "Einsatzgebiete – Von Osnabrück im DACH-Raum | Doris Gunsch",
        "title_en": "Service Areas – From Osnabrück across the DACH region | Doris Gunsch",
        "desc_de": "Coaching und Beratung in Osnabrück, im DACH-Raum und hybrid — ausgewählte Einsatzorte in Hamburg, Berlin, Frankfurt, München, Zürich und weiteren Regionen.",
        "desc_en": "Coaching and consulting in Osnabrück, across the DACH region and hybrid — selected locations in Hamburg, Berlin, Frankfurt, Munich, Zurich and other regions.",
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
    "coaching-formate.html": {
        "page": "leistungen",
        "active": "formate",
        "schema": "webpage",
        "title_de": "Format-Finder – Welches Coaching passt? | Doris Gunsch",
        "title_en": "Format Finder – Which Coaching Fits? | Doris Gunsch",
        "desc_de": "Coaching-Formate interaktiv vergleichen: nach Anlass oder Durchführung — bis zu zwei Formate nebeneinander. Orientierung für Führungskräfte.",
        "desc_en": "Compare coaching formats interactively: by occasion or delivery — up to two formats side by side. Orientation for leaders.",
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
        "title_de": "Kontakt – Doris Gunsch",
        "title_en": "Contact – Doris Gunsch",
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

SIDEBAR_KEYS = ["home", "leistungen", "coaching", "trainings", "team", "diagnostik", "person", "einsatzgebiete", "referenzen", "links"]

SERVICE_SUB_PAGES = ("coaching", "formate", "trainings", "team", "diagnostik")
SIDEBAR_SERVICE_SUB_PAGES = ("coaching", "trainings", "team", "diagnostik")

SERVICE_PAGES_WITH_SUBNAV = frozenset({
    "leistungen.html",
    "coaching.html",
    "coaching-formate.html",
    "trainings.html",
    "team.html",
    "diagnostik.html",
})

SIDEBAR_LABEL_KEYS = {
    "home": "home",
    "einsatzgebiete": "einsatzgebiete",
    "leistungen": "services",
    "coaching": "coaching",
    "formate": "formate",
    "trainings": "trainings",
    "team": "team",
    "diagnostik": "diagnostik",
    "person": "person",
    "referenzen": "referenzen",
    "links": "links",
}

LABELS = {
    "de": {
        "nav": "Navigation",
        "home": "Start",
        "einsatzgebiete": "Einsatzgebiete",
        "services": "Leistungen",
        "coaching": "Coaching",
        "formate": "Format-Finder",
        "trainings": "Trainings & Seminare",
        "team": "Team & Prozess",
        "diagnostik": "Diagnostik",
        "person": "Zur Person",
        "referenzen": "Referenzen",
        "links": "Empfehlungen",
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
        "back_einsatzgebiete": "← Zurück zu Einsatzgebieten",
        "breadcrumb_aria": "Brotkrumen-Navigation",
        "next_step": "Nächster Schritt",
        "skip_link": "Zum Inhalt springen",
        "services_overview": "Übersicht",
    },
    "en": {
        "nav": "Navigation",
        "home": "Home",
        "einsatzgebiete": "Service areas",
        "services": "Services",
        "coaching": "Coaching",
        "formate": "Format finder",
        "trainings": "Training & Seminars",
        "team": "Team & Process",
        "diagnostik": "Diagnostics",
        "person": "About",
        "referenzen": "References",
        "links": "Recommendations",
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
        "back_einsatzgebiete": "← Back to service areas",
        "breadcrumb_aria": "Breadcrumb navigation",
        "next_step": "Next step",
        "skip_link": "Skip to main content",
        "services_overview": "Overview",
    },
}

SERVICE_DETAIL_PAGES = {
    "coaching.html",
    "coaching-formate.html",
    "trainings.html",
    "team.html",
    "diagnostik.html",
}

PAGE_TRAILS = {
    "einsatzgebiete.html": [("home", "index.html"), ("einsatzgebiete", None)],
    "leistungen.html": [("home", "index.html"), ("services", None)],
    "coaching.html": [("home", "index.html"), ("services", "leistungen.html"), ("coaching", None)],
    "coaching-formate.html": [
        ("home", "index.html"),
        ("services", "leistungen.html"),
        ("formate", None),
    ],
    "trainings.html": [("home", "index.html"), ("services", "leistungen.html"), ("trainings", None)],
    "team.html": [("home", "index.html"), ("services", "leistungen.html"), ("team", None)],
    "diagnostik.html": [("home", "index.html"), ("services", "leistungen.html"), ("diagnostik", None)],
    "person.html": [("home", "index.html"), ("person", None)],
    "referenzen.html": [("home", "index.html"), ("referenzen", None)],
    "links.html": [("home", "index.html"), ("links", None)],
    "kontakt.html": [("home", "index.html"), ("contact", None)],
    "impressum.html": [("home", "index.html"), ("impressum", None)],
    "datenschutz.html": [("home", "index.html"), ("datenschutz", None)],
}

NEXT_STEP = {
    "coaching-formate.html": {
        "de": {
            "title": "Format abstimmen",
            "text": "Sie haben ein Format im Blick oder möchten gemeinsam klären, was passt? Schreiben Sie mir — wir finden den passenden Rahmen.",
        },
        "en": {
            "title": "Align on a format",
            "text": "Have a format in mind or want to clarify together what fits? Get in touch — we will find a suitable approach.",
        },
    },
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
    return page_href("index.html", nav_prefix(filename))


def strip_wrapped_artifacts(content: str) -> str:
    """Remove shell blocks preserved inside extracted <main> content."""
    patterns = [
        r'^\s*<nav class="breadcrumbs-wrap[^>]*>.*?</nav>\s*',
        r'^\s*<div class="container page-back">\s*.*?\s*</div>\s*',
        r'^\s*<div class="(?:container sub-nav-wrap|sub-nav-wrap)">\s*(?:<div class="container">\s*)?.*?(?:</div>\s*)?</div>\s*',
        r'^\s*<!-- SERVICES_SUB_NAV -->\s*',
    ]
    for pattern in patterns:
        prev = None
        while prev != content:
            prev = content
            content = re.sub(pattern, "", content, count=1, flags=re.DOTALL)

    pattern_next_step = r'\s*<aside class="container page-next-step">\s*.*?\s*</aside>\s*$'
    prev = None
    while prev != content:
        prev = content
        content = re.sub(pattern_next_step, "", content, count=1, flags=re.DOTALL)
    content = re.sub(
        r'\s*<details class="home-standorte">.*?</details>\s*',
        "\n        <!-- HOME_STANDORTE -->\n",
        content,
        count=1,
        flags=re.DOTALL,
    )
    return content


def is_standort_page(filename: str) -> bool:
    return filename.startswith("standorte/")


def breadcrumbs(lang: str, filename: str, asset: str, meta: Optional[dict] = None) -> str:
    meta = meta or META.get(filename, {})
    custom_label = meta.get("breadcrumb_" + lang)
    if custom_label:
        L = LABELS[lang]
        nav = nav_prefix(filename)
        if is_standort_page(filename):
            return f"""      <nav class="breadcrumbs-wrap container" aria-label="{L["breadcrumb_aria"]}">
        <ol class="breadcrumbs">
        <li class="breadcrumbs__item"><a href="{home_href(filename)}">{L["home"]}</a></li>
        <li class="breadcrumbs__item"><a href="{page_href("einsatzgebiete.html", nav)}">{L["einsatzgebiete"]}</a></li>
        <li class="breadcrumbs__item" aria-current="page">{custom_label}</li>
        </ol>
      </nav>
"""
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
                f'<a href="{page_href(href, nav_prefix(filename))}">{label}</a></li>'
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


SERVICES_SUB_NAV_MARKER = "<!-- SERVICES_SUB_NAV -->"


def render_services_subnav(lang: str, active: str, filename: str) -> str:
    L = LABELS[lang]
    nav = nav_prefix(filename)
    items = (
        ("leistungen", "leistungen.html", "leistungen", False),
        ("coaching", "coaching.html", "coaching", False),
        ("trainings", "trainings.html", "trainings", False),
        ("team", "team.html", "team", False),
        ("diagnostik", "diagnostik.html", "diagnostik", False),
        ("formate", "coaching-formate.html", "formate", True),
    )
    links = []
    for key, href_file, active_key, featured in items:
        classes: list[str] = []
        if active == active_key:
            classes.append("is-active")
        if featured:
            classes.append("sub-nav__highlight")
        cls = f' class="{" ".join(classes)}"' if classes else ""
        label = L["services_overview"] if key == "leistungen" else L[SIDEBAR_LABEL_KEYS[key]]
        links.append(f'        <a href="{page_href(href_file, nav)}"{cls}>{label}</a>')
    aria = "Leistungsbereiche" if lang == "de" else "Service areas"
    return f"""{SERVICES_SUB_NAV_MARKER}
<div class="sub-nav-wrap">
      <div class="container">
      <nav class="sub-nav" aria-label="{aria}">
{chr(10).join(links)}
      </nav>
      </div>
    </div>"""


def strip_service_subnav(content: str) -> str:
    """Remove generated sub-nav blocks before re-injecting."""
    prev = None
    while prev != content:
        prev = content
        content = re.sub(
            r'\s*<div class="(?:container sub-nav-wrap|sub-nav-wrap)">\s*(?:<div class="container">\s*)?.*?(?:</div>\s*)?</div>\s*',
            "\n",
            content,
            count=1,
            flags=re.DOTALL,
        )
    content = re.sub(r'\s*<!-- SERVICES_SUB_NAV -->\s*', "\n", content)
    return content


def inject_services_subnav(content: str, lang: str, filename: str) -> str:
    if filename not in SERVICE_PAGES_WITH_SUBNAV:
        return content
    content = strip_service_subnav(content)
    block = render_services_subnav(lang, META[filename]["active"], filename).strip()
    page_back = re.search(r'(<div class="container page-back">\s*.*?\s*</div>)', content, re.DOTALL)
    if page_back:
        insert_at = page_back.end()
        return content[:insert_at] + "\n" + block + content[insert_at:]
    return block + "\n" + content


def page_back(lang: str, filename: str, _asset: str) -> str:
    L = LABELS[lang]
    nav = nav_prefix(filename)
    if filename == "coaching-formate.html":
        href = home_href(filename)
        label = L["back_home"]
    elif filename in SERVICE_DETAIL_PAGES:
        href = page_href("leistungen.html", nav)
        label = L["back_services"]
    elif is_standort_page(filename):
        href = page_href("einsatzgebiete.html", nav)
        label = L["back_einsatzgebiete"]
    else:
        href = home_href(filename)
        label = L["back_home"]
    return f"""      <div class="container page-back">
        <a href="{href}" class="btn btn-secondary btn-back">{label}</a>
      </div>
"""


def inject_wizard_cta_links(content: str, filename: str, link_prefix: str) -> str:
    """Prefill wizard deep-links on in-page service CTAs (not header/shell)."""
    href = wizard_href_for_page(filename, link_prefix)
    default = wizard_href(link_prefix)
    if href == default:
        return content
    needle = 'href="kontakt" class="btn btn-primary">'
    if needle not in content:
        return content
    return content.replace(needle, f'href="{href}" class="btn btn-primary">', 1)


def next_step_block(lang: str, filename: str, _asset: str = "") -> str:
    step = NEXT_STEP.get(filename, {}).get(lang)
    if not step:
        return ""

    L = LABELS[lang]
    href = wizard_href_for_page(filename, nav_prefix(filename))
    return f"""      <aside class="container page-next-step">
        <div class="card card--lead page-next-step__card">
          <p class="eyebrow">{L["next_step"]}</p>
          <p class="page-next-step__title">{step["title"]}</p>
          <p class="page-next-step__text">{step["text"]}</p>
          <a href="{href}" class="btn btn-primary">{L["contact"]}</a>
        </div>
      </aside>
"""


CONTACT_WIZARD_MARKER = "<!-- CONTACT_WIZARD -->"
CONTACT_WIZARD_SECTION = re.compile(
    r'<section class="section page-section section-contact-wizard" id="kontakt-anfrage">.*?</section>',
    re.DOTALL,
)


CONTACT_WIZARD_HEADER = re.compile(
    r'<header class="contact-wizard__header">.*?</header>\s*',
    re.DOTALL,
)


def contact_wizard_partial(lang: str, *, include_header: bool = True) -> str:
    path = ROOT / "partials" / f"contact-wizard.{lang}.html"
    partial = path.read_text(encoding="utf-8").strip()
    endpoint = html.escape(FORMSPREE_ENDPOINT, quote=True)
    partial = partial.replace('data-formspree-endpoint=""', f'data-formspree-endpoint="{endpoint}"')
    if not include_header:
        partial = CONTACT_WIZARD_HEADER.sub("", partial, count=1)
    return partial


HOME_CONTACT_CTA_MARKER = "<!-- HOME_CONTACT_CTA -->"


def home_wizard_phone_partial(lang: str) -> str:
    if lang == "de":
        return """    <div class="container home-wizard-phone">
      <p class="home-wizard-phone__label">Lieber telefonisch?</p>
      <a href="tel:+4954114496" class="btn btn-secondary">Anrufen</a>
    </div>"""
    return """    <div class="container home-wizard-phone">
      <p class="home-wizard-phone__label">Prefer to call?</p>
      <a href="tel:+4954114496" class="btn btn-secondary">Call</a>
    </div>"""


def sync_home_contact_wizard(html: str, lang: str) -> str:
    if HOME_CONTACT_CTA_MARKER not in html:
        return html
    block = contact_wizard_partial(lang) + "\n\n" + home_wizard_phone_partial(lang)
    return html.replace(HOME_CONTACT_CTA_MARKER, block)


def sync_contact_wizard(html: str, lang: str) -> str:
    if HOME_CONTACT_CTA_MARKER in html:
        return sync_home_contact_wizard(html, lang)
    partial = contact_wizard_partial(lang, include_header=False)
    if CONTACT_WIZARD_MARKER in html:
        return html.replace(CONTACT_WIZARD_MARKER, partial)
    if 'id="kontakt-anfrage"' in html:
        return CONTACT_WIZARD_SECTION.sub(partial, html, count=1)
    return html


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
        "home": page_href("index.html", p),
        "einsatzgebiete": page_href("einsatzgebiete.html", p),
        "leistungen": page_href("leistungen.html", p),
        "coaching": page_href("coaching.html", p),
        "formate": page_href("coaching-formate.html", p),
        "trainings": page_href("trainings.html", p),
        "team": page_href("team.html", p),
        "diagnostik": page_href("diagnostik.html", p),
        "person": page_href("person.html", p),
        "referenzen": page_href("referenzen.html", p),
        "links": page_href("links.html", p),
    }
    emphasis_keys = {"einsatzgebiete", "person", "referenzen", "links", "leistungen"}

    def a(k, label, extra=""):
        emph = " sidebar-link--emphasis" if k in emphasis_keys else ""
        return f'          <a href="{keys[k]}" class="sidebar-link{active_class(k, active)}{emph}{extra}">{label}</a>'

    services_open = active == "leistungen" or active in SERVICE_SUB_PAGES
    dropdown_state = " sidebar-dropdown--active" if services_open else ""
    open_attr = " open" if services_open else ""
    leistungen_active = active_class("leistungen", active)
    sub_links = "\n".join(
        a(k, L[SIDEBAR_LABEL_KEYS[k]], " sidebar-link--sub") for k in SIDEBAR_SERVICE_SUB_PAGES
    )
    imp_cls = ' class="is-active"' if legal_page == "impressum" else ""
    ds_cls = ' class="is-active"' if legal_page == "datenschutz" else ""
    kontakt_active = ' is-active' if active == "kontakt" else ""
    return f'''  <aside class="site-sidebar" id="site-sidebar" aria-label="{L["nav"]}">
    <nav class="sidebar-nav">
      {a("home", L["home"])}
      <details class="sidebar-dropdown{dropdown_state}"{open_attr}>
        <summary class="sidebar-dropdown__summary">
          <span class="sidebar-link sidebar-link--emphasis{leistungen_active}">{L["services"]}</span>
          <span class="sidebar-dropdown__toggle" aria-hidden="true">
            <svg class="sidebar-dropdown__chevron" viewBox="0 0 10 6"><path d="M1 1l4 4 4-4"></path></svg>
          </span>
        </summary>
        <div class="sidebar-dropdown__panel">
          <a href="{keys["leistungen"]}" class="sidebar-link sidebar-link--sub{leistungen_active}">{L["services_overview"]}</a>
{sub_links}
        </div>
      </details>
      {a("person", L["person"])}
      {a("einsatzgebiete", L["einsatzgebiete"])}
      {a("referenzen", L["referenzen"])}
      {a("links", L["links"])}
    </nav>
    <div class="sidebar-footer">
      <a href="{page_href("kontakt.html", p)}" class="btn btn-primary btn-header{kontakt_active}">{L["contact"]}</a>
      <div class="sidebar-lang" role="group" aria-label="{L["lang"]}">
        <button type="button" class="sidebar-lang__btn" data-lang="de" aria-pressed="false">DE</button>
        <button type="button" class="sidebar-lang__btn" data-lang="en" aria-pressed="false">EN</button>
      </div>
    </div>
    <div class="sidebar-legal">
      <a href="{page_href("impressum.html", p)}"{imp_cls}>{L["impressum"]}</a>
      <a href="{page_href("datenschutz.html", p)}"{ds_cls}>{L["datenschutz"]}</a>
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
{open_graph(filename, lang, raw_title, raw_desc, city=city)}
{structured_data(filename, lang, raw_title, raw_desc, meta.get("schema", "webpage"), city=city)}"""
    robots_meta = '  <meta name="robots" content="noindex, follow">\n' if meta.get("noindex") else ""
    page_nav = ""
    page_footer = ""
    if filename not in ("index.html", "404.html"):
        page_nav = page_back(lang, filename, asset)
        page_footer = next_step_block(lang, filename, asset)

    extra_scripts = ""
    if filename == "referenzen.html":
        extra_scripts = f'\n  <script src="{asset}js/referenzen.js?v={ASSET_VERSION}" defer></script>'
    elif filename == "coaching-formate.html":
        extra_scripts = f'\n  <script src="{asset}js/coaching-formats.js?v={ASSET_VERSION}" defer></script>'
    elif filename in ("kontakt.html", "index.html"):
        extra_scripts = (
            f'\n  <script src="{asset}js/contact-config.js?v={ASSET_VERSION}" defer></script>'
            f'\n  <script src="{asset}js/kontakt-wizard.js?v={ASSET_VERSION}" defer></script>'
        )

    logo_label = L["logo"]
    logo_priority = "high" if filename in ("index.html", "404.html") else "auto"
    page_html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="{asset}js/theme-init.js?v={ASSET_VERSION}"></script>
{robots_meta}  <title>{title}</title>
  <meta name="description" content="{description}">
{performance_head(asset, filename)}
{favicon_head(asset)}
{seo_head}
</head>
<body data-page="{meta["page"]}">
  <a href="#main-content" class="skip-link">{L["skip_link"]}</a>

<div class="site-shell">
  <div class="sidebar-overlay" aria-hidden="true"></div>

  <div class="site-content">
    <header class="site-header" id="top">
      <div class="container header-inner">
        <a href="{home_link}" class="logo" aria-label="{logo_label}">
{logo_image(asset, label="Doris Gunsch", fetchpriority=logo_priority)}
        </a>
        <div class="header-right">
          <div class="header-controls">
            <a href="{page_href("kontakt.html", nav)}" class="btn btn-primary btn-header{active_kontakt}">{L["contact"]}</a>
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

    <main id="main-content">
{page_nav}{main_content}
{page_footer}    </main>

    <footer class="site-footer">
      <div class="container footer-inner">
        <p class="footer-brand">Doris Gunsch</p>
        <p class="footer-tagline">{"Psychologische Managementberatung" if lang == "de" else "Psychological Management Consulting"}</p>
        <p class="footer-science">{PSI_TEXT[lang]["footer_science"]} · <a href="{page_href("person.html", nav)}">{PSI_TEXT[lang]["footer_science_link"]}</a></p>
        <nav aria-label="{L["footer_nav"]}">
          <ul>
            <li><a href="{page_href("kontakt.html", nav)}">{L["contact"]}</a></li>
            <li><a href="{page_href("leistungen.html", nav)}">{"Leistungen" if lang == "de" else "Services"}</a></li>
            <li><a href="{page_href("person.html", nav)}">{"Zur Person" if lang == "de" else "About"}</a></li>
            <li><a href="{page_href("impressum.html", nav)}">{L["impressum"]}</a></li>
            <li><a href="{page_href("datenschutz.html", nav)}">{L["datenschutz"]}</a></li>
          </ul>
        </nav>
        <p class="footer-copy">&copy; <span id="year"></span> Doris Gunsch</p>
      </div>
    </footer>
  </div>
{sidebar(lang, active, nav, meta.get("legal_page"))}
</div>

  <script src="{asset}js/nav-return.js?v={ASSET_VERSION}" defer></script>
  <script src="{asset}js/site.js?v={ASSET_VERSION}" defer></script>{extra_scripts}
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
            raw = de_src.read_text(encoding="utf-8")
            content = clean_internal_hrefs(
                strip_wrapped_artifacts(extract_main(sync_contact_wizard(raw, "de")))
            )
            content = inject_wizard_cta_links(content, filename, nav_prefix(filename))
            content = inject_services_subnav(content, "de", filename)
            build_page("de", filename, content, de_src)

        if filename == "404.html":
            en_404_main = """      <section class="page-section page-section--hero">
        <div class="container">
          <h1>Page not found</h1>
          <p class="lead">The requested page does not exist or has been moved.</p>
          <p><a href="./" class="btn btn-primary">Back to home</a></p>
        </div>
      </section>"""
            build_page("en", "404.html", en_404_main, en_dir / "404.html")
            continue

        en_fragment = en_dir / filename
        if en_fragment.exists():
            raw = en_fragment.read_text(encoding="utf-8")
            content = clean_internal_hrefs(
                strip_wrapped_artifacts(extract_main(sync_contact_wizard(raw, "en")))
            )
            content = inject_wizard_cta_links(content, filename, nav_prefix(filename))
            if filename in ("impressum.html", "datenschutz.html") and "legal-page" not in content:
                content = f'    <div class="container legal-page">\n{content}\n    </div>'
            content = inject_services_subnav(content, "en", filename)
            build_page("en", filename, content, en_fragment)

    page_count = sum(
        1
        for f in META
        if (ROOT / f).exists() and (f == "404.html" or (en_dir / f).exists())
    )
    print("Wrapped", page_count, "pages (DE + EN)")


if __name__ == "__main__":
    main()
