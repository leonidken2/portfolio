#!/usr/bin/env python3
"""Builds the resume as PDF in Russian and English: cv/Leonid_Krivoshein_CV_RU.pdf and _EN.pdf.

Numbers come from build.py (the site) so the resume and the portfolio never disagree.
Run from the repository root:  python3 cv-src/build_cv.py
Needs Playwright with Chromium (used to print the HTML to PDF).
"""
import asyncio
import importlib.util
import re
import subprocess
import sys
import time
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("portfolio_build", ROOT / "build.py")
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)
D, n, dec, usd = site.D, site.n, site.dec, site.usd

PORTFOLIO = "leonidken2.github.io/portfolio"
MAIL = "kriwoshein.leonid248@gmail.com"
PHONE_SHOW, PHONE = "+995 574 01 80 32", "+99574018032"
TG = "leokrivoshein"
LI = "linkedin.com/in/leonid-krivoshein"


def e(s):
    return escape(str(s), quote=True)


def k(v, lang):
    """1800 -> '1,8 тыс.' / '1.8K'"""
    x = v / 1000
    s = str(round(x)) if abs(x - round(x)) < 0.05 else dec(x, lang)
    return f"{s} тыс." if lang == "ru" else f"{s}K"


def content(lang):
    ru = lang == "ru"
    c = {}
    c["title"] = "Леонид Кривошеин — резюме" if ru else "Leonid Krivoshein — resume"
    c["name"] = "Леонид Кривошеин" if ru else "Leonid Krivoshein"
    c["role"] = "Product Marketing | Growth | GTM"
    c["contacts"] = [
        ("Портфолио" if ru else "Portfolio", PORTFOLIO + ("/" if ru else "/en/"), f"https://{PORTFOLIO}/" + ("" if ru else "en/")),
        ("Telegram", f"@{TG}", f"https://t.me/{TG}"),
        ("Почта" if ru else "Email", MAIL, f"mailto:{MAIL}"),
        ("Телефон, WhatsApp" if ru else "Phone, WhatsApp", PHONE_SHOW, f"https://wa.me/{PHONE.lstrip('+')}"),
        ("LinkedIn", LI, f"https://{LI}/"),
        ("Где" if ru else "Location", "Грузия, удалённо" if ru else "Georgia, remote", None),
    ]
    if ru:
        c["contacts"].append(("Дата рождения", "20.12.1996", None))
    c["summary"] = (
        f"Маркетолог в HealthTech, медицине и B2B. Начинаю с исследования аудитории и заканчиваю выручкой, которую можно посчитать: "
        f"{usd(D['g_rev'], lang)} атрибутированной выручки при ROAS {dec(D['roas'], lang)}× в Google Ads, {D['g_pat']} пациент, "
        f"GTM-исследование на {D['resp']}+ респондентов и {D['interviews']} интервью."
        if ru else
        f"Marketer in HealthTech, healthcare and B2B. I start with customer research and finish with revenue you can count: "
        f"{usd(D['g_rev'], lang)} attributed revenue at {dec(D['roas'], lang)}x ROAS on Google Ads, {D['g_pat']} patients, "
        f"GTM research with {D['resp']}+ respondents and {D['interviews']} interviews.")
    c["kpis"] = [
        (f"{dec(D['roas'], lang)}×", "ROAS в Google Ads" if ru else "Google Ads ROAS"),
        (usd(D['g_rev'], lang), "атрибутированной выручки" if ru else "attributed revenue"),
        (str(D["g_pat"]), "пациент из рекламы" if ru else "patients from ads"),
        (f"{D['resp']}+", "респондентов в GTM-исследовании" if ru else "GTM research respondents"),
        (f"0 → {n(D['c_total'], lang)}", "подписчиков сообщества" if ru else "community followers"),
    ]
    c["exp_h"] = "Опыт" if ru else "Experience"
    c["jobs"] = [
        dict(
            years="2025 — сейчас" if ru else "2025 — present",
            where="удалённо" if ru else "remote",
            role="Маркетинг-стратег / координатор проектов" if ru else "Marketing Strategist / Project Coordinator",
            org="RS Agency",
            sub=("Ключевой проект: OncoDiag — product marketing и GTM теста для диагностики рака на основе биомаркера CA-62"
                 if ru else
                 "Key project: OncoDiag — product marketing and GTM for a cancer-diagnostics test based on the CA-62 biomarker"),
            lines=[],
            bullets=[
                f"Составил анкету исследования (<b>{D['resp']}+ респондентов</b>) и сам провёл <b>{D['interviews']} глубинных интервью</b>" if ru else
                f"Wrote the research survey (<b>{D['resp']}+ respondents</b>) and ran <b>{D['interviews']} in-depth interviews</b> myself",
                f"Построил воронку проблемы и из <b>{D['ideas']} идей</b> отобрал <b>{D['hyp']} приоритетных GTM-гипотез</b> по четырём критериям: стадия продукта, реализуемость, измеримость, масштабируемость" if ru else
                f"Built a problem funnel and narrowed <b>{D['ideas']} ideas</b> to <b>{D['hyp']} priority GTM hypotheses</b> on four criteria: product stage, feasibility, measurability, scalability",
                f"Финализировал позиционирование CA-62 и поставил ТЗ на образовательную программу для врачей (<b>{D['lecture']} слайда</b>) и врачебный канал" if ru else
                f"Finalized CA-62 positioning and briefed the <b>{D['lecture']}-slide</b> physician education program and the physician channel",
                f"Выстроил B2B-коммуникацию для врачей, лабораторий и партнёров: по моим ТЗ копирайтеры и дизайнеры сделали скрипты для администраторов Ситилаб, обучающий набор из <b>{D['formats']} форматов</b>, {D['decks']} презентации продукта" if ru else
                f"Built B2B communication for doctors, labs and partners: from my briefs copywriters and designers produced Citilab front-desk scripts, a <b>{D['formats']}-format</b> partner toolkit, {D['decks']} product presentations",
                "Предложил и запустил чат-бота в Salebot вместе с разработчиком" if ru else "Proposed and launched a Salebot chatbot with a developer",
                f"Проверил коммуникацию на конференции PreventMed: <b>{D['pm_materials']}+ материалов</b>, {D['pm_scenarios']} сценария внедрения в клинику; вопросы врачей вернул в обучение" if ru else
                f"Field-tested messaging at the PreventMed conference: <b>{D['pm_materials']}+ materials</b>, {D['pm_scenarios']} clinic adoption scenarios; doctors' questions fed back into training",
                f"Поддерживал образовательные мероприятия для <b>{D['hcp']}+ медицинских специалистов</b>" if ru else
                f"Supported educational activities for <b>{D['hcp']}+ healthcare professionals</b>",
                f"Веду активацию «Розовый октябрь» с Ситилаб: цифровой календарь здоровья, QR-воронка, ролики для холлов, <b>{n(D['promo'], lang)} промокодов</b>" if ru else
                f"Running a Pink October activation with Citilab: digital health calendar, QR funnel, lobby videos, <b>{n(D['promo'], lang)} promo codes</b>",
                "Координирую копирайтеров, дизайнеров и подрядчиков" if ru else "Coordinate copywriters, designers and contractors",
            ],
            extra=(f"Ещё в RS Agency: исследования рынка и аудитории, сегментация {D['specs']} медицинских специальностей по {D['client_types']} типам клиентов, координация клиентских проектов."
                   if ru else
                   f"Also at RS Agency: market and audience research, segmentation of {D['specs']} medical specialties across {D['client_types']} client types, client project coordination."),
        ),
        dict(
            years="2023 — 2025",
            where="Грузия" if ru else "Georgia",
            role="Growth & Performance Marketing Lead",
            org="Minimum Innovative Dentistry",
            sub=None,
            lines=[
                ("Google Ads", f"{usd(D['g_spend'], lang)} бюджета → <b>{usd(D['g_rev'], lang)} атрибутированной выручки</b> • ROAS {dec(D['roas'], lang)}× • {D['g_pat']} пациент" if ru else
                 f"{usd(D['g_spend'], lang)} spend → <b>{usd(D['g_rev'], lang)} attributed revenue</b> • {dec(D['roas'], lang)}x ROAS • {D['g_pat']} patients"),
                ("Instagram", f"{D['i_pat']} пациента по CRM → {usd(D['i_rev'], lang)} • 637 тыс.+ показов • 6,2 тыс.+ переходов" if ru else
                 f"{D['i_pat']} CRM-attributed patients → {usd(D['i_rev'], lang)} • 637K+ impressions • 6.2K+ link clicks"),
                ("Поиск" if ru else "Search", f"{D['seo_pages']} страниц услуг для SEO и Google Ads → {k(D['pages_sessions'], lang)} сессий • {k(D['search_visits'], lang)} переходов из поисковых систем" if ru else
                 f"{D['seo_pages']} service pages for SEO and Google Ads → {k(D['pages_sessions'], lang)} sessions • {k(D['search_visits'], lang)} visits from search engines"),
            ],
            bullets=[
                "Построил и вёл 3 воронки привлечения и связал рекламу со страницами услуг, CRM, WhatsApp, записью, пациентами и выручкой" if ru else
                "Built and ran 3 acquisition funnels, linking ads to service pages, CRM, WhatsApp, appointments, patients and revenue",
                f"Запустил поисковые кампании Google Ads под отдельные услуги: около <b>{k(D['ads_service_clicks'], lang)} кликов</b> прямо на страницы услуг" if ru else
                f"Ran per-service Google Ads search campaigns: about <b>{k(D['ads_service_clicks'], lang)} clicks</b> straight to service pages",
                f"Разобрал <b>{D['leads_total']} заявки</b> с сайта: среди тех, где указан источник, {D['search_share']}% пришли из поиска Google и Яндекса" if ru else
                f"Analysed <b>{D['leads_total']} site leads</b>: of those naming a source, {D['search_share']}% came from Google or Yandex search",
                f"Разработал стратегию для {D['segments']} сегментов аудитории; контент-система из {D['pillars']} рубрик и {D['posts']} постов" if ru else
                f"Developed strategy for {D['segments']} audience segments; content system with {D['pillars']} pillars and {D['posts']} posts",
                f"Снимал фото и видео: врачи, клинические случаи, Reels и Stories; вырастил Instagram до <b>{n(D['followers'], lang)}+ целевых подписчиков</b>" if ru else
                f"Produced photo and video: doctors, cases, Reels and Stories; grew Instagram to <b>{n(D['followers'], lang)}+ targeted followers</b>",
            ],
            extra=None,
        ),
        dict(
            years="2018 — 2019",
            where="Санкт-Петербург" if ru else "Saint Petersburg",
            role="Основатель / Community Growth Lead" if ru else "Founder / Community Growth Lead",
            org="медиа-проект и сообщество" if ru else "Independent Media & Community Project",
            sub=None,
            lines=[],
            bullets=[
                f"Вырастил сообщество с нуля до <b>{n(D['c_total'], lang)} подписчиков</b>: {D['c_integr']} интеграций с блогерами, лучшая дала <b>+{D['c_best']}</b>; механика взаимного пиара — {D['c_act']} активаций → <b>+{D['c_ref']}</b>" if ru else
                f"Grew the community from zero to <b>{n(D['c_total'], lang)} followers</b>: {D['c_integr']} influencer integrations, the best brought <b>+{D['c_best']}</b>; referral mechanic — {D['c_act']} activations → <b>+{D['c_ref']}</b>",
                f"Провёл благотворительную акцию с {D['c_partners']} брендами: {D['c_comments']}+ комментариев, {n(D['c_charity'], lang)} ₽ перечислено в фонд" if ru else
                f"Ran a charity campaign with {D['c_partners']} partner brands: {D['c_comments']}+ comments, RUB {n(D['c_charity'], lang)} donated",
                f"Спродюсировал {D['c_videos']} видеоисторий участников; проект показали по телевидению" if ru else
                f"Produced {D['c_videos']} storytelling videos; the project was featured on TV",
                f"Руководил командой из {D['c_team']} человек: еженедельные планёрки, задачи в таск-менеджере" if ru else
                f"Led a team of {D['c_team']}: weekly planning, tasks in a task manager",
            ],
            extra=None,
        ),
    ]
    c["tools_h"] = "Инструменты" if ru else "Tools"
    c["tools"] = ("Google Ads, Meta Ads, Яндекс Директ, SEO-страницы услуг, CRM, WhatsApp Business, Tilda, Figma, Salebot, Kaiten; опросы и глубинные интервью"
                  if ru else
                  "Google Ads, Meta Ads, Yandex Direct, SEO service pages, CRM, WhatsApp Business, Tilda, Figma, Salebot, Kaiten; surveys and in-depth interviews")
    c["foot"] = (f"Кейсы с графиками и дашбордами: {PORTFOLIO}" if ru else f"Cases with charts and dashboards: {PORTFOLIO}/en/")
    return c


