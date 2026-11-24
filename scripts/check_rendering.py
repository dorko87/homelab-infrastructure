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
    boxes = [[int(float(node.attrib[k])) for k in ("x", "y", "width", "height")] +
             [node.get("data-tile-bg", "#f1f5f9"), node.get("data-service", "unknown")]
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
<picture><source media="(max-width: 600px)" srcset="__MOBILE__">
<img id="map" alt="Service ecosystem" src="__DESKTOP__"></picture>
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
    const counts = a.boxes.map(([x,y,w,h,bg,label]) => {
      const p = ctx.getImageData(x,y,w,h).data;
      const rgb = bg.match(/[0-9a-f]{2}/gi).map(v => parseInt(v,16));
      let different = 0;
      for(let i=0;i<p.length;i+=4)
        if (Math.abs(p[i]-rgb[0])+Math.abs(p[i+1]-rgb[1])+Math.abs(p[i+2]-rgb[2])>35)
          different++;
      if (different < 30) throw Error(a.name + ': blank logo tile ' + label);
      return different;
    });
    reports.push(a.name + ' ' + im.naturalWidth + 'x' + im.naturalHeight +
      ' rendered' + (counts.length ? '; '+counts.length+' populated tiles' : ''));
  }
  const map = document.getElementById('map');
  await map.decode();
  const narrow = matchMedia('(max-width: 600px)').matches;
  if (map.currentSrc !== assets[narrow ? 1 : 0].uri) throw Error('incorrect responsive source');
  if (document.documentElement.scrollWidth > innerWidth) throw Error('horizontal overflow');
  // Real iframe viewports avoid Chromium's minimum desktop window size.
  for (const width of [320,375,768]) {
    const frame = document.createElement('iframe');
    frame.style.cssText = 'position:absolute;left:-10000px;top:0;border:0;width:'+width+'px;height:2000px';
    const loaded = new Promise(resolve => frame.onload = resolve);
    frame.srcdoc = '<!doctype html><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{margin:0}img{display:block;width:100%;height:auto}</style><picture><source media="(max-width: 600px)" srcset="'+assets[1].uri+'"><img src="'+assets[0].uri+'"></picture>';
    document.body.append(frame);
    await loaded;
    const win = frame.contentWindow, doc = frame.contentDocument, image = doc.querySelector('img');
    // Layout and picture selection may settle after the iframe's load event.
    const expectedUri = assets[width <= 600 ? 1 : 0].uri;
    // Hidden frames can suspend animation frames; poll from the parent instead.
    for (let attempt=0; attempt<20 && image.currentSrc!==expectedUri; attempt++) {
      await new Promise(resolve => setTimeout(resolve,50));
    }
    await image.decode();
    const mediaMatches = win.matchMedia('(max-width: 600px)').matches;
    const selected = image.currentSrc === assets[1].uri ? 'mobile' :
                     image.currentSrc === assets[0].uri ? 'desktop' : 'unknown';
    const expected = width <= 600 ? 'mobile' : 'desktop';
    if (win.innerWidth !== width || doc.documentElement.scrollWidth > width ||
        mediaMatches !== (width <= 600) || selected !== expected) {
      throw Error('responsive iframe '+width+' inner='+win.innerWidth+' scroll='+doc.documentElement.scrollWidth+
                  ' media='+mediaMatches+' selected='+selected+' expected='+expected);
    }
    frame.remove();
    reports.push('viewport '+width+' passed');
  }
  // Verify the actual SMIL timeline, not merely the presence of animation markup.
  const flow = assets.find(a => a.name === 'deployment-flow.svg');
  const bytes = Uint8Array.from(atob(flow.uri.split(',')[1]), v=>v.charCodeAt(0));
  const parsed = new DOMParser().parseFromString(new TextDecoder().decode(bytes),'image/svg+xml');
  const svg = document.importNode(parsed.documentElement,true);
  svg.style.cssText = 'position:absolute;left:-10000px;top:0';
  document.body.append(svg);
  svg.pauseAnimations();
  const moving = svg.querySelector('.moving');
  const stages = Array.from(moving.querySelectorAll('rect')).filter(r=>r.querySelector('animate[attributeName="opacity"]'));
  const progress = Array.from(moving.querySelectorAll('rect')).find(r=>r.querySelector('animate[attributeName="width"]'));
  if (stages.length !== 6 || !progress) throw Error('unexpected animation stages');
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    if (getComputedStyle(moving).display !== 'none') throw Error('reduced motion not respected');
    reports.push('reduced motion passed');
  } else {
    for (let i=0;i<6;i++) {
      svg.setCurrentTime(i*.8+.4);
      await new Promise(requestAnimationFrame);
      const opacity = Number(getComputedStyle(stages[i]).opacity);
      const active = stages.filter(r=>Number(getComputedStyle(r).opacity)>.5).length;
      if (opacity < .9 || active !== 1) throw Error('animation stage '+(i+1)+' opacity='+opacity+' active='+active);
      const expected = 740*(i*.8+.4)/4.8;
      if (Math.abs(progress.width.animVal.value-expected)>3) throw Error('progress timing mismatch at stage '+(i+1));
    }
    svg.setCurrentTime(5);
    await new Promise(requestAnimationFrame);
    if (stages.some(r=>Number(getComputedStyle(r).opacity)>.01) || Math.abs(progress.width.animVal.value-740)>3) throw Error('animation did not finish');
    reports.push('six animation stages and 4.8s completion passed');
  }
  svg.remove();
  document.getElementById('qa').textContent = 'PASS | viewport ' + innerWidth + ' | ' + reports.join(' | ');
})().catch(e => {document.getElementById('qa').textContent = 'FAIL | '+e.message;});
</script></body></html>"""
page = page.replace("__MOBILE__", mobile["uri"]).replace("__DESKTOP__", desktop["uri"])

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
    for name, size in [("desktop", "1280,900"), ("mobile", "420,1100"), ("reduced-motion", "1280,900")]:
        flags = ["--force-prefers-reduced-motion"] if name == "reduced-motion" else []
        result = run(["--window-size=" + size, "--dump-dom"] + flags, tmp / (name+"-profile"), test.as_uri())
        status = re.search(r'<pre id="qa">([^<]*)</pre>', result)
        status = html.unescape(status.group(1)) if status else "Missing QA result"
        print(name + ": " + status, flush=True)
        if not status.startswith("PASS"):
            raise SystemExit(1)
        if (name == "mobile") != (int(re.search(r"viewport (\d+)", status)[1]) <= 600):
            raise SystemExit("Unexpected viewport: " + status)
        if name == "reduced-motion":
            if "reduced motion passed" not in status:
                raise SystemExit("Browser did not apply reduced-motion preference")
            continue
        # Produce a visual review artifact without test diagnostic text.
        preview = tmp / (name+".html")
        selected = mobile if name == "mobile" else desktop
        preview.write_text('<!doctype html><meta charset="utf-8"><style>body{margin:10px;background:#0b1526}img{width:100%;max-width:1000px;display:block;margin:auto}</style><img src="' +
                           selected["uri"] + '">', encoding="utf-8")
        run(["--window-size=" + size, "--screenshot=" + str(OUT / (name + ".png"))],
            tmp / (name+"-screen"), preview.as_uri())
    for a in assets[2:]:
        preview = tmp / (a["name"] + ".html")
        preview.write_text('<!doctype html><meta charset="utf-8"><style>body{margin:10px;background:#0b1526}img{width:100%;max-width:1000px;display:block;margin:auto}</style><img src="' +
                           a["uri"] + '">', encoding="utf-8")
        run(["--window-size=1280,900", "--screenshot=" + str(OUT / (a["name"].replace(".svg", ".png")))],
            tmp / (a["name"]+"-screen"), preview.as_uri())
print("Browser smoke tests passed; screenshots saved to qa-renders.")

