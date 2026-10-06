#!/usr/bin/env python3
"""Builds the bilingual portfolio: index.html (RU) and en/index.html (EN).

All numbers live in DATA below and come from the resume (FlowCV, Oct 2026).
Derived values (cost per patient, CTR, ...) are computed here, never typed by hand.
Edit texts in T["ru"] / T["en"], then run:  python3 build.py
"""
from html import escape
from pathlib import Path

SITE_URL = ""  # e.g. "https://username.github.io/portfolio" — used for og:image / hreflang
ROOT = Path(__file__).parent

# ---------------------------------------------------------------- data
DATA = dict(
    g_spend=23000, g_rev=181000, roas=7.9, g_pat=261,
    i_pat=43, i_rev=53000, i_impr=637000, i_clicks=6200, i_spend_usd=1100,
    seo_pages=13, segments=5, pillars=6, posts=36, followers=2000,
    resp=260, interviews=20, hyp=10, hcp=100, formats=6, decks=3, specs=88, client_types=3,
    c_total=1800, c_ref=700, c_best=487, c_integr=10, c_act=50, c_partners=5,
    c_charity=30000, c_comments=100, c_videos=5, c_team=10,
)
D = DATA
D["c_other"] = D["c_total"] - D["c_ref"] - D["c_best"]          # 613
D["g_cpp"] = round(D["g_spend"] / D["g_pat"])                    # 88 GEL per patient
D["g_rpp"] = round(D["g_rev"] / D["g_pat"])                      # 693 GEL per patient
D["i_rpp"] = round(D["i_rev"] / D["i_pat"])                      # 1233 GEL per patient
D["i_ctr"] = D["i_clicks"] / D["i_impr"] * 100                   # 0.97 %
D["i_c2p"] = D["i_pat"] / D["i_clicks"] * 100                    # 0.69 %
D["i_cpc"] = D["i_spend_usd"] / D["i_clicks"]                    # $0.18
assert abs(D["g_rev"] / D["g_spend"] - D["roas"]) < 0.05


def n(v, lang):
    s = f"{v:,}"
    return s.replace(",", " ") if lang == "ru" else s


def dec(v, lang, p=1):
    s = f"{v:.{p}f}"
    return s.replace(".", ",") if lang == "ru" else s


def e(s):
    return escape(str(s), quote=True)


# ---------------------------------------------------------------- icons
ICON = {
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/></svg>',
    "ext": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
    "down": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 4v16M5 13l7 7 7-7"/></svg>',
    "dash": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M8 21v-8M13 21v-5M18 21V12"/></svg>',
    "table": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M3 15h18M9 4v16"/></svg>',
    "step": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M8 2v11M3.5 8.5 8 13l4.5-4.5"/></svg>',
}
PERSON = '<svg viewBox="0 0 26 34" aria-hidden="true"{cls}><circle cx="13" cy="8" r="6" fill="currentColor"/><path d="M2 34v-7a9 9 0 0 1 9-9h4a9 9 0 0 1 9 9v7z" fill="currentColor"/></svg>'
PAGE = '<svg viewBox="0 0 18 24" aria-hidden="true"><rect x="1" y="1" width="16" height="22" rx="2" fill="#fff" stroke="var(--seo)" stroke-width="1.6"/><path d="M4.5 7h9M4.5 11h9M4.5 15h6" stroke="var(--seo)" stroke-width="1.4"/></svg>'
CHAT = '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M20 4C11.2 4 4 10.6 4 18.8c0 4.4 2.1 8.3 5.4 11L8 36l7-3.4c1.6.5 3.3.7 5 .7 8.8 0 16-6.6 16-14.6S28.8 4 20 4z" fill="var(--seo)"/><path d="M13 17h14M13 22h9" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg>'


