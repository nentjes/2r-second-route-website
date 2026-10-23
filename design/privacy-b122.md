# Privacyconcept B-122 — wacht op Roel

Bron: Roels aangeleverde tekst van 23 oktober 2026, ook in
`../../voorstellen/2026-10-23-privacytekst-voor-codex.md`.
Besluit: `../../docs/2R-DECISIONS.md`, B-122; FO §12; DPIA §2b.

## Klaargezet

`privacy-b122.json` bevat NL en EN zoals aangeleverd en vertalingen in DE,
FR, ES en PT. Bewaartermijnen worden tijdens het renderen uit
`../../gedeeld/waarheden.json` ingevuld. Geen aanpassing aan app of backend.

`python3 preview_privacy.py` maakt zes conceptpagina's in een nieuwe tijdelijke
map en toont het pad. Start daar een lokale webserver; open `/nl/privacy.html`.
De bestaande huisstijl, navigatie, taalwissel en contactmogelijkheid blijven
beschikbaar. Iedere pagina heeft een conceptmelding en `noindex, nofollow`.

De gewone `python3 build.py` gebruikt nog het bestaande privacybeleid.
Het concept komt niet in `public/` en dus ook niet mee bij een gewone deploy.
Er is niets gepubliceerd. `build.py` is alleen importeerbaar gemaakt zodat
de conceptweergave dezelfde siteshell kan gebruiken zonder de website te bouwen.
De route-inleesfunctie en haar bestaande controles draaien bij de gewone build,
zodat een privacyvoorvertoning niet afhankelijk is van routegegevens.

## Vóór vrijgave inhoudelijk afstemmen

1. Roels expliciete sein blijft nodig. B-122 is later aangevuld: build 124
   bevat de nieuwe locatieopslag en de webtekst moet vóór de winkelrelease
   aansluiten. De status van die release is hier niet vastgesteld.
2. B-122 en FO FR-12.6–12.7 zeggen dat gesproken vragen en partnertips nog
   niet bestaan. Het aangeleverde concept beschrijft ze als beschikbaar.
   Beslis bij vrijgave of die passages toekomstig worden geformuleerd of
   wachten op de betreffende functies. Niet stilzwijgend als live publiceren.
3. De korte tekst vervangt inhoudelijk nog niet alle details van het bestaande
   beleid: het overige logboek, verhalen, meldingen en aankopen hebben volgens
   FO FR-12.5 eigen bewaartermijnen. Ook "Niets bijhouden" (met de uitzondering
   voor testers) uit FR-12.2–12.4 ontbreekt. Neem deze details bij de definitieve
   pagina mee; "alles wissen" moet aansluiten op wat werkelijk wordt gewist.
4. "Niet delen met anderen" staat naast verwerking door leveranciers. Maak
   bij definitieve redactie duidelijk dat die leveranciers gegevens namens 2R
   verwerken. Controleer daarbij de werkelijk gebruikte leveranciers.
5. App Store-privacylabel en acceptatie van verwerkersvoorwaarden zijn volgens
   de briefing nog acties van Roel. Dit werk bevestigt niet dat ze zijn afgerond.

## Controleplan

- NL/EN: alle vijf alinea's letterlijk gelijk aan de briefing na invullen van
  de bewaartermijnen; vier vertalingen op dezelfde strekking controleren.
- Zes taalpagina's: juiste taal, conceptmelding, noindex, geen oude bewering
  dat locatie standaard niet wordt bewaard, geen oude dertigdagentermijn.
- Desktop en mobiel: leesbaarheid, taalwissel, contact en geen horizontale overloop.
- Conceptgeneratie verandert geen bestand in `public/`; gewone build neemt
  het concept niet mee. Routegegevens, routeaudio en worker blijven onaangeraakt.
- Vóór echte publicatie: red-teamreview volgens het testprotocol, actuele
  andere wijzigingen opnemen, committen en na deploy het smoke-ritueel uitvoeren.

## Latere activering

Na Roels sein en bovenstaande afstemming de definitieve tekst en benodigde
detailsecties in de gewone `build_privacy` verwerken. Verwijder dan de oude
tegenstrijdige samenvattingen en metadata in alle talen en zet de werkelijke
publicatiedatum. De conceptweergave is bewust geen publicatieknop.

## Uitkomst controles (23 oktober 2026)

- Eenheidstoetsen: 411/411 geslaagd; reisproef: 7/7 geslaagd;
  gelijkloopcontrole met `--lokaal`: geslaagd (geen controle van de live site).
- Zes concepten gerenderd, taal en noindex gecontroleerd; NL/EN letterlijk
  vergeleken met de aangeleverde bron. Publieke HTML bleef ongewijzigd.
- Lokale browsercontrole: Nederlandse tekst op smal scherm en Engelse tekst
  op desktop bekeken; geen horizontale overloop.
- `python3 build.py` stopt vóór het schrijven op ontbrekende `begaanbaarheid`
  voor `jubilee-walk-central-london-circular-walk`. Dit is een bestaande
  routegegevensblokkade. Geen controles verwijderd of data aangepast.
- Geen deploy; de releasecontrole en het smoke-ritueel horen bij de latere
  publicatie na Roels sein.
