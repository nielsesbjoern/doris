#!/usr/bin/env python3
"""Coaching format comparison content (DE + EN)."""

from __future__ import annotations

from typing import TypedDict


class Format(TypedDict):
    id: str
    group: str
    title_de: str
    title_en: str
    duration_de: str
    duration_en: str
    occasion_de: str
    occasion_en: str
    outcome_de: str
    outcome_en: str
    suitable_de: str
    suitable_en: str
    less_suitable_de: str
    less_suitable_en: str


FORMATS: list[Format] = [
    {
        "id": "situativ",
        "group": "anlass",
        "title_de": "Situatives Coaching",
        "title_en": "Situational Coaching",
        "duration_de": "1–3 Termine à 2–3 Stunden",
        "duration_en": "1–3 sessions of 2–3 hours",
        "occasion_de": "Konkrete Führungssituation, wichtiges Gespräch oder Entscheidung",
        "occasion_en": "A concrete leadership situation, important conversation or decision",
        "outcome_de": "Klarheit, Handlungsoptionen, Gesprächsvorbereitung",
        "outcome_en": "Clarity, options for action, conversation preparation",
        "suitable_de": "Führungskräfte mit akutem Klärungsbedarf",
        "suitable_en": "Leaders with an immediate need for clarification",
        "less_suitable_de": "Langfristige Entwicklungsthemen ohne zeitlichen Druck",
        "less_suitable_en": "Long-term development topics without time pressure",
    },
    {
        "id": "onboarding",
        "group": "anlass",
        "title_de": "Onboarding-Coaching",
        "title_en": "Onboarding Coaching",
        "duration_de": "3–6 Termine über mehrere Wochen",
        "duration_en": "3–6 sessions over several weeks",
        "occasion_de": "Übernahme eines neuen Unternehmens, Bereichs oder einer Führungsrolle",
        "occasion_en": "Taking on a new company, division or leadership role",
        "outcome_de": "Systematischer Einstieg, Rollenklärung, Vermeidung früher Fehltritte",
        "outcome_en": "Structured start, role clarity, avoiding early missteps",
        "suitable_de": "Neue Geschäftsführer, Bereichsleiter, Führungskräfte nach Wechsel",
        "suitable_en": "New managing directors, division heads, leaders after a change of role",
        "less_suitable_de": "Etablierte Führungskräfte ohne Rollenwechsel",
        "less_suitable_en": "Established leaders without a change of role",
    },
    {
        "id": "positionierung",
        "group": "anlass",
        "title_de": "Positionierungs-Coaching",
        "title_en": "Positioning Coaching",
        "duration_de": "2–4 Termine",
        "duration_en": "2–4 sessions",
        "occasion_de": "Unklare Rolle im Unternehmen, Veränderungen in der Organisationsstruktur",
        "occasion_en": "Unclear role in the organisation, changes in organisational structure",
        "outcome_de": "Struktureller Überblick, klare Positionierung im Gefüge",
        "outcome_en": "Structural overview, clear positioning within the organisation",
        "suitable_de": "Führungskräfte nach Reorganisation oder bei Rollenunsicherheit",
        "suitable_en": "Leaders after reorganisation or with role uncertainty",
        "less_suitable_de": "Rein fachliche Aufgaben ohne organisationale Dimension",
        "less_suitable_en": "Purely technical tasks without an organisational dimension",
    },
    {
        "id": "aufgaben",
        "group": "anlass",
        "title_de": "Aufgabenbezogenes Coaching",
        "title_en": "Task-Focused Coaching",
        "duration_de": "2–5 Termine, ggf. mit Trainingselementen",
        "duration_en": "2–5 sessions, with training elements on request",
        "occasion_de": "Konkrete Führungsaufgabe (Feedback, Delegation, schwieriges Gespräch)",
        "occasion_en": "A specific leadership task (feedback, delegation, difficult conversation)",
        "outcome_de": "Praxisnahe Werkzeuge und Umsetzung für die konkrete Aufgabe",
        "outcome_en": "Practical tools and implementation for the specific task",
        "suitable_de": "Führungskräfte mit klar umrissener Aufgabenstellung",
        "suitable_en": "Leaders with a clearly defined task",
        "less_suitable_de": "Grundsätzliche Orientierungs- oder Identitätsfragen",
        "less_suitable_en": "Fundamental questions of orientation or identity",
    },
    {
        "id": "persoenlichkeit",
        "group": "anlass",
        "title_de": "Persönlichkeitscoaching",
        "title_en": "Personality Coaching",
        "duration_de": "4–8 Termine über mehrere Monate",
        "duration_en": "4–8 sessions over several months",
        "occasion_de": "Selbstentwicklung, Reflexion der eigenen Wirkung, Potenzialanalyse",
        "occasion_en": "Self-development, reflection on your impact, potential analysis",
        "outcome_de": "Vertiefte Selbsterkenntnis, neue Zielsetzungen, nachhaltige Entwicklung",
        "outcome_en": "Deeper self-awareness, new objectives, sustainable development",
        "suitable_de": "Führungskräfte mit Raum für langfristige persönliche Entwicklung",
        "suitable_en": "Leaders with scope for long-term personal development",
        "less_suitable_de": "Akute Krisen oder unmittelbar anstehende Entscheidungen",
        "less_suitable_en": "Acute crises or decisions due imminently",
    },
    {
        "id": "therapeutisch",
        "group": "anlass",
        "title_de": "Therapeutisches Coaching",
        "title_en": "Therapeutic Coaching",
        "duration_de": "Individuell, oft längerfristig",
        "duration_en": "Individual, often longer-term",
        "occasion_de": "Motivationsschwierigkeiten, Burnout-Verdacht, Energieverlust, innere Konflikte",
        "occasion_en": "Motivation difficulties, suspected burnout, loss of energy, inner conflicts",
        "outcome_de": "Ursachenklärung, Stabilisierung, Abgrenzung von rein fachlichen Themen",
        "outcome_en": "Root-cause clarification, stabilisation, distinction from purely professional topics",
        "suitable_de": "Situationen an der Grenze von Coaching und Therapie — mit Approbation abgedeckt",
        "suitable_en": "Situations at the boundary of coaching and therapy — covered by my licence",
        "less_suitable_de": "Reine Business- oder Strategiefragen ohne persönliche Belastung",
        "less_suitable_en": "Pure business or strategy questions without personal strain",
    },
    {
        "id": "intensiv",
        "group": "durchfuehrung",
        "title_de": "Intensiv-Settings",
        "title_en": "Intensive Settings",
        "duration_de": "1–2 intensive Termine à 3–4 Stunden",
        "duration_en": "1–2 intensive sessions of 3–4 hours",
        "occasion_de": "Wenig Zeit, hoher Klärungsbedarf — voller Kalender",
        "occasion_en": "Little time, high need for clarity — a full calendar",
        "outcome_de": "Komprimierte Arbeit an einer Kernfrage mit nachhaltiger Wirkung",
        "outcome_en": "Compressed work on a core question with lasting effect",
        "suitable_de": "Führungskräfte, die selten regelmäßige Termine wahrnehmen können",
        "suitable_en": "Leaders who rarely have scope for regular appointments",
        "less_suitable_de": "Themen, die Kontinuität und längere Begleitung erfordern",
        "less_suitable_en": "Topics that require continuity and longer-term support",
    },
    {
        "id": "smart",
        "group": "durchfuehrung",
        "title_de": "Smart-Coaching",
        "title_en": "Smart Coaching",
        "duration_de": "Kurze Impulse (30–45 Min.) per Telefon oder Video",
        "duration_en": "Short impulses (30–45 min.) by phone or video",
        "occasion_de": "Zwischen den Terminen, vor wichtigen Situationen, schnelle Reflexion",
        "occasion_en": "Between sessions, before important situations, quick reflection",
        "outcome_de": "Orientierung und Klarheit ohne großen Zeitaufwand",
        "outcome_en": "Orientation and clarity without a large time commitment",
        "suitable_de": "Führungskräfte mit wenig Zeit zwischen den Hauptterminen",
        "suitable_en": "Leaders with little time between main sessions",
        "less_suitable_de": "Tiefgehende Klärung komplexer Situationen",
        "less_suitable_en": "In-depth clarification of complex situations",
    },
    {
        "id": "cotj",
        "group": "durchfuehrung",
        "title_de": "Coaching-on-the-job",
        "title_en": "Coaching on the Job",
        "duration_de": "Begleitung im Arbeitsalltag, Termine vor Ort beim Kunden",
        "duration_en": "Support in the working day, sessions on site at your organisation",
        "occasion_de": "Umsetzung im direkten Führungskontakt, Beobachtung und Reflexion im Einsatz",
        "occasion_en": "Implementation in direct leadership contact, observation and reflection in practice",
        "outcome_de": "Direkter Transfer in die Praxis, Feedback zur Außenwirkung",
        "outcome_en": "Direct transfer into practice, feedback on external impact",
        "suitable_de": "Führungskräfte, die Lernen direkt in der Situation wollen",
        "suitable_en": "Leaders who want to learn directly in the situation",
        "less_suitable_de": "Themen, die vertraulichen Rückzug und Ruhe erfordern",
        "less_suitable_en": "Topics that require confidential retreat and calm",
    },
]

