# Featured references (max 3) — shown separately at top, excluded from sector lists.

FEATURED = [
    "Telekom AG",
    '<span class="referenzen-featured-name">BARMER</span> <span class="ref-tag ref-tag--stacked">{tag}</span>',
    "Lindt &amp; Sprüngli GmbH, Aachen",
]

FEATURED_SECTORS = [
    "it-telekom-energie",
    "gesundheit-soziales",
    "konsumgueter-handel",
]

SECTOR_SLUGS = [
    "gesundheit-soziales",
    "industrie-technik",
    "it-telekom-energie",
    "automotive-maschinenbau",
    "konsumgueter-handel",
    "finanzen-versicherung",
    "personal-beratung",
    "oeffentlicher-sektor",
    "bildung-kultur-wissenschaft",
    "weitere-unternehmen",
]

SECTORS_DE = [
    ("Gesundheit &amp; Soziales", [
        "BBraun Melsungen AG",
        "BBraun Travacare GmbH",
        "Bildungsinstitut Gesundheit am Klinikum Leer",
        "Caritas Pflegezentrum Georgsmarienhütte GmbH",
        "Deutsche Leberhilfe e.V.",
        "Die Akademie am Klinikum Osnabrück",
        "Elisabeth-Kinderkrankenhaus im Klinikum Oldenburg",
        "Euregioklinik Nordhorn",
        "Evangelisches Krankenhaus Oldenburg",
        "FERRING Arzneimittel GmbH",
        "Kinderklinik Siegen",
        "Klinikum Oldenburg",
        "Klinikum Osnabrück",
        "Krankenhaus Agatharied GmbH",
        "Landesbildungszentrum für Hörgeschädigte Osnabrück",
        "Lebenshilfe Nordhorn gGmbH",
        "Malteser Hilfsdienst e.V.",
        "Marienhospital Hamm",
        "Medizinische Hochschule Hannover",
        "MedoClin Hedon Klinik Lingen",
        "MVZ Dentologicum GbR Hamburg",
        "Nephrologisches Zentrum Emsland",
        "Sozialstation der Diakonie, Oldenburg",
        "St.-Vinzenz-Hospital Haselünne GmbH",
        "Stiftung Neuerkerode",
        "Villa Savelsberg Pflegedienst",
    ]),
    ("Industrie &amp; Technik", [
        "CKS Systeme GmbH",
        "Eichsfelder Energie- und Wasserversorgungs GmbH",
        "EWEX Engineering GmbH + Co. KG, Boxberg",
        "Eylarduswerk, Bad Bentheim",
        "Hartford Steam Boiler International GmbH",
        "Holzner Druckbehälter GmbH",
        "Ingenieurgemeinschaft igk Krabbe GmbH &amp; Co. KG",
        "Liebherr-Werk Biberach GmbH",
        "Lüning Ladenbau GmbH",
        "Ruhr-Steinkohle AG",
        "Salzgitter Mannesmann Line Pipe GmbH",
        "Sedai Druck GmbH &amp; Co. KG",
        "Sedus Systems GmbH",
        "Vanderlande Industries GmbH",
        "Wilo SE Werk Minden GmbH",
    ]),
    ("IT, Telekommunikation &amp; Energie", [
        "Condor Flugdienst GmbH",
        "T-Systems International GmbH",
        "Vattenfall Deutschland",
    ]),
    ("Automotive &amp; Maschinenbau", [
        "Jopp Automotive GmbH",
        "Putzmeister Concrete Pumps GmbH, Aichtal",
    ]),
    ("Konsumgüter &amp; Handel", [
        "Feet Control GmbH",
    ]),
    ("Finanzen &amp; Versicherung", [
        "Oldenburgische Landesbank",
        "Operational Services GmbH &amp; Co KG",
        "Sparkasse Ostprignitz-Ruppin",
        "Stadtsparkasse Schmallenberg",
    ]),
    ("Personal &amp; Beratung", [
        "c-p-o gmbH, CH <span class=\"ref-tag\">{tag}</span>",
        "CMC Personal GmbH",
        "Empalis GmbH",
        "Emprise AG, Düsseldorf",
        "Emprise Human Value GmbH",
        'Footpower Service GmbH, Gummersbach <span class="ref-tag">{tag}</span>',
        "IMPART GmbH, Osnabrück",
        "milch &amp; zucker Talent Acquisition &amp; Talent Management Company AG",
        "OBIC Voss &amp; Partner GmbH",
        "Palaimon Consulting Hamburg",
        "SCAN-UP AG, Hamburg",
        "Successnet AG München",
        "Topalis AG, Stuttgart",
        'wilob AG, Weiterbildungsinstitut für lösungsorientierte Therapie und Beratung, CH <span class="ref-tag">{tag}</span>',
    ]),
    ("Öffentlicher Sektor", [
        "BVMW Servicegesellschaft, Berlin",
        "Gemeinde Lengede",
        "Gemeinde Ritterhude",
        "Kreis Pinneberg",
        "Landkreis Ammerland",
        "Stadt Baden-Baden",
        "Stadt Cottbus",
        "Stadt Haren",
        "Stadt Helmstedt",
        "Stadt Leverkusen",
        "Stadt Osnabrück",
        "Stadt Schwarzenbek",
        "Stadt Zehdenick, Brandenburg",
    ]),
    ("Bildung, Kultur &amp; Wissenschaft", [
        "Akademie Waldschlösschen, Göttingen",
        "Berufsbildungswerk Nürnberg",
        "Hochschule für Management Technik und Kultur, Osnabrück",
        "K.I.T.A. gGmbH",
        "Kulturfabrik Kampnagel, Hamburg",
        "Rondo Seminarhaus Lembruch",
        "Staatliche Hochschule für Musik Trossingen",
        "Tanzschule Knaul",
        "Theaterpädagogische Werkstatt Osnabrück",
        "Universität Osnabrück, FB Persönlichkeitspsychologie",
    ]),
    ("Weitere Unternehmen", [
        "Arithnea GmbH",
        "Baugenossenschaft Wiederaufbau eG, Braunschweig",
        "Knutzen Wohnen GmbH",
        "MeDiTa GmbH",
        "Stadtsportbund Osnabrück",
        "VNB Göttingen",
    ]),
]

