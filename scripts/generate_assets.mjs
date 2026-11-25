// Rebuild the public ecosystem graphics from one catalog. No dependencies.
import {readFileSync, writeFileSync} from "node:fs";
import {fileURLToPath} from "node:url";
import {join} from "node:path";
const root=fileURLToPath(new URL("../",import.meta.url));
function base64(s) { return Buffer.from(s, 'utf8').toString('base64'); }
function render(catalog,readIcon,mobile) {
  const esc=s=>s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/"/g,"&quot;");
  const W=mobile?500:1000,row=180,top=100,cardW=mobile?460:464,cardH=164,rows=Math.ceil(catalog.groups.length/(mobile?1:2)),H=top+rows*row+30;
  const cards=catalog.groups.map(({name,color,purpose,services},i)=>{
    if(!services.length||services.length>4||!/^#[0-9a-fA-F]{6}$/.test(color))throw Error("Invalid catalog group");
    const x=mobile?20:i%2===0?24:512,y=top+Math.floor(i/(mobile?1:2))*row;
    const inner=name==="AI-assisted operations" && services.length===1 && services[0][0]==="AI agents" ? `<g><rect x="${x+20}" y="${y+59}" width="62" height="62" rx="12" fill="#292547"/><g stroke="#c4b5fd" stroke-width="2.5" fill="none"><rect x="${x+31}" y="${y+77}" width="40" height="29" rx="7"/><path d="M${x+51} ${y+77}v-8"/><circle cx="${x+41}" cy="${y+91}" r="3"/><circle cx="${x+61}" cy="${y+91}" r="3"/></g><text x="${x+96}" y="${y+84}" font-size="18" font-weight="600" fill="#f8fafc">AI agents</text><text x="${x+96}" y="${y+107}" font-size="15" fill="#cbd5e1">Independent operational experiments</text></g>` : services.map(([label,file],j)=>{
      const cx=x+(cardW/services.length)*(j+.5);
      const bg=label==="Uptime Kuma"?"#24374a":"#f1f5f9";
      const size=label==="Docker"?54:48;
      const tx=`<text x="${cx}" y="${y+146}" text-anchor="middle" font-size="${mobile?(label.length>10?15:17):14}" fill="#e2e8f0">${esc(label)}</text>`;
      let icon;
      if(file){if(!/^[a-z0-9-]+\.svg$/.test(file))throw Error("Invalid icon filename");
        const raw=readIcon(file);if(!raw.includes("<svg")||/<script\b|<foreignObject\b|<!DOCTYPE/i.test(raw))throw Error("Invalid icon: "+file);icon=`<image data-service="${esc(label)}" data-tile-bg="${bg}" href="data:image/svg+xml;base64,${base64(raw)}" x="${cx-size/2}" y="${y+89-size/2}" width="${size}" height="${size}" preserveAspectRatio="xMidYMid meet"/>`;
      } else if(label==="AI agents"){icon=`<g stroke="#475569" stroke-width="2.5" fill="none"><rect x="${cx-20}" y="${y+72}" width="40" height="32" rx="7"/><path d="M${cx} ${y+72}v-8"/><circle cx="${cx-10}" cy="${y+88}" r="3"/><circle cx="${cx+10}" cy="${y+88}" r="3"/></g>`;
      } else {icon=`<g stroke="#475569" fill="none" stroke-width="2.4"><ellipse cx="${cx}" cy="${y+75}" rx="15" ry="6"/><path d="M${cx-15} ${y+75}v22a15 6 0 0 0 30 0v-22M${cx-15} ${y+86}a15 6 0 0 0 30 0"/></g>`;}
      return `<rect x="${cx-31}" y="${y+58}" width="62" height="62" rx="12" fill="${bg}"/>${icon}${tx}`;
    }).join("");
    return `<g><rect x="${x}" y="${y}" width="${cardW}" height="${cardH}" rx="14" fill="#142238" stroke="${color}" stroke-opacity=".8"/><text x="${x+18}" y="${y+25}" fill="${color}" font-size="${mobile?18:16}" font-weight="700" letter-spacing=".5">${esc(name.toUpperCase())}</text><text x="${x+18}" y="${y+44}" fill="#cbd5e1" font-size="${mobile?14:12}">${esc(purpose)}</text>${inner}</g>`;
  }).join("");
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-labelledby="map-title map-desc"><title id="map-title">Homelab service ecosystem</title><desc id="map-desc">Selected technologies grouped by logical responsibilities, not physical topology or live inventory.</desc><rect width="${W}" height="${H}" rx="20" fill="#0b1526"/><g font-family="system-ui,Segoe UI,sans-serif"><text x="24" y="42" fill="#f8fafc" font-size="${mobile?24:28}" font-weight="700">${mobile?"Homelab service ecosystem":"One environment. Many responsibilities."}</text><text x="24" y="71" fill="#94a3b8" font-size="15">Selected services · independent engineering</text>${cards}<text x="24" y="${H-17}" fill="#94a3b8" font-size="12">Logical groups · not live status · generic Restic / AI symbols</text></g></svg>\n`;}
const catalog=JSON.parse(readFileSync(join(root,"assets/services.json"),"utf8"));
const readIcon=n=>readFileSync(join(root,"assets/icons",n),"utf8");
for(const [file,mobile] of [["service-ecosystem.svg",false],["service-ecosystem-mobile.svg",true]]){
  const path=join(root,"assets",file); const output=render(catalog,readIcon,mobile);
  if(process.argv.includes("--check")){if(readFileSync(path,"utf8")!==output){console.error(file+" is stale; regenerate assets");process.exitCode=1;}}
  else writeFileSync(path,output);
}
