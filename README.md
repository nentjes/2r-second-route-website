# 2R (Second Route) — website

De publieke, filmische merk- en productwebsite voor **2R**: een reisgenoot die
de wereld onderweg een stem geeft. De site presenteert twee manieren om te
luisteren:

- **Vrij op pad** — live verhalen bij de omgeving, afgestemd op tempo en interesse.
- **Luisterroutes** — redactioneel opgebouwde wandel- en fietsroutes met kaart,
  hoofdstukken, audio en herleidbare bronnen.

De website richt zich op reizigers te voet, op de fiets, per trein en met de
auto. Daarnaast is er een eigen verhaal voor routebeheerders, uitgevers,
erfgoedorganisaties en regio's.

## Opbouw

De bronteksten, vertalingen en paginabouw staan in `build.py`. Die generator
maakt de statische website in `public/` voor zes talen: Nederlands, Engels,
Duits, Frans, Spaans en Portugees.

Belangrijke pagina's:

- `/{taal}/` — merk- en productverhaal
- `/{taal}/zo-werkt-het` — filmische uitleg
- `/{taal}/routes/` — luisterroutes en routeboeken
- `/{taal}/stories/` — het levende verhalenarchief
- `/{taal}/partners/` — propositie voor routebeheerders en uitgevers
- `/{taal}/kwaliteit/` — controleerbare werkwijze voor bronnen, redactie en correcties
- `/{taal}/roadmap` en `/{taal}/privacy`

Routeaantallen, provincies, afstanden, hoofdstukken en begaanbaarheid worden bij elke build uit `public/routes-data/index.json` en `routes-content/` gelezen. De visuele bron is `docs/2R-stijlgids-v1.0.md` in het bovenliggende 2Route-
project. Route-inhoud en audio worden samen met de app beheerd en vallen buiten
de redactionele websitegenerator.

## Bouwen en lokaal bekijken

```bash
python3 build.py
python3 -m http.server 8000 --directory public
```

Open daarna `http://127.0.0.1:8000/nl/`.

Voor een tekstcorrectie op de partnerpagina gebruikt u `python3 build.py
--partners-only`. Deze gerichte bouw werkt uitsluitend de zes partnerpagina’s
bij en behoudt alle andere bestanden, inclusief de bestaande routepublicatie.

`python3 build.py --discovery-only` werkt de routeoverzichten en downloadpagina’s
bij en laat bestaande algemene downloadknoppen naar de platformkeuze wijzen.
Er komen daarmee geen nieuwe routepagina’s online. De overzichtskaart en de
routetegels gebruiken dezelfde selectie: openbare routes die al een pagina
hebben. Startpunten, afstanden en aantallen komen uit de routegegevens.
De Android-winkelpagina staat op één plek in `PLAY_STORE_URL`; zolang
`ANDROID_IN_REVIEW` waar is, vermeldt de downloadpagina dat Google de app nog
beoordeelt en dat beschikbaarheid binnen enkele dagen wordt verwacht.

Cloudflare serveert HTML met schone adressen: `index.html` als mapadres en
andere HTML-bestanden zonder `.html`. `public_url()` in `build.py` bepaalt
deze adressen voor sitemap, canonical, hreflang en interne links. Een gewone
Python-bestandsserver past die Cloudflare-routering niet toe; gebruik voor
URL-controles `npx wrangler dev --local --local-upstream 2route.nl` (anders
kan Wrangler de www-route als host kiezen) en in een tweede terminal:

```bash
python3 check_urls.py --origin http://localhost:8787
```

`python3 check_urls.py` controleert de gegenereerde bestanden zonder netwerk.
`python3 build.py --urls-only` corrigeert uitsluitend de URL-attributen,
de Nederlandse navigatieshell en de sitemap van de bestaande publicatie.
Daarbij worden routegegevens en gepubliceerde teksten niet opnieuw opgebouwd.

`python3 build.py --route-guidance-only` werkt uitsluitend de volgtekst op
bestaande routetegels en routepagina's en de startlinks bij de routekaart bij.
Dit voegt geen nieuwe routes toe en behoudt hoofdstukken, audio, kaartdata en
alle overige pagina-inhoud. Ontbrekende gegevens blijven onzichtbaar; een
onbekende volgtekst wordt buiten het Nederlands pas na vertaling getoond.

## Publiceren

`python3 build.py --brand-name-only` werkt uitsluitend de product-/vertellernaam
bij in de bestaande pagina’s. `PRODUCT_NAME` is daarvoor de centrale schrijfwijze.
De gerichte bouw gebruikt volledige merkzinnen uit de vertalingen, zodat gewone
route-aanduidingen behouden blijven en geen nieuwe routes gepubliceerd worden.
Een volgende uitvoering wijzigt reeds bijgewerkte teksten niet opnieuw.

De statische bestanden worden als Cloudflare Worker Assets gepubliceerd. Bouw
altijd eerst opnieuw, controleer `public/` en leg wijzigingen vast in Git vóór
een deploy.

```bash
python3 build.py
npx wrangler deploy
```

Live: [2route.nl](https://2route.nl/)