def coins(value, label, color, lang):
    full = int(value)
    frac = value - full
    r, step = 12, 30
    count = full + (1 if frac > 0 else 0)
    w = count * step
    out = [f'<svg viewBox="0 0 {w} 30" width="{w}" height="30" role="img" aria-label="{e(label)}">']
    for i in range(full):
        out.append(f'<circle cx="{i*step+15}" cy="15" r="{r}" fill="{color}"/>')
    if frac > 0:
        cx = full * step + 15
        cid = f"clip{int(value*10)}"
        out.append(f'<clipPath id="{cid}"><rect x="{cx-r}" y="0" width="{2*r*frac:.1f}" height="30"/></clipPath>')
        out.append(f'<circle cx="{cx}" cy="15" r="{r-0.75}" fill="none" stroke="{color}" stroke-width="1.5"/>')
        out.append(f'<circle cx="{cx}" cy="15" r="{r}" fill="{color}" clip-path="url(#{cid})"/>')
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------- texts
def texts(lang):
    ru = lang == "ru"
    gel = "лари" if ru else "GEL"
    money = (lambda v: f"{n(v, lang)} {gel}")
    t = {}
    t["html_lang"] = lang
    t["title"] = ("Леонид Кривошеин — product marketing и growth в HealthTech" if ru
                  else "Leonid Krivoshein — product marketing and growth in HealthTech")
    t["desc"] = ("Портфолио маркетолога: GTM медтех-продукта OncoDiag, привлечение пациентов стоматологии с ROAS 7,9×, рост сообщества с нуля до 1 800 подписчиков."
                 if ru else
                 "Marketing portfolio: GTM for the OncoDiag medtech product, dental patient acquisition at 7.9x ROAS, community growth from zero to 1,800 followers.")
    t["name"] = "Леонид Кривошеин" if ru else "Leonid Krivoshein"
    t["skip"] = "К содержанию" if ru else "Skip to content"
    t["nav"] = [("#cases", "Кейсы" if ru else "Cases"), ("#experience", "Опыт" if ru else "Experience"),
                ("#approach", "Подход" if ru else "Approach"), ("#contact", "Контакты" if ru else "Contact")]
    t["lang_link"] = ("en/", "EN", "English version") if ru else ("../", "RU", "Русская версия")

    t["h1"] = "Леонид<br>Кривошеин" if ru else "Leonid<br>Krivoshein"
    t["role"] = ("Product marketing, growth и GTM в HealthTech и медицине" if ru
                 else "Product marketing, growth and GTM for HealthTech and healthcare")
    t["lead"] = ("Начинаю с исследования аудитории и заканчиваю выручкой, которую можно посчитать. Сейчас вывожу на рынок медтех-продукт для онкодиагностики, до этого два года строил каналы привлечения пациентов для стоматологии в Батуми."
                 if ru else
                 "I start with customer research and finish with revenue you can count. Right now I'm taking a cancer-diagnostics medtech product to market; before that I spent two years building patient acquisition for a dental clinic in Batumi.")
    t["cta_cases"] = "Смотреть кейсы" if ru else "See the cases"
    t["cta_mail"] = "Написать на почту" if ru else "Email me"
    t["photo_alt"] = "Леонид Кривошеин" if ru else "Leonid Krivoshein"

    t["roas_h"] = ("Каждый лари в Google Ads вернул 7,9 лари выручки" if ru
                   else "Every lari spent on Google Ads brought back 7.9 in revenue")
    t["roas_src"] = ("Стоматология Minimum, Батуми, 2023–2025" if ru
                     else "Minimum dental clinic, Batumi, 2023–2025")
    t["roas_rows"] = [
        (money(D["g_spend"]), "вложено в рекламу" if ru else "ad spend", "spend", D["g_spend"] / D["g_rev"] * 100),
        (money(D["g_rev"]), "атрибутированная выручка" if ru else "attributed revenue", "revenue", 100.0),
    ]
    t["roas_chip"] = f"ROAS {dec(D['roas'], lang)}×"
    t["roas_foot"] = [
        (n(D["g_pat"], lang), "пациент из Google Ads" if ru else "patients from Google Ads"),
        (f"~{money(D['g_cpp'])}", "за одного пациента" if ru else "per patient"),
    ]
    t["roas_more"] = "Разбор кейса" if ru else "Read the case"

    # index
    t["idx_h"] = "Три кейса" if ru else "Three cases"
    t["idx_p"] = "От исследования до выручки" if ru else "From research to revenue"
    t["idx"] = [
        ("#oncodiag", "2025 — сейчас" if ru else "2025 — now", "OncoDiag",
         "GTM и product marketing теста для онкодиагностики" if ru else "GTM and product marketing for a cancer-diagnostics test",
         f"{D['resp']}+", "респондентов в исследовании" if ru else "research respondents"),
        ("#dental", "2023 — 2025", "Minimum Innovative Dentistry",
         "Три канала привлечения пациентов: Google Ads, Instagram, SEO" if ru else "Three patient acquisition channels: Google Ads, Instagram, SEO",
         f"{dec(D['roas'], lang)}×", "ROAS в Google Ads" if ru else "Google Ads ROAS"),
        ("#community", "2018 — 2019", "Медиа-проект и сообщество" if ru else "Media and community project",
         "Рост с нуля через блогеров, взаимный пиар и партнёрства" if ru else "Growth from zero through influencers, referrals and partnerships",
         n(D["c_total"], lang), "подписчиков с нуля" if ru else "followers from zero"),
    ]

    # ---- OncoDiag
    o = {}
    o["years"] = "2025 — сейчас" if ru else "2025 — present"
    o["where"] = "RS Agency, удалённо" if ru else "RS Agency, remote"
    o["role"] = "Marketing Strategist / Project Coordinator"
    o["meta_l"] = ("Период", "Где", "Роль") if ru else ("Period", "Where", "Role")
    o["h2"] = ("OncoDiag: вывод на рынок теста для онкодиагностики" if ru
               else "OncoDiag: taking a cancer-diagnostics test to market")
    o["context"] = ("Инновационный продукт для диагностики рака на основе биомаркера CA-62. Покупатель здесь не один: решение проходит через врачей, лаборатории и партнёров. Поэтому работа началась с исследования, а не с рекламы."
                    if ru else
                    "An innovative cancer-diagnostics product based on the CA-62 biomarker. There's no single buyer: the decision runs through doctors, laboratories and partners. So the work started with research, not with ads.")
    o["did"] = [
        f"Провёл исследование аудитории: <b>{D['resp']}+ респондентов</b> и <b>{D['interviews']} глубинных интервью</b>" if ru else f"Ran customer research with <b>{D['resp']}+ respondents</b> and <b>{D['interviews']} in-depth interviews</b>",
        f"Сформулировал позиционирование и GTM-стратегию, собрал <b>{D['hyp']} GTM-гипотез</b>" if ru else f"Developed product positioning and GTM strategy; created <b>{D['hyp']} GTM hypotheses</b>",
        "Выстроил B2B-маркетинг для врачей, лабораторий и партнёров" if ru else "Built B2B marketing for doctors, laboratories and partners",
        f"Сделал обучающий набор для партнёров из <b>{D['formats']} форматов</b> и <b>{D['decks']} презентации</b> продукта" if ru else f"Created a <b>{D['formats']}-format</b> partner education toolkit and <b>{D['decks']} product presentations</b>",
        f"Поддерживал образовательные мероприятия для <b>{D['hcp']}+ медицинских специалистов</b>" if ru else f"Supported educational activities for <b>{D['hcp']}+ healthcare professionals</b>",
        "Координировал копирайтеров, дизайнеров и подрядчиков" if ru else "Coordinated copywriters, designers and project contributors",
    ]
    o["dash_h"] = "GTM-панель OncoDiag" if ru else "OncoDiag GTM panel"
    o["kpis"] = [
        (f"{D['resp']}+", "респондентов в опросе" if ru else "survey respondents"),
        (str(D["interviews"]), "глубинных интервью" if ru else "in-depth interviews"),
        (str(D["hyp"]), "GTM-гипотез" if ru else "GTM hypotheses"),
        (f"{D['hcp']}+", "медицинских специалистов на обучении" if ru else "healthcare professionals trained"),
        (str(D["formats"]), "форматов обучения партнёров" if ru else "partner education formats"),
        (str(D["decks"]), "презентации продукта" if ru else "product presentations"),
    ]
    o["chain_h"] = "Как продукт выходит на рынок" if ru else "How the product goes to market"
    o["chain_sub"] = "Последовательность работы" if ru else "Order of work"
    o["chain"] = [
        ("Исследование" if ru else "Research", f"{D['resp']}+ анкет и {D['interviews']} интервью" if ru else f"{D['resp']}+ surveys, {D['interviews']} interviews"),
        ("Позиционирование" if ru else "Positioning", "ценность теста для каждой аудитории" if ru else "the test's value for each audience"),
        ("Гипотезы" if ru else "Hypotheses", f"{D['hyp']} GTM-гипотез" if ru else f"{D['hyp']} GTM hypotheses"),
        ("B2B-маркетинг" if ru else "B2B marketing", "врачи, лаборатории, партнёры" if ru else "doctors, labs, partners"),
        ("Обучение" if ru else "Enablement", f"{D['formats']} форматов, {D['hcp']}+ специалистов" if ru else f"{D['formats']} formats, {D['hcp']}+ professionals"),
    ]
    o["res_h"] = "Исследование аудитории" if ru else "Customer research"
    o["res_sub"] = "Количественная и качественная часть, человек" if ru else "Quantitative and qualitative, people"
    o["res"] = [
        ("Опрос" if ru else "Survey", D["resp"], f"{D['resp']}+"),
        ("Интервью" if ru else "Interviews", D["interviews"], str(D["interviews"])),
    ]
    o["hub_h"] = "Три B2B-аудитории" if ru else "Three B2B audiences"
    o["hub_sub"] = "Кому продаётся тест" if ru else "Who the test is sold through"
    o["hub_core"] = ("OncoDiag", "тест на биомаркер CA-62" if ru else "CA-62 biomarker test")
    o["hub"] = [
        ("Врачи" if ru else "Doctors", f"образовательные мероприятия, {D['hcp']}+ специалистов" if ru else f"educational events, {D['hcp']}+ professionals"),
        ("Лаборатории" if ru else "Laboratories", "B2B-маркетинг для лабораторий-партнёров" if ru else "B2B marketing for partner labs"),
        ("Партнёры" if ru else "Partners", f"обучающий набор из {D['formats']} форматов" if ru else f"a {D['formats']}-format education toolkit"),
    ]
    o["mx_h"] = (f"Сегментация {D['specs']} медицинских специальностей" if ru
                 else f"Segmentation of {D['specs']} medical specialties")
    o["mx_sub"] = ("Ещё в RS Agency: матрица для коммерческих предложений агентства. Каждая клетка — отдельное сочетание специальности и типа клиента со своим типом продажи, каналами, оффером и KPI."
                   if ru else
                   "Also at RS Agency: a matrix behind the agency's proposals. Each cell pairs a specialty with a client type and has its own sale type, channels, offer and KPIs.")
    o["mx_rows"] = ["Врач" if ru else "Doctor", "Клиника" if ru else "Clinic", "Медпродукт" if ru else "Med product"]
    o["mx_axis"] = ("1", f"{D['specs']} специальностей" if ru else f"{D['specs']} specialties")
    o["tbl_cap"] = "Ключевые цифры OncoDiag и RS Agency" if ru else "Key figures, OncoDiag and RS Agency"
    o["tbl_cols"] = ("Показатель", "Значение") if ru else ("Metric", "Value")
    o["tbl"] = [(lab, val) for val, lab in o["kpis"]] + [
        ("медицинских специальностей в матрице" if ru else "medical specialties in the matrix", str(D["specs"])),
        ("типа клиентов агентства" if ru else "agency client types", str(D["client_types"])),
    ]
    t["onco"] = o

    # ---- Dental
    d = {}
    d["years"] = "2023 — 2025"
    d["where"] = "Батуми, Грузия" if ru else "Batumi, Georgia"
    d["role"] = "Growth & Performance Marketing Lead"
    d["meta_l"] = o["meta_l"]
    d["h2"] = ("Minimum Innovative Dentistry: пациенты из трёх каналов" if ru
               else "Minimum Innovative Dentistry: patients from three channels")
    d["context"] = ("Частная стоматология в Батуми. Цель была не «вести рекламу», а приводить пациентов и знать, сколько выручки принёс каждый канал. Для этого реклама, страницы услуг, WhatsApp, запись и CRM работали как одна цепочка."
                    if ru else
                    "A private dental clinic in Batumi. The goal wasn't to “run ads” but to bring in patients and know how much revenue each channel produced. So ads, service pages, WhatsApp, appointments and the CRM worked as one chain.")
    d["did"] = [
        "Построил и вёл <b>3 воронки привлечения</b>: Google Ads, Instagram и органический поиск" if ru else "Built and managed <b>3 acquisition funnels</b> across Google Ads, Instagram and organic search",
        "Связал рекламу со страницами услуг, CRM, WhatsApp, записью, пациентами и выручкой" if ru else "Connected acquisition with landing pages, CRM, WhatsApp, appointments, patients and revenue",
        f"Вёл рекламу в Instagram: <b>{n(637, lang)} тыс.+ показов</b> и <b>6,2 тыс.+ переходов</b> при бюджете около $1,1 тыс." if ru else "Managed Instagram paid campaigns: <b>637K+ impressions</b> and <b>6.2K+ link clicks</b> on about $1.1K spend",
        f"Собрал SEO-воронку из <b>{D['seo_pages']} страниц</b> под конкретные услуги" if ru else f"Built an SEO conversion funnel with <b>{D['seo_pages']} service-specific pages</b>",
        f"Разработал маркетинговую стратегию для <b>{D['segments']} сегментов</b> аудитории" if ru else f"Developed marketing strategy for <b>{D['segments']} audience segments</b>",
        f"Выстроил контент-систему: <b>{D['pillars']} рубрик</b> и <b>{D['posts']} постов</b> в Instagram" if ru else f"Built a content system with <b>{D['pillars']} content pillars</b> and <b>{D['posts']} Instagram posts</b>",
        "Снимал фото и видео: врачи, клинические случаи, Reels и Stories" if ru else "Produced photo and video content: doctors, cases, Reels and Stories",
        f"Вырастил Instagram до <b>{n(D['followers'], lang)}+ целевых подписчиков</b>" if ru else f"Grew Instagram to <b>{n(D['followers'], lang)}+ targeted followers</b>",
    ]
    d["dash_h"] = "Привлечение пациентов" if ru else "Patient acquisition"
    d["seg"] = [("all", "Все" if ru else "All", None), ("google", "Google Ads", "var(--google)"),
                ("insta", "Instagram", "var(--insta)"), ("seo", "SEO", "var(--seo)")]
    d["seg_label"] = "Канал" if ru else "Channel"
    calc = "расчёт" if ru else "calculated"
    d["kpis"] = {
        "all": [
            (money(D["g_rev"]), "выручка из Google Ads" if ru else "Google Ads revenue", "var(--google)", None),
            (money(D["i_rev"]), "выручка из Instagram" if ru else "Instagram revenue", "var(--insta)", None),
            (str(D["seo_pages"]), "SEO-страниц под услуги" if ru else "SEO service pages", "var(--seo)", None),
            (f"{n(D['followers'], lang)}+", "целевых подписчиков" if ru else "targeted followers", "var(--insta)", None),
        ],
        "google": [
            (money(D["g_spend"]), "бюджет" if ru else "spend", "var(--google)", None),
            (money(D["g_rev"]), "атрибутированная выручка" if ru else "attributed revenue", "var(--google)", None),
            (f"{dec(D['roas'], lang)}×", "ROAS", "var(--google)", None),
            (n(D["g_pat"], lang), "пациент" if ru else "patients", "var(--google)", None),
            (f"~{money(D['g_cpp'])}", "стоимость пациента" if ru else "cost per patient", "var(--google)", calc),
            (f"~{money(D['g_rpp'])}", "выручка на пациента" if ru else "revenue per patient", "var(--google)", calc),
        ],
        "insta": [
            (f"{n(637, lang)} тыс.+" if ru else "637K+", "платных показов" if ru else "paid impressions", "var(--insta)", None),
            ("6,2 тыс.+" if ru else "6.2K+", "переходов по ссылке" if ru else "link clicks", "var(--insta)", None),
            ("~$1,1 тыс." if ru else "~$1.1K", "бюджет" if ru else "spend", "var(--insta)", None),
            (str(D["i_pat"]), "пациента по CRM" if ru else "CRM-attributed patients", "var(--insta)", None),
            (money(D["i_rev"]), "атрибутированная выручка" if ru else "attributed revenue", "var(--insta)", None),
            (f"~{dec(D['i_ctr'], lang, 2)}%", "CTR", "var(--insta)", calc),
        ],
        "seo": [
            (str(D["seo_pages"]), "страниц под конкретные услуги" if ru else "service-specific pages", "var(--seo)", None),
            ("WhatsApp", "куда ведёт страница" if ru else "where each page hands off", "var(--seo)", None),
            ("—", "отдельной атрибуции выручки нет" if ru else "no separate revenue attribution", "var(--seo)", None),
        ],
    }
    d["rev_h"] = "Атрибутированная выручка" if ru else "Attributed revenue"
    d["rev_sub"] = "По каналам, лари" if ru else "By channel, GEL"
    d["pat_h"] = "Пациенты из рекламы" if ru else "Patients from ads"
    d["pat_sub"] = "По каналам, человек" if ru else "By channel, people"
    d["seo_none"] = "отдельно не считалась" if ru else "not attributed separately"
    d["rev"] = [("google", "Google Ads", D["g_rev"], money(D["g_rev"])), ("insta", "Instagram", D["i_rev"], money(D["i_rev"])), ("seo", "SEO", None, None)]
    d["pat"] = [("google", "Google Ads", D["g_pat"], n(D["g_pat"], lang)), ("insta", "Instagram", D["i_pat"], str(D["i_pat"])), ("seo", "SEO", None, None)]
    d["coin_h"] = "Окупаемость Google Ads" if ru else "Google Ads payback"
    d["coin_sub"] = "Один кружок — один лари" if ru else "One circle is one lari"
    d["coin_rows"] = [("1 лари рекламы" if ru else "1 lari of ads", 1.0, "var(--google-light)"),
                      (f"{dec(D['roas'], lang)} лари выручки" if ru else f"{dec(D['roas'], lang)} lari of revenue", D["roas"], "var(--google)")]
    d["lad_h"] = "Воронка Instagram" if ru else "Instagram funnel"
    d["lad_sub"] = "От показа до пациента в CRM" if ru else "From impression to a patient in the CRM"
    d["lad"] = [
        (f"{n(637, lang)} тыс.+" if ru else "637K+", "платных показов" if ru else "paid impressions"),
        (f"~{dec(D['i_ctr'], lang, 2)}%", "кликают по ссылке" if ru else "click through"),
        ("6,2 тыс.+" if ru else "6.2K+", "переходов" if ru else "link clicks"),
        (f"~{dec(D['i_c2p'], lang, 2)}%", "становятся пациентами" if ru else "become patients"),
        (str(D["i_pat"]), f"пациента, {money(D['i_rev'])} выручки" if ru else f"patients, {money(D['i_rev'])} revenue"),
    ]
    d["flow_h"] = "Путь от обращения до выручки" if ru else "From first click to revenue"
    d["flow_sub"] = "Одна цепочка для всех каналов" if ru else "One chain for every channel"
    d["flow"] = [
        ("Реклама или поиск" if ru else "Ad or search", "Google Ads, Instagram, органика" if ru else "Google Ads, Instagram, organic"),
        ("Страница услуги" if ru else "Service page", "под конкретный запрос" if ru else "matches the exact query"),
        ("WhatsApp", "переписка с клиникой" if ru else "a chat with the clinic"),
        ("Запись" if ru else "Appointment", "время у врача" if ru else "a slot with the doctor"),
        ("Пациент в CRM" if ru else "Patient in CRM", "источник сохранён" if ru else "source is kept"),
        ("Выручка" if ru else "Revenue", "видно по каждому каналу" if ru else "visible per channel"),
    ]
    d["seo_h"] = "SEO-воронка" if ru else "SEO funnel"
    d["seo_sub"] = (f"{D['seo_pages']} страниц под услуги, с каждой — сразу в WhatsApp" if ru
                    else f"{D['seo_pages']} service pages, each handing off straight to WhatsApp")
    d["posts_h"] = "Контент в Instagram" if ru else "Instagram content"
    d["posts_sub"] = (f"{D['posts']} постов в {D['pillars']} рубриках, плюс Reels и Stories" if ru
                      else f"{D['posts']} posts across {D['pillars']} pillars, plus Reels and Stories")
    d["posts_leg"] = ("один пост" if ru else "one post", f"{n(D['followers'], lang)}+ целевых подписчиков" if ru else f"{n(D['followers'], lang)}+ targeted followers")
    d["tbl_cap"] = "Данные панели по каналам" if ru else "Panel data by channel"
    d["tbl_cols"] = (("Канал", "Бюджет", "Выручка", "Пациенты", "Ещё") if ru else ("Channel", "Spend", "Revenue", "Patients", "Other"))
    d["tbl"] = [
        ("Google Ads", money(D["g_spend"]), money(D["g_rev"]), n(D["g_pat"], lang), f"ROAS {dec(D['roas'], lang)}×"),
        ("Instagram", "~$1,1 тыс." if ru else "~$1.1K", money(D["i_rev"]), str(D["i_pat"]),
         "637 тыс.+ показов, 6,2 тыс.+ переходов" if ru else "637K+ impressions, 6.2K+ clicks"),
        ("SEO", "—", "—", "—", f"{D['seo_pages']} страниц услуг, переход в WhatsApp" if ru else f"{D['seo_pages']} service pages, WhatsApp handoff"),
    ]
    d["note"] = ("Выручка атрибутированная: обращения из рекламы связаны с записями, пациентами и оплатами. Значения с «~» посчитаны по этим данным."
                 if ru else
                 "Revenue is attributed: ad inquiries are linked to appointments, patients and payments. Values marked “~” are calculated from that data.")
    t["dental"] = d

    # ---- Community
    c = {}
    c["years"] = "2018 — 2019"
    c["where"] = "Санкт-Петербург" if ru else "Saint Petersburg"
    c["role"] = "Founder / Community Growth Lead"
    c["meta_l"] = o["meta_l"]
    c["h2"] = ("Медиа-проект и сообщество: с нуля до 1 800 подписчиков" if ru
               else "Media and community project: from zero to 1,800 followers")
    c["context"] = ("Собственный проект в Instagram с командой из 10 человек. Аудиторию собирали через блогеров, взаимный пиар, партнёрства с брендами и видеоистории участников."
                    if ru else
                    "My own Instagram project with a team of 10. The audience came from influencers, referral mechanics, brand partnerships and participants' video stories.")
    c["did"] = [
        f"Договорился о <b>{D['c_integr']} интеграциях</b> с блогерами; лучшая коллаборация принесла <b>+{D['c_best']} подписчиков</b>" if ru else f"Organized <b>{D['c_integr']} influencer integrations</b>; the best collaboration brought <b>+{D['c_best']} followers</b>",
        f"Придумал механику взаимного пиара: аудит аккаунта подписчика и репост в Stories в обмен на репост проекта. <b>{D['c_act']} активаций</b> дали <b>+{D['c_ref']} подписчиков</b>" if ru else f"Built a referral mechanic: an account audit and a Stories shout-out in exchange for sharing the project. <b>{D['c_act']} activations</b> brought <b>+{D['c_ref']} followers</b>",
        "Запустил «день блогера»: гость вёл аккаунт проекта весь день, вечером — совместный эфир" if ru else "Ran takeovers: a guest blogger hosted the account for a day, ending with a joint live stream",
        f"Провёл благотворительную акцию с <b>{D['c_partners']} брендами</b>: {D['c_comments']}+ комментариев, <b>{n(D['c_charity'], lang)} рублей</b> перечислено в фонд" if ru else f"Ran a charity campaign with <b>{D['c_partners']} partner brands</b>: {D['c_comments']}+ comments, <b>RUB {n(D['c_charity'], lang)}</b> donated to a foundation",
        f"Спродюсировал <b>{D['c_videos']} видеоисторий</b> участников; проект показали по телевидению" if ru else f"Produced <b>{D['c_videos']} storytelling videos</b>; the project was featured on TV",
        f"Руководил командой из <b>{D['c_team']} человек</b>: еженедельные планёрки, задачи в таск-менеджере" if ru else f"Led a cross-functional team of <b>{D['c_team']}</b>: weekly planning, tasks in a task manager",
    ]
    c["dash_h"] = "Рост сообщества" if ru else "Community growth"
    c["kpis"] = [
        (n(D["c_total"], lang), "подписчиков с нуля" if ru else "followers from zero"),
        (str(D["c_integr"]), "интеграций с блогерами" if ru else "influencer integrations"),
        (str(D["c_act"]), "активаций взаимного пиара" if ru else "referral activations"),
        (str(D["c_partners"]), "брендов-партнёров" if ru else "partner brands"),
        (f"{n(D['c_charity'], lang)}" if ru else f"RUB {n(D['c_charity'], lang)}", "рублей в благотворительный фонд" if ru else "raised for charity"),
        (str(D["c_videos"]), "видеоисторий и эфир на ТВ" if ru else "story videos, plus TV"),
    ]
    c["wf_h"] = f"Откуда пришли {n(D['c_total'], lang)} подписчиков" if ru else f"Where the {n(D['c_total'], lang)} followers came from"
    c["wf_sub"] = "Прирост по механикам, человек" if ru else "Growth by mechanic, people"
    c["wf"] = [
        ("start", "Старт" if ru else "Start", 0, 0, "Старт" if ru else "Start"),
        ("inc", "Взаимный пиар" if ru else "Referral mechanic", 0, D["c_ref"], "Взаимный пиар" if ru else "Referral"),
        ("inc", "Лучшая коллаборация с блогером" if ru else "Best influencer collaboration", D["c_ref"], D["c_best"], "Лучший блогер" if ru else "Top influencer"),
        ("inc", "Другие блогеры, эфиры, видео и акции" if ru else "Other influencers, live streams, video and campaigns", D["c_ref"] + D["c_best"], D["c_other"], "Другие механики" if ru else "Other mechanics"),
        ("total", "Итого" if ru else "Total", 0, D["c_total"], "Итого" if ru else "Total"),
    ]
    c["mech_h"] = "Механики" if ru else "Mechanics"
    c["mech_sub"] = "Что работало и какой дало результат" if ru else "What worked and what it produced"
    c["mech"] = [
        ("Взаимный пиар" if ru else "Referral mechanic", f"+{D['c_ref']}"),
        ("Лучшая коллаборация с блогером" if ru else "Best influencer collaboration", f"+{D['c_best']}"),
        ("Благотворительная акция, 5 брендов" if ru else "Charity campaign, 5 brands", f"{D['c_comments']}+ " + ("комментариев" if ru else "comments")),
        ("Видеоистории участников" if ru else "Participant video stories", ("5 роликов + ТВ" if ru else "5 videos + TV")),
        ("«День блогера» и эфир" if ru else "Takeover day and live stream", ("удержание аудитории" if ru else "audience retention")),
    ]
    c["team_h"] = f"Команда из {D['c_team']} человек" if ru else f"A team of {D['c_team']}"
    c["team_sub"] = "Еженедельные планёрки, задачи в таск-менеджере" if ru else "Weekly planning, tasks in a task manager"
    c["team_lead"] = "основатель" if ru else "founder"
    c["roles"] = (["копирайтеры", "дизайнеры", "редакторы", "операционный директор", "коммерческий директор", "креативная группа"] if ru
                  else ["copywriters", "designers", "editors", "operations director", "commercial director", "creative team"])
    c["tbl_cap"] = "Прирост подписчиков по механикам" if ru else "Follower growth by mechanic"
    c["tbl_cols"] = ("Источник", "Подписчики") if ru else ("Source", "Followers")
    c["tbl"] = [(lab, f"+{n(v, lang)}") for k, lab, b, v, short in c["wf"] if k == "inc"] + [("Итого" if ru else "Total", n(D["c_total"], lang))]
    t["comm"] = c

    t["tbl_show"] = "Таблица" if ru else "Table"
    t["tbl_hide"] = "Скрыть таблицу" if ru else "Hide table"

    # experience
    t["exp_h"] = "Опыт" if ru else "Experience"
    t["exp"] = [
        ("2025 — сейчас" if ru else "2025 — present", "Marketing Strategist / Project Coordinator", "RS Agency, удалённо" if ru else "RS Agency, remote",
         "OncoDiag: GTM и product marketing. Также исследования рынка, сегментация 88 медицинских специальностей, координация клиентских проектов." if ru else
         "OncoDiag: GTM and product marketing. Also market research, segmentation of 88 medical specialties, client project coordination."),
        ("2023 — 2025", "Growth & Performance Marketing Lead", "Minimum Innovative Dentistry, Батуми" if ru else "Minimum Innovative Dentistry, Batumi",
         "Google Ads, Instagram, SEO, CRM и контент. ROAS 7,9× в Google Ads." if ru else "Google Ads, Instagram, SEO, CRM and content. 7.9x ROAS on Google Ads."),
        ("2018 — 2019", "Founder / Community Growth Lead", "Медиа-проект, Санкт-Петербург" if ru else "Media project, Saint Petersburg",
         "Рост с нуля до 1 800 подписчиков, команда из 10 человек." if ru else "Growth from zero to 1,800 followers, a team of 10."),
    ]

    # approach
    t["app_h"] = "Как я работаю" if ru else "How I work"
    t["app_p"] = "Четыре шага, которые повторяются в каждом кейсе" if ru else "Four steps that repeat across every case"
    t["steps"] = [
        ("Исследую" if ru else "Research", "Опросы и глубинные интервью до того, как тратить бюджет. Ищу, кто принимает решение и что его останавливает." if ru else "Surveys and in-depth interviews before any budget is spent. I look for who decides and what stops them.",
         f"OncoDiag: {D['resp']}+ респондентов, {D['interviews']} интервью" if ru else f"OncoDiag: {D['resp']}+ respondents, {D['interviews']} interviews"),
        ("Позиционирую" if ru else "Position", "Формулирую ценность для каждой аудитории и превращаю её в гипотезы, которые можно проверить." if ru else "I define the value for each audience and turn it into hypotheses that can be tested.",
         f"OncoDiag: {D['hyp']} GTM-гипотез" if ru else f"OncoDiag: {D['hyp']} GTM hypotheses"),
        ("Строю каналы" if ru else "Build channels", "Реклама, SEO, контент, партнёрства и блогеры. У каждого канала своя воронка и своя страница." if ru else "Ads, SEO, content, partnerships and influencers. Each channel gets its own funnel and its own page.",
         "Стоматология: 3 воронки, 13 SEO-страниц" if ru else "Dental: 3 funnels, 13 SEO pages"),
        ("Считаю выручку" if ru else "Count revenue", "Связываю обращение с записью, пациентом и оплатой, чтобы бюджет шёл туда, где он окупается." if ru else "I link each inquiry to an appointment, a patient and a payment, so budget goes where it pays back.",
         f"Google Ads: ROAS {dec(D['roas'], lang)}×" if ru else f"Google Ads: {dec(D['roas'], lang)}x ROAS"),
    ]
    t["tools_h"] = "Инструменты" if ru else "Tools"
    t["tools"] = (["Google Ads", "Meta Ads", "Яндекс Директ", "SEO-страницы услуг", "CRM", "WhatsApp Business", "Make.com", "Kaiten", "опросы", "глубинные интервью"] if ru
                  else ["Google Ads", "Meta Ads", "Yandex Direct", "SEO service pages", "CRM", "WhatsApp Business", "Make.com", "Kaiten", "surveys", "in-depth interviews"])

    # contact
    t["c_h"] = "Обсудим вашу задачу" if ru else "Let's talk about your project"
    t["c_p"] = ("Открыт к ролям и проектам в product marketing, growth и GTM: HealthTech, медицина, B2B. Работаю удалённо из Грузии."
                if ru else
                "Open to roles and projects in product marketing, growth and GTM: HealthTech, healthcare, B2B. Working remotely from Georgia.")
    t["c_mail"] = "kriwoshein.leonid248@gmail.com"
    t["c_li"] = "linkedin.com/in/leonid-krivoshein"
    t["c_labels"] = ("Почта", "LinkedIn", "Где") if ru else ("Email", "LinkedIn", "Location")
    t["c_where"] = "Грузия, удалённо" if ru else "Georgia, remote"
    t["c_btn_mail"] = "Написать письмо" if ru else "Write an email"
    t["c_btn_li"] = "Открыть LinkedIn" if ru else "Open LinkedIn"
    t["foot_note"] = ("Цифры взяты из рабочих отчётов и CRM. Выручка указана атрибутированная."
                      if ru else "Figures come from work reports and CRM data. Revenue is attributed revenue.")
    return t


