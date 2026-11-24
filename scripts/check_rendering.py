"""Headless Chromium smoke test for the public diagrams and embedded logos."""
import base64
import html
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "qa-renders"
OUT.mkdir(exist_ok=True)
SVG = "{http://www.w3.org/2000/svg}"
BROWSER = next((shutil.which(name) for name in
                ("google-chrome", "chromium", "chromium-browser")
                if shutil.which(name)), None)
if not BROWSER:
    raise SystemExit("Chromium-compatible browser not installed")

def asset(name):
    path = ROOT / "assets" / name
    raw = path.read_bytes()
    root = ET.fromstring(raw)
    boxes = [[int(float(node.attrib[k])) for k in ("x", "y", "width", "height")]
             for node in root.iter(SVG + "image")]
    return {"name": name, "uri": "data:image/svg+xml;base64," +
            base64.b64encode(raw).decode("ascii"), "boxes": boxes}

desktop = asset("service-ecosystem.svg")
mobile = asset("service-ecosystem-mobile.svg")
assets = [desktop, mobile] + [asset(n) for n in
    ("hero.svg", "platform-layers.svg", "deployment-flow.svg", "recovery-map.svg")]
payload = json.dumps(assets)
page = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{margin:12px;background:#0b1526;color:white}
main{max-width:1000px;margin:auto}img{max-width:100%;height:auto;display:block}
pre{white-space:pre-wrap;font-size:12px}</style></head><body><main>
<picture><source media="(max-width: 600px)" srcset="""" + mobile["uri"] + """">
<img id="map" alt="Service ecosystem" src="""" + desktop["uri"] + """"></picture>
<pre id="qa">PENDING</pre></main><script>
const assets = """ + payload + """;
(async () => {
  const reports = [];
  for (const a of assets) {
    const im = new Image();
    im.src = a.uri;
    await im.decode();
    if (!im.naturalWidth || !im.naturalHeight) throw Error(a.name + ': empty image');
    const canvas = document.createElement('canvas');
    canvas.width = im.naturalWidth; canvas.height = im.naturalHeight;
    const ctx = canvas.getContext('2d', {willReadFrequently:true});
    ctx.drawImage(im, 0, 0);
    const counts = a.boxes.map(([x,y,w,h]) => {
      const p = ctx.getImageData(x,y,w,h).data;
      let different = 0;
      for(let i=0;i<p.length;i+=4)
        if (Math.abs(p[i]-241)+Math.abs(p[i+1]-245)+Math.abs(p[i+2]-249)>35)
          different++;
      return different;
    });
    if (counts.some(n => n < 30)) throw Error(a.name + ': blank logo tile ' + counts);
    reports.push(a.name + ' ' + im.naturalWidth + 'x' + im.naturalHeight +
      ' rendered' + (counts.length ? '; '+counts.length+' populated tiles' : ''));
  }
  const map = document.getElementById('map');
  await map.decode();
  const narrow = matchMedia('(max-width: 600px)').matches;
  if (map.currentSrc !== assets[narrow ? 1 : 0].uri) throw Error('incorrect responsive source');
  if (document.documentElement.scrollWidth > innerWidth) throw Error('horizontal overflow');
  document.getElementById('qa').textContent = 'PASS | viewport ' + innerWidth + ' | ' + reports.join(' | ');
})().catch(e => {document.getElementById('qa').textContent = 'FAIL | '+e.message;});
</script></body></html>"""

def run(args, profile, url):
    command = [BROWSER, "--headless", "--no-sandbox", "--disable-dev-shm-usage",
               "--disable-gpu", "--no-first-run", "--no-default-browser-check",
               "--user-data-dir=" + str(profile), "--virtual-time-budget=12000"] + args + [url]
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise RuntimeError(result.stderr[-2000:])
    return result.stdout

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    test = tmp / "render.html"
    test.write_text(page, encoding="utf-8")
    for name, size in [("desktop", "1280,900"), ("mobile", "420,1100")]:
        result = run(["--window-size=" + size, "--dump-dom"], tmp / (name+"-profile"), test.as_uri())
        status = re.search(r'<pre id="qa">([^<]*)</pre>', result)
        status = html.unescape(status.group(1)) if status else "Missing QA result"
        print(name + ": " + status, flush=True)
        if not status.startswith("PASS"):
            raise SystemExit(1)
        if (name == "mobile") != (int(re.search(r"viewport (\d+)", status)[1]) <= 600):
            raise SystemExit("Unexpected viewport: " + status)
        # Produce a visual review artifact without test diagnostic text.
        preview = tmp / (name+".html")
        selected = mobile if name == "mobile" else desktop
        preview.write_text('<!doctype html><meta charset="utf-8"><style>body{margin:10px;background:#0b1526}img{width:100%;max-width:1000px;display:block;margin:auto}</style><img src="' +
                           selected["uri"] + '">', encoding="utf-8")
        run(["--window-size=" + size, "--screenshot=" + str(OUT / (name + ".png"))],
            tmp / (name+"-screen"), preview.as_uri())
print("Browser smoke tests passed; screenshots saved to qa-renders.")