SECTORS_EN = [
    ("Healthcare &amp; social services", SECTORS_DE[0][1]),
    ("Industry &amp; engineering", SECTORS_DE[1][1]),
    ("IT, telecommunications &amp; energy", SECTORS_DE[2][1]),
    ("Automotive &amp; mechanical engineering", SECTORS_DE[3][1]),
    ("Consumer goods &amp; retail", SECTORS_DE[4][1]),
    ("Finance &amp; insurance", SECTORS_DE[5][1]),
    ("HR &amp; consulting", SECTORS_DE[6][1]),
    ("Public sector", SECTORS_DE[7][1]),
    ("Education, culture &amp; science", SECTORS_DE[8][1]),
    ("Other companies", SECTORS_DE[9][1]),
]

TEXT = {
    "de": {
        "comment": "Referenzen",
        "eyebrow": "Referenzen",
        "h1": "Ausgewählte Kunden und Kooperationen",
        "intro": (
            "Die aufgelisteten Firmen stellen eine Auswahl von Kunden dar, für die "
            "Personalentwicklungsmaßnahmen oder Prozessbegleitungen erfolgt sind."
        ),
        "featured_title": "Ausgewählte Referenzen",
        "tag": "Kooperation",
        "sector_count": "{n} Unternehmen",
        "note": "sowie diverse Landes- und Bundesämter und Ministerien",
        "disclaimer": (
            "Bitte haben Sie Verständnis dafür, dass Coaching-Kunden und einige "
            "Unternehmen vertraulich behandelt werden."
        ),
        "filter_label": "Nach Branche filtern",
        "filter_all": "Alle Branchen",
        "search_label": "Unternehmen suchen",
        "search_placeholder": "Unternehmen suchen …",
        "filter_results_one": "{n} Unternehmen in {sector}",
        "filter_results_many": "{n} Unternehmen in {count} Branchen",
        "filter_empty": "Keine Treffer — Filter zurücksetzen",
        "filter_reset": "Filter zurücksetzen",
    },
    "en": {
        "comment": "References",
        "eyebrow": "References",
        "h1": "Selected clients and collaborations",
        "intro": (
            "The companies listed represent a selection of clients for whom "
            "human resources development measures or process facilitation have been provided."
        ),
        "featured_title": "Selected references",
        "tag": "Collaboration",
        "sector_count": "{n} companies",
        "note": "as well as various state and federal agencies and ministries",
        "disclaimer": (
            "Please understand that coaching clients and some "
            "companies are treated confidentially."
        ),
        "filter_label": "Filter by sector",
        "filter_all": "All sectors",
        "search_label": "Search companies",
        "search_placeholder": "Search companies …",
        "filter_results_one": "{n} companies in {sector}",
        "filter_results_many": "{n} companies in {count} sectors",
        "filter_empty": "No results — reset filters",
        "filter_reset": "Reset filters",
    },
}