# ---------------------------------------------------------------- render helpers
UNITS = ("лари", "GEL")


def unit_small(val):
    """'181 000 лари' -> '181 000 <small>лари</small>' so big figures fit their tile."""
    head, _, tail = str(val).rpartition(" ")
    if head and tail in UNITS:
        return f"{e(head)}<small>&nbsp;{e(tail)}</small>"
    return e(val)


def kpi_cells(items, with_dot=False):
    out = []
    for it in items:
        if len(it) == 4:
            val, lab, color, note = it
        else:
            val, lab = it
            color, note = None, None
        dot = f'<i style="background:{color}"></i>' if (with_dot and color) else ""
        nt = f'<div class="kpi-note">{e(note)}</div>' if note else ""
        out.append(f'<div class="kpi"><div class="kpi-label">{dot}{e(lab)}</div><div class="kpi-value">{unit_small(val)}</div>{nt}</div>')
    return "".join(out)


def hbars(rows, maxv, color_map, none_text, unit_label, lang):
    out = ['<div class="hbars">']
    for key, name, v, vs in rows:
        col = color_map.get(key, "var(--onco)")
        dot = f'<i style="background:{col}"></i>'
        if v is None:
            out.append(f'<div class="hbar" data-ch="{key}"><div class="hbar-name">{dot}{e(name)}</div>'
                       f'<div class="hbar-track"><span class="hbar-none">{e(none_text)}</span></div></div>')
            continue
        r = v / maxv  # bar length as a share of the space left after the value label
        out.append(
            f'<div class="hbar" data-ch="{key}"><div class="hbar-name">{dot}{e(name)}</div>'
            f'<div class="hbar-track"><span class="hbar-fill" tabindex="0" style="--r:{r:.4f};background:{col}" '
            f'data-tip="{e(vs)}" data-tip-label="{e(name + ", " + unit_label)}" aria-label="{e(name)}: {e(vs)}"></span>'
            f'<span class="hbar-val">{e(vs)}</span></div></div>')
    out.append("</div>")
    return "".join(out)


