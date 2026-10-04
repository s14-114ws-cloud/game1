#!/usr/bin/env python3
"""src/index.template.html を単体で動作する index.html にビルドする。

  {{asset:相対パス}} … Base64 data URI に置換
  {{json:相対パス}}  … JSON ファイルの中身に置換（ファイルが無ければ null）

  python3 tools/build.py
"""
import base64
import json
import mimetypes
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "index.template.html"
OUT = ROOT / "index.html"

MIME = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg",
        ".woff2": "font/woff2", ".svg": "image/svg+xml"}


def data_uri(rel: str) -> str:
    path = ROOT / rel
    mime = MIME.get(path.suffix) or mimetypes.guess_type(path.name)[0]
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def main() -> None:
    html = SRC.read_text(encoding="utf-8")
    cache: dict[str, str] = {}

    def repl(m: re.Match) -> str:
        rel = m.group(1)
        if rel not in cache:
            cache[rel] = data_uri(rel)
        return cache[rel]

    def json_repl(m: re.Match) -> str:
        path = ROOT / m.group(1)
        if not path.exists():
            print(f"note: {m.group(1)} が無いため null を埋め込みます")
            return "null"
        return json.dumps(json.loads(path.read_text(encoding="utf-8")), ensure_ascii=False)

    out = re.sub(r"\{\{asset:([^}]+)\}\}", repl, html)
    out = re.sub(r"\{\{json:([^}]+)\}\}", json_repl, out)
    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB, {len(cache)} assets)")


if __name__ == "__main__":
    main()
