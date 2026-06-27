"""Content and SEO metadata for city landing pages (DE + EN)."""

from standorte_metro_cities import METRO_CITIES
from standorte_zurich import ZUERICH

REGION_SLUGS = ["osnabrueck", "oldenburg", "hannover", "bremen", "muenster"]
METRO_SLUGS = ["hamburg", "berlin", "frankfurt", "muenchen", "duesseldorf", "zuerich"]
ORPHAN_SLUGS: list[str] = []
CITY_SLUGS = REGION_SLUGS + METRO_SLUGS + ORPHAN_SLUGS

STANDORT_UI = {
    "de": {
        "mini_case_title": "Beispielszenario zur Veranschaulichung",
        "mini_case_disclaimer": (
            "Das folgende Beispiel ist anonymisiert und frei erfunden — es dient "
            "ausschließlich der Veranschaulichung typischer Anliegen und beschreibt "
            "kein konkretes Mandat."
        ),
        "logistics_title": "Erreichbarkeit & Termine vor Ort",
        "related_title": "Weitere Einsatzorte in der Nähe",
        "format_teaser_kicker": "Coaching-Formate",
        "format_teaser_title": "Welches Format passt zu Ihrem Anliegen?",
        "format_teaser_text": (
            "Einzelcoaching, Intensiv-Termine oder Prozessbegleitung — "
            "im Format-Finder vergleichen Sie Formate nach Anlass und Durchführung."
        ),
        "format_teaser_btn": "Zum Format-Finder",
    },
    "en": {
        "mini_case_title": "Illustrative example scenario",
        "mini_case_disclaimer": (
            "The following example is anonymised and fictional — it is for "
            "illustration only and does not describe a specific mandate."
        ),
        "logistics_title": "Travel & on-site sessions",
        "related_title": "Further locations nearby",
        "format_teaser_kicker": "Coaching formats",
        "format_teaser_title": "Which format fits your situation?",
        "format_teaser_text": (
            "Individual coaching, intensive sessions or process facilitation — "
            "compare formats by occasion and delivery in the format finder."
        ),
        "format_teaser_btn": "Open format finder",
    },
}

RELATED_SLUGS: dict[str, list[str]] = {
    "osnabrueck": ["muenster", "oldenburg", "bremen", "hannover"],
    "muenster": ["osnabrueck", "oldenburg", "hannover"],
    "oldenburg": ["osnabrueck", "bremen", "hannover"],
    "hannover": ["bremen", "hamburg", "osnabrueck"],
    "bremen": ["hamburg", "hannover", "osnabrueck"],
    "hamburg": ["bremen", "hannover", "berlin"],
    "berlin": ["hamburg", "hannover", "frankfurt"],
    "frankfurt": ["duesseldorf", "muenchen", "berlin"],
    "muenchen": ["frankfurt", "duesseldorf", "zuerich"],
    "duesseldorf": ["frankfurt", "muenchen", "hannover"],
    "zuerich": ["muenchen", "frankfurt", "hamburg"],
}

REACH_FEATURED_SLUGS = [
    "osnabrueck",
    "muenster",
    "hamburg",
    "berlin",
    "frankfurt",
    "muenchen",
    "zuerich",
]

HOME_GROUPS = {
    "de": [
        ("Nordwesten", ["osnabrueck", "oldenburg", "hannover", "bremen", "muenster"]),
        (
            "Weitere Städte",
            ["hamburg", "berlin", "frankfurt", "muenchen", "duesseldorf", "zuerich"],
        ),
    ],
    "en": [
        ("North-west Germany", ["osnabrueck", "oldenburg", "hannover", "bremen", "muenster"]),
        (
            "Further cities",
            ["hamburg", "berlin", "frankfurt", "muenchen", "duesseldorf", "zuerich"],
        ),
    ],
}

REACH_COPY = {
    "de": {
        "places_kicker": "Auszug der Einsatzorte",
        "more_summary": "Weitere Standorte",
    },
    "en": {
        "places_kicker": "Selected locations",
        "more_summary": "Further locations",
    },
}

EINSATZGEBIETE_COPY = {
    "de": {
        "eyebrow": "Einsatzgebiete",
        "h1": "Von Osnabrück aus im gesamten DACH-Raum im Einsatz",
        "lead": "Beratung, Coaching und Trainings für Führungskräfte und Organisationen in Deutschland, Österreich und der Schweiz.",
        "body": "Vor Ort in Osnabrück, in vielen Regionen des DACH-Raums beim Kunden und in zahlreichen Formaten auch hybrid.",
        "note": "Ausgewählte Einsatzorte in Hamburg, Berlin, Hannover, Frankfurt, München, Münster, Zürich und weiteren Regionen.",
        "places_aria": "Ausgewählte Einsatzorte",
    },
    "en": {
        "eyebrow": "Service areas",
        "h1": "From Osnabrück, working across the DACH region",
        "lead": "Consulting, coaching and training for leaders and organisations in Germany, Austria and Switzerland.",
        "body": "On site in Osnabrück, at client locations across the DACH region, and in many formats also hybrid.",
        "note": "Selected locations in Hamburg, Berlin, Hanover, Frankfurt, Munich, Münster, Zurich and other regions.",
        "places_aria": "Selected locations",
    },
}

REACH_DESCRIPTIONS = {
    "osnabrueck": {
        "de": "Büro Newtonstraße 3 — Coachings und Beratung vor Ort",
        "en": "Office on Newtonstraße — coaching and consulting on site",
    },
    "hamburg": {
        "de": "Konzerne, Häfen, viele Schnittstellen und hohe Sichtbarkeit",
        "en": "Leadership in complex organisations",
    },
    "berlin": {
        "de": "Verbände, Transformation, institutionelle und politische Nähe",
        "en": "Associations, transformation, institutional contexts",
    },
    "frankfurt": {
        "de": "Finanzwirtschaft, Entscheidungsdruck, hybride Begleitung",
        "en": "Hybrid support under high decision pressure",
    },
    "muenchen": {
        "de": "Industrie, Konzerne, leistungsorientierte Führungsteams",
        "en": "Coaching in performance-oriented work environments",
    },
    "muenster": {
        "de": "Verwaltung, Bildung und institutionelle Kontexte",
        "en": "Administration, education and institutional contexts",
    },
    "oldenburg": {
        "de": "Gesundheitswesen, Sozialwirtschaft und regionale Träger",
        "en": "Healthcare, social sector and regional institutions",
    },
    "zuerich": {
        "de": "Internationaler Führungskontext",
        "en": "International leadership context",
    },
}

