# 2R (Second Route) — Website

Marketingwebsite voor **2R**, een AI-reisgids die tijdens het rijden, fietsen
of wandelen live vertelt over de omgeving — geschiedenis, natuur en lokale
verhalen, in jouw taal en op maat van jouw interesses.

**1 Route brengt je er. 2 Route vertelt je wat je ziet.**

🔗 Live: https://2route.roelnentjes.workers.dev
🔗 Probeer de app: https://mapsinfo.roelnentjes.workers.dev

## Stack

Statische, meertalige (NL/EN) site, gehost als Cloudflare Worker (Assets).
Geen build-stap — platte HTML/CSS.

```
website/
├── public/
│   ├── nl/          Nederlandse pagina's
│   ├── en/           English pages
│   ├── style.css     Gedeelde stijl (2R-huisstijl)
│   └── icon-2r.png
├── wrangler.jsonc
```

## Lokaal draaien

```bash
npx wrangler dev
```

## Deployen

```bash
npx wrangler deploy
```

---

Onderdeel van de 1R-familie — zie ook [Autestme](https://autestme.com) en
[Kindertekening](https://kindertekening.com).
