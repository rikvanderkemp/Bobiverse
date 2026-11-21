#!/usr/bin/env python3
"""Rebuild index.html: generate data/bobiverse.json from src/build_bobiverse.py,
then inline it into src/template.html at the __DATA__ placeholder."""
import json, pathlib, subprocess, sys

root = pathlib.Path(__file__).resolve().parent
data_path = root / "data" / "bobiverse.json"
subprocess.run([sys.executable, str(root / "src" / "build_bobiverse.py"), str(data_path)], check=True)

data = json.loads(data_path.read_text(encoding="utf-8"))
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
template = (root / "src" / "template.html").read_text(encoding="utf-8")
assert template.count("__DATA__") == 1, "template must contain exactly one __DATA__"
(root / "index.html").write_text(template.replace("__DATA__", payload), encoding="utf-8")
print("wrote index.html")
