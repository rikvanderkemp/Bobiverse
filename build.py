#!/usr/bin/env python3
"""Rebuild index.html and map.html: generate data/bobiverse.json from src/build_bobiverse.py,
then inline it into src/template.html and src/map.html at the __DATA__ placeholder."""
import json, pathlib, subprocess, sys

root = pathlib.Path(__file__).resolve().parent
data_path = root / "data" / "bobiverse.json"
subprocess.run([sys.executable, str(root / "src" / "build_bobiverse.py"), str(data_path)], check=True)

data = json.loads(data_path.read_text(encoding="utf-8"))
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
for src, out in (("template.html", "index.html"), ("map.html", "map.html")):
    template = (root / "src" / src).read_text(encoding="utf-8")
    assert template.count("__DATA__") == 1, f"{src} must contain exactly one __DATA__"
    (root / out).write_text(template.replace("__DATA__", payload), encoding="utf-8")
    print("wrote", out)
