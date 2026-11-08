#!/usr/bin/env python3
"""Build the handbook pages.

Each page body lives in src/<page>.html as hand-written bilingual HTML
(<span lang="en">…</span><span lang="zh">…</span>). This script wraps every
body in the shared head, nav and footer and writes <page>.html at the repo
root. Two bodies carry generated parts:

  <!--GALLERY-->   on maps.html, built from GALLERY below
  <!--FILES-->     on archive.html, built from the Discord JSON export

Run from anywhere:  python3 tools/build.py
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA = "archive/discord/media"
THUMBS = "assets/thumbs"

PAGES = [
    ("index",   "Start",    "開始"),
    ("course",  "Course",   "課程"),
    ("skills",  "Skills",   "技術"),
    ("data",    "Data",     "資料來源"),
    ("maps",    "Maps",     "地圖作品"),
    ("project", "Project",  "從地圖到 wiki"),
    ("archive", "Archive",  "原始紀錄"),
]

TITLES = {
    "index":   "GEMS GIS Handbook",
    "course":  "GIS Course · GEMS GIS Handbook",
    "skills":  "QGIS Skills · GEMS GIS Handbook",
    "data":    "Data Sources · GEMS GIS Handbook",
    "maps":    "Maps · GEMS GIS Handbook",
    "project": "From Maps to the Wiki · GEMS GIS Handbook",
    "archive": "Archive · GEMS GIS Handbook",
}


def bi(en, zh):
    return f'<span lang="en">{en}</span><span lang="zh">{zh}</span>'


def shell(page, body):
    links = []
    for key, en, zh in PAGES[1:]:
        on = ' class="on"' if key == page else ""
        links.append(f'<a href="{key}.html"{on}>{bi(en, zh)}</a>')
    nav = "\n    ".join(links)
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLES[page]}</title>
<meta name="description" content="How GEMS Taiwan learned QGIS in summer 2026 and turned it into the ReLEAF Geospatial Analysis page: course, skills, data sources, maps and the full Discord record.">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body data-lang="zh">

<nav class="nav"><div class="nav-in">
  <a class="brand" href="index.html">GEMS GIS</a>
  <div class="nav-links">
    {nav}
  </div>
  <button id="langbtn" class="langbtn" type="button">English</button>
</div></nav>

{body}

<footer><div class="wrap">
  <p>{bi("GEMS Taiwan · GIS training, 2 July to 6 August 2026 · built from the GIS + Data Phys Discord server, the team's Google Docs and the ReLEAF Geospatial Analysis page.",
          "GEMS Taiwan · GIS 培訓，2026 年 7 月 2 日至 8 月 6 日 · 內容整理自 GIS + Data Phys Discord 伺服器、團隊 Google 文件與 ReLEAF Geospatial Analysis 頁面。")}</p>
</div></footer>

<div id="lb"><img alt=""></div>
<script src="assets/js/site.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------- gallery
# (group id, group title en, group title zh, intro en, intro zh, items)
# item: (media file, author, caption en, caption zh)
GALLERY = [
    ("first-map", "First Taiwan map", "第一張台灣地圖",
     "Homework set on 2 July: one raster and four vector layers from the NLSC map server, with a title, north arrow and scale, exported as PDF.",
     "7 月 2 日的作業：從國土測繪中心圖資服務取一個網格圖層加四個向量圖層，加上標題、指北針、比例尺，輸出成 PDF。",
     [("Olivias_7_7QGISHW_compressed-33762e85deed39bf.pdf", "Olivia",
       "Northern Taiwan: agricultural use, soil liquefaction and geologically sensitive areas",
       "北台灣農業使用、土壤液化與地質敏感區")]),
    ("power-plants", "Power plants in China", "中國發電廠分布",
     "In-class exercise on 7 July with world data: renewable and non-renewable power plants, styled by category.",
     "7 月 7 日課堂練習，用全球資料把再生與非再生發電廠依類別上色。",
     [("Screenshot_2026-07-07_at_2.29.19_PM-8cfbaa43bd82f2fd.png", "Dr. Daniel", "Renewable and non-renewable power plants in China", "中國再生與非再生發電廠"),
      ("Screenshot_2026-07-07_at_2.29.13_PM-4ccaea1c66f22e59.png", "Anna", "Power plants in eastern China", "中國東部發電廠"),
      ("Screenshot_2026-07-07_at_2.29.29_PM-1ddde0e2937af9ab.png", "Olivia", "Power plants in eastern China", "中國東部發電廠"),
      ("image-252ff6ad607e4261.png", "Eva", "Power plants in China", "中國發電廠"),
      ("Screen_Shot_2026-07-07_at_2.37.45_PM-3e411b61e2a7464e.png", "Renee", "Power plants in eastern China", "中國東部發電廠")]),
    ("landslides", "Landslides and sensitive areas", "山崩與地質敏感區",
     "Same day, Taiwan data: the Geological Survey's sensitive-area layers on the NLSC basemap, one region per person.",
     "同一天改用台灣資料：地調所地質敏感區圖層疊在國土測繪中心底圖上，每人負責一個區域。",
     [("Landslides_in_the_North_Taipei_Region-6f8ece44c86f44f7.pdf", "Dr. Daniel", "Landslides in the North Taipei region", "台北北區山崩"),
      ("0707_-_Eastern_Taiwan_Landslides_and_Relic-2cba0c7a2d15c9c6.pdf", "Anna", "Eastern Taiwan landslides and relics", "東台灣山崩與古蹟"),
      ("pingtung_county_plain_landslides_and_vulne-1ed75a4449483a84.pdf", "Renee", "Pingtung plain landslides and vulnerable areas", "屏東平原山崩與脆弱地區"),
      ("geographically_sensitive_areas_of_southern-8d3115b2ecaef8ad.pdf", "Olivia", "Geologically sensitive areas, southern Taipei", "台北南區地質敏感區"),
      ("image-7384cdd77b1dd300.png", "Eva", "Landslides in western Taiwan", "西台灣山崩")]),
    ("population", "Population maps", "人口地圖",
     "9 July: each person mapped a country's population with graduated colours.",
     "7 月 9 日：每人選一個國家，用分級色彩畫人口分布。",
     [("Caribbean_Population_2000-f64cb150bc97ecc8.pdf", "Dr. Daniel", "Caribbean population, 2000", "加勒比海人口，2000"),
      ("Japannnn_pop_den-e8b04b48431afe3e.pdf", "Olivia", "Japan population density, 2000", "日本人口密度，2000"),
      ("Population_of_Egypt_in_2010_Along_the_Nile-543e62a89d80c07c.pdf", "Anna", "Egypt population along the Nile, 2010", "尼羅河沿岸埃及人口，2010"),
      ("image-f135bfc7cd8fba9a.png", "Eva", "Australia population, 2000", "澳洲人口，2000"),
      ("Screen_Shot_2026-07-09_at_2.00.51_PM-7b86a893f2d343dd.png", "Renee", "United States and Mexico population, 2010", "美國與墨西哥人口，2010")]),
    ("stations", "Weather stations", "氣象測站",
     "9 July: station coordinates from a CSV turned into points, then joined to 1991 to 2020 climate normals.",
     "7 月 9 日：把 CSV 的測站經緯度轉成點，再接上 1991 至 2020 年氣候平均值。",
     [("Screenshot_2026-07-09_at_3.48.54_PM-86572151131ae453.png", "Dr. Daniel", "CWA weather stations in Taiwan", "台灣氣象署測站"),
      ("image-2d2fbf93bd2bc958.png", "Eva", "Weather stations in Taiwan", "台灣氣象測站"),
      ("Screenshot_2026-07-09_at_3.47.51_PM-f38812eb36151455.png", "Whiteboard", "The plan for the day: CSV layout, the climate variables and the datasets to link", "當天白板：CSV 欄位格式、氣候變數與要連結的資料集")]),
    ("crops", "Crops, temperature and terrain", "作物、溫度與地形",
     "20 to 28 July: the first maps that put two variables on one sheet.",
     "7 月 20 至 28 日：第一批把兩個變數放在同一張圖上的地圖。",
     [("Screenshot_2026-07-20_at_8.34.58_PM-85982571a67363e4.png", "Anna", "Mean temperature 1991 to 2021 by county, with rice yield as proportional circles", "1991 至 2021 年各縣市平均溫度，稻米單位產量以比例圓表示"),
      ("image-70f66439499626b0.png", "Eva", "Crops and landslides", "作物與山崩"),
      ("Screenshot_2026-07-28_at_1.39.36_PM-acdf0482b86a342c.png", "Anna", "Reservoir storage over county temperature", "水庫蓄水率疊加縣市溫度"),
      ("Screenshot_2026-07-28_at_1.51.59_PM-b4b5bd83e98e5e9c.png", "Olivia", "Rice area by county and year, loaded as points", "各縣市逐年稻作面積，以點圖層載入")]),
    ("warming", "Global warming in Taiwan", "台灣暖化",
     "23 July: everyone made the same map from the same brief, which makes this set the best one for comparing design choices.",
     "7 月 23 日：同一份題目、每人各畫一張，最適合拿來比較設計選擇。",
     [("Taiwan_Global_Warming-99d160d3fb3fb960.pdf", "Dr. Daniel", "Global warming in Taiwan", "台灣暖化"),
      ("TaiwanLabelWarming-5cbf346c076d0d64.pdf", "Anna", "Warming in Taiwan, labelled", "台灣暖化（附標籤）"),
      ("warming-e69dfe9fa3668466.pdf", "Olivia", "Warming in Taiwan", "台灣暖化"),
      ("global_warmarmaramarma-f875852d494f0d98.pdf", "Renee", "Warming in Taiwan, version 1", "台灣暖化，第 1 版"),
      ("Global_Warming_oh_no-88fa0a6cf0294025.pdf", "Renee", "Warming in Taiwan, version 2", "台灣暖化，第 2 版"),
      ("Warming_map_taiwan-5d8685ac6ffa4367.pdf", "Eva", "Warming in Taiwan", "台灣暖化")]),
    ("animation", "Warming animation", "暖化動畫",
     "25 to 30 July: five versions of one animated map. The brief: four seconds at most, overlay the difference, let counties appear when their data starts.",
     "7 月 25 至 30 日：同一張動畫地圖的五個版本。要求：最多四秒、疊出差異、縣市在有資料的年份才出現。",
     [("taiwan_warming_speed-3f319ee72eb17184.gif", "Eva", "Version 1", "第 1 版"),
      ("taiwan_warming_speed_v2-8cfca3919ff531cc.gif", "Eva", "Version 2, after class feedback", "第 2 版，依課堂意見修改"),
      ("taiwan_warming_speed_1980-33dc3a051f6a707b.gif", "Eva", "From 1980", "從 1980 年起"),
      ("taiwan_warming_speed_1980-7e41a09e87abbb8c.gif", "Eva", "From 1980, three stations removed", "從 1980 年起，移除三個測站"),
      ("taiwan_warming_choropleth_1980-8306413bf26a8731.gif", "Eva", "Whole counties: blank has too few years, hatched is less precise", "以整個縣市上色：空白是年份太少，斜線是精度較低")]),
    ("farmers", "Farmer age and heat stress", "農民年齡與熱逆境",
     "29 July to 6 August: the demographic layer, and the overlay that became Figure 4 on the wiki.",
     "7 月 29 日至 8 月 6 日：人口結構圖層，以及後來成為 wiki 圖 4 的疊圖。",
     [("Average_age_of_farmers_in_Taiwan-ce4cb6d6cce9ea2c.pdf", "Renee", "Average age of farmers by county", "各縣市農民平均年齡"),
      ("age_plus_stress-46c87e2ac1b4f2b8.pdf", "Renee", "Average farmer age against temperature increase, 1999 to 2020", "農民平均年齡對比 1999 至 2020 年升溫幅度")]),
    ("boards", "Whiteboards", "白板",
     "The class planned on whiteboards. These photos are the only record of several assignments.",
     "課堂規劃都寫在白板上，好幾份作業只有這些照片留下紀錄。",
     [("IMG_8216-3425d5fcffe2fc50.jpg", "2 July", "Homework: tutorials, then a Taiwan map with one raster and four vectors, exported with your name", "作業：先做教學，再做一張一網格四向量的台灣地圖，署名輸出"),
      ("IMG_7744-c87934090e7aef1f.jpg", "7 July", "Storyline structure: farmers 30%, climate change 30%, biomanufacturing 40%", "故事線架構：農民 30%、氣候變遷 30%、生物製造 40%"),
      ("IMG_2984-e6e77ddeafd97f2c.jpg", "23 July", "Homework: maps, pick one map to own, give Claude your CSV for an animated GIF, edit the text with the field trip", "作業：地圖、每人認領一張、把 CSV 交給 Claude 做動畫 GIF、把校外考察寫進文字"),
      ("IMG_7809-439521366e1f0030.jpg", "30 July", "Word of the day: urgent. A version 1 of every map", "今日關鍵字：急。每張圖都要有第 1 版"),
      ("Screenshot_2026-07-30_at_2.53.50_PM-e86cc13070b263d1.png", "30 July", "The same list with the weekend's work: biotic stress from heat and humidity", "同一份清單，加上週末工作：高溫加濕度造成的生物逆境")]),
]


def is_img(f):
    return f.lower().rsplit(".", 1)[-1] in ("png", "jpg", "jpeg", "gif", "webp")


def thumb(f):
    return f"{THUMBS}/{os.path.splitext(f)[0]}.webp"


def gallery_html():
    out = ['<div class="subnav"><div class="wrap wide"><div class="toc">']
    for gid, en, zh, *_ in GALLERY:
        out.append(f'<a href="#{gid}">{bi(en, zh)}</a>')
    out.append("</div></div></div>")
    for gid, en, zh, ien, izh, items in GALLERY:
        out.append(f'<section id="{gid}" class="tight"><div class="wrap wide">')
        out.append(f"<h2>{bi(en, zh)}</h2>")
        out.append(f'<p class="sub">{bi(ien, izh)}</p>')
        out.append('<div class="gal">')
        for f, by, cen, czh in items:
            path = f"{MEDIA}/{f}"
            assert os.path.exists(os.path.join(ROOT, path)), path
            assert os.path.exists(os.path.join(ROOT, thumb(f))), thumb(f)
            if is_img(f):
                a = f'<a class="frame" href="{path}" data-lb>'
            else:
                a = f'<a class="frame pdf" href="{path}" target="_blank" rel="noopener">'
            alt = html.escape(cen)
            out.append(
                f'<figure class="map">{a}<img src="{thumb(f)}" alt="{alt}" loading="lazy"></a>'
                f'<figcaption>{bi(cen, czh)}<span class="by">{html.escape(by)}'
                f'{"" if is_img(f) else " · PDF"}</span></figcaption></figure>')
        out.append("</div></div></section>")
    return "\n".join(out)


# ---------------------------------------------------------------- archive
CHANNELS = [
    ("general-announcements", "#general-announcements"),
    ("chat", "#chat"),
    ("milestones", "#milestones"),
    ("important-documents--preliminary", "important-documents › Preliminary"),
    ("important-documents--marburg-case-study", "important-documents › Marburg Case Study"),
    ("important-documents--doc", "important-documents › DOC"),
]

KIND = {
    "pdf": ("Map or document", "地圖或文件"),
    "png": ("Image", "圖片"), "jpg": ("Photo", "照片"), "gif": ("Animation", "動畫"),
    "csv": ("Table", "表格"), "zip": ("Shapefile bundle", "Shapefile 壓縮檔"),
    "qgz": ("QGIS project", "QGIS 專案"), "svg": ("Image", "圖片"), "mp4": ("Video", "影片"),
    "json": ("Data", "資料"),
}


def files_html():
    rows_c = []
    rows_f = []
    for slug, label in CHANNELS:
        d = json.load(open(os.path.join(ROOT, "archive/discord/json", slug + ".json"), encoding="utf-8"))
        msgs = [m for m in d["messages"] if m["type"] != "GuildMemberJoin"]
        n_att = sum(len(m["attachments"]) for m in msgs)
        first = msgs[0]["timestamp"][:10] if msgs else ""
        last = msgs[-1]["timestamp"][:10] if msgs else ""
        rows_c.append(
            f'<tr><td><a href="archive/discord/html/{slug}.html">{html.escape(label)}</a></td>'
            f'<td>{len(msgs)}</td><td>{n_att}</td><td>{first} → {last}</td>'
            f'<td><a href="archive/discord/json/{slug}.json">JSON</a></td></tr>')
        for m in msgs:
            for a in m["attachments"]:
                fn = a["url"].split("/")[-1]
                ext = fn.rsplit(".", 1)[-1].lower()
                ken, kzh = KIND.get(ext, ("File", "檔案"))
                kb = a["fileSizeBytes"] // 1024
                size = f"{kb/1024:.1f} MB" if kb >= 1024 else f"{kb} KB"
                rows_f.append(
                    f'<tr><td>{m["timestamp"][:10]}</td>'
                    f'<td><a href="{MEDIA}/{fn}">{html.escape(a["fileName"])}</a></td>'
                    f'<td>{bi(ken, kzh)}</td><td>{html.escape(m["author"].get("nickname") or m["author"]["name"])}</td>'
                    f'<td>{size}</td></tr>')
    rows_f.sort()
    c = ('<table class="t"><thead><tr><th>' + bi("Channel", "頻道") + "</th><th>" + bi("Messages", "訊息")
         + "</th><th>" + bi("Files", "檔案") + "</th><th>" + bi("Dates", "日期") + "</th><th></th></tr></thead><tbody>"
         + "".join(rows_c) + "</tbody></table>")
    f = ('<table class="t"><thead><tr><th>' + bi("Date", "日期") + "</th><th>" + bi("File", "檔案")
         + "</th><th>" + bi("Kind", "類型") + "</th><th>" + bi("Posted by", "上傳者") + "</th><th>"
         + bi("Size", "大小") + "</th></tr></thead><tbody>" + "".join(rows_f) + "</tbody></table>")
    return c, f


def main():
    chan, files = files_html()
    for key, *_ in PAGES:
        src = open(os.path.join(ROOT, "src", key + ".html"), encoding="utf-8").read()
        src = src.replace("<!--GALLERY-->", gallery_html())
        src = src.replace("<!--CHANNELS-->", chan).replace("<!--FILES-->", files)
        open(os.path.join(ROOT, key + ".html"), "w", encoding="utf-8").write(shell(key, src))
        print("wrote", key + ".html")


if __name__ == "__main__":
    main()
