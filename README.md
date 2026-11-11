# Malmös väder i terminalen

Ett litet undervisningsexempel i Python som hämtar sju dagars väderprognos
från [Open-Meteo](https://open-meteo.com/en/docs). Ingen API-nyckel behövs
för detta icke-kommersiella exempel.

> Skrivet av OpenAI Codex.

## Kör programmet

Du behöver Python 3 och internetanslutning. Kör i projektmappen:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python weather.py
```

På Windows aktiverar du miljön med `.venv\Scripts\activate` i stället.

## Visa eleverna

Följ de tre stegen i `weather.py`:

1. **Förfrågan:** `requests.get()` skickar koordinater, önskade vädervärden
   och tidszon till API:et. `params` blir parametrar i webbadressen.
2. **Svar:** `raise_for_status()` kontrollerar HTTP-statusen och `svar.json()`
   gör om JSON-svaret till Python-dictionaries och listor.
3. **Presentation:** `skriv_prognos()` läser listorna i `data["daily"]`.
   Samma index i varje lista hör till samma datum. Väderkoder översätts till
   svenska och f-strängar ger tabellen jämna kolumner.

Prova att lägga `print(svar.url)` och `print(svar.status_code)` efter
`requests.get()` för att se adressen och HTTP-statusen. Lägg
`print(data)` efter `data = hamta_prognos()` för att undersöka JSON-svaret
som Python-data innan det formateras.

Elevuppgifter: byt koordinater till en annan stad, ändra `forecast_days`
till 3 eller hitta den varmaste dagen i prognosen.

Prognosen kan ändras mellan körningar. Strecket `–` betyder att ett värde
saknas. Datakälla: [Open-Meteo](https://open-meteo.com/).
