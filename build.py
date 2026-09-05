#!/usr/bin/env python3
"""
src/page.html  ->  index.html

src/page.html is the working file: a document fragment, the same shape Claude's
Artifact host accepts (no doctype, no <head>, no <body>). This script wraps it
into a standalone page for GitHub Pages — the parts the host would otherwise
supply, above all the viewport meta, without which the page breaks on phones.

    python build.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src', 'page.html')
OUT = os.path.join(ROOT, 'index.html')

SITE = 'https://hfot.github.io/cardano-spiral/'

DESC = ('最も分散化されたチェーンは、持続可能な状態にあるのか。'
        '立場と利害、選抜圧力、責任の空白、トレジャリー枯渇まで、'
        '検証済みの数字で Cardano のガバナンスを分析する。')

TEMPLATE = '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="dark light">
<meta name="theme-color" content="#05070B">
<link rel="canonical" href="{site}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon.png" sizes="32x32" type="image/png">
<link rel="shortcut icon" href="favicon.ico">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:url" content="{site}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:locale" content="ja_JP">
<meta property="og:locale:alternate" content="en_US">
<!-- 絶対URLでないと各SNSのクローラーが拾えない -->
<meta property="og:image" content="{site}og.png?v=1">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="分散型スパイラル — 構造と事象で考える">
<meta name="twitter:card" content="summary_large_image">
{head}
<style>
/* minimal reset — the artifact host supplies this; a standalone page must not rely on it */
*,*::before,*::after{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
img,svg,canvas{{display:block;max-width:100%}}
button,input,select,textarea{{font:inherit;color:inherit}}
</style>
</head>
<body>
{body}
</body>
</html>
'''


def main():
    if not os.path.exists(SRC):
        sys.exit('missing %s' % SRC)

    s = open(SRC, encoding='utf-8').read()

    # everything before the first <style> is head material; the rest is the page
    i = s.index('<style>')
    head, body = s[:i], s[i:]

    m = re.search(r'<title>(.*?)</title>', head, re.S)
    title = m.group(1).strip() if m else 'Decentralization Spiral'

    # charset and title are re-declared in the template
    head = re.sub(r'<meta charset="utf-8">\s*', '', head)
    head = re.sub(r'<title>.*?</title>\s*', '', head, flags=re.S)

    html = TEMPLATE.format(title=title, desc=DESC, site=SITE,
                           head=head.strip(), body=body.strip())
    open(OUT, 'w', encoding='utf-8', newline='\n').write(html)

    print('built %s  (%d bytes)' % (os.path.relpath(OUT, ROOT), len(html.encode('utf-8'))))
    print('title: %s' % title)


if __name__ == '__main__':
    main()
