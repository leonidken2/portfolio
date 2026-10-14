"""Builds the link-preview images assets/og-ru.png and og-en.png from the site numbers.
Run from the repository root:  python3 og-src/make_og.py  (needs Playwright with Chromium)
"""
import asyncio, sys, tempfile
from pathlib import Path
from playwright.async_api import async_playwright
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import importlib.util
spec = importlib.util.spec_from_file_location("b", ROOT / "build.py"); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
D = b.D
CFG = {
 "ru": dict(name="Леонид<br>Кривошеин", role="Product marketing, growth и<br>GTM в HealthTech",
            spend=b.usd(D["g_spend"], "ru"), rev=b.usd(D["g_rev"], "ru"), l1="вложено в Google Ads", l2="атрибутированная выручка", chip="ROAS 7,9×"),
 "en": dict(name="Leonid<br>Krivoshein", role="Product marketing, growth<br>and GTM in HealthTech",
            spend=b.usd(D["g_spend"], "en"), rev=b.usd(D["g_rev"], "en"), l1="Google Ads spend", l2="attributed revenue", chip="ROAS 7.9x"),
}
def val(v):
    h, _, t = v.rpartition(" ")
    return f'{h}<small> {t}</small>' if h else v
def page(c):
    w = D["g_spend"] / D["g_rev"]
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:G;src:url("file://{ROOT}/assets/fonts/geologica-cyrillic-full-normal.woff2") format("woff2");font-weight:100 900;unicode-range:U+0400-04FF}}
@font-face{{font-family:G;src:url("file://{ROOT}/assets/fonts/geologica-latin-full-normal.woff2") format("woff2");font-weight:100 900}}
*{{margin:0;box-sizing:border-box}} body{{width:1200px;height:630px;background:#edf2f4;font-family:G,sans-serif;color:#102a35;position:relative;overflow:hidden}}
.ph{{position:absolute;right:0;top:0;width:330px;height:630px;background:url("file://{ROOT}/assets/leonid.jpg") center/cover}}
h1{{position:absolute;left:72px;top:64px;font-size:90px;line-height:1.02;font-weight:700;letter-spacing:-.02em}}
.r{{position:absolute;left:72px;top:268px;font-size:28px;line-height:1.28;font-weight:500}}
.bars{{position:absolute;left:72px;top:462px;width:750px}}
.row{{display:flex;align-items:center;gap:16px;margin-bottom:18px}}
.v{{width:210px;text-align:right}} .v b{{display:block;font-size:30px;font-weight:700;line-height:1}} .v b small{{font-size:19px}} .v span{{font-size:14px;color:#4a616c}}
.bar{{height:40px;border-radius:0 6px 6px 0}} .chip{{background:#fff;border-radius:20px;padding:7px 14px;font-size:17px;margin-left:4px}}
</style></head><body><div class="ph"></div><h1>{c["name"]}</h1><div class="r">{c["role"]}</div>
<div class="bars"><div class="row"><div class="v"><b>{val(c["spend"])}</b><span>{c["l1"]}</span></div><div class="bar" style="width:{524*w:.0f}px;background:#86b6ef"></div><span class="chip">{c["chip"]}</span></div>
<div class="row"><div class="v"><b>{val(c["rev"])}</b><span>{c["l2"]}</span></div><div class="bar" style="width:524px;background:#2a78d6"></div></div></div></body></html>'''
async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch()
        for lang, c in CFG.items():
            f = Path(tempfile.gettempdir()) / f"og-{lang}.html"; f.write_text(page(c), encoding="utf-8")
            pg = await br.new_page(viewport={"width": 1200, "height": 630})
            await pg.goto(f"file://{f.resolve()}"); await pg.wait_for_timeout(600)
            await pg.screenshot(path=str(ROOT / "assets" / f"og-{lang}.png"))
        await br.close()
asyncio.run(main())
