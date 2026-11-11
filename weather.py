"""Hämta Malmös sjudygnsprognos med requests och Open-Meteo."""

from datetime import date
import sys

import requests


API_URL = "https://api.open-meteo.com/v1/forecast"
VECKODAGAR = ["mån", "tis", "ons", "tor", "fre", "lör", "sön"]

# API:et använder WMO-koder för att beskriva vädret.
VADERKODER = {
    0: "Klart", 1: "Mestadels klart", 2: "Halvklart", 3: "Mulet",
    45: "Dimma", 48: "Rimfrostdimma",
    51: "Lätt duggregn", 53: "Duggregn", 55: "Tätt duggregn",
    56: "Lätt underkylt duggregn", 57: "Underkylt duggregn",
    61: "Lätt regn", 63: "Regn", 65: "Kraftigt regn",
    66: "Lätt underkylt regn", 67: "Underkylt regn",
    71: "Lätt snöfall", 73: "Snöfall", 75: "Kraftigt snöfall",
    77: "Snökorn", 80: "Lätta regnskurar", 81: "Regnskurar",
    82: "Kraftiga regnskurar", 85: "Lätta snöbyar", 86: "Kraftiga snöbyar",
    95: "Åska", 96: "Åska med hagel", 99: "Åska med kraftigt hagel",
}


def hamta_prognos():
    """1. Skicka en HTTP-förfrågan och 2. omvandla JSON till en dictionary."""
    parametrar = {
        "latitude": 55.6050,
        "longitude": 13.0038,
        "daily": "weather_code,temperature_2m_min,temperature_2m_max,precipitation_sum",
        "timezone": "Europe/Stockholm",
        "forecast_days": 7,
        "temperature_unit": "celsius",
        "precipitation_unit": "mm",
    }
    svar = requests.get(API_URL, params=parametrar, timeout=15)
    svar.raise_for_status()  # Ger ett fel om servern t.ex. svarar med HTTP 500.
    return svar.json()


def tal(varde):
    """Visa en decimal med svenskt decimaltecken; hantera saknade värden."""
    return "–" if varde is None else f"{varde:.1f}".replace(".", ",")


def skriv_prognos(data):
    """3. Plocka ut värden ur svaret och visa dem i en tabell."""
    dagar = data["daily"]
    print("\nVÄDERPROGNOS FÖR MALMÖ")
    print("Kommande 7 dagar • lokal tid: Europe/Stockholm\n")
    print(f"{'Dag':<12} {'Väder':<28} {'Min °C':>8} {'Max °C':>8} {'Regn/snö mm':>12}")
    print("─" * 72)

    for i, datumtext in enumerate(dagar["time"]):
        datum = date.fromisoformat(datumtext)
        dag = f"{VECKODAGAR[datum.weekday()]} {datum:%d/%m}"
        kod = dagar["weather_code"][i]
        vader = VADERKODER.get(kod, "Uppgift saknas")
        minimum = tal(dagar["temperature_2m_min"][i])
        maximum = tal(dagar["temperature_2m_max"][i])
        nederbord = tal(dagar["precipitation_sum"][i])
        print(f"{dag:<12} {vader:<28} {minimum:>8} {maximum:>8} {nederbord:>12}")

    print("\nNederbörd anges som vattenmängd, även för snö.")
    print("Källa: Open-Meteo • https://open-meteo.com/\n")


def main():
    try:
        data = hamta_prognos()
        skriv_prognos(data)
    except requests.exceptions.RequestException as fel:
        print(f"Kunde inte hämta vädret. Kontrollera internetanslutningen.\n{fel}", file=sys.stderr)
        return 1
    except (ValueError, KeyError, TypeError, IndexError):
        print("API:et skickade ett oväntat svar. Försök igen senare.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
