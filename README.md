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
- `/{taal}/zo-werkt-het.html` — filmische uitleg
- `/{taal}/routes/` — luisterroutes en routeboeken
- `/{taal}/stories/` — het levende verhalenarchief
- `/{taal}/partners/` — propositie voor routebeheerders en uitgevers
- `/{taal}/roadmap.html` en `/{taal}/privacy.html`

De visuele bron is `docs/2R-stijlgids-v1.0.md` in het bovenliggende 2Route-
project. Route-inhoud en audio worden samen met de app beheerd en vallen buiten
de redactionele websitegenerator.

## Bouwen en lokaal bekijken

```bash
python3 build.py
python3 -m http.server 8000 --directory public
```

Open daarna `http://127.0.0.1:8000/nl/`.

## Publiceren

De statische bestanden worden als Cloudflare Worker Assets gepubliceerd. Bouw
altijd eerst opnieuw, controleer `public/` en leg wijzigingen vast in Git vóór
een deploy.

```bash
python3 build.py
npx wrangler deploy
```

Live: [2route.nl](https://2route.nl/)
