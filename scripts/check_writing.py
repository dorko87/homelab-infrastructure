"""Check long dashes in original Markdown prose, not quoted or code material."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASH = re.compile("[\u2013\u2014]")
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")

def findings(text):
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not line[match.end():].strip():
                fence = None
            continue
        if fence or line.lstrip().startswith(">"):
            continue
        prose = re.sub(r"`[^`]*`", "", line)
        prose = re.sub(r"https?://[^\s<>\)]+", "", prose)
        if DASH.search(prose):
            yield number

def main():
    errors = []
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT)
        if any(part in {".git", "node_modules", "licenses"} for part in rel.parts):
            continue
        for number in findings(path.read_text(encoding="utf-8")):
            errors.append(f"{rel}:{number}: replace long dash in prose")
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: Markdown prose dash check")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