# Map markers for assets/map-dach.svg (build_map_dach.py).
# label_side: -1 left / 1 right / 0 centered below
MAP_CITIES = [
    {
        "slug": "osnabrueck",
        "name_de": "Osnabrück",
        "name_en": "Osnabrück",
        "lon": 8.0472,
        "lat": 52.2799,
        "home": True,
        "ring": False,
        "link": True,
        "label_side": 0,
        "label_dx": 0,
        "label_dy": 28,
    },
    {
        "slug": "hamburg",
        "name_de": "Hamburg",
        "name_en": "Hamburg",
        "lon": 9.9937,
        "lat": 53.5511,
        "home": False,
        "ring": True,
        "link": True,
        "label_side": 1,
        "label_dx": 10,
        "label_dy": -2,
    },
    {
        "slug": "berlin",
        "name_de": "Berlin",
        "name_en": "Berlin",
        "lon": 13.4050,
        "lat": 52.5200,
        "home": False,
        "ring": True,
        "link": True,
        "label_side": -1,
        "label_dx": -10,
        "label_dy": 0,
    },
    {
        "slug": "hannover",
        "name_de": "Hannover",
        "name_en": "Hanover",
        "lon": 9.7320,
        "lat": 52.3759,
        "home": False,
        "ring": False,
        "link": True,
        "label_side": 1,
        "label_dx": 10,
        "label_dy": 0,
    },
    {
        "slug": "bremen",
        "name_de": "Bremen",
        "name_en": "Bremen",
        "lon": 8.8017,
        "lat": 53.0793,
        "home": False,
        "ring": False,
        "link": True,
        "label_side": -1,
        "label_dx": -10,
        "label_dy": 0,
    },
    {
        "slug": "oldenburg",
        "name_de": "Oldenburg",
        "name_en": "Oldenburg",
        "lon": 8.2146,
        "lat": 53.1435,
        "home": False,
        "ring": False,
        "link": True,
        "label_side": -1,
        "label_dx": -10,
        "label_dy": -8,
        "hit_r": 12,
    },
    {
        "slug": "muenster",
        "name_de": "Münster",
        "name_en": "Münster",
        "lon": 7.6261,
        "lat": 51.9607,
        "home": False,
        "ring": False,
        "link": True,
        "label_side": 1,
        "label_dx": 10,
        "label_dy": 4,
        "hit_r": 12,
    },
    {
        "slug": "duesseldorf",
        "name_de": "Düsseldorf",
        "name_en": "Düsseldorf",
        "lon": 6.7735,
        "lat": 51.2277,
        "home": False,
        "ring": False,
        "link": True,
        "label_side": 1,
        "label_dx": 10,
        "label_dy": 0,
        "hit_r": 10,
    },
    {
        "slug": "frankfurt",
        "name_de": "Frankfurt",
        "name_en": "Frankfurt",
        "lon": 8.6821,
        "lat": 50.1109,
        "home": False,
        "ring": True,
        "link": True,
        "label_side": 1,
        "label_dx": 10,
        "label_dy": 0,
        "hit_r": 14,
    },
    {
        "slug": "muenchen",
        "name_de": "München",
        "name_en": "Munich",
        "lon": 11.5820,
        "lat": 48.1351,
        "home": False,
        "ring": True,
        "link": True,
        "label_side": -1,
        "label_dx": -10,
        "label_dy": 0,
        "hit_r": 14,
    },
    {
        "slug": "zuerich",
        "name_de": "Zürich",
        "name_en": "Zurich",
        "lon": 8.5417,
        "lat": 47.3769,
        "home": False,
        "ring": False,
        "link": True,
        "label_side": 0,
        "label_dx": 0,
        "label_dy": 14,
        "hit_r": 13,
    },
]

MAP_SUBMAP_CITIES = []

MAP_SLUGS = [city["slug"] for city in MAP_CITIES if city.get("slug")]

HOME_STANDORTE = {
    "de": {
        "summary": "Beratung in Ihrer Region",
        "intro": "Coaching und Prozessbegleitung für Führungskräfte — Büro in Osnabrück, Mandate im Nordwesten und im gesamten DACH-Raum.",
    },
    "en": {
        "summary": "Consulting in your region",
        "intro": "Coaching and process facilitation for leaders — based in Osnabrück, with mandates across north-west Germany and the DACH region.",
    },
}

