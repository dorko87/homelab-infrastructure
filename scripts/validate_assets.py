"""Validate public portfolio assets and relative links; no third-party dependencies."""
import base64
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG = "http://www.w3.org/2000/svg"
DATA = "data:image/svg+xml;base64,"
errors = []
count = 0

def fail(label, reason):
    errors.append(f"{label}: {reason}")

def validate_svg(raw, label, depth=0):
    global count
    count += 1
    if depth > 2:
        fail(label, "unexpected nested data image")
        return
    if re.search(rb"<!DOCTYPE|<!ENTITY", raw, re.I):
        fail(label, "DTD or entity declaration")
        return
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        fail(label, f"XML parse error: {exc}")
        return
    if root.tag != f"{{{SVG}}}svg":
        fail(label, "root is not SVG")
    try:
        box = [float(v) for v in root.attrib["viewBox"].replace(",", " ").split()]
        if len(box) != 4 or not all(math.isfinite(v) for v in box) or box[2] <= 0 or box[3] <= 0:
            raise ValueError
    except (KeyError, ValueError):
        fail(label, "missing or invalid viewBox")
    ids = set()
    refs = []
    for el in root.iter():
        tag = el.tag.rsplit("}", 1)[-1]
        if tag.lower() in {"script", "foreignobject", "iframe", "object", "embed"}:
            fail(label, f"active element {tag}")
        if "id" in el.attrib:
            ident = el.attrib["id"]
            if ident in ids:
                fail(label, f"duplicate ID {ident}")
            ids.add(ident)
        for attr, value in el.attrib.items():
            name = attr.rsplit("}", 1)[-1]
            if name.lower().startswith("on"):
                fail(label, f"event attribute {name}")
            if name in {"href", "src"}:
                if value.startswith("#"):
                    refs.append(value[1:])
                elif tag == "image" and value.startswith(DATA):
                    try:
                        validate_svg(base64.b64decode(value[len(DATA):], validate=True),
                                     f"{label} / embedded SVG", depth + 1)
                    except (ValueError, TypeError) as exc:
                        fail(label, f"invalid base64: {exc}")
                else:
                    fail(label, f"unexpected external reference: {value[:100]}")
            if re.search(r"url\(\s*['\"]?(?:https?:|//|javascript:|file:)", value, re.I):
                fail(label, "external SVG resource")
            for ref in re.findall(r"url\(\s*['\"]?#([^)'\"]+)['\"]?\s*\)", value):
                refs.append(ref)
        if tag == "style" and el.text:
            refs.extend(re.findall(r"url\(\s*['\"]?#([^)'\"]+)['\"]?\s*\)", el.text))
            if re.search(r"@import|url\(\s*['\"]?(?:https?:|//|javascript:)", el.text, re.I):
                fail(label, "external CSS resource")
    for ref in refs:
        if ref not in ids:
            fail(label, f"unresolved SVG reference #{ref}")

def markdown_anchors(path):
    """Approximate GitHub heading slugs, including duplicate suffixes."""
    text = re.sub(r"```[\s\S]*?```", "", path.read_text(encoding="utf-8"))
    anchors = set(re.findall(r'<(?:a|[a-z]+)\s+[^>]*(?:id|name)="([^"]+)"', text))
    seen = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        anchors.add(slug if not n else f"{slug}-{n}")
    return anchors

def validate_link(file, target):
    target = target.strip().strip("<>")
    if not target:
        return
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return
    path = (file.parent / unquote(parsed.path)).resolve() if parsed.path else file.resolve()
    if not path.is_relative_to(ROOT) or not path.exists():
        fail(file.relative_to(ROOT), f"broken local link: {target}")
    elif parsed.fragment and path.suffix.lower() == ".md" and unquote(parsed.fragment) not in markdown_anchors(path):
        fail(file.relative_to(ROOT), f"broken Markdown anchor: {target}")

def validate_catalog():
    catalog = json.loads((ROOT / "assets/services.json").read_text(encoding="utf-8"))
    expected = {}
    names = set()
    for group in catalog["groups"]:
        for label, icon in group["services"]:
            if label in names:
                fail("service catalog", f"duplicate label {label}")
            names.add(label)
            if icon is not None:
                path = ROOT / "assets/icons" / icon
                if not re.fullmatch(r"[a-z0-9-]+\.svg", icon) or not path.is_file():
                    fail("service catalog", f"invalid local icon {icon}")
                    continue
                expected[label] = path.read_bytes()
    for name in ("service-ecosystem.svg", "service-ecosystem-mobile.svg"):
        file = ROOT / "assets" / name
        if not file.is_file():
            fail(name, "missing generated map")
            continue
        try:
            root = ET.fromstring(file.read_bytes())
        except ET.ParseError:
            continue
        images = root.findall(f".//{{{SVG}}}image")
        actual = {}
        for img in images:
            label = img.get("data-service")
            if label in actual:
                fail(name, f"duplicate embedded service {label}")
            try:
                href = img.get("href", "")
                if not href.startswith(DATA):
                    raise ValueError("not a local embedded SVG")
                actual[label] = base64.b64decode(href[len(DATA):], validate=True)
            except (ValueError, TypeError):
                fail(name, f"invalid embedded service {label}")
        if actual != expected:
            fail(name, "embedded artwork does not match the service catalog")

def main():
    global count
    errors.clear()
    count = 0
    for file in sorted((ROOT / "assets").rglob("*.svg")):
        validate_svg(file.read_bytes(), str(file.relative_to(ROOT)))
    for file in sorted(ROOT.rglob("*.md")):
        if ".git" in file.parts or "node_modules" in file.parts:
            continue
        text = file.read_text(encoding="utf-8")
        text = re.sub(r"```[\s\S]*?```", "", text)
        for target in re.findall(r"\]\(([^)\s]+)\)", text):
            validate_link(file, target)
        for target in re.findall(r'(?:src|srcset|href)="([^"]+)"', text):
            validate_link(file, target)
    validate_catalog()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"OK: {count} SVG documents (including embedded logos), catalog and local Markdown links.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
