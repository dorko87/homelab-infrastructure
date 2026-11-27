"""Render Mermaid fenced blocks with a pinned CLI and system Chromium."""
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
browser = next((shutil.which(n) for n in ("google-chrome", "chromium", "chromium-browser") if shutil.which(n)), None)
if not browser:
    raise SystemExit("Chromium-compatible browser required")
blocks = []
for doc in sorted(ROOT.rglob("*.md")):
    if ".git" in doc.parts or "node_modules" in doc.parts:
        continue
    for i, diagram in enumerate(re.findall(r"^```mermaid\s*\n(.*?)^```\s*$", doc.read_text(encoding="utf-8"), re.M | re.S), 1):
        blocks.append((str(doc.relative_to(ROOT)), i, diagram))
if not blocks:
    raise SystemExit("No Mermaid diagrams found")
review_dir = ROOT / "qa-mermaid"
review_dir.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    config = tmp / "puppeteer.json"
    config.write_text(json.dumps({"executablePath": browser, "args": ["--no-sandbox", "--disable-dev-shm-usage"]}))
    # One invocation per diagram gives a precise location on failure.
    for n, (path, i, diagram) in enumerate(blocks):
        source = tmp / f"diagram-{n}.mmd"
        output = review_dir / f"{path.replace(chr(47), chr(95) * 2)}-{i}.png"
        source.write_text(diagram, encoding="utf-8")
        print(f"Rendering {path}, diagram {i}", flush=True)
        subprocess.run(["npx", "--yes", "--package=@mermaid-js/mermaid-cli@11.4.2",
                        "mmdc", "-i", str(source), "-o", str(output), "-p", str(config)],
                       cwd=tmp, check=True, timeout=180)
        if not output.is_file() or not output.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
            raise SystemExit(f"Missing render: {path}, diagram {i}")
print(f"PASS: {len(blocks)} Mermaid diagrams rendered.")