TEXT = {
    "de": {
        "title": "Formate im Vergleich",
        "intro": (
            "Welches Format passt zu Ihrer Situation? Die Übersicht ordnet Anlässe "
            "und Durchführungsformen ein — inklusive ehrlicher Abgrenzung."
        ),
        "jump": "Formate vergleichen",
        "group_anlass": "Anlässe & Themen",
        "group_durchfuehrung": "Durchführung",
        "filter_label": "Format filtern",
        "filter_all": "Alle anzeigen",
        "badge_anlass": "Anlass",
        "badge_durchfuehrung": "Durchführung",
        "label_duration": "Dauer / Setting",
        "label_occasion": "Typischer Anlass",
        "label_outcome": "Ergebnis",
        "label_suitable": "Gut geeignet für",
        "label_less_suitable": "Weniger geeignet für",
        "note": (
            "Gemeinsam klären wir, welches Format zur Situation passt — "
            "der Vergleich dient der Orientierung, nicht der Selbstdiagnose."
        ),
    },
    "en": {
        "title": "Compare formats",
        "intro": (
            "Which format fits your situation? This overview maps occasions "
            "and delivery modes — including honest guidance on when a format is less suitable."
        ),
        "jump": "Compare formats",
        "group_anlass": "Occasions & topics",
        "group_durchfuehrung": "Delivery",
        "filter_label": "Filter format",
        "filter_all": "Show all",
        "badge_anlass": "Occasion",
        "badge_durchfuehrung": "Delivery",
        "label_duration": "Duration / setting",
        "label_occasion": "Typical occasion",
        "label_outcome": "Outcome",
        "label_suitable": "Well suited for",
        "label_less_suitable": "Less suited for",
        "note": (
            "Together we clarify which format fits your situation — "
            "this comparison is for orientation, not self-diagnosis."
        ),
    },
}
