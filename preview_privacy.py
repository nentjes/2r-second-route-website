#!/usr/bin/env python3
"""Render B-122 for review outside public/. Never publishes or activates it."""
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
import build

ROOT = Path(__file__).resolve().parent


from privacy_policy import load_policy as load_draft, render_policy


def render_draft(lang, text):
    return render_policy(lang, text, build.PRIVACY[lang], build.PRIV_EXTRA[lang],
                         build.page_shell, preview=True)


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
