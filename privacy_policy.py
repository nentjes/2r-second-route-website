"""B-122 privacy copy and rendering, shared by publication and local preview."""
from datetime import date
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_policy():
    policy = json.loads((ROOT / 'privacy.json').read_text(encoding='utf-8'))
    terms = json.loads((ROOT.parent / 'gedeeld/waarheden.json').read_text(encoding='utf-8'))['bewaartermijnen_dagen']
    if terms['opname'] != 0:
        raise ValueError('Opnamebeleid gewijzigd: beoordeel eerst de privacytekst opnieuw.')
    words = {'nl': {7: 'zeven'}, 'en': {7: 'seven'}, 'de': {7: 'sieben'},
             'fr': {7: 'sept'}, 'es': {7: 'siete'}, 'pt': {7: 'sete'}}
    copy = policy['languages']
    if set(copy) != set(words):
        raise ValueError('Privacytekst moet alle zes websitetalen bevatten.')
    for lang, text in copy.items():
        values = {key: words[lang].get(terms[key], str(terms[key]))
                  for key in ('locatie', 'vraag_tekst', 'logboek', 'verhalen', 'meldingen')}
        text['paragraphs'] = [p.format(**values) for p in text['paragraphs']]
        text['details'] = text['details'].format(**values)
        text['rollout'] = text['rollout'].format(build=policy['effective_build'])
        text['updated'] = text['updated'].format(date=date.fromisoformat(policy['updated']).strftime('%d-%m-%Y'))
    return copy


def render_policy(lang, text, metadata, framing, page_shell, *, preview=False):
    status = text['draft'] if preview else text['updated']
    paragraphs = '\n'.join(f'<p>{html.escape(p)}</p>' for p in text['paragraphs'])
    body = f'''
  <section class="priv-hero">
    <img class="priv-hero-img" src="/images/2r-privacy-rust-v1.webp" alt="{html.escape(framing['alt'])}" width="1672" height="941" fetchpriority="high">
    <div class="priv-hero-shade" aria-hidden="true"></div>
    <div class="priv-hero-content">
      <p class="eyebrow on-photo">{html.escape(metadata['eyebrow'])}</p>
      <h1>{html.escape(framing['h1'])}</h1>
      <p class="priv-hero-lede">{html.escape(text['heading'])}</p>
      <p class="priv-updated">{html.escape(status)}</p>
    </div>
  </section>
  <section class="priv-body"><div class="wrap" style="max-width:800px">
    <article class="priv-text" aria-labelledby="privacy-heading">
      <p class="priv-fieldnote">{html.escape(text['rollout'])}</p>
      <section class="priv-sec">
        <h2 id="privacy-heading">{html.escape(text['heading'])}</h2>
        {paragraphs}
      </section>
      <section class="priv-sec">
        <h2>{html.escape(text['details_heading'])}</h2>
        <p>{html.escape(text['details'])}</p>
      </section>
      <section class="priv-sec" id="contact">
        <h2>{metadata['h_contact']}</h2>
        <p>{metadata['contact_text']}</p>
      </section>
    </article>
  </div></section>
'''
    page = page_shell(lang, metadata['title'], text['paragraphs'][0], 'privacy',
                      body, path='privacy.html', immersive=True)
    for target in load_language_labels():
        active = ' class="active"' if target == lang else ''
        page = page.replace(f'<a href="/{target}/"{active}>{target.upper()}</a>',
                            f'<a href="/{target}/privacy.html"{active}>{target.upper()}</a>')
    if preview:
        page = page.replace('<head>', '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
    return page


def load_language_labels():
    return json.loads((ROOT / 'privacy.json').read_text(encoding='utf-8'))['languages']
