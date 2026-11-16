# Canonieke websiteadressen — 16 november 2026

Bron: `../../voorstellen/2026-11-16-claude-website-canonical-voor-codex.md`
en Roels Search Console-schermafbeeldingen van 16 november.

## Scenario's vóór de wijziging

| Scenario | Verwacht na herstel |
|---|---|
| Losse pagina, stad of verhaal, in elke taal | Sitemap, canonical, hreflang, og:url en interne links gebruiken het adres zonder `.html`. |
| Homepage of mappagina | Adres met afsluitende slash blijft behouden. |
| Oude `.html`-link van buitenaf | Bestaande Cloudflare-omleiding blijft werken. |
| Taalwissel op de privacypagina | Blijft op privacy, met een schoon adres. |
| Nederlandse navigatie zonder paginaherlading | Canonical, hreflang en og:url volgen de nieuwe pagina. |
| Foto, audio, GPX, externe link, query of fragment | Geen onbedoelde URL-wijziging. |
| Routegegevens onvolledig | Volledige build blijft falen; de gerichte URL-correctie verandert alleen bestaande HTML en sitemap. |
| Daan Boom-verhaal | Blijft verwijderd en buiten de sitemap; geen omleiding naar andere inhoud. |

## Uitgangssituatie

- Schone websitecheckout, `HEAD == origin/main == e53dce1` na fetch.
- Live bevestigd: `/nl/zo-werkt-het.html` geeft 307 naar `/nl/zo-werkt-het`.
- `python3 build.py` faalt vóór het schrijven op ontbrekende begaanbaarheid
  van `jubilee-walk-central-london-circular-walk`; een bestaande blokkade,
  ook vastgelegd bij de publicaties van B-122 en B-125.
- Daan Boom is op 30 augustus verwijderd in commit `d380219`, met reden
  "gehallucineerd". De ontbrekende adressen uit Search Console horen daarbij.

## Uitgevoerde controles

- De nieuwe controle `python3 check_urls.py` faalde vóór de correctie met
  691 bevindingen bij 192 sitemapadressen. Hiermee is de regressie aangetoond.
- Na `python3 build.py --urls-only`: alle 192 adressen slagen voor sitemap,
  canonical, hreflang, og:url, interne paginalinks en volledigheid.
  De 78 losse HTML-adressen zijn nu schoon; de mappagina's behouden hun slash.
- `python3 check_urls.py --origin http://127.0.0.1:8787` slaagt tegen de echte
  lokale Cloudflare Assets-router: alle 192 pagina's geven direct HTTP 200.
  Start met `wrangler dev --local --local-upstream 2route.nl`; zonder die
  laatste optie kiest Wrangler de www-route en wordt iedere aanvraag 301.
- Grensgevallen beproefd: homepage, mappagina, detailpagina, `mijnindex.html`,
  query/fragment, externe link, data-attribuut, audio en tekst binnen scripts.
  Herschrijven is idempotent: de tweede URL-build wijzigt nul pagina's.
- Verse pagina- en privacyrendering gecontroleerd in alle zes talen.
- 29 unieke inline scripts in 192 pagina's slagen voor JavaScript-syntaxis.
  De aanvullende headless-browserproef kon hier niet worden uitgevoerd:
  Chrome stopt in deze omgeving met exitcode 134. De klik-/geschiedenistoets
  is daarom niet als geslaagd aangemerkt.
- De tekst en markup buiten URL-attributen en het navigatiescript zijn
  vergeleken met de uitgangscommit: identiek. Alle 222 beschermde route-,
  audio-, configuratie- en workerbestanden hebben dezelfde SHA-256.
- App-eenheidstoetsen: 417/417 geslaagd. Gelijkloop `--lokaal --poort`:
  exit 0 met bestaande niet-blokkerende signalen over de homepageprivacytekst;
  die tekst is niet onderdeel van deze wijziging.
- Wrangler dry-run geslaagd: 604 assets, ongewijzigde worker en binding.
- Live sitemap en negen representatieve pagina's/routebestanden waren
  vóór publicatie byte voor byte gelijk aan de uitgangscommit. Geen recentere
  live inhoud aangetroffen die deze publicatie zou overschrijven.

## Daan Boom-adressen

De zes gemelde adressen blijven bewust 404. Ze komen niet voor in sitemap
of interne links. Er is geen inhoudelijk gelijkwaardige vervangende pagina;
een redirect naar een ander verhaal zou de verwijdering onjuist voorstellen.
Google behandelt 404 en 410 voor indexering als verdwenen inhoud; een aparte
410-regel is hiervoor niet nodig. Bron: [Google HTTP-statuscodes](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes).

## Publicatie

Wordt aangevuld na de live controles.