def chain(items, numbered=True):
    out = [f'<ol class="chain" style="--n:{len(items)}">']
    for i, (h, p) in enumerate(items, 1):
        cls = ' class="end"' if i == len(items) else ""
        out.append(f'<li{cls}><span class="dot">{i}</span><h5>{e(h)}</h5><p>{e(p)}</p></li>')
    out.append("</ol>")
    return "".join(out)


def table(cap, cols, rows, num_cols=()):
    head = "".join(f'<th scope="col"{" class=\"num\"" if i in num_cols else ""}>{e(c)}</th>' for i, c in enumerate(cols))
    body = []
    for r in rows:
        cells = []
        for i, v in enumerate(r):
            if i == 0:
                cells.append(f'<th scope="row">{e(v)}</th>')
            else:
                cells.append(f'<td{" class=\"num\"" if i in num_cols else ""}>{e(v)}</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f'<table class="dtable"><caption>{e(cap)}</caption><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table>'


def tbl_toggle(tid, t):
    return (f'<button class="tbl-toggle" type="button" aria-expanded="false" aria-controls="{tid}" '
            f'data-show="{e(t["tbl_show"])}" data-hide="{e(t["tbl_hide"])}">{ICON["table"]}<span>{e(t["tbl_show"])}</span></button>')


def dash_bar(title, sub, extra=""):
    return (f'<div class="dash-bar"><div class="dash-title">{ICON["dash"]}<h3>{e(title)}</h3><span>{e(sub)}</span></div>{extra}</div>')


def case_top(x):
    l1, l2, l3 = x["meta_l"]
    did = "".join(f"<li>{s}</li>" for s in x["did"])
    return f'''<div class="case-top">
  <dl class="case-meta"><div><dt>{e(l1)}</dt><dd>{e(x["years"])}</dd></div><div><dt>{e(l2)}</dt><dd>{e(x["where"])}</dd></div><div><dt>{e(l3)}</dt><dd>{e(x["role"])}</dd></div></dl>
  <div>
    <h2>{e(x["h2"])}</h2>
    <p class="context">{e(x["context"])}</p>
    <ul class="did">{did}</ul>
  </div>
</div>'''


# ---------------------------------------------------------------- sections
def render(lang):
    t = texts(lang)
    ru = lang == "ru"
    P = "" if ru else "../"
    o, d, c = t["onco"], t["dental"], t["comm"]
    gel_unit = "лари" if ru else "GEL"
    ppl_unit = "человек" if ru else "people"

    nav = "".join(f'<a href="{h}">{e(lab)}</a>' for h, lab in t["nav"])
    lhref, ltext, ltitle = t["lang_link"]

    # hero bars
    spend_w = t["roas_rows"][0][3]
    rows = []
    for val, lab, kind, w in t["roas_rows"]:
        chip = f'<span class="roas-mult">{e(t["roas_chip"])}</span>' if kind == "spend" else ""
        rows.append(f'<div class="roas-row"><div class="roas-val"><b>{unit_small(val)}</b><span>{e(lab)}</span></div>'
                    f'<div class="roas-track" style="--w-spend:{spend_w:.2f}%"><div class="roas-bar {kind}" style="--w:{w:.2f}%"></div>{chip}</div></div>')
    foot = "".join(f"<span><b>{e(a)}</b> {e(b)}</span>" for a, b in t["roas_foot"])
    foot += f'<a href="#dental">{e(t["roas_more"])}</a>'

    idx = "".join(
        f'<a href="{h}"><span class="index-years">{e(y)}</span><span><span class="index-title">{e(ti)}</span>'
        f'<span class="index-desc">{e(de)}</span></span><span class="index-metric">{e(m)}<small>{e(ml)}</small></span></a>'
        for h, y, ti, de, m, ml in t["idx"])

    # ---- OncoDiag dashboard
    res = hbars([("onco", lab, v, vs) for lab, v, vs in o["res"]], o["res"][0][1], {"onco": "var(--onco)"}, "", ppl_unit, lang)
    hub_nodes = "".join(f'<div class="hub-node n{i}"><h5>{e(h)}</h5><p>{e(p)}</p></div>' for i, (h, p) in enumerate(o["hub"], 1))
    mx_rows = []
    for i, lab in enumerate(o["mx_rows"], 1):
        cells = "<span></span>" * D["specs"]
        mx_rows.append(f'<div class="matrix-label">{e(lab)}</div><div class="matrix-row r{i}">{cells}</div>')
    onco_dash = f'''<div class="dash">
  {dash_bar(o["dash_h"], o["years"], tbl_toggle("tbl-onco", t))}
  <div class="dtable-wrap" id="tbl-onco" hidden>{table(o["tbl_cap"], o["tbl_cols"], o["tbl"], num_cols=(1,))}</div>
  <div class="kpis">{kpi_cells(o["kpis"])}</div>
  <div class="panels">
    <section class="panel wide"><h4>{e(o["chain_h"])}</h4><p class="sub">{e(o["chain_sub"])}</p>{chain(o["chain"])}</section>
    <section class="panel"><h4>{e(o["res_h"])}</h4><p class="sub">{e(o["res_sub"])}</p>{res}</section>
    <section class="panel"><h4>{e(o["hub_h"])}</h4><p class="sub">{e(o["hub_sub"])}</p>
      <div class="hub"><div class="hub-core"><b>{e(o["hub_core"][0])}</b><span>{e(o["hub_core"][1])}</span></div>{hub_nodes}</div></section>
    <section class="panel wide"><h4>{e(o["mx_h"])}</h4><p class="sub">{e(o["mx_sub"])}</p>
      <div class="matrix" role="img" aria-label="{e(o["mx_h"])}: {D['specs']} × {D['client_types']}">{"".join(mx_rows)}
      <div class="matrix-axis"><span>{e(o["mx_axis"][0])}</span><span>{e(o["mx_axis"][1])}</span></div></div></section>
  </div>
</div>'''

    # ---- Dental dashboard
    seg = "".join(
        f'<button type="button" data-view="{k}" aria-pressed="{"true" if k == "all" else "false"}">'
        f'{f"<i style=\"background:{col}\"></i>" if col else ""}{e(lab)}</button>'
        for k, lab, col in d["seg"])
    seg_html = f'<div class="seg" role="group" aria-label="{e(d["seg_label"])}">{seg}</div>'
    kpi_groups = "".join(
        f'<div class="kpis" data-view="{k}"{"" if k == "all" else " hidden"}>{kpi_cells(v, with_dot=True)}</div>'
        for k, v in d["kpis"].items())
    cmap = {"google": "var(--google)", "insta": "var(--insta)", "seo": "var(--seo)"}
    rev = hbars(d["rev"], D["g_rev"], cmap, d["seo_none"], gel_unit, lang)
    pat = hbars(d["pat"], D["g_pat"], cmap, d["seo_none"], ppl_unit, lang)
    coin_rows = "".join(f'<div class="coins-row"><span>{e(lab)}</span>{coins(v, lab, col, lang)}</div>' for lab, v, col in d["coin_rows"])
    lad = []
    for i, (val, lab) in enumerate(d["lad"]):
        if i % 2 == 0:
            lad.append(f'<div class="ladder-step"><span>{e(lab)}</span><b>{e(val)}</b></div>')
        else:
            lad.append(f'<div class="ladder-rate">{ICON["step"]}<span><b>{e(val)}</b> {e(lab)}</span></div>')
    pages = "".join(PAGE for _ in range(D["seo_pages"]))
    seo_vis = (f'<div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap" role="img" aria-label="{e(d["seo_sub"])}">'
               f'<div style="display:grid;grid-template-columns:repeat(7,18px);gap:6px">{pages}</div>'
               f'<svg viewBox="0 0 40 16" width="40" height="16" aria-hidden="true"><path d="M2 8h34M30 2l6 6-6 6" fill="none" stroke="var(--ink)" stroke-width="1.6"/></svg>'
               f'<div style="width:44px">{CHAT}</div></div>')
    posts = "<span></span>" * D["posts"]
    dental_dash = f'''<div class="dash" data-view="all">
  {dash_bar(d["dash_h"], d["years"], seg_html + tbl_toggle("tbl-dental", t))}
  <div class="dtable-wrap" id="tbl-dental" hidden>{table(d["tbl_cap"], d["tbl_cols"], d["tbl"], num_cols=(1, 2, 3))}</div>
  {kpi_groups}
  <div class="panels">
    <section class="panel" data-ch="all google insta"><h4>{e(d["rev_h"])}</h4><p class="sub">{e(d["rev_sub"])}</p>{rev}</section>
    <section class="panel" data-ch="all google insta"><h4>{e(d["pat_h"])}</h4><p class="sub">{e(d["pat_sub"])}</p>{pat}</section>
    <section class="panel" data-ch="google"><h4>{e(d["coin_h"])}</h4><p class="sub">{e(d["coin_sub"])}</p><div class="coins">{coin_rows}</div></section>
    <section class="panel" data-ch="insta"><h4>{e(d["lad_h"])}</h4><p class="sub">{e(d["lad_sub"])}</p><div class="ladder">{"".join(lad)}</div></section>
    <section class="panel wide" data-ch="all"><h4>{e(d["flow_h"])}</h4><p class="sub">{e(d["flow_sub"])}</p>{chain(d["flow"])}</section>
    <section class="panel" data-ch="seo"><h4>{e(d["seo_h"])}</h4><p class="sub">{e(d["seo_sub"])}</p>{seo_vis}</section>
    <section class="panel" data-ch="insta"><h4>{e(d["posts_h"])}</h4><p class="sub">{e(d["posts_sub"])}</p>
      <div class="posts" role="img" aria-label="{e(d["posts_sub"])}">{posts}</div>
      <div class="legend"><span><i style="background:var(--insta-wash)"></i>{e(d["posts_leg"][0])}</span><span>{e(d["posts_leg"][1])}</span></div></section>
  </div>
  <p class="dash-note">{e(d["note"])}</p>
</div>'''

    # ---- Community dashboard (waterfall)
    top = 2000
    ticks = [0, 500, 1000, 1500, 2000]
    grid = "".join(f'<div class="{"base" if v == 0 else ""}" style="bottom:{v/top*100:.2f}%"><span>{n(v, lang)}</span></div>' for v in ticks)
    cols, labels = [], []
    for i, (kind, lab, base, val, short) in enumerate(c["wf"]):
        b = base / top * 100
        h = val / top * 100
        topp = (base + val) / top * 100
        inner = ""
        if kind == "start":
            inner += f'<span class="wf-val" style="--top:0%">0</span>'
            inner += f'<span class="wf-link r" style="--y:0%"></span>'
        else:
            vs = f"+{n(val, lang)}" if kind == "inc" else n(val, lang)
            cls = "wf-bar total" if kind == "total" else "wf-bar"
            inner += (f'<span class="{cls}" tabindex="0" style="--b:{b:.2f}%;--h:{h:.2f}%" data-tip="{e(vs)}" '
                      f'data-tip-label="{e(lab)}" aria-label="{e(lab)}: {e(vs)}"></span>')
            inner += f'<span class="wf-val" style="--top:{topp:.2f}%">{e(vs)}</span>'
            if kind == "inc":
                inner += f'<span class="wf-link l" style="--y:{b:.2f}%"></span><span class="wf-link r" style="--y:{topp:.2f}%"></span>'
            else:
                inner += f'<span class="wf-link l" style="--y:{topp:.2f}%"></span>'
        cols.append(f'<div class="wf-col">{inner}</div>')
        labels.append(f'<span title="{e(lab)}">{e(short)}</span>')
    nwf = len(c["wf"])
    wf = (f'<div class="wfall" style="--n:{nwf}"><div class="wf-grid" aria-hidden="true">{grid}</div>{"".join(cols)}</div>'
          f'<div class="wf-labels" style="--n:{nwf}">{"".join(labels)}</div>')
    mech = "".join(f"<li><span>{e(a)}</span><b>{e(b)}</b></li>" for a, b in c["mech"])
    team = PERSON.format(cls=' class="lead"') + "".join(PERSON.format(cls="") for _ in range(D["c_team"] - 1))
    roles = "".join(f"<span>{e(r)}</span>" for r in c["roles"])
    comm_dash = f'''<div class="dash">
  {dash_bar(c["dash_h"], c["years"], tbl_toggle("tbl-comm", t))}
  <div class="dtable-wrap" id="tbl-comm" hidden>{table(c["tbl_cap"], c["tbl_cols"], c["tbl"], num_cols=(1,))}</div>
  <div class="kpis">{kpi_cells(c["kpis"])}</div>
  <div class="panels">
    <section class="panel wide"><h4>{e(c["wf_h"])}</h4><p class="sub">{e(c["wf_sub"])}</p>{wf}</section>
    <section class="panel"><h4>{e(c["mech_h"])}</h4><p class="sub">{e(c["mech_sub"])}</p><ul class="mech">{mech}</ul></section>
    <section class="panel"><h4>{e(c["team_h"])}</h4><p class="sub">{e(c["team_sub"])}</p>
      <div class="team" role="img" aria-label="{e(c["team_h"])}">{team}</div>
      <div class="legend"><span><i style="background:var(--ink);border-radius:50%"></i>{e(c["team_lead"])}</span></div>
      <div class="roles">{roles}</div></section>
  </div>
</div>'''

    exp = "".join(
        f'<li><span class="exp-years">{e(y)}</span><span><span class="exp-role">{e(r)}</span><br><span class="exp-org">{e(org)}</span></span>'
        f'<span class="exp-what">{e(w)}</span></li>' for y, r, org, w in t["exp"])
    steps = "".join(
        f'<li><span class="n">{i}</span><h3>{e(h)}</h3><p>{e(p)}</p><p class="proof">{e(pr)}</p></li>'
        for i, (h, p, pr) in enumerate(t["steps"], 1))
    tools = "".join(f"<li>{e(x)}</li>" for x in t["tools"])
    l1, l2, l3 = t["c_labels"]

    site = SITE_URL.rstrip("/")
    abs_url = (site + "/" + ("" if ru else "en/")) if site else ""
    og_img = f'<meta property="og:image" content="{site}/assets/og-{lang}.png">' if site else ""
    alt_links = (f'<link rel="alternate" hreflang="ru" href="{site}/"><link rel="alternate" hreflang="en" href="{site}/en/">'
                 f'<link rel="canonical" href="{abs_url}">') if site else ""

    return f'''<!doctype html>
<html lang="{t["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["desc"])}">
<meta property="og:locale" content="{"ru_RU" if ru else "en_US"}">
{og_img}
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#edf2f4">
{alt_links}
<link rel="icon" href="{P}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{P}assets/fonts/geologica-{"cyrillic" if ru else "latin"}-full-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{P}assets/style.css">
<script>document.documentElement.className+=" js"</script>
</head>
<body>
<a class="skip" href="#main">{e(t["skip"])}</a>
<header class="topbar"><div class="wrap">
  <a class="brand" href="#top">{e(t["name"])}</a>
  <nav class="nav" aria-label="{e("Разделы" if ru else "Sections")}">{nav}</nav>
  <a class="lang" href="{lhref}" hreflang="{"en" if ru else "ru"}" title="{e(ltitle)}">{ltext}</a>
</div></header>

<main id="main">
<section class="hero" id="top"><div class="wrap">
  <div class="hero-grid">
    <div>
      <h1>{t["h1"]}</h1>
      <p class="role">{e(t["role"])}</p>
      <p class="lead">{e(t["lead"])}</p>
      <div class="actions">
        <a class="btn btn-solid" href="#cases">{ICON["down"]}{e(t["cta_cases"])}</a>
        <a class="btn btn-line" href="mailto:{t["c_mail"]}">{ICON["mail"]}{e(t["cta_mail"])}</a>
      </div>
    </div>
    <figure class="portrait"><img src="{P}assets/leonid.jpg" width="600" height="600" alt="{e(t["photo_alt"])}"></figure>
  </div>
  <div class="roas">
    <div class="roas-head"><h2>{e(t["roas_h"])}</h2><p>{e(t["roas_src"])}</p></div>
    {"".join(rows)}
    <div class="roas-foot">{foot}</div>
  </div>
</div></section>

<section class="section" id="cases"><div class="wrap">
  <div class="section-head"><h2>{e(t["idx_h"])}</h2><p>{e(t["idx_p"])}</p></div>
  <nav class="index" aria-label="{e(t["idx_h"])}">{idx}</nav>
</div></section>

<section class="section case" id="oncodiag"><div class="wrap">
  {case_top(o)}
  {onco_dash}
</div></section>

<section class="section case" id="dental"><div class="wrap">
  {case_top(d)}
  {dental_dash}
</div></section>

<section class="section case" id="community"><div class="wrap">
  {case_top(c)}
  {comm_dash}
</div></section>

<section class="section" id="experience"><div class="wrap">
  <div class="section-head"><h2>{e(t["exp_h"])}</h2></div>
  <ol class="exp">{exp}</ol>
</div></section>

<section class="section" id="approach" style="padding-top:0"><div class="wrap">
  <div class="section-head"><h2>{e(t["app_h"])}</h2><p>{e(t["app_p"])}</p></div>
  <ol class="steps">{steps}</ol>
  <ul class="tools"><li style="border:0;background:none;padding-left:0"><h3>{e(t["tools_h"])}</h3></li>{tools}</ul>
</div></section>

<section class="section contact" id="contact"><div class="wrap contact-grid">
  <div>
    <h2>{e(t["c_h"])}</h2>
    <p>{e(t["c_p"])}</p>
    <div class="actions">
      <a class="btn btn-solid" href="mailto:{t["c_mail"]}">{ICON["mail"]}{e(t["c_btn_mail"])}</a>
      <a class="btn btn-line" href="https://{t["c_li"]}/" target="_blank" rel="noopener">{ICON["ext"]}{e(t["c_btn_li"])}</a>
    </div>
  </div>
  <dl>
    <dt>{e(l1)}</dt><dd><a href="mailto:{t["c_mail"]}">{e(t["c_mail"])}</a></dd>
    <dt>{e(l2)}</dt><dd><a href="https://{t["c_li"]}/" target="_blank" rel="noopener">{e(t["c_li"])}</a></dd>
    <dt>{e(l3)}</dt><dd>{e(t["c_where"])}</dd>
  </dl>
</div></section>
</main>

<footer class="footer"><div class="wrap">
  <p>© 2026 {e(t["name"])}</p>
  <p>{e(t["foot_note"])}</p>
  <p><a href="{lhref}" hreflang="{"en" if ru else "ru"}">{e(ltitle)}</a></p>
</div></footer>
<script src="{P}assets/app.js" defer></script>
</body>
</html>
'''


def keep_numbers_together(html):
    """'1 800' must never break across lines: swap the plain space for a no-break space."""
    import re
    return re.sub(r"(?<=\d) (?=\d{3}\b)", "\u00a0", html)


if __name__ == "__main__":
    (ROOT / "index.html").write_text(keep_numbers_together(render("ru")), encoding="utf-8")
    (ROOT / "en").mkdir(exist_ok=True)
    (ROOT / "en" / "index.html").write_text(render("en"), encoding="utf-8")
    print("built index.html and en/index.html")
    print({k: D[k] for k in ("c_other", "g_cpp", "g_rpp", "i_rpp")}, f"CTR {D['i_ctr']:.2f}%", f"click->patient {D['i_c2p']:.2f}%", f"CPC ${D['i_cpc']:.2f}")
