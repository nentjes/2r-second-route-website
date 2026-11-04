# B-125 — Nederlandse uitleg over de natuurlijke stem

4 november 2026. Op verzoek van Roel zijn uitsluitend de twee aangeleverde
zinnen in de Nederlandse uitlegpagina aangepast. De overige vijf talen
volgen later. Bron: `../build.py`; maandlimiet:
`../../gedeeld/waarheden.json`, `stemmen.vloer_verhalen_per_maand`.
De schrijfwijze “honderd” is een tekstuele weergave van die registerwaarde;
een andere waarde wordt als getal weergegeven. Geen wijziging in structuur,
iconen, app of routegegevens.

## Controleplan vóór de build

| Scenario | Verwacht |
|---|---|
| Zonder stemtegoed | Beide passages noemen de natuurlijke stem en de maandlimiet. |
| Betaalde mogelijkheden | De afsluiting noemt de extra expressieve stem en sommige luisterroutes. |
| Registerwaarde verandert | Beide passages volgen de gewijzigde waarde; geen oude limiet blijft staan. |
| Ontbrekende of ongeldige waarde | Bouw stopt in plaats van een gratis aanbod te verzinnen. |
| Afbakening | Alleen de twee zinnen in `public/nl/zo-werkt-het.html` veranderen. |

## Redactionele review

De gratis stem is begrensd per maand; de tekst belooft geen onbeperkte
natuurlijke stem en noemt geen eenmalig proefpotje. De systeemstem na
verbruik van de vloer en de abonnementsvoorwaarden staan niet in deze twee
korte passages; de opdracht is bewust beperkt tot de aangeleverde vervanging.
De bestaande namen “Standaardstem” en “Mooie stem” zijn niet hernoemd.

## Bouwen

De volledige generator controleert ook routegegevens. Als de bestaande
ontbrekende begaanbaarheid van de Jubilee-route de volledige build blokkeert,
kan uitsluitend deze onafhankelijke uitlegpagina worden gegenereerd:

```bash
python3 -c "import build; build.write('nl/zo-werkt-het.html', build.build_howto('nl'))"
```

Daarbij blijven routecontroles en routegegevens intact. Publicatie vereist
een actuele checkout, een commit en het bestaande smoke-ritueel.
