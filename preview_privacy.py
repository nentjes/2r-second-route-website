#!/usr/bin/env python3
"""Render B-122 for review outside public/. Never publishes or activates it."""
import html
import json
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
import build

ROOT = Path(__file__).resolve().parent


def load_draft():
    copy = json.loads((ROOT / 'design/privacy-b122.json').read_text())
    terms = json.loads((ROOT.parent / 'gedeeld/waarheden.json').read_text())['bewaartermijnen_dagen']
    if set(copy) != set(build.LANGS):
        raise ValueError('Het privacyconcept moet alle websitetalen bevatten.')
    if terms['opname'] != 0:
        raise ValueError('Opnamebeleid is gewijzigd: beoordeel eerst de concepttekst opnieuw.')
    # Getallen komen uit het register; hieronder staat alleen hun vertaling.
    words = {'nl': {7: 'zeven'}, 'en': {7: 'seven'}, 'de': {7: 'sieben'},
             'fr': {7: 'sept'}, 'es': {7: 'siete'}, 'pt': {7: 'sete'}}
    for lang, text in copy.items():
        values = {key: words[lang].get(terms[key], str(terms[key]))
                  for key in ('locatie', 'vraag_tekst')}
        text['paragraphs'] = [paragraph.format(**values) for paragraph in text['paragraphs']]
    return copy


def render_draft(lang, text):
    metadata = build.PRIVACY[lang]
    framing = build.PRIV_EXTRA[lang]
    paragraphs = '\n'.join(f'<p>{html.escape(p)}</p>' for p in text['paragraphs'])
    body = f'''
  <section class="priv-hero">
    <img class="priv-hero-img" src="/images/2r-privacy-rust-v1.webp" alt="{html.escape(framing['alt'])}" width="1672" height="941" fetchpriority="high">
    <div class="priv-hero-shade" aria-hidden="true"></div>
    <div class="priv-hero-content">
      <p class="eyebrow on-photo">{html.escape(metadata['eyebrow'])}</p>
      <h1>{html.escape(framing['h1'])}</h1>
      <p class="priv-hero-lede">{html.escape(text['draft'])}</p>
    </div>
  </section>
  <section class="priv-body"><div class="wrap" style="max-width:800px">
    <article class="priv-text" aria-labelledby="privacy-heading">
      <p class="priv-fieldnote">{html.escape(text['draft'])} · B-122 · 23-10-2026</p>
      <section class="priv-sec">
        <h2 id="privacy-heading">{html.escape(text['heading'])}</h2>
        {paragraphs}
      </section>
      <section class="priv-sec" id="contact">
        <h2>{metadata['h_contact']}</h2>
        <p>{metadata['contact_text']}</p>
      </section>
    </article>
  </div></section>
'''
    page = build.page_shell(lang, metadata['title'], text['heading'], 'privacy',
                            body, path='privacy.html', immersive=True)
    # Keep language changes on this concept instead of the existing home page.
    for target in build.LANGS:
        active = ' class="active"' if target == lang else ''
        label = build.LANG_LABEL[target]
        page = page.replace(f'<a href="/{target}/"{active}>{label}</a>',
                            f'<a href="/{target}/privacy.html"{active}>{label}</a>')
    return page.replace('<head>', '<head>\n<meta name="robots" content="noindex, nofollow">', 1)


def make_preview():
    copy = load_draft()
    # A fresh temporary directory prevents any write through a public/ symlink.
    destination = Path(tempfile.mkdtemp(prefix='2r-privacy-b122-'))
    public = ROOT / 'public'
    for asset in public.iterdir():
        if asset.name not in build.LANGS:
            (destination / asset.name).symlink_to(asset, target_is_directory=asset.is_dir())
    for lang in build.LANGS:
        folder = destination / lang
        folder.mkdir()
        for asset in (public / lang).iterdir():
            if asset.name != 'privacy.html':
                (folder / asset.name).symlink_to(asset, target_is_directory=asset.is_dir())
        (folder / 'privacy.html').write_text(render_draft(lang, copy[lang]), encoding='utf-8')
    return destination


if __name__ == '__main__':
    print(make_preview())
