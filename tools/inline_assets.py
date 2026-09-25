# -*- coding: utf-8 -*-
"""جاسازی theme.css و deck.js داخل فایل‌های اسلاید تا هر فایل کاملاً مستقل (آفلاین) باشد."""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLIDES = os.path.join(ROOT, "slides")

with io.open(os.path.join(SLIDES, "theme.css"), encoding="utf-8") as f:
    CSS = f.read()
with io.open(os.path.join(SLIDES, "deck.js"), encoding="utf-8") as f:
    JS = f.read()

STYLE_BLOCK = "<style>\n" + CSS + "\n</style>"
SCRIPT_BLOCK = "<script>\n" + JS + "\n</script>"

# فقط فایل‌های دک (index.html بدون deck.js است؛ هرگز دست نمی‌خورد)
target_files = [f for f in os.listdir(SLIDES)
                if f.endswith(".html") and f != "index.html"
                and not f.startswith("_")]

changed = []
for name in sorted(target_files):
    path = os.path.join(SLIDES, name)
    with io.open(path, encoding="utf-8") as f:
        html = f.read()
    original = html

    # ۱) حذف هر نسخه‌ای از قالب/اسکریپت درج‌شده‌ی قبلی
    html = html.replace(STYLE_BLOCK, "@@CSS_SLOT@@")
    html = html.replace(SCRIPT_BLOCK, "@@JS_SLOT@@")

    # ۲) حذف ارجاع به فایل خارجی
    html = html.replace('<link rel="stylesheet" href="theme.css">', "@@CSS_SLOT@@")
    html = html.replace('<script src="deck.js"></script>', "@@JS_SLOT@@")

    # ۳) قطعه‌های خراب احتمالی از تلاش قبلی — پاک‌سازی
    html = re.sub(r"<style>\s*/\* ===== قالب مشترک.*?</style>", "@@CSS_SLOT@@", html, flags=re.S)
    html = re.sub(r"<script>\s*/\* موتور اسلاید.*?</script>\s*<script>\s*/\* موتور اسلاید.*?</script>",
                  "@@JS_SLOT@@", html, flags=re.S)

    # ۴) جای‌گذاری نهایی: اولین اسلات CSS را با بلوک کامل پر کن، بقیه حذف
    def fill_single(text, slot, block):
        parts = text.split(slot)
        if len(parts) <= 1:
            return text, False
        out = parts[0] + block + "".join(parts[1:])
        return out, True

    html, css_done = fill_single(html, "@@CSS_SLOT@@", STYLE_BLOCK)
    html, js_done = fill_single(html, "@@JS_SLOT@@", SCRIPT_BLOCK)

    # اگر اصلاً اسلاتی نبود (فایل دست‌نخورده)، درج استاندارد
    if not css_done:
        html = html.replace("</head>", STYLE_BLOCK + "\n</head>", 1)
    if not js_done:
        html = html.replace("</body>", SCRIPT_BLOCK + "\n</body>", 1)

    if html != original:
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        changed.append(name)

print("Updated:", ", ".join(changed) if changed else "(none)")
