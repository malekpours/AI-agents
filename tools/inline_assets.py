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

    # Remove every embedded copy so repeated builds never leave stale assets behind.
    def remove_theme(match):
        block = match.group(0)
        if "قالب مشترک اسلایدها" in block or "/* قالب مشترک اسلایدها" in block:
            return "@@CSS_SLOT@@"
        return block

    def remove_deck_script(match):
        block = match.group(0)
        if "موتور اسلاید" in block or "موتور ساده اسلاید" in block:
            return "@@JS_SLOT@@"
        return block

    html = re.sub(r"<style\b[^>]*>.*?</style>", remove_theme, html, flags=re.S | re.I)
    html = re.sub(r"<script\b[^>]*>.*?</script>", remove_deck_script, html, flags=re.S | re.I)
    html = html.replace('<link rel="stylesheet" href="theme.css">', "@@CSS_SLOT@@")
    html = html.replace('<script src="deck.js"></script>', "@@JS_SLOT@@")

    # ۴) جای‌گذاری نهایی: اولین اسلات CSS را با بلوک کامل پر کن، بقیه حذف
    def fill_single(text, slot, block):
        parts = text.split(slot)
        if len(parts) <= 1:
            return text, False
        out = parts[0] + block + "".join(parts[1:])
        return out, True

    html, css_done = fill_single(html, "@@CSS_SLOT@@", STYLE_BLOCK)
    html = html.replace("@@JS_SLOT@@", "")
    html = re.sub(r"\n{3,}", "\n\n", html)

    # اگر اصلاً اسلاتی نبود (فایل دست‌نخورده)، درج استاندارد
    if not css_done:
        html = html.replace("</head>", STYLE_BLOCK + "\n</head>", 1)
    html = html.replace("</body>", SCRIPT_BLOCK + "\n</body>", 1)

    if html != original:
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        changed.append(name)

print("Updated:", ", ".join(changed) if changed else "(none)")
