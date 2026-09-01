#!/usr/bin/env python3
"""
Generates the site mark: a spiral opening from the centre outward, coloured
along the same cyan -> azure -> indigo ramp the headline uses, ending in one
bright node — the sixteen that the whole field waits on.

    python tools/make_icons.py

Writes favicon.svg (primary), plus PNG and ICO fallbacks, into the repo root.
Geometry is shared between the vector and raster outputs so they cannot drift.
"""

import math
import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOX = 64.0            # viewBox / design units
CX = CY = BOX / 2
R0, R1 = 4.8, 19.8    # keeps the node and its halo clear of the rounded corner
TURNS = 1.25          # per-turn gap ≈ 12u, so a 5.2u stroke leaves it open
STROKE = 5.2
NODE_R = 3.4
GROUND = (5, 7, 11)   # --void
RADIUS = 14.0         # rounded-square corner

# the ramp, inner -> outer
STOPS = [
    (0.00, (34, 211, 238)),    # #22D3EE cyan
    (0.42, (79, 134, 255)),    # #4F86FF
    (0.70, (110, 151, 255)),   # #6E97FF azure
    (1.00, (168, 85, 247)),    # #A855F7 indigo
]


def ramp(t):
    t = max(0.0, min(1.0, t))
    for i in range(len(STOPS) - 1):
        a, ca = STOPS[i]
        b, cb = STOPS[i + 1]
        if a <= t <= b:
            u = 0.0 if b == a else (t - a) / (b - a)
            return tuple(round(ca[j] + (cb[j] - ca[j]) * u) for j in range(3))
    return STOPS[-1][1]


def spiral_points(n=240):
    """Archimedean-ish spiral: even spacing reads better at 16px than a log spiral."""
    pts = []
    tmax = TURNS * 2 * math.pi
    for i in range(n + 1):
        u = i / n
        th = u * tmax
        r = R0 + (R1 - R0) * (u ** 0.86)
        # start at the top and open clockwise
        a = th - math.pi / 2
        pts.append((CX + r * math.cos(a), CY + r * math.sin(a), u))
    return pts


# ── vector ────────────────────────────────────────────────────────────────
def write_svg(path):
    pts = spiral_points(160)
    d = 'M %.2f %.2f' % (pts[0][0], pts[0][1])
    for x, y, _ in pts[1:]:
        d += ' L %.2f %.2f' % (x, y)
    ex, ey, _ = pts[-1]
    sx, sy, _ = pts[0]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="分散型スパイラル">
  <defs>
    <linearGradient id="g" x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#22D3EE"/>
      <stop offset="0.42" stop-color="#4F86FF"/>
      <stop offset="0.70" stop-color="#6E97FF"/>
      <stop offset="1" stop-color="#A855F7"/>
    </linearGradient>
    <radialGradient id="bloom" cx="50%" cy="50%" r="52%">
      <stop offset="0" stop-color="#6E97FF" stop-opacity="0.30"/>
      <stop offset="1" stop-color="#6E97FF" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="64" height="64" rx="{RADIUS:.0f}" fill="#05070B"/>
  <rect width="64" height="64" rx="{RADIUS:.0f}" fill="url(#bloom)"/>
  <path d="{d}" fill="none" stroke="url(#g)" stroke-width="{STROKE:.1f}" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="{ex:.2f}" cy="{ey:.2f}" r="{NODE_R:.1f}" fill="#FFFFFF"/>
</svg>
'''
    open(path, 'w', encoding='utf-8', newline='\n').write(svg)
    return path


# ── raster ────────────────────────────────────────────────────────────────
def render(size, ss=8):
    """Draw at ss× then downsample — Pillow has no antialiased stroke."""
    S = size * ss
    k = S / BOX
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=RADIUS * k, fill=GROUND + (255,))

    # bloom: build it small with a real radial falloff, then scale up smoothly
    B = 96
    bl = Image.new('RGBA', (B, B), (0, 0, 0, 0))
    px = bl.load()
    for yy in range(B):
        for xx in range(B):
            dx, dy = (xx - B / 2) / (B / 2), (yy - B / 2) / (B / 2)
            r = math.hypot(dx, dy)
            if r >= 1.0:
                continue
            a = int(34 * (1 - r) ** 2.2)
            if a:
                px[xx, yy] = (110, 151, 255, a)
    img.alpha_composite(bl.resize((S, S), Image.LANCZOS))

    pts = spiral_points(360)
    w = STROKE * k
    for i in range(len(pts) - 1):
        x1, y1, u1 = pts[i]
        x2, y2, _ = pts[i + 1]
        c = ramp(u1) + (255,)
        d.line([x1 * k, y1 * k, x2 * k, y2 * k], fill=c, width=max(1, int(round(w))))
        # round the joint so the stroke does not look chipped
        rr = w / 2
        d.ellipse([x1 * k - rr, y1 * k - rr, x1 * k + rr, y1 * k + rr], fill=c)

    ex, ey, _ = pts[-1]
    nr = NODE_R * k
    d.ellipse([ex * k - nr * 1.75, ey * k - nr * 1.75, ex * k + nr * 1.75, ey * k + nr * 1.75],
              fill=(190, 214, 255, 46))
    d.ellipse([ex * k - nr, ey * k - nr, ex * k + nr, ey * k + nr], fill=(255, 255, 255, 255))

    return img.resize((size, size), Image.LANCZOS)


def main():
    svg = write_svg(os.path.join(ROOT, 'favicon.svg'))
    print('wrote', os.path.relpath(svg, ROOT))

    for size, name in [(32, 'favicon.png'), (180, 'apple-touch-icon.png'), (512, 'icon-512.png')]:
        p = os.path.join(ROOT, name)
        render(size).save(p)
        print('wrote %s (%d×%d)' % (name, size, size))

    ico = os.path.join(ROOT, 'favicon.ico')
    render(64).save(ico, sizes=[(16, 16), (32, 32), (48, 48)])
    print('wrote favicon.ico (16/32/48)')


if __name__ == '__main__':
    main()
