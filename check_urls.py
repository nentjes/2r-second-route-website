#!/usr/bin/env python3
"""Controleer sitemap, canonicals, hreflang en interne links, lokaal of via HTTP."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
import sys
import subprocess
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
import build


class Page(HTMLParser):
    def __init__(self, document):
        super().__init__()
        self.canonicals, self.alternates, self.og_urls, self.links = [], {}, [], []
        self.feed(document)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs.get('href'))
        if tag == 'link' and attrs.get('rel') == 'alternate' and 'hreflang' in attrs:
            self.alternates.setdefault(attrs['hreflang'], []).append(attrs.get('href'))
        if tag == 'meta' and attrs.get('property') == 'og:url':
            self.og_urls.append(attrs.get('content'))
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])


def asset_for(url):
    path = urlsplit(url).path
    relative = path.lstrip('/')
    return Path(build.OUT) / (relative + 'index.html' if path.endswith('/') else relative + '.html')


def inspect(url, document, sitemap):
    page = Page(document)
    errors = []
    if page.canonicals != [url]:
        errors.append(f'{url}: canonical {page.canonicals!r}')
    if page.og_urls != [url]:
        errors.append(f'{url}: og:url {page.og_urls!r}')
    lang, _, tail = urlsplit(url).path.lstrip('/').partition('/')
    expected = {target: [f'{build.BASE_URL}/{target}/{tail}'] for target in build.LANGS}
    expected['x-default'] = expected['nl']
    if page.alternates != expected:
        errors.append(f'{url}: ontbrekende, dubbele of afwijkende hreflang-links')
    for href in page.links:
        target = urlsplit(urljoin(url, href))
        if target.netloc != urlsplit(build.BASE_URL).netloc:
            continue
        if target.path.split('/')[1:2] not in [[lang] for lang in build.LANGS]:
            continue
        if target.path.endswith('.html'):
            errors.append(f'{url}: interne link naar omleiding {href}')
        elif not Path(target.path).suffix:
            address = build.BASE_URL + target.path
            if address not in sitemap:
                errors.append(f'{url}: interne paginalink buiten sitemap {href}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--origin', help='Controleer tevens HTTP zonder omleidingen, bijvoorbeeld http://localhost:8787')
    args = parser.parse_args()
    urls = [node.text for node in ET.parse(Path(build.OUT) / 'sitemap.xml').iter()
            if node.tag.endswith('}loc')]
    sitemap = set(urls)
    errors = []
    if len(urls) != len(sitemap):
        errors.append('Dubbele URL in sitemap')
    for url in urls:
        parsed = urlsplit(url)
        if (parsed.scheme + '://' + parsed.netloc != build.BASE_URL or parsed.query
                or parsed.fragment or parsed.path.endswith('.html')):
            errors.append(f'Sitemap noemt geen schoon voorkeursadres: {url}')
        asset = asset_for(url)
        if not asset.is_file():
            errors.append(f'Geen lokaal HTML-bestand voor {url}')
            continue
        errors.extend(inspect(url, asset.read_text(encoding='utf-8'), sitemap))
    published = {path for lang in build.LANGS for path in (Path(build.OUT) / lang).rglob('*.html')}
    listed = {asset_for(url) for url in urls}
    if published != listed:
        errors.append(f'HTML/sitemap verschillen: {len(published - listed)} niet vermeld, {len(listed - published)} ontbrekend')
    if args.origin and not errors:
        def fetch(url):
            address = args.origin.rstrip('/') + urlsplit(url).path
            try:
                # Net als het bestaande smoke-ritueel: curl, zonder -L, zodat
                # een omleiding niet ongemerkt als een geslaagde pagina telt.
                result = subprocess.run(['curl', '--silent', '--show-error', '--max-time', '30',
                                         '--write-out', '\n%{http_code}', address],
                                        capture_output=True, text=True, timeout=35)
                document, _, status = result.stdout.rpartition('\n')
                if result.returncode or status != '200':
                    return [f'{url}: HTTP {status}, curl {result.returncode}, verwacht 200']
                return inspect(url, document, sitemap)
            except (OSError, subprocess.TimeoutExpired) as error:
                return [f'{url}: {error}']
        with ThreadPoolExecutor(max_workers=8) as pool:
            for findings in pool.map(fetch, urls):
                errors.extend(findings)
    if errors:
        print('\n'.join(errors[:8]))
        print(f'FOUT: {len(errors)} bevindingen bij {len(urls)} sitemapadressen')
        return 1
    print(f'OK: {len(urls)} sitemapadressen, canonicals, hreflang en interne links'
          + ('; HTTP overal 200 zonder omleiding' if args.origin else ''))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
