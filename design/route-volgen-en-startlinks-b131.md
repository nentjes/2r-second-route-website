# Route volgen en startlinks — B-131, 18 november 2026

Bron: `../../voorstellen/2026-11-18-claude-route-volgen-en-startlinks-voor-codex.md`.
De nieuwe gegevens worden uitsluitend uit `routes-content/<slug>.json` gelezen.

## Scenario's vóór de build

| Scenario | Verwacht |
|---|---|
| Gemarkeerde route, bijvoorbeeld Berkheide | Volgtekst als tekstlabel naast klim, verharding en bankjes op de groene tegel én routepagina. |
| Geen bevestigde markering | De aangeleverde tekst verwijst naar de kaart in de app; geen markering verzinnen. |
| Drakensteyn: geen `volgen` en geen `start` | Geen volglabel, startblok of lege links. |
| Engels, Duits, Frans, Spaans en Portugees | Alle zes bekende volgteksten en beide startlinks vertaald. |
| Nieuwe, nog onvertaalde volgtekst | Alleen op de Nederlandse pagina zichtbaar. |
| Kaart of Street View openen | Exact het aangeleverde adres, nieuw tabblad, `noopener noreferrer`. |
| Eén startlink ontbreekt | Alleen de beschikbare link zichtbaar. |
| Kleine schermen, grote tekst en toetsenbord | Labels en links mogen omslaan; links minstens 44 px hoog en met zichtbare focus. |
| Herhaalde gerichte build | Identieke uitvoer, geen dubbele labels of links. |
| Onvolledige, nog niet gepubliceerde London-routes | Volledige build blijft blokkeren; gerichte build publiceert geen nieuwe routes. |
| Afbakening | Routegegevens, kaartbestanden, audio, worker en alle overige pagina-inhoud blijven gelijk. |

## Opbouw

`route_follow_badge()` en `route_start_html()` zijn de gedeelde rendering voor
de volledige generator en de gerichte build. De Nederlandse tekst en de twee
linkadressen komen uit de routegegevens; vertalingen staan één keer in de
websitetaaltabellen. Het startblok staat bij de routekaart, vóór de kaart zelf.

De volledige build controleert ook de nog niet gepubliceerde routes en blijft
terecht stoppen als hun begaanbaarheid ontbreekt. Daarom werkt
`python3 build.py --route-guidance-only` uitsluitend de bestaande tegels en
routepagina's bij. Geen route wordt toegevoegd, geen controle versoepeld en
geen nieuwe route- of audio-inhoud gepubliceerd. Alle vervangingen worden
eerst gecontroleerd; pas daarna worden bestanden geschreven.

## Uitgevoerde controles

- Actuele `origin/main` opgehaald; uitgangscommit `4f8ffc2`, geen afwijkende
  remote commits of lokale wijzigingen bij aanvang.
- Volledige `python3 build.py` stopt vóór het schrijven op de bestaande
  ontbrekende begaanbaarheid van `jubilee-walk-central-london-circular-walk`.
- Gerichte build geslaagd: 84 bestanden aangepast (zes overzichten en
  dertien routepagina's per taal). Drakensteyn blijft ongewijzigd.
- Alle 90 bestaande routepagina's en overzichten, 84 tegels en 156 startlinks
  gecontroleerd op tekst, exact bronadres, nieuw tabblad en veilige `rel`.
- Normale pagina- en overzichtsrendering in alle zes talen gecontroleerd,
  uitsluitend in geheugen met de reeds gepubliceerde routes.
- Ontbrekende en lege velden, onvertaalde tekst, één beschikbare startlink
  en HTML-escaping gecontroleerd. Bewust de Engelse vertaling weggelaten:
  de controle vond de fout. Geen brongegevens aangepast.
- Tweede gerichte build wijzigt nul bestanden. Afwijkende markup in een
  tijdelijke kopie blokkeert de hele gerichte build vóór enige schrijfactie.
- Na het verwijderen van uitsluitend de nieuwe labels en startblokken is
  de HTML byte voor byte gelijk aan de uitgangscommit. Alle 221 beschermde
  route-, audio-, kaartdata- en workerbestanden hebben dezelfde SHA-256.
- `python3 check_urls.py`: alle 192 sitemapadressen slagen voor canonical,
  hreflang en interne links. `git diff --check` slaagt.
- App-eenheidstoetsen: 417/417 geslaagd. Gelijkloop `--lokaal --poort`:
  exit 0 met bestaande signalen over privacyteksten buiten deze wijziging.
- Reisproef niet uitvoerbaar: de sandbox weigert het openen van een lokale
  serverpoort (`PermissionError`). De visuele browsercontrole is eveneens
  onvoltooid: de browserbeveiliging staat geen lokale `file:`-adressen toe.
  Mobiele weergave, grotere tekst en interactie zijn dus niet als visueel
  geslaagd aangemerkt. De nieuwe links hebben in CSS een tikhoogte van
  minimaal 44 px, omslaande regels en een expliciete focusrand.

## Publicatiestatus

Lokaal geïmplementeerd en gecontroleerd. Geen push of live deploy uitgevoerd.
Voor publicatie: actuele remote stand opnemen, commit/push, daarna deploy en
`../worker/controle-na-deploy.sh` plus een live weergave- en linkcontrole.