CSS = """
@font-face { font-family: "Geologica"; font-weight: 100 900; src: url(../assets/fonts/geologica-cyrillic-full-normal.woff2) format("woff2-variations");
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116; }
@font-face { font-family: "Geologica"; font-weight: 100 900; src: url(../assets/fonts/geologica-latin-full-normal.woff2) format("woff2-variations");
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }
@page { size: A4; margin: 14mm 15mm 13mm; }
:root { --ink: #102a35; --ink-2: #4a616c; --muted: #66787f; --line: #d3dde1; --soft: #edf2f4; --blue: #2a78d6; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: "Geologica", system-ui, sans-serif; color: var(--ink); font-size: 9.6pt; line-height: 1.42; font-weight: 360; }
a { color: inherit; text-decoration: none; }
b { font-weight: 600; }
.head { display: grid; grid-template-columns: 1fr 27mm; gap: 8mm; align-items: start; }
h1 { margin: 0; font-size: 25pt; font-weight: 700; letter-spacing: -0.03em; line-height: 1; font-variation-settings: "SHRP" 70; }
.role { margin: 2.2mm 0 3.6mm; font-size: 11.5pt; font-weight: 500; color: var(--ink-2); }
.contacts { display: grid; grid-template-columns: auto 1fr; gap: 0.7mm 4mm; font-size: 8.8pt; }
.contacts dt { color: var(--muted); }
.contacts dd { margin: 0; }
.contacts a { border-bottom: 0.6pt solid #9fb3bc; }
.contacts .main a { color: var(--blue); border-bottom-color: var(--blue); font-weight: 560; }
.photo { width: 27mm; height: 33mm; object-fit: cover; object-position: 50% 18%; border-radius: 2mm; }
.summary { margin: 4.5mm 0 0; font-size: 10pt; line-height: 1.45; max-width: 165mm; }
.kpis { display: grid; grid-template-columns: repeat(5, 1fr); margin: 4.5mm 0 1mm; border-top: 1.2pt solid var(--ink); border-bottom: 0.6pt solid var(--line); }
.kpi { padding: 2.4mm 2.5mm 2.6mm 0; }
.kpi + .kpi { padding-left: 2.5mm; border-left: 0.6pt solid var(--line); }
.kpi b { display: block; font-size: 13.5pt; font-weight: 650; letter-spacing: -0.02em; line-height: 1.15; white-space: nowrap; }
.kpi span { display: block; font-size: 7.8pt; color: var(--ink-2); line-height: 1.25; margin-top: 0.6mm; }
h2 { margin: 5.5mm 0 0; font-size: 12pt; font-weight: 650; letter-spacing: -0.01em; padding-bottom: 1.6mm; border-bottom: 1.2pt solid var(--ink); }
.job { display: grid; grid-template-columns: 30mm 1fr; gap: 5mm; padding: 3.4mm 0 3.2mm; border-bottom: 0.6pt solid var(--line); }
.job h3, .job .sub, .lines, li, .extra { break-inside: avoid; }
.job h3 { break-after: avoid; }
.job:last-of-type { border-bottom: 0; }
.when { font-size: 8.8pt; color: var(--ink-2); line-height: 1.35; }
.when b { display: block; color: var(--ink); font-weight: 560; }
.job h3 { margin: 0; font-size: 10.6pt; font-weight: 620; line-height: 1.3; }
.job h3 span { font-weight: 420; color: var(--ink-2); }
.sub { margin: 0.8mm 0 0; color: var(--ink-2); font-size: 9.2pt; }
.lines { margin: 1.8mm 0 0; display: grid; grid-template-columns: auto 1fr; gap: 0.6mm 3mm; font-size: 9.2pt; }
.lines dt { font-weight: 600; }
.lines dd { margin: 0; }
ul { margin: 1.8mm 0 0; padding: 0; list-style: none; }
li { position: relative; padding-left: 4mm; margin: 0.9mm 0; }
li::before { content: ""; position: absolute; left: 0; top: 2.1mm; width: 2mm; height: 0.8pt; background: var(--ink); }
.extra { margin: 1.8mm 0 0; font-size: 9pt; color: var(--ink-2); }
.tools { display: grid; grid-template-columns: 30mm 1fr; gap: 5mm; padding-top: 3mm; font-size: 9.2pt; }
.tools b { font-weight: 600; }
.foot { margin-top: 4mm; padding-top: 2.5mm; border-top: 0.6pt solid var(--line); font-size: 8.6pt; color: var(--ink-2); }
.foot a { color: var(--blue); }
"""


