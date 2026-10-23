# Privacy B-122 — vrijgegeven door Roel op 23 oktober 2026

Roel heeft bevestigd dat de privacytekst vóór de winkelrelease van build 124
op 2route.nl moet staan. De aangeleverde Nederlandse en Engelse alinea's
staan ongewijzigd in `../privacy.json`, met vier vertalingen (DE/FR/ES/PT).
De bewaartermijnen worden uit `../../gedeeld/waarheden.json` ingevuld.

De pagina vermeldt dat de uitleg bij build 124 hoort en dat gesproken vragen
en partnertips nog niet beschikbaar zijn. De toelichting bij de vijf alinea's
behoudt de overige bewaartermijnen, de keuze “Niets bijhouden”, de uitzondering
voor testers en het bewaren van aankoopgegevens buiten de logboek-wisfunctie.
Bronnen: B-122, FO §12, DPIA §2b en `handleWisMijnGegevens` in de Worker.

## Opbouw en publicatie

- `privacy.json`: enige bron van de privacyteksten en publicatiedatum.
- `privacy_policy.py`: invullen van termijnen en renderen in de bestaande huisstijl.
- `python3 build.py --privacy-only`: schrijft alleen de zes privacypagina's.
- `python3 preview_privacy.py`: optionele lokale voorvertoning, buiten `public/`.
- Gewone `python3 build.py`: bevat dezelfde nieuwe privacyrenderer, maar stopt
  momenteel op bestaande ontbrekende begaanbaarheidsdata van de Jubilee-route.

De gerichte build behoudt alle andere publieke bestanden en schakelt de
routecontroles niet uit. Routeinhoud, audio, routegegevens en worker zijn
ongewijzigd. De laatste remote commits zijn opgehaald; de checkout bevat
Claude's Londense routes van 13 oktober. Vooraf zijn homepage, uitlegpagina,
stijl, route-index, Drakensteyn en beide Londense manifesten vergeleken met live:
identiek. De laatste Cloudflare-publicatie vóór deze wijziging is
`cf9365d5-1460-43a8-87e9-aa74c1571df7` van 13 oktober 2026.

## Controle vóór publicatie

- Eenheidstoetsen 411/411, reisproef 7/7, waarhedencontrole 244 spiegels,
  gelijkloopcontrole lokaal: geslaagd.
- Alle zes pagina's gegenereerd en vergeleken met de bron; NL/EN letterlijk
  gelijk aan de aangeleverde vijf alinea's. Geen conceptlabels of noindex in
  de publieke pagina's; correcte taal, canonieke links en taalwissels.
- Alleen de zes privacybestanden veranderen binnen `public/`.
- Bestaande algemene buildblokkade opnieuw bevestigd; geen routegegevens
  aangevuld of validaties omzeild. De privacybuild heeft die data niet nodig.
- Visuele controle van de definitieve Nederlandse pagina; eerdere controle
  van dezelfde opmaak op een smal scherm en desktop, zonder horizontale overloop.

## Red-teamreview (denkoefening, geen juridisch advies of gebruikersonderzoek)

| Bevinding | Afhandeling |
|---|---|
| Spraak en partnertips lijken al beschikbaar | Hersteld: opvallende toelichting boven de tekst noemt beide als nog niet beschikbaar. |
| Zeven dagen zou ten onrechte op alle gegevens kunnen slaan | Hersteld: overige bewaartermijnen staan afzonderlijk uitgelegd. |
| “Alles wissen” kan aankoopgegevens suggereren | Hersteld: uitzondering in de toelichting; gecontroleerd dat de wisfunctie events en stories wist. |
| Niet-delenbelofte naast leveranciers | Aanvaard als door Roel aangeleverde formulering: de direct volgende zin noemt de verwerkers expliciet en hun opdrachtrelatie. |
| Termijnen kunnen uit elkaar lopen | Hersteld: bron is het register, geen handmatige kopieën van de termijnen in de talen. |
| Volledige deploy kan ouder werk terugzetten | Afgehandeld: fetch, clean start, vergelijking met live en uitsluitend zes gewijzigde publieke bestanden. |
| App Store-label en verwerkersvoorwaarden | Blijven acties van Roel volgens de briefing; deze websitepublicatie bevestigt niet dat ze zijn afgerond en geeft de app niet vrij. |

Na publicatie volgen verificatie van alle zes live pagina's en het verplichte
`worker/controle-na-deploy.sh`. De winkelrelease zelf valt buiten deze opdracht.

## Publicatie bevestigd

- Gepubliceerd op 23 oktober 2026, websitecommit `15650c8`.
- Cloudflare-versie: `3fbdcfa9-6359-43b4-bf43-9763e288d69b`.
- Wrangler bevestigt uitsluitend zes gewijzigde assets: de privacypagina's.
- Alle zes live pagina's opgehaald met redirects en byte voor byte gelijk
  bevonden aan de lokale publicatiebestanden; geen conceptmelding of noindex.
- Live Nederlandse pagina visueel gecontroleerd.
- `worker/controle-na-deploy.sh`: exit 0, alle ingangen gezond, beide API's
  op b124, route/audio/CORS/redirect gezond, gecachte én verse stem geslaagd.