CITIES = {
    "osnabrueck": {
        "name_de": "Osnabrück",
        "name_en": "Osnabrück",
        "module_order": [
            "hero",
            "intro",
            "collaboration",
            "mandates",
            "references",
            "formats",
            "faq",
            "services",
            "nearby",
            "cta",
        ],
        "de": {
            "seo_title": "Coaching & Beratung vor Ort in Osnabrück – Büro Newtonstraße | Doris Gunsch",
            "seo_desc": "Persönliche Beratung in Osnabrück: Coachings und Beratung in der Newtonstraße 3, Mandate im Mittelstand, Gesundheitswesen und öffentlicher Verwaltung der Region.",
            "home_label": "Osnabrück — Hauptsitz",
            "hero_kicker": "Osnabrück",
            "h1": "Beratung vor Ort — Büro in der Newtonstraße",
            "hero_lead": "Ihr Ansprechpartner vor Ort — für Führungskräfte in Mittelstand, Verwaltung und sozialen Trägern.",
            "intro_title": "Beratung mit kurzen Wegen",
            "intro": (
                "In Osnabrück bin ich zu Hause: Newtonstraße 3 ist mein Büro und Ausgangspunkt für "
                "Coaching, Trainings und Prozessbegleitung. Viele Mandate entstehen aus langjährigen "
                "Beziehungen im regionalen Mittelstand, in Kliniken und im öffentlichen Umfeld — "
                "Vertrauen entsteht hier oft durch persönliche Nähe und Verlässlichkeit über Jahre."
            ),
            "collaboration_title": "Zusammenarbeit in Osnabrück",
            "collaboration": (
                "Einzelcoachings und Beratung finden in der Regel in meinen Räumen in der Newtonstraße statt. "
                "Für Teams und längere Formate komme ich zu Ihnen — in Unternehmen, Verwaltung oder Klinikverbünden "
                "in Osnabrück und der direkten Umgebung. Kurze Wege, vertrauliche Settings, klare Absprachen."
            ),
            "mandates_title": "Typische Anliegen in Osnabrück",
            "mandates": [
                "Führungswechsel und Rollenklärung in etablierten Mittelstandsunternehmen",
                "Konflikte in Leitungsteams mit langer gemeinsamer Geschichte",
                "Begleitung von Veränderungsprozessen in Kliniken und sozialen Einrichtungen",
            ],
            "references_title": "Referenzen aus Osnabrück und der Region",
            "references_intro": "Ausgewählte Mandate und Kooperationen mit Bezug zu Osnabrück:",
            "references": [
                "Stadt Osnabrück",
                "Klinikum Osnabrück",
                "Universität Osnabrück, FB Persönlichkeitspsychologie",
                "IMPART GmbH, Osnabrück",
            ],
            "formats_title": "Formate vor Ort",
            "formats": [
                ("Einzelcoaching", "Vertrauliche Klärung komplexer Führungssituationen — im Büro oder bei Ihnen."),
                ("Teamentwicklung", "Workshops und Moderation für Führungsteams in Veränderungsphasen."),
                ("Diagnostik", "Fundierte Persönlichkeits- und Potenzialanalysen als Entscheidungsgrundlage."),
            ],
            "faq_title": "Häufige Fragen — Osnabrück",
            "faq": [
                (
                    "Wo finden Coachings statt?",
                    "In der Regel in meinen Räumen in der Newtonstraße 3 oder — nach Absprache — bei Ihnen im Unternehmen.",
                ),
                (
                    "Arbeiten Sie nur in Osnabrück?",
                    "Mein Büro liegt in Osnabrück; ich begleite Führungskräfte auch im gesamten DACH-Raum — viele Mandate beginnen jedoch in der Region.",
                ),
                (
                    "Für welche Branchen in Osnabrück?",
                    "Schwerpunkte sind Mittelstand, Gesundheitswesen, öffentliche Verwaltung und soziale Träger — passend zur Wirtschaftsstruktur der Region.",
                ),
                (
                    "Wie nehme ich Kontakt auf?",
                    "Telefonisch unter +49 (0)541 14496 oder per E-Mail an dg@doris-gunsch.eu — wir klären Anlass und passendes Format.",
                ),
            ],
            "services_title": "Passende Leistungen",
            "audience_title": "Geeignet für",
            "audience": "Geschäftsführung, Bereichsleitungen und Projektleitungen in Osnabrück und dem Osnabrücker Land.",
            "nearby_title": "Auch im Umfeld",
            "nearby": "Georgsmarienhütte, Melle, Bramsche, Bersenbrück — kurze Anfahrt vom Büro in Osnabrück.",
            "cta_title": "Kontakt in Osnabrück",
            "cta_text": "Sie führen in Osnabrück und suchen eine vertrauliche, erfahrene Begleitung? Ich freue mich auf Ihre Nachricht.",
            "cta_btn": "Kontakt aufnehmen",
        },
        "en": {
            "seo_title": "On-site Consulting in Osnabrück – Newtonstraße Office | Doris Gunsch",
            "seo_desc": "Personal consulting in Osnabrück: coaching and consulting at Newtonstraße 3, mandates in regional mid-market, healthcare and public administration.",
            "home_label": "Osnabrück — headquarters",
            "hero_kicker": "Osnabrück",
            "h1": "On-site consulting — office on Newtonstraße",
            "hero_lead": "Your local contact — for leaders in mid-sized business, public administration and social-sector organisations.",
            "intro_title": "Consulting with short distances",
            "intro": (
                "Osnabrück is my home base: Newtonstraße 3 is my office and starting point for "
                "coaching, training and process facilitation. Many mandates grow from long-standing "
                "relationships in the regional mid-market, hospitals and public sector — "
                "trust here is often built through personal proximity over years."
            ),
            "collaboration_title": "Working together in Osnabrück",
            "collaboration": (
                "Individual coaching and consulting usually take place at my Newtonstraße office. "
                "For teams and longer formats I come to you — in companies, administration or hospital "
                "networks in Osnabrück and the immediate area."
            ),
            "mandates_title": "Typical concerns in Osnabrück",
            "mandates": [
                "Leadership transitions and role clarification in established mid-sized companies",
                "Conflicts in leadership teams with a long shared history",
                "Supporting change processes in hospitals and social-sector institutions",
            ],
            "references_title": "References from Osnabrück and the region",
            "references_intro": "Selected mandates and collaborations linked to Osnabrück:",
            "references": [
                "Stadt Osnabrück",
                "Klinikum Osnabrück",
                "Universität Osnabrück, Department of Personality Psychology",
                "IMPART GmbH, Osnabrück",
            ],
            "formats_title": "Formats on site",
            "formats": [
                ("Individual coaching", "Confidential clarification of complex leadership situations — at the office or at your premises."),
                ("Team development", "Workshops and facilitation for leadership teams in phases of change."),
                ("Diagnostics", "Sound personality and potential analyses as a basis for decisions."),
            ],
            "faq_title": "Frequently asked questions — Osnabrück",
            "faq": [
                (
                    "Where do coaching sessions take place?",
                    "Usually at my office at Newtonstraße 3 or — by arrangement — at your organisation.",
                ),
                (
                    "Do you only work in Osnabrück?",
                    "My office is in Osnabrück; I also work with leaders across the DACH region — but many mandates start in the region.",
                ),
                (
                    "Which sectors in Osnabrück?",
                    "Focus areas include mid-sized business, healthcare, public administration and social-sector organisations.",
                ),
                (
                    "How do I get in touch?",
                    "By phone on +49 (0)541 14496 or email at dg@doris-gunsch.eu — we clarify your situation and a suitable format.",
                ),
            ],
            "services_title": "Relevant services",
            "audience_title": "Suitable for",
            "audience": "Managing directors, department heads and project leads in Osnabrück and Osnabrück district.",
            "nearby_title": "Also in the surrounding area",
            "nearby": "Georgsmarienhütte, Melle, Bramsche, Bersenbrück — a short drive from the Osnabrück office.",
            "cta_title": "Contact in Osnabrück",
            "cta_text": "Leading in Osnabrück and looking for confidential, experienced support? I look forward to hearing from you.",
            "cta_btn": "Get in touch",
        },
    },
    "muenster": {
        "name_de": "Münster",
        "name_en": "Münster",
        "module_order": [
            "hero",
            "intro",
            "sectors",
            "mandates",
            "mini_case",
            "faq",
            "references",
            "formats",
            "services",
            "cta",
        ],
        "de": {
            "seo_title": "Coaching für Führungskräfte in Münster | Doris Gunsch",
            "seo_desc": "Coaching und Prozessbegleitung in Münster: Führung in Verwaltung, Bildung und institutionellen Kontexten. Psychologische Beratung aus Osnabrück — gut erreichbar.",
            "home_label": "Münster — Verwaltung & Institutionen",
            "hero_kicker": "Münster",
            "h1": "Coaching für Führungskräfte in Münster",
            "hero_lead": "Führungsbegleitung dort, wo fachliche Exzellenz auf institutionelle Komplexität trifft.",
            "intro_title": "Führung zwischen Profession und Organisation",
            "intro": (
                "In Münster begleite ich Führungskräfte in Organisationen, in denen fachliche Exzellenz "
                "und institutionelle Komplexität eng zusammenkommen — in Verwaltung, Bildung, "
                "kirchlichen und sozialen Trägern sowie in wissenschaftsnahen Einrichtungen. "
                "Von Osnabrück aus ist Münster in etwa einer Stunde erreichbar; viele Formate "
                "kombinieren Vor-Ort-Termine mit Online-Phasen."
            ),
            "sectors_title": "Branchenfokus im Münsterland",
            "sectors": [
                "Öffentliche Verwaltung und kommunale Träger",
                "Hochschulen, Bildung und wissenschaftsnahe Einrichtungen",
                "Kirchliche und diakonische Organisationen",
                "Stiftungen und gemeinnützige Strukturen",
            ],
            "mandates_title": "Typische Anliegen in Münster",
            "mandates": [
                "Konflikte in Leitungsteams mit unterschiedlichen Professionen",
                "Rollenklärung zwischen Fachlichkeit und Hierarchie",
                "Veränderungsbegleitung bei Struktur- oder Strategiewechsel",
                "Belastete Kommunikation in lang gewachsenen Organisationen",
            ],
            "mini_case_title": "Typisches Anliegen",
            "mini_case": (
                "Eine Bereichsleitung in einer diakonischen Einrichtung im Münsterland "
                "steht zwischen Fachbereich, Trägergremien und politischen Erwartungen — "
                "und spürt, dass Entscheidungen zunehmend blockiert werden. Im Coaching "
                "werden Rollen, Kommunikationswege und tragfähige nächste Schritte "
                "strukturiert, ohne die fachliche Autonomie der Teams zu verlieren."
            ),
            "faq_title": "Häufige Fragen — Münster",
            "faq": [
                (
                    "Betreuen Sie Mandate direkt in Münster?",
                    "Ja — Coachings, Workshops und Prozessbegleitungen führe ich regelmäßig in Münster und im Münsterland durch, ergänzt durch Termine in Osnabrück oder online.",
                ),
                (
                    "Was unterscheidet Münster von anderen Standorten?",
                    "Hier stehen oft institutionelle Logiken, Ehrenamt/Fachlichkeit und mehrstufige Entscheidungswege im Vordergrund — das prägt meine Begleitung.",
                ),
                (
                    "Für welche Führungsebenen?",
                    "Obere und mittlere Führung, Bereichsleitungen, Projektleitungen und Geschäftsführungen in mittelgroßen Organisationen.",
                ),
                (
                    "Wie starten wir die Zusammenarbeit?",
                    "In einem vertraulichen Gespräch klären wir Anlass, Rahmen und ob Coaching, Training oder Prozessbegleitung passt.",
                ),
            ],
            "references_title": "Erfahrung im nordwestdeutschen Raum",
            "references_intro": "Ausgewählte Mandate mit Bezug zu institutionellen und sozialen Kontexten — auch für Führungskräfte aus Münster:",
            "references": [
                "Caritas Pflegezentrum Georgsmarienhütte GmbH",
                "Malteser Hilfsdienst e.V.",
                "Stiftung Neuerkerode",
                "Landkreis Ammerland",
            ],
            "formats_title": "Formate für Münster",
            "formats": [
                ("Coaching", "Einzelbegleitung bei Rollen- und Konfliktfragen — vor Ort oder hybrid."),
                ("Prozessbegleitung", "Moderation in Veränderungs- und Strategieprozessen."),
                ("Trainings", "Seminare zu Führung, Kommunikation und Konfliktklärung."),
            ],
            "services_title": "Passende Leistungen",
            "audience_title": "Geeignet für",
            "audience": "Führungskräfte in Verwaltung, Bildung und sozialen Trägern im Münsterland.",
            "cta_title": "Kontakt für Coaching und Prozessbegleitung in Münster",
            "cta_text": "Sie tragen Verantwortung in einer komplexen Organisation in Münster? Sprechen Sie mich an.",
            "cta_btn": "Vertraulich anfragen",
        },
        "en": {
            "seo_title": "Executive Coaching in Münster | Doris Gunsch",
            "seo_desc": "Coaching and process facilitation in Münster: leadership in administration, education and institutional contexts. Psychological consulting from Osnabrück — easily reachable.",
            "home_label": "Münster — administration & institutions",
            "hero_kicker": "Münster",
            "h1": "Executive coaching in Münster",
            "hero_lead": "Leadership support where professional excellence meets institutional complexity.",
            "intro_title": "Leadership between profession and organisation",
            "intro": (
                "In Münster I support leaders in organisations where professional excellence "
                "and institutional complexity closely intersect — in administration, education, "
                "church and social-sector bodies and science-related institutions. "
                "Münster is about an hour from Osnabrück; many formats combine on-site sessions with online phases."
            ),
            "sectors_title": "Sector focus in the Münsterland",
            "sectors": [
                "Public administration and municipal bodies",
                "Universities, education and science-related institutions",
                "Church and diaconal organisations",
                "Foundations and non-profit structures",
            ],
            "mandates_title": "Typical concerns in Münster",
            "mandates": [
                "Conflicts in leadership teams with different professions",
                "Role clarification between expertise and hierarchy",
                "Change facilitation during structural or strategic shifts",
                "Strained communication in long-established organisations",
            ],
            "mini_case_title": "A typical concern",
            "mini_case": (
                "A department head in a diaconal organisation in the Münsterland is caught "
                "between professional departments, governing bodies and political expectations — "
                "and finds decisions increasingly blocked. In coaching, roles, communication "
                "channels and workable next steps are structured without losing teams' "
                "professional autonomy."
            ),
            "faq_title": "Frequently asked questions — Münster",
            "faq": [
                (
                    "Do you take on mandates directly in Münster?",
                    "Yes — I regularly deliver coaching, workshops and process facilitation in Münster and the Münsterland, supplemented by sessions in Osnabrück or online.",
                ),
                (
                    "What makes Münster different from other locations?",
                    "Institutional logics, volunteer/professional dynamics and multi-level decision paths are often central — that shapes my approach.",
                ),
                (
                    "Which leadership levels?",
                    "Senior and middle management, department heads, project leads and managing directors in medium-sized organisations.",
                ),
                (
                    "How do we start working together?",
                    "In a confidential conversation we clarify your situation, framework and whether coaching, training or facilitation fits.",
                ),
            ],
            "references_title": "Experience in north-west Germany",
            "references_intro": "Selected mandates in institutional and social contexts — also for leaders from Münster:",
            "references": [
                "Caritas Pflegezentrum Georgsmarienhütte GmbH",
                "Malteser Hilfsdienst e.V.",
                "Stiftung Neuerkerode",
                "Landkreis Ammerland",
            ],
            "formats_title": "Formats for Münster",
            "formats": [
                ("Coaching", "Individual support on role and conflict issues — on site or hybrid."),
                ("Process facilitation", "Moderation in change and strategy processes."),
                ("Training", "Seminars on leadership, communication and conflict resolution."),
            ],
            "services_title": "Relevant services",
            "audience_title": "Suitable for",
            "audience": "Leaders in administration, education and social-sector organisations in the Münsterland.",
            "cta_title": "Contact for coaching and facilitation in Münster",
            "cta_text": "Carrying responsibility in a complex organisation in Münster? Get in touch.",
            "cta_btn": "Get in touch confidentially",
        },
    },
    "oldenburg": {
        "name_de": "Oldenburg",
        "name_en": "Oldenburg",
        "module_order": [
            "hero",
            "intro",
            "references",
            "sectors",
            "mini_case",
            "formats",
            "faq",
            "services",
            "cta",
        ],
        "de": {
            "seo_title": "Coaching im Gesundheitswesen — Oldenburg | Doris Gunsch",
            "seo_desc": "Coaching und Prozessbegleitung in Oldenburg mit Schwerpunkt Gesundheitswesen und Sozialwirtschaft. Erfahrung mit Klinikum Oldenburg und regionalen Trägern.",
            "home_label": "Oldenburg — Gesundheit & Soziales",
            "hero_kicker": "Oldenburg",
            "h1": "Coaching im Gesundheitswesen — Oldenburg",
            "hero_lead": "Begleitung von Führungskräften in Gesundheitswesen, Sozialwirtschaft und regionalen Institutionen.",
            "intro_title": "Veränderung in komplexen Organisationen",
            "intro": (
                "Oldenburg ist geprägt von Klinikverbünden, sozialen Trägern und regionalen "
                "Institutionen mit hoher Verantwortungsdichte. Hier begleite ich Führungskräfte, "
                "wenn Veränderungsdruck, personelle Dynamiken und fachliche Anforderungen "
                "gleichzeitig wirken — mit psychologischem Verständnis und klarer Prozessführung."
            ),
            "references_title": "Referenzen mit Oldenburg-Bezug",
            "references_intro": "Ausgewählte Mandate und Kooperationen in Oldenburg und der Region:",
            "references": [
                "Klinikum Oldenburg",
                "Evangelisches Krankenhaus Oldenburg",
                "Elisabeth-Kinderkrankenhaus im Klinikum Oldenburg",
                "Sozialstation der Diakonie, Oldenburg",
                "Oldenburgische Landesbank",
            ],
            "sectors_title": "Branchenerfahrung im Umfeld von Oldenburg",
            "sectors": [
                "Akut- und Regelversorgung, Klinikverbünde",
                "Soziale Dienste und diakonische Träger",
                "Regionale Finanzinstitute und Dienstleister",
            ],
            "mini_case_title": "Typisches Anliegen",
            "mini_case": (
                "Eine Leitungsebene im Gesundheitswesen steht vor der Aufgabe, ein interdisziplinäres "
                "Team durch eine Organisationsveränderung zu führen — bei gleichzeitig hoher Auslastung "
                "und sensibler Personalpolitik. Im Coaching werden Kommunikationslinien geklärt, "
                "Konfliktpotenziale früh erkannt und tragfähige nächste Schritte entwickelt."
            ),
            "formats_title": "Zusammenarbeit in Oldenburg",
            "formats": [
                ("Vor Ort", "Workshops und Teamentwicklung bei Ihnen — in Kliniken und Trägerstrukturen."),
                ("Coaching", "Einzelbegleitung für Geschäftsführung und Bereichsleitungen."),
                ("Hybrid", "Kombination aus Präsenzterminen und Online-Phasen bei engen Kalendern."),
            ],
            "faq_title": "Häufige Fragen — Oldenburg",
            "faq": [
                (
                    "Haben Sie Erfahrung im Oldenburger Gesundheitswesen?",
                    "Ja — mehrere langjährige Mandate mit Kliniken und sozialen Einrichtungen in Oldenburg und Umgebung.",
                ),
                (
                    "Begleiten Sie auch ganze Teams?",
                    "Ja — von Moderation einzelner Konfliktsituationen bis zu mehrtägigen Entwicklungsworkshops.",
                ),
                (
                    "Wie schnell ist ein Termin möglich?",
                    "Nach Ihrer Anfrage stimmen wir Rhythmus und Format ab — oft innerhalb weniger Wochen.",
                ),
                (
                    "Was kostet eine Begleitung?",
                    "Das hängt von Format und Dauer ab — bei der Anfrage klären wir Rahmen und Honorar transparent.",
                ),
            ],
            "services_title": "Passende Leistungen",
            "audience_title": "Geeignet für",
            "audience": "Klinikdirektionen, Pflegedienstleitungen, Verwaltungsleitungen und Geschäftsführungen sozialer Träger.",
            "cta_title": "Kontakt für Führungskräfte in Oldenburg",
            "cta_text": "Sie gestalten Veränderung in Oldenburg und suchen professionelle Begleitung? Melden Sie sich.",
            "cta_btn": "Kontakt aufnehmen",
        },
        "en": {
            "seo_title": "Healthcare Coaching — Oldenburg | Doris Gunsch",
            "seo_desc": "Coaching and process facilitation in Oldenburg with a focus on healthcare and the social sector. Experience with Klinikum Oldenburg and regional organisations.",
            "home_label": "Oldenburg — healthcare & social sector",
            "hero_kicker": "Oldenburg",
            "h1": "Healthcare coaching — Oldenburg",
            "hero_lead": "Support for leaders in healthcare, the social sector and regional institutions.",
            "intro_title": "Change in complex organisations",
            "intro": (
                "Oldenburg is shaped by hospital networks, social-sector bodies and regional "
                "institutions with high responsibility density. I support leaders when pressure "
                "to change, personnel dynamics and professional demands coincide — with psychological "
                "understanding and clear process leadership."
            ),
            "references_title": "References linked to Oldenburg",
            "references_intro": "Selected mandates and collaborations in Oldenburg and the region:",
            "references": [
                "Klinikum Oldenburg",
                "Evangelisches Krankenhaus Oldenburg",
                "Elisabeth Children's Hospital at Klinikum Oldenburg",
                "Sozialstation der Diakonie, Oldenburg",
                "Oldenburgische Landesbank",
            ],
            "sectors_title": "Sector experience around Oldenburg",
            "sectors": [
                "Acute and standard care, hospital networks",
                "Social services and diaconal bodies",
                "Regional financial institutions and service providers",
            ],
            "mini_case_title": "A typical concern",
            "mini_case": (
                "A leadership level in healthcare faces the task of guiding an interdisciplinary "
                "team through organisational change — with high workload and sensitive HR policy "
                "at the same time. Coaching clarifies communication lines, identifies conflict "
                "potential early and develops viable next steps."
            ),
            "formats_title": "Working together in Oldenburg",
            "formats": [
                ("On site", "Workshops and team development at your premises — in hospitals and provider structures."),
                ("Coaching", "Individual support for managing directors and department heads."),
                ("Hybrid", "A mix of in-person and online sessions for tight calendars."),
            ],
            "faq_title": "Frequently asked questions — Oldenburg",
            "faq": [
                (
                    "Do you have experience in Oldenburg healthcare?",
                    "Yes — several long-term mandates with hospitals and social institutions in Oldenburg and the area.",
                ),
                (
                    "Do you also support whole teams?",
                    "Yes — from moderating individual conflict situations to multi-day development workshops.",
                ),
                (
                    "How soon can we start?",
                    "After your enquiry we agree rhythm and format — often within a few weeks.",
                ),
                (
                    "What does support cost?",
                    "That depends on format and duration — we clarify framework and fees transparently when you get in touch.",
                ),
            ],
            "services_title": "Relevant services",
            "audience_title": "Suitable for",
            "audience": "Hospital directors, nursing service leads, administrative heads and managing directors of social-sector bodies.",
            "cta_title": "Contact for leaders in Oldenburg",
            "cta_text": "Shaping change in Oldenburg and looking for professional support? Get in touch.",
            "cta_btn": "Get in touch",
        },
    },
    "hannover": {
        "name_de": "Hannover",
        "name_en": "Hannover",
        "module_order": [
            "hero",
            "intro",
            "mandates",
            "formats",
            "references",
            "faq",
            "services",
            "quote",
            "cta",
        ],
        "de": {
            "seo_title": "Führungskräfte-Coaching in Hannover | Doris Gunsch",
            "seo_desc": "Coaching und Prozessbegleitung in Hannover: Führung in größeren Organisationen, Hochschulmedizin und Verwaltungsnähe. Psychologische Beratung aus Osnabrück.",
            "home_label": "Hannover — große Organisationen",
            "hero_kicker": "Hannover",
            "h1": "Führungskräfte-Coaching in Hannover",
            "hero_lead": "Begleitung bei Konflikten, Rollenklärungen und anspruchsvollen Veränderungsprozessen in großen Strukturen.",
            "intro_title": "Führung in matrixartigen Organisationen",
            "intro": (
                "In Hannover begleite ich Führungskräfte bei Konflikten, Rollenklärungen und "
                "anspruchsvollen Veränderungsprozessen in größeren Organisationsstrukturen — "
                "in Medizin, Verwaltung und verbundenen Einrichtungen. Die Landeshauptstadt "
                "bringt oft hohe Entscheidungsdichte und viele Stakeholder mit sich; "
                "meine Arbeit schafft Klarheit, ohne Komplexität zu vereinfachen."
            ),
            "mandates_title": "Typische Anliegen in Hannover",
            "mandates": [
                "Rollenunklarheit in mittlerer Führungsebene",
                "Konflikte zwischen Linien- und Projektverantwortung",
                "Veränderungsprozesse mit Widerstand in großen Teams",
                "Vorbereitung schwieriger Personal- oder Strategiegespräche",
            ],
            "formats_title": "Formate für Hannover",
            "formats": [
                ("Prozessbegleitung", "Moderation in mehrstufigen Veränderungs- und Entwicklungsprozessen."),
                ("Coaching", "Einzelbegleitung für Führungskräfte unter hoher Verantwortung."),
                ("Trainings", "Seminare zu Führung, Kommunikation und Konfliktmanagement."),
            ],
            "references_title": "Referenzen mit Hannover-Bezug",
            "references_intro": "Ausgewählte Mandate und Kooperationen:",
            "references": [
                "Medizinische Hochschule Hannover",
                "Kinderklinik Siegen",
                "Marienhospital Hamm",
            ],
            "faq_title": "Häufige Fragen — Hannover",
            "faq": [
                (
                    "Wie oft sind Sie in Hannover vor Ort?",
                    "Je nach Mandat in regelmäßigen Abständen — ergänzt durch Online-Termine zwischen den Präsenzphasen.",
                ),
                (
                    "Arbeiten Sie mit Konzernstrukturen?",
                    "Mein Schwerpunkt liegt auf mittleren und größeren Organisationen in Medizin, Verwaltung und Dienstleistung — nicht auf Konzern-Top-Management.",
                ),
                (
                    "Was ist der erste Schritt?",
                    "Per Telefon oder Videokonferenz klären wir vertraulich Anlass und Ziel.",
                ),
                (
                    "Bieten Sie auch Teamentwicklung an?",
                    "Ja — von Einzeltagen bis zu mehrtägigen Workshop-Reihen, abgestimmt auf Ihre Situation.",
                ),
            ],
            "services_title": "Passende Leistungen",
            "audience_title": "Geeignet für",
            "audience": "Bereichsleitungen, Klinikdirektionen, Verwaltungsleitungen und Projektverantwortliche in Hannover.",
            "quote": (
                "„In großen Organisationen geht es selten um schnelle Antworten — "
                "sondern um tragfähige nächste Schritte, die alle Beteiligten mittragen können.“"
            ),
            "cta_title": "Vertrauliche Anfrage für Führungskräfte in Hannover",
            "cta_text": "Sie tragen Verantwortung in Hannover und suchen eine erfahrene Begleitung? Ich freue mich auf Ihre Nachricht.",
            "cta_btn": "Kontakt aufnehmen",
        },
        "en": {
            "seo_title": "Leadership Coaching in Hannover | Doris Gunsch",
            "seo_desc": "Coaching and process facilitation in Hannover: leadership in larger organisations, university medicine and public administration. Psychological consulting from Osnabrück.",
            "home_label": "Hannover — larger organisations",
            "hero_kicker": "Hannover",
            "h1": "Leadership coaching in Hannover",
            "hero_lead": "Support with conflicts, role clarification and demanding change processes in large structures.",
            "intro_title": "Leadership in matrix-like organisations",
            "intro": (
                "In Hannover I support leaders with conflicts, role clarification and "
                "demanding change processes in larger organisational structures — "
                "in medicine, administration and affiliated institutions. The state capital "
                "often brings high decision density and many stakeholders; "
                "my work creates clarity without oversimplifying complexity."
            ),
            "mandates_title": "Typical concerns in Hannover",
            "mandates": [
                "Role ambiguity at middle management level",
                "Conflicts between line and project responsibility",
                "Change processes with resistance in large teams",
                "Preparing difficult HR or strategy conversations",
            ],
            "formats_title": "Formats for Hannover",
            "formats": [
                ("Process facilitation", "Moderation in multi-stage change and development processes."),
                ("Coaching", "Individual support for leaders under high responsibility."),
                ("Training", "Seminars on leadership, communication and conflict management."),
            ],
            "references_title": "References linked to Hannover",
            "references_intro": "Selected mandates and collaborations:",
            "references": [
                "Medizinische Hochschule Hannover",
                "Kinderklinik Siegen",
                "Marienhospital Hamm",
            ],
            "faq_title": "Frequently asked questions — Hannover",
            "faq": [
                (
                    "How often are you on site in Hannover?",
                    "Depending on the mandate at regular intervals — supplemented by online sessions between in-person phases.",
                ),
                (
                    "Do you work with corporate structures?",
                    "My focus is on medium and larger organisations in medicine, administration and services — not top corporate management.",
                ),
                (
                    "What is the first step?",
                    "By phone or video we clarify your situation and goals confidentially.",
                ),
                (
                    "Do you offer team development?",
                    "Yes — from single days to multi-day workshop series, tailored to your situation.",
                ),
            ],
            "services_title": "Relevant services",
            "audience_title": "Suitable for",
            "audience": "Department heads, hospital directors, administrative leads and project owners in Hannover.",
            "quote": (
                "“In large organisations it is rarely about quick answers — "
                "but about viable next steps that all parties can support.”"
            ),
            "cta_title": "Confidential enquiry for leaders in Hannover",
            "cta_text": "Carrying responsibility in Hannover and looking for experienced support? I look forward to hearing from you.",
            "cta_btn": "Get in touch",
        },
    },
    "bremen": {
        "name_de": "Bremen",
        "name_en": "Bremen",
        "module_order": [
            "hero",
            "intro",
            "mandates",
            "faq",
            "references",
            "formats",
            "mini_case",
            "services",
            "cta",
        ],
        "de": {
            "seo_title": "Coaching & Konfliktmoderation in Bremen | Doris Gunsch",
            "seo_desc": "Coaching und Prozessbegleitung in Bremen: Führung zwischen Wandel, Tempo und Verantwortung in Handel, Logistik und Industrie. Gut erreichbar aus Osnabrück.",
            "home_label": "Bremen — Wandel & Verantwortung",
            "hero_kicker": "Bremen",
            "h1": "Coaching & Konfliktmoderation in Bremen",
            "hero_lead": "Unterstützung in Situationen, in denen Veränderungsdruck, operative Verantwortung und personelle Dynamiken gleichzeitig wirksam werden.",
            "intro_title": "Führung unter Tempo und Veränderungsdruck",
            "intro": (
                "In Bremen unterstütze ich Führung in Situationen, in denen Veränderungsdruck, "
                "operative Verantwortung und personelle Dynamiken gleichzeitig wirksam werden — "
                "in Handel, Logistik, Industrie und angrenzenden Dienstleistungsbereichen. "
                "Bremen ist von Osnabrück aus gut erreichbar; Mandate kombinieren oft "
                "präzise Einzelcoachings mit gezielten Team- oder Prozessformaten."
            ),
            "mandates_title": "Typische Anliegen in Bremen",
            "mandates": [
                "Führungswechsel in wachstums- oder krisenbedingten Phasen",
                "Reibungen zwischen operativer Exzellenz und strategischer Neuausrichtung",
                "Konflikte in leistungsstarken Teams mit hoher Taktung",
                "Belastete Kommunikation zwischen Standorten oder Bereichen",
            ],
            "faq_title": "Häufige Fragen — Bremen",
            "faq": [
                (
                    "Welche Branchen in Bremen betreuen Sie?",
                    "Schwerpunkte sind Handel, Logistik, Industrie und professionelle Dienstleistungen — passend zur Bremer Wirtschaftsstruktur.",
                ),
                (
                    "Wie schnell kann Begleitung starten?",
                    "Nach Ihrer Anfrage — oft innerhalb von zwei bis drei Wochen, je nach Dringlichkeit und Format.",
                ),
                (
                    "Moderieren Sie auch Konflikte im Team?",
                    "Ja — von der Klärung zweierer Parteien bis zur Begleitung ganzer Führungsteams.",
                ),
                (
                    "Ist Online-Coaching möglich?",
                    "Ja — viele Führungskräfte kombinieren Präsenz in Bremen mit Online-Terminen für kurze Abstimmungen.",
                ),
            ],
            "references_title": "Erfahrung in der Region",
            "references_intro": "Ausgewählte Mandate im norddeutschen Raum — relevant für Führungskräfte in Bremen:",
            "references": [
                "Gemeinde Ritterhude",
                "Kreis Pinneberg",
                "Wilo SE Werk Minden GmbH",
                "Condor Flugdienst GmbH",
            ],
            "formats_title": "Formate in Bremen",
            "formats": [
                ("Konfliktmoderation", "Strukturierte Klärung belasteter Beziehungen und Rollen."),
                ("Coaching", "Einzelbegleitung bei Führungsfragen und Entscheidungssituationen."),
                ("Prozessbegleitung", "Begleitung von Veränderungs- und Teamentwicklungsprozessen."),
            ],
            "mini_case_title": "Typisches Anliegen",
            "mini_case": (
                "Eine Bereichsleitung im industriellen Umfeld spürt, dass ein erfahrenes Team "
                "unter neuer Strategie und erhöhtem Tempo an seine Grenzen stößt — Motivation "
                "und Zusammenarbeit leiden. In der Begleitung werden Erwartungen geklärt, "
                "Kommunikationsmuster sichtbar gemacht und konkrete Interventionen entwickelt."
            ),
            "services_title": "Passende Leistungen",
            "audience_title": "Geeignet für",
            "audience": "Werksleitungen, Bereichsleitungen und Geschäftsführungen mittelständischer Unternehmen in Bremen.",
            "cta_title": "Kontakt für Führungskräfte in Bremen",
            "cta_text": "Veränderung und Verantwortung in Bremen — ich begleite Sie vertraulich und praxisnah.",
            "cta_btn": "Kontakt aufnehmen",
        },
        "en": {
            "seo_title": "Coaching & Conflict Facilitation in Bremen | Doris Gunsch",
            "seo_desc": "Coaching and process facilitation in Bremen: leadership between change, pace and responsibility in trade, logistics and industry. Easily reachable from Osnabrück.",
            "home_label": "Bremen — change & responsibility",
            "hero_kicker": "Bremen",
            "h1": "Coaching & conflict facilitation in Bremen",
            "hero_lead": "Support when pressure to change, operational responsibility and personnel dynamics coincide.",
            "intro_title": "Leadership under pace and pressure to change",
            "intro": (
                "In Bremen I support leadership when pressure to change, operational "
                "responsibility and personnel dynamics coincide — "
                "in trade, logistics, industry and related service sectors. "
                "Bremen is easily reached from Osnabrück; mandates often combine "
                "focused individual coaching with targeted team or process formats."
            ),
            "mandates_title": "Typical concerns in Bremen",
            "mandates": [
                "Leadership transitions in growth or crisis phases",
                "Friction between operational excellence and strategic realignment",
                "Conflicts in high-performing teams under intense pace",
                "Strained communication between sites or departments",
            ],
            "faq_title": "Frequently asked questions — Bremen",
            "faq": [
                (
                    "Which sectors in Bremen do you support?",
                    "Focus areas include trade, logistics, industry and professional services — matching Bremen's economic structure.",
                ),
                (
                    "How quickly can support start?",
                    "After your enquiry — often within two to three weeks, depending on urgency and format.",
                ),
                (
                    "Do you facilitate team conflicts?",
                    "Yes — from clarifying between two parties to supporting entire leadership teams.",
                ),
                (
                    "Is online coaching possible?",
                    "Yes — many leaders combine in-person sessions in Bremen with online appointments for brief check-ins.",
                ),
            ],
            "references_title": "Experience in the region",
            "references_intro": "Selected mandates in northern Germany — relevant for leaders in Bremen:",
            "references": [
                "Gemeinde Ritterhude",
                "Kreis Pinneberg",
                "Wilo SE Werk Minden GmbH",
                "Condor Flugdienst GmbH",
            ],
            "formats_title": "Formats in Bremen",
            "formats": [
                ("Conflict facilitation", "Structured clarification of strained relationships and roles."),
                ("Coaching", "Individual support on leadership issues and decisions."),
                ("Process facilitation", "Support for change and team development processes."),
            ],
            "mini_case_title": "A typical concern",
            "mini_case": (
                "A department head in an industrial setting senses that an experienced team "
                "is reaching its limits under new strategy and increased pace — motivation "
                "and collaboration suffer. Facilitation clarifies expectations, makes "
                "communication patterns visible and develops concrete interventions."
            ),
            "services_title": "Relevant services",
            "audience_title": "Suitable for",
            "audience": "Plant managers, department heads and managing directors of mid-sized companies in Bremen.",
            "cta_title": "Contact for leaders in Bremen",
            "cta_text": "Change and responsibility in Bremen — I support you confidentially and practically.",
            "cta_btn": "Get in touch",
        },
    },
}

