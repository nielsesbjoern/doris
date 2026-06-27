#!/usr/bin/env python3
"""Apply standort content patches (mini_case, references, logistics, module_order)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# fmt: off
PATCHES: dict[str, dict] = {
    "osnabrueck": {
        "module_order": [
            "hero", "intro", "collaboration", "mandates", "mini_case",
            "references", "formats", "format_teaser", "faq", "services", "nearby", "related", "cta",
        ],
        "de": {
            "mini_case": (
                "Eine Geschäftsführerin eines etablierten Mittelstandsunternehmens im "
                "Osnabrücker Land spürt nach einem Führungswechsel im Leitungskreis, dass "
                "alte Loyalitäten und neue Strategie aufeinanderprallen. Im Coaching werden "
                "Rollen, Erwartungen und Gesprächswege geklärt — ohne die gewachsene Kultur "
                "des Unternehmens zu überfahren."
            ),
            "references": [
                ("Stadt Osnabrück", "Coaching und Prozessbegleitung in der Verwaltung"),
                ("Klinikum Osnabrück", "Führungskräfteentwicklung und Teamentwicklung"),
                ("Universität Osnabrück, FB Persönlichkeitspsychologie", "Wissenschaftliche Kooperation und Lehre"),
                ("IMPART GmbH, Osnabrück", "Coaching und Organisationsberatung"),
            ],
        },
        "en": {
            "mini_case": (
                "A managing director of an established mid-sized company in the Osnabrück "
                "area senses after a leadership change in the executive team that old "
                "loyalties and new strategy are colliding. Coaching clarifies roles, "
                "expectations and conversation paths — without overriding the company's "
                "grown culture."
            ),
            "references": [
                ("Stadt Osnabrück", "Coaching and process facilitation in public administration"),
                ("Klinikum Osnabrück", "Leadership development and team development"),
                ("Universität Osnabrück, Department of Personality Psychology", "Academic cooperation and teaching"),
                ("IMPART GmbH, Osnabrück", "Coaching and organisational consulting"),
            ],
        },
    },
    "hannover": {
        "module_order": [
            "hero", "intro", "mandates", "mini_case", "logistics", "formats",
            "references", "faq", "quote", "format_teaser", "services", "related", "cta",
        ],
        "de": {
            "logistics": (
                "Vom Büro in Osnabrück (Newtonstraße) ist Hannover in etwa einer Stunde "
                "erreichbar. Mandate kombinieren in der Regel Präsenztermine in Hannover "
                "mit Online-Phasen für kurze Abstimmungen — so bleibt die Begleitung "
                "kontinuierlich, ohne unnötigen Reiseaufwand."
            ),
            "mini_case": (
                "Eine Klinikdirektion in der Landeshauptstadt steht vor der Fusion zweier "
                "Bereiche — Linien- und Projektverantwortung überschneiden sich, "
                "Entscheidungen verzögern sich. In der Prozessbegleitung werden "
                "Entscheidungswege, Rollen und Kommunikationsroutinen neu strukturiert."
            ),
            "references": [
                ("Medizinische Hochschule Hannover", "Coaching und Prozessbegleitung in Hochschulmedizin"),
                ("Klinikum Oldenburg", "Teamentwicklung im Gesundheitswesen (Region Nordwest)"),
                ("Marienhospital Hamm", "Führungskräfteentwicklung im Klinikumfeld"),
            ],
        },
        "en": {
            "logistics": (
                "From the Osnabrück office (Newtonstraße), Hanover is about an hour away. "
                "Mandates typically combine in-person sessions in Hanover with online phases "
                "for short check-ins — keeping support continuous without unnecessary travel."
            ),
            "mini_case": (
                "A hospital director in the state capital faces merging two departments — "
                "line and project responsibilities overlap and decisions stall. Process "
                "facilitation restructures decision paths, roles and communication routines."
            ),
            "references": [
                ("Medizinische Hochschule Hannover", "Coaching and facilitation in university medicine"),
                ("Klinikum Oldenburg", "Team development in healthcare (north-west region)"),
                ("Marienhospital Hamm", "Leadership development in a hospital setting"),
            ],
        },
    },
    "frankfurt": {
        "module_order": [
            "hero", "intro", "collaboration", "mandates", "mini_case", "logistics",
            "formats", "references", "faq", "quote", "format_teaser", "services", "related", "cta",
        ],
        "de": {
            "logistics": (
                "Frankfurt ist vom Büro in Osnabrück aus per Bahn in etwa zwei bis "
                "zweieinhalb Stunden erreichbar. Üblich sind kompakte Präsenzblöcke vor "
                "Ort — ergänzt durch Online-Termine zwischen den Terminen."
            ),
            "mini_case": (
                "Eine Bereichsleitung in einem wirtschaftsnahen Umfeld trägt gleichzeitig "
                "Verantwortung für ein sensibles Restrukturierungsprojekt und ein "
                "leistungsstarkes Kernteam — der Entscheidungsdruck ist hoch, Vertrauen "
                "im Leitungskreis bröckelt. Im Coaching werden Prioritäten, Gesprächsstrategien "
                "und tragfähige nächste Schritte entwickelt."
            ),
            "references_title": "Referenzen mit Frankfurt-Bezug",
            "references_intro": "Ausgewählte Mandate und Kooperationen im Rhein-Main-Raum und angrenzenden Kontexten:",
            "references": [
                ("Vattenfall Deutschland", "Coaching und Prozessbegleitung im Energiesektor"),
                ("T-Systems International GmbH", "Führungskräfteentwicklung in komplexen Organisationen"),
                ("Emprise AG, Düsseldorf", "Executive Coaching in wirtschaftsnahen Kontexten (Region Rhein-Main)"),
            ],
        },
        "en": {
            "logistics": (
                "Frankfurt is about two to two-and-a-half hours by train from the Osnabrück "
                "office. Compact on-site blocks are typical — supplemented by online "
                "sessions between appointments."
            ),
            "mini_case": (
                "A department head in a business-oriented environment simultaneously carries "
                "responsibility for a sensitive restructuring project and a high-performing "
                "core team — decision pressure is high and trust in the leadership circle "
                "is eroding. Coaching develops priorities, conversation strategies and viable next steps."
            ),
            "references_title": "References linked to Frankfurt",
            "references_intro": "Selected mandates and collaborations in the Rhine-Main area and related contexts:",
            "references": [
                ("Vattenfall Deutschland", "Coaching and facilitation in the energy sector"),
                ("T-Systems International GmbH", "Leadership development in complex organisations"),
                ("Emprise AG, Düsseldorf", "Executive coaching in business contexts (Rhine-Main region)"),
            ],
        },
    },
    "muenchen": {
        "module_order": [
            "hero", "intro", "sectors", "mandates", "mini_case", "logistics",
            "references", "faq", "quote", "format_teaser", "services", "related", "cta",
        ],
        "de": {
            "logistics": (
                "München ist vom Büro in Osnabrück aus per Bahn in etwa vier bis fünf "
                "Stunden erreichbar. Mandate in München setzen deshalb oft auf kompakte "
                "Präsenzblöcke und kontinuierliche Online-Phasen dazwischen."
            ),
            "mini_case": (
                "Eine erfahrene Führungskraft übernimmt in einer spezialisierten Organisation "
                "eine neue Rolle mit internationalem Schnittstellenbezug — hohe Erwartungen "
                "von innen und außen, das Selbstbild passt nicht mehr zur neuen Position. "
                "Im Coaching werden Rollenverständnis, Kommunikation und Entscheidungsroutinen "
                "neu justiert."
            ),
            "references_title": "Referenzen mit München-Bezug",
            "references_intro": "Ausgewählte Mandate und Kooperationen in Bayern und angrenzenden Kontexten:",
            "references": [
                ("Successnet AG München", "Coaching und Teamentwicklung"),
                ("Liebherr-Werk Biberach GmbH", "Führungskräfteentwicklung in Industrie und Technik"),
                ("Krankenhaus Agatharied GmbH", "Prozessbegleitung im Gesundheitswesen (Bayern)"),
            ],
        },
        "en": {
            "logistics": (
                "Munich is about four to five hours by train from the Osnabrück office. "
                "Munich mandates therefore often rely on compact in-person blocks and "
                "continuous online phases in between."
            ),
            "mini_case": (
                "An experienced leader takes on a new role with international interface "
                "responsibility in a specialised organisation — high expectations internally "
                "and externally, self-image no longer matches the new position. Coaching "
                "realigns role understanding, communication and decision routines."
            ),
            "references_title": "References linked to Munich",
            "references_intro": "Selected mandates and collaborations in Bavaria and related contexts:",
            "references": [
                ("Successnet AG Munich", "Coaching and team development"),
                ("Liebherr-Werk Biberach GmbH", "Leadership development in industry and technology"),
                ("Krankenhaus Agatharied GmbH", "Process facilitation in healthcare (Bavaria)"),
            ],
        },
    },
    "zuerich": {
        "module_order": [
            "hero", "intro", "sectors", "mandates", "mini_case", "logistics",
            "formats", "references", "faq", "quote", "format_teaser", "services", "related", "cta",
        ],
        "de": {
            "logistics": (
                "Zürich ist vom Büro in Osnabrück aus per Bahn in etwa sechs bis sieben "
                "Stunden erreichbar — Mandate entstehen über Empfehlungen und langjährige "
                "Zusammenarbeit. Üblich sind kompakte Präsenzblöcke in Zürich, ergänzt "
                "durch Online-Phasen und bei Bedarf Termine in Osnabrück."
            ),
            "mini_case": (
                "Ein Leitungsteam mit Standorten in der Schweiz und Deutschland spürt, "
                "dass unterschiedliche Erwartungskulturen und Entscheidungswege die "
                "Zusammenarbeit belasten. In der Begleitung werden gemeinsame "
                "Kommunikationsstandards, Rollen und Eskalationswege entwickelt — "
                "ohne eine Seite zu bevorzugen."
            ),
            "references_title": "Referenzen im internationalen Kontext",
            "references_intro": "Ausgewählte Mandate und Kooperationen — relevant für Führungskräfte in Zürich:",
            "references": [
                ("Vattenfall Deutschland", "Coaching in internationalen Führungskontexten"),
                ("Telekom AG", "Prozessbegleitung in komplexen Organisationen (DACH)"),
                ("Lindt & Sprüngli GmbH, Aachen", "Führungskräfteentwicklung in internationalen Strukturen"),
            ],
        },
        "en": {
            "logistics": (
                "Zurich is about six to seven hours by train from the Osnabrück office — "
                "mandates usually arise through referrals and long-standing collaboration. "
                "Compact in-person blocks in Zurich are typical, supplemented by online "
                "phases and Osnabrück sessions when helpful."
            ),
            "mini_case": (
                "A leadership team with sites in Switzerland and Germany senses that "
                "different expectation cultures and decision paths are straining "
                "collaboration. Facilitation develops shared communication standards, "
                "roles and escalation paths — without favouring either side."
            ),
            "references_title": "References in international contexts",
            "references_intro": "Selected mandates and collaborations — relevant for leaders in Zurich:",
            "references": [
                ("Vattenfall Deutschland", "Coaching in international leadership contexts"),
                ("Telekom AG", "Process facilitation in complex organisations (DACH)"),
                ("Lindt & Sprüngli GmbH, Aachen", "Leadership development in international structures"),
            ],
        },
    },
}

METRO_PATCHES: dict[str, dict] = {
    "hamburg": {
        "module_order": [
            "hero", "intro", "mandates", "mini_case", "logistics", "references",
            "formats", "faq", "format_teaser", "services", "related", "cta",
        ],
        "de": {
            "logistics": (
                "Hamburg ist vom Büro in Osnabrück aus in etwa zwei Stunden erreichbar. "
                "Mandate wechseln zwischen Präsenz in Hamburg und Online-Phasen — "
                "sinnvoll bei hoher Taktung und vielen Schnittstellen."
            ),
            "references_intro": "Ausgewählte Mandate und Kooperationen in Hamburg:",
            "references": [
                ("Palaimon Consulting Hamburg", "Coaching und Prozessbegleitung"),
                ("SCAN-UP AG, Hamburg", "Führungskräfteentwicklung"),
                ("MVZ Dentologicum GbR Hamburg", "Teamentwicklung im Gesundheitswesen"),
                ("Kulturfabrik Kampnagel, Hamburg", "Moderation und Prozessbegleitung"),
            ],
        },
        "en": {
            "logistics": (
                "Hamburg is about two hours from the Osnabrück office. Mandates alternate "
                "between in-person sessions in Hamburg and online phases — practical under "
                "high pace and many interfaces."
            ),
            "references": [
                ("Palaimon Consulting Hamburg", "Coaching and process facilitation"),
                ("SCAN-UP AG, Hamburg", "Leadership development"),
                ("MVZ Dentologicum GbR Hamburg", "Team development in healthcare"),
                ("Kulturfabrik Kampnagel, Hamburg", "Facilitation and process support"),
            ],
        },
    },
    "berlin": {
        "module_order": [
            "hero", "intro", "sectors", "mandates", "mini_case", "logistics",
            "faq", "references", "format_teaser", "services", "related", "cta",
        ],
        "de": {
            "logistics": (
                "Berlin ist vom Büro in Osnabrück aus in etwa drei Stunden erreichbar. "
                "Für Verbände und institutionelle Mandate kombiniere ich Präsenztermine "
                "in Berlin mit Online-Phasen für laufende Abstimmungen."
            ),
            "references_title": "Referenzen mit Berlin-Bezug",
            "references_intro": "Ausgewählte Mandate im öffentlichen und institutionellen Umfeld:",
            "references": [
                ("BVMW Servicegesellschaft, Berlin", "Coaching in Verbands- und institutionellen Kontexten"),
                ("Deutsche Leberhilfe e.V.", "Prozessbegleitung in gemeinnützigen Strukturen"),
                ("Telekom AG", "Führungskräfteentwicklung in komplexen Organisationen"),
            ],
        },
        "en": {
            "logistics": (
                "Berlin is about three hours from the Osnabrück office. For association "
                "and institutional mandates I combine in-person sessions in Berlin with "
                "online phases for ongoing alignment."
            ),
            "references_title": "References linked to Berlin",
            "references_intro": "Selected mandates in the public and institutional sector:",
            "references": [
                ("BVMW Servicegesellschaft, Berlin", "Coaching in association and institutional contexts"),
                ("Deutsche Leberhilfe e.V.", "Process facilitation in non-profit structures"),
                ("Telekom AG", "Leadership development in complex organisations"),
            ],
        },
    },
    "duesseldorf": {
        "module_order": [
            "hero", "intro", "mandates", "mini_case", "logistics", "references",
            "formats", "faq", "format_teaser", "services", "related", "cta",
        ],
        "de": {
            "logistics": (
                "Düsseldorf ist vom Büro in Osnabrück aus in etwa zwei Stunden erreichbar. "
                "Präsenztermine vor Ort werden mit Online-Phasen verbunden — "
                "passend zu wirtschaftsnahen, getakteten Kalendern."
            ),
            "references_title": "Referenzen mit Düsseldorf-Bezug",
            "references_intro": "Ausgewählte Mandate in wirtschaftsnahen und industriellen Kontexten:",
            "references": [
                ("Emprise AG, Düsseldorf", "Coaching und Moderation in wirtschaftsnahen Kontexten"),
                ("Ruhr-Steinkohle AG", "Prozessbegleitung in Industrie und Wandel"),
                ("Salzgitter Mannesmann Line Pipe GmbH", "Führungskräfteentwicklung in Industrieumfeldern"),
            ],
        },
        "en": {
            "logistics": (
                "Düsseldorf is about two hours from the Osnabrück office. On-site sessions "
                "are combined with online phases — suited to business-oriented, tightly "
                "scheduled calendars."
            ),
            "references_title": "References linked to Düsseldorf",
            "references_intro": "Selected mandates in business-oriented and industrial contexts:",
            "references": [
                ("Emprise AG, Düsseldorf", "Coaching and facilitation in business contexts"),
                ("Ruhr-Steinkohle AG", "Process facilitation in industry and change"),
                ("Salzgitter Mannesmann Line Pipe GmbH", "Leadership development in industrial settings"),
            ],
        },
    },
}

REGION_PATCHES: dict[str, dict] = {
    "muenster": {
        "module_order": [
            "hero", "intro", "sectors", "mandates", "mini_case", "logistics",
            "faq", "references", "formats", "format_teaser", "services", "related", "cta",
        ],
        "de": {
            "logistics": (
                "Münster ist vom Büro in Osnabrück aus in etwa einer Stunde erreichbar — "
                "viele Mandate kombinieren Termine in Münster mit Coachings in Osnabrück."
            ),
            "references": [
                ("Caritas Pflegezentrum Georgsmarienhütte GmbH", "Coaching im Gesundheits- und Sozialwesen"),
                ("Malteser Hilfsdienst e.V.", "Prozessbegleitung in sozialen Trägern"),
                ("Stiftung Neuerkerode", "Führungskräfteentwicklung in institutionellen Kontexten"),
                ("Landkreis Ammerland", "Coaching in der öffentlichen Verwaltung"),
            ],
        },
        "en": {
            "logistics": (
                "Münster is about an hour from the Osnabrück office — many mandates combine "
                "sessions in Münster with coaching in Osnabrück."
            ),
            "references": [
                ("Caritas Pflegezentrum Georgsmarienhütte GmbH", "Coaching in healthcare and the social sector"),
                ("Malteser Hilfsdienst e.V.", "Process facilitation in social-sector bodies"),
                ("Stiftung Neuerkerode", "Leadership development in institutional contexts"),
                ("Landkreis Ammerland", "Coaching in public administration"),
            ],
        },
    },
    "oldenburg": {
        "module_order": [
            "hero", "intro", "references", "sectors", "mini_case", "logistics",
            "formats", "faq", "format_teaser", "services", "related", "cta",
        ],
        "de": {
            "logistics": (
                "Oldenburg ist vom Büro in Osnabrück aus in etwa 45 Minuten erreichbar — "
                "kurze Wege für Coachings, Workshops und Prozessbegleitung vor Ort."
            ),
            "references": [
                ("Klinikum Oldenburg", "Coaching und Teamentwicklung im Klinikverbund"),
                ("Evangelisches Krankenhaus Oldenburg", "Führungskräfteentwicklung im Gesundheitswesen"),
                ("Elisabeth-Kinderkrankenhaus im Klinikum Oldenburg", "Prozessbegleitung in der Pädiatrie"),
                ("Sozialstation der Diakonie, Oldenburg", "Coaching in sozialen Trägern"),
                ("Oldenburgische Landesbank", "Coaching in Finanz- und Dienstleistungskontexten"),
            ],
        },
        "en": {
            "logistics": (
                "Oldenburg is about 45 minutes from the Osnabrück office — short distances "
                "for coaching, workshops and on-site process facilitation."
            ),
            "references": [
                ("Klinikum Oldenburg", "Coaching and team development in a hospital network"),
                ("Evangelisches Krankenhaus Oldenburg", "Leadership development in healthcare"),
                ("Elisabeth Children's Hospital at Klinikum Oldenburg", "Process facilitation in paediatrics"),
                ("Sozialstation der Diakonie, Oldenburg", "Coaching in social-sector bodies"),
                ("Oldenburgische Landesbank", "Coaching in financial and service contexts"),
            ],
        },
    },
    "bremen": {
        "module_order": [
            "hero", "intro", "mandates", "faq", "references", "formats", "mini_case",
            "logistics", "format_teaser", "services", "related", "cta",
        ],
        "de": {
            "logistics": (
                "Bremen ist vom Büro in Osnabrück aus in etwa einer Stunde erreichbar — "
                "regelmäßige Präsenztermine sind gut planbar, ergänzt durch Online-Phasen."
            ),
            "references": [
                ("Gemeinde Ritterhude", "Coaching in der kommunalen Verwaltung"),
                ("Kreis Pinneberg", "Prozessbegleitung im öffentlichen Sektor"),
                ("Wilo SE Werk Minden GmbH", "Führungskräfteentwicklung in Industrie und Technik"),
                ("Condor Flugdienst GmbH", "Coaching in wandelnden Organisationen"),
            ],
        },
        "en": {
            "logistics": (
                "Bremen is about an hour from the Osnabrück office — regular in-person "
                "sessions are easy to plan, supplemented by online phases."
            ),
            "references": [
                ("Gemeinde Ritterhude", "Coaching in municipal administration"),
                ("Kreis Pinneberg", "Process facilitation in the public sector"),
                ("Wilo SE Werk Minden GmbH", "Leadership development in industry and technology"),
                ("Condor Flugdienst GmbH", "Coaching in changing organisations"),
            ],
        },
    },
}


def apply_patch(target: dict, patch: dict) -> None:
    if "module_order" in patch:
        target["module_order"] = patch["module_order"]
    for lang in ("de", "en"):
        if lang not in patch:
            continue
        target[lang].update(patch[lang])


def apply_all_patches() -> None:
    from standorte_data import CITIES
    from standorte_metro_cities import METRO_CITIES
    from standorte_zurich import ZUERICH

    for slug, patch in PATCHES.items():
        apply_patch(CITIES[slug], patch)
    for slug, patch in METRO_PATCHES.items():
        apply_patch(METRO_CITIES[slug], patch)
    for slug, patch in REGION_PATCHES.items():
        apply_patch(CITIES[slug], patch)
    apply_patch(ZUERICH, PATCHES["zuerich"])


if __name__ == "__main__":
    apply_all_patches()
    print("Applied standort content patches")