def html(lang):
    c = content(lang)
    contacts = []
    for i, (lab, val, href) in enumerate(c["contacts"]):
        cls = ' class="main"' if i == 0 else ""
        inner = f'<a href="{e(href)}">{e(val)}</a>' if href else e(val)
        contacts.append(f"<dt>{e(lab)}</dt><dd{cls}>{inner}</dd>")
    kpis = "".join(f"<div class=\"kpi\"><b>{e(v)}</b><span>{e(l)}</span></div>" for v, l in c["kpis"])
    jobs = []
    for j in c["jobs"]:
        sub = f'<p class="sub">{e(j["sub"])}</p>' if j["sub"] else ""
        lines = ("<dl class=\"lines\">" + "".join(f"<dt>{e(a)}</dt><dd>{b}</dd>" for a, b in j["lines"]) + "</dl>") if j["lines"] else ""
        bullets = "<ul>" + "".join(f"<li>{b}</li>" for b in j["bullets"]) + "</ul>"
        extra = f'<p class="extra">{e(j["extra"])}</p>' if j["extra"] else ""
        jobs.append(f'<section class="job"><div class="when"><b>{e(j["years"])}</b>{e(j["where"])}</div>'
                    f'<div><h3>{e(j["role"])}, <span>{e(j["org"])}</span></h3>{sub}{lines}{bullets}{extra}</div></section>')
    foot_url = f"https://{PORTFOLIO}/" + ("" if lang == "ru" else "en/")
    foot = c["foot"].replace(PORTFOLIO + ("/en/" if lang == "en" else ""), f'<a href="{foot_url}">{PORTFOLIO + ("/en/" if lang == "en" else "")}</a>')
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>{e(c["title"])}</title><style>{CSS}</style></head><body>
<header class="head"><div><h1>{e(c["name"])}</h1><p class="role">{e(c["role"])}</p><dl class="contacts">{"".join(contacts)}</dl></div>
<img class="photo" src="../assets/leonid.jpg" alt=""></header>
<p class="summary">{e(c["summary"])}</p>
<div class="kpis">{kpis}</div>
<h2>{e(c["exp_h"])}</h2>
{"".join(jobs)}
<div class="tools"><b>{e(c["tools_h"])}</b><span>{e(c["tools"])}</span></div>
<p class="foot">{foot}</p>
</body></html>"""


def keep_numbers_together(s):
    return re.sub(r">([^<]+)<", lambda m: ">" + re.sub(r"(?<=\d) (?=\d{3}\b)", " ", m.group(1)) + "<", s)


async def to_pdf(port):
    from playwright.async_api import async_playwright
    out = ROOT / "cv"
    out.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        for lang in ("ru", "en"):
            await pg.goto(f"http://localhost:{port}/cv-src/{lang}.html", wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.pdf(path=str(out / f"Leonid_Krivoshein_CV_{lang.upper()}.pdf"), format="A4", print_background=True, prefer_css_page_size=True)
        await b.close()


if __name__ == "__main__":
    for lang in ("ru", "en"):
        (ROOT / "cv-src" / f"{lang}.html").write_text(keep_numbers_together(html(lang)), encoding="utf-8")
    port = 8799
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1)
        asyncio.run(to_pdf(port))
    finally:
        srv.terminate()
    print("built cv/Leonid_Krivoshein_CV_RU.pdf and cv/Leonid_Krivoshein_CV_EN.pdf")