CITIES.update(METRO_CITIES)
CITIES["zuerich"] = ZUERICH

from patch_standorte_content import apply_all_patches  # noqa: E402

apply_all_patches()

SERVICE_LINKS = {
    "de": [
        ("coaching.html", "Coaching"),
        ("trainings.html", "Trainings & Seminare"),
        ("team.html", "Team & Prozess"),
        ("diagnostik.html", "Diagnostik"),
    ],
    "en": [
        ("coaching.html", "Coaching"),
        ("trainings.html", "Training & Seminars"),
        ("team.html", "Team & Process"),
        ("diagnostik.html", "Diagnostics"),
    ],
}


def meta_for(slug: str) -> dict:
    c = CITIES[slug]
    filename = f"standorte/{slug}.html"
    return {
        "page": "standort",
        "active": "",
        "schema": "city_location",
        "city_de": c["name_de"],
        "city_en": c["name_en"],
        "title_de": c["de"]["seo_title"],
        "title_en": c["en"]["seo_title"],
        "desc_de": c["de"]["seo_desc"],
        "desc_en": c["en"]["seo_desc"],
        "breadcrumb_de": c["name_de"],
        "breadcrumb_en": c["name_en"],
        "filename": filename,
    }


STANDORTE_META = {meta_for(s)["filename"]: meta_for(s) for s in CITY_SLUGS}
