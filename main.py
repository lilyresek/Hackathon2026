#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


## ODMAP v2 — Pronunciation Button + Similar Brand Names + Enhanced Info Card

Adds Web Speech API pronunciation, similar brand-name grouping, and polished baseball-card sidebar to the existing D3.js graph.


# In[4]:


import os
os.makedirs("./outputs", exist_ok=True)

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>ODMAP — Drug Interaction Network</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#0d1117;color:#e6edf3;font-family:'Segoe UI',sans-serif;display:flex;flex-direction:column;height:100vh;overflow:hidden}
  #header{background:#161b22;border-bottom:1px solid #30363d;padding:10px 20px;display:flex;align-items:center;gap:16px;flex-shrink:0;flex-wrap:wrap}
  #header h1{font-size:1.2rem;color:#58a6ff;letter-spacing:2px;font-weight:700}
  #search-area{display:flex;gap:8px;align-items:center;margin-left:auto}
  #search-area input{background:#21262d;border:1px solid #30363d;border-radius:6px;color:#e6edf3;padding:6px 12px;font-size:.85rem;width:150px}
  #search-area input:focus{outline:none;border-color:#58a6ff}
  #go-btn{background:#238636;border:none;color:#fff;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:.85rem;font-weight:600}
  #go-btn:hover{background:#2ea043}
  #search-result{position:fixed;top:56px;right:20px;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px 18px;z-index:999;display:none;max-width:320px;font-size:.85rem;line-height:1.6}
  #search-result h3{color:#58a6ff;margin-bottom:6px}
  #search-result .close-btn{float:right;cursor:pointer;color:#8b949e;font-size:1rem}
  #history-bar{background:#0d1117;border-bottom:1px solid #21262d;padding:6px 16px;display:flex;gap:8px;align-items:center;overflow-x:auto;flex-shrink:0;min-height:36px}
  #history-bar span.hist-label{font-size:.75rem;color:#8b949e;flex-shrink:0}
  .hist-chip{background:#21262d;border:1px solid #30363d;border-radius:12px;padding:3px 10px;font-size:.75rem;cursor:pointer;color:#58a6ff;white-space:nowrap}
  .hist-chip:hover{background:#30363d}
  #main{display:flex;flex:1;overflow:hidden}
  #graph-area{flex:1;position:relative}
  svg{width:100%;height:100%}

  /* ── INFO PANEL ── */
  #info-panel{width:300px;background:#161b22;border-left:1px solid #30363d;overflow-y:auto;padding:0;flex-shrink:0;display:none;flex-direction:column}
  .card-header{background:#1c2128;padding:16px 18px 12px;border-bottom:1px solid #30363d}
  .card-brand{font-size:1.1rem;font-weight:700;color:#e6edf3;display:flex;align-items:center;gap:8px}
  .card-class{font-size:.78rem;color:#8b949e;margin-top:3px}
  .pronunc-btn{background:none;border:1px solid #30363d;border-radius:6px;color:#58a6ff;cursor:pointer;padding:3px 8px;font-size:.78rem;display:inline-flex;align-items:center;gap:4px;white-space:nowrap}
  .pronunc-btn:hover{background:#21262d}
  .card-body{padding:14px 18px;flex:1}
  .card-section-title{font-size:.7rem;color:#8b949e;text-transform:uppercase;letter-spacing:1px;margin-top:14px;margin-bottom:4px;font-weight:600}
  .card-val{font-size:.85rem;color:#e6edf3;line-height:1.5}
  .similar-chip{display:inline-block;background:#21262d;border:1px solid #30363d;border-radius:10px;padding:2px 9px;font-size:.75rem;color:#79c0ff;margin:2px 2px 2px 0;cursor:pointer}
  .similar-chip:hover{background:#30363d}
  .icard{background:#21262d;border-radius:6px;padding:8px 10px;margin-top:8px;border-left:3px solid #58a6ff}
  .icard .ic-title{font-size:.8rem;font-weight:600;color:#e6edf3;display:flex;align-items:center;gap:6px}
  .ic-badge{font-size:.68rem;padding:1px 6px;border-radius:8px;font-weight:700;text-transform:uppercase}
  .ic-badge.severe{background:#f851491a;color:#f85149;border:1px solid #f8514940}
  .ic-badge.moderate{background:#e3a4001a;color:#e3a400;border:1px solid #e3a40040}
  .ic-badge.mild{background:#3fb9501a;color:#3fb950;border:1px solid #3fb95040}
  .icard .ic-sub{font-size:.75rem;color:#8b949e;margin-top:4px;line-height:1.4}
  .icard.severe{border-left-color:#f85149}
  .icard.moderate{border-left-color:#e3a400}
  .icard.mild{border-left-color:#3fb950}
  .close-panel-btn{width:100%;background:#21262d;border:none;border-top:1px solid #30363d;color:#8b949e;padding:8px;cursor:pointer;font-size:.8rem;margin-top:8px}
  .close-panel-btn:hover{background:#30363d;color:#e6edf3}

  /* ── LEGEND ── */
  #legend{position:absolute;bottom:14px;left:14px;background:#161b22cc;border:1px solid #30363d;border-radius:8px;padding:10px 14px;font-size:.73rem;line-height:1.9;backdrop-filter:blur(4px)}
  #legend .leg-title{color:#8b949e;margin-bottom:2px;font-weight:600;font-size:.72rem;text-transform:uppercase;letter-spacing:.8px}
  .leg-row{display:flex;align-items:center;gap:8px;color:#c9d1d9}

  #tooltip{position:fixed;background:#21262d;border:1px solid #30363d;border-radius:6px;padding:7px 11px;font-size:.78rem;pointer-events:none;display:none;z-index:800;max-width:240px;line-height:1.5}
</style>
</head>
<body>

<div id="header">
  <h1>⬡ ODMAP</h1>
  <div style="font-size:.78rem;color:#8b949e">Drug Interaction Network</div>
  <div id="search-area">
    <input id="drug1" placeholder="Drug 1"/>
    <input id="drug2" placeholder="Drug 2"/>
    <button id="go-btn" onclick="searchInteraction()">Go</button>
  </div>
</div>

<div id="history-bar">
  <span class="hist-label">History:</span>
</div>

<div id="search-result">
  <span class="close-btn" onclick="this.parentElement.style.display='none'">✕</span>
  <h3 id="sr-title"></h3>
  <div id="sr-body"></div>
</div>

<div id="main">
  <div id="graph-area">
    <svg id="svg"></svg>
    <div id="legend">
      <div class="leg-title">Severity</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#f85149" stroke-width="2.5"/></svg> Severe</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#e3a400" stroke-width="2" stroke-dasharray="6,3"/></svg> Moderate</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#3fb950" stroke-width="1.5" stroke-dasharray="2,3"/></svg> Mild</div>
      <div class="leg-title" style="margin-top:8px">Interaction Type</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#8b949e" stroke-width="2"/></svg> Hematologic</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#8b949e" stroke-width="2" stroke-dasharray="8,4"/></svg> Metabolic</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#8b949e" stroke-width="2" stroke-dasharray="4,2"/></svg> Cardiovascular</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#8b949e" stroke-width="2" stroke-dasharray="2,5"/></svg> Neurological</div>
    </div>
  </div>
  <div id="info-panel"></div>
</div>
<div id="tooltip"></div>

<script>
// ─── DATA ────────────────────────────────────────────────────────────────────
// pronunciation: IPA-friendly string fed to Web Speech API
// similar: brand names that share the same active ingredient
const ALL_DRUGS = {
  "Warfarin":    {ingredient:"Warfarin sodium",       pronounce:"WAR-fuh-rin",  cls:"Anticoagulant",       similar:["Coumadin","Jantoven"],                    desc:"Prevents blood clots by inhibiting Vitamin K-dependent clotting factors."},
  "Aspirin":     {ingredient:"Acetylsalicylic acid",  pronounce:"AS-pir-in",    cls:"NSAID / Antiplatelet", similar:["Bayer","Bufferin","Ecotrin"],             desc:"Reduces pain, fever, and platelet aggregation."},
  "Lipitor":     {ingredient:"Atorvastatin",          pronounce:"LIP-ih-tor",   cls:"Statin",              similar:["Torvast"],                                desc:"Lowers LDL cholesterol by inhibiting HMG-CoA reductase."},
  "Paxil":       {ingredient:"Paroxetine",            pronounce:"PAX-il",       cls:"SSRI",                similar:["Pexeva","Brisdelle"],                      desc:"Selective serotonin reuptake inhibitor for depression and anxiety."},
  "Prozac":      {ingredient:"Fluoxetine",            pronounce:"PRO-zak",      cls:"SSRI",                similar:["Sarafem","Rapiflux"],                      desc:"Increases serotonin levels; treats depression and OCD."},
  "Xanax":       {ingredient:"Alprazolam",            pronounce:"ZAN-ax",       cls:"Benzodiazepine",      similar:["Niravam","Alprazolam ER"],                 desc:"Short-term management of anxiety disorders."},
  "Metformin":   {ingredient:"Metformin HCl",         pronounce:"met-FOR-min",  cls:"Biguanide",           similar:["Glucophage","Fortamet","Glumetza"],        desc:"First-line treatment for type 2 diabetes; reduces hepatic glucose output."},
  "Lisinopril":  {ingredient:"Lisinopril",            pronounce:"lye-SIN-oh-pril", cls:"ACE Inhibitor",   similar:["Zestril","Prinivil","Qbrelis"],            desc:"Treats high blood pressure and heart failure."},
  "Ibuprofen":   {ingredient:"Ibuprofen",             pronounce:"eye-byoo-PRO-fen", cls:"NSAID",          similar:["Advil","Motrin","Nuprin"],                 desc:"Reduces inflammation, pain, and fever."},
  "Amoxicillin": {ingredient:"Amoxicillin trihydrate",pronounce:"am-ox-ih-SIL-in", cls:"Antibiotic",     similar:["Amoxil","Trimox","Moxatag"],               desc:"Broad-spectrum penicillin antibiotic."},
  "Digoxin":     {ingredient:"Digoxin",               pronounce:"dih-JOX-in",   cls:"Cardiac Glycoside",  similar:["Lanoxin","Digitek"],                       desc:"Strengthens heart contractions; treats heart failure and AFib."},
  "Zoloft":      {ingredient:"Sertraline",            pronounce:"ZO-loft",      cls:"SSRI",               similar:["Lustral"],                                 desc:"Treats depression, panic disorder, and PTSD."},
};

const ALL_INTERACTIONS = [
  {source:"Warfarin",   target:"Aspirin",    severity:"severe",   type:"Hematologic",    desc:"Concurrent use significantly increases bleeding risk due to additive antiplatelet and anticoagulant effects."},
  {source:"Warfarin",   target:"Ibuprofen",  severity:"severe",   type:"Hematologic",    desc:"NSAIDs inhibit platelet function and may displace Warfarin from protein binding, raising hemorrhage risk."},
  {source:"Warfarin",   target:"Amoxicillin",severity:"moderate", type:"Metabolic",      desc:"Antibiotics alter gut flora that produce Vitamin K, potentially increasing INR unpredictably."},
  {source:"Warfarin",   target:"Lipitor",    severity:"moderate", type:"Metabolic",      desc:"Atorvastatin inhibits CYP2C9, raising Warfarin plasma levels and anticoagulation effect."},
  {source:"Paxil",      target:"Zoloft",     severity:"severe",   type:"Neurological",   desc:"Combining SSRIs increases serotonin syndrome risk: hyperthermia, seizures, cardiovascular collapse."},
  {source:"Paxil",      target:"Prozac",     severity:"severe",   type:"Neurological",   desc:"Two SSRIs together can precipitate life-threatening serotonin syndrome."},
  {source:"Prozac",     target:"Zoloft",     severity:"severe",   type:"Neurological",   desc:"Dual SSRI therapy dramatically increases serotonin toxicity risk."},
  {source:"Xanax",      target:"Prozac",     severity:"moderate", type:"Neurological",   desc:"Fluoxetine inhibits CYP3A4, slowing Alprazolam metabolism and potentiating CNS depression."},
  {source:"Xanax",      target:"Paxil",      severity:"moderate", type:"Neurological",   desc:"Paroxetine raises Alprazolam exposure through CYP3A4 inhibition, increasing sedation risk."},
  {source:"Lisinopril", target:"Ibuprofen",  severity:"moderate", type:"Cardiovascular", desc:"NSAIDs blunt the antihypertensive effect of ACE inhibitors and may worsen renal function."},
  {source:"Lisinopril", target:"Metformin",  severity:"mild",     type:"Metabolic",      desc:"ACE inhibitors may slightly enhance insulin sensitivity, risk of hypoglycemia with Metformin."},
  {source:"Digoxin",    target:"Lisinopril", severity:"moderate", type:"Cardiovascular", desc:"ACE inhibitors can raise Digoxin levels through renal hemodynamic changes."},
  {source:"Digoxin",    target:"Aspirin",    severity:"mild",     type:"Hematologic",    desc:"Low-dose aspirin has minimal effect on Digoxin but GI bleeding risk is additive."},
  {source:"Lipitor",    target:"Digoxin",    severity:"moderate", type:"Metabolic",      desc:"Atorvastatin increases Digoxin AUC ~15% via P-glycoprotein inhibition — monitor Digoxin levels."},
  {source:"Metformin",  target:"Ibuprofen",  severity:"mild",     type:"Metabolic",      desc:"NSAIDs can impair renal function, reducing Metformin clearance and raising lactic acidosis risk."},
  {source:"Aspirin",    target:"Lisinopril", severity:"mild",     type:"Cardiovascular", desc:"High-dose aspirin may attenuate the hemodynamic benefits of ACE inhibitors in heart failure."},
];

// ─── STATE ───────────────────────────────────────────────────────────────────
let currentRoot = "Warfarin";
let history = [];
let simulation;

// ─── PRONUNCIATION (Web Speech API) ─────────────────────────────────────────
function pronounce(text) {
  if (!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.rate = 0.85; u.pitch = 1.0; u.lang = "en-US";
  window.speechSynthesis.speak(u);
}

// ─── GRAPH BUILDER ───────────────────────────────────────────────────────────
function buildGraph(rootName) {
  if (history[history.length-1] !== rootName) {
    history.push(rootName);
    renderHistory();
  }
  currentRoot = rootName;

  const relEdges = ALL_INTERACTIONS.filter(e => e.source === rootName || e.target === rootName);
  const neighborNames = new Set([rootName]);
  relEdges.forEach(e => { neighborNames.add(e.source); neighborNames.add(e.target); });

  const nodes = [...neighborNames].map(n => ({ id:n, isRoot:n===rootName, ...ALL_DRUGS[n] }));
  const links = relEdges.map(e => ({...e}));
  renderD3(nodes, links, rootName);
}

function renderHistory() {
  const bar = document.getElementById("history-bar");
  bar.querySelectorAll(".hist-chip").forEach(c => c.remove());
  history.forEach((h, i) => {
    const chip = document.createElement("span");
    chip.className = "hist-chip";
    chip.textContent = h;
    chip.title = "Jump back to " + h;
    chip.onclick = () => { history = history.slice(0, i); buildGraph(h); };
    bar.appendChild(chip);
  });
}

// ─── D3 RENDER ───────────────────────────────────────────────────────────────
function renderD3(nodes, links, rootName) {
  const svg = d3.select("#svg");
  svg.selectAll("*").remove();

  const W = document.getElementById("graph-area").clientWidth;
  const H = document.getElementById("graph-area").clientHeight;

  const defs = svg.append("defs");
  ["severe","moderate","mild"].forEach(sev => {
    const col = sev==="severe"?"#f85149": sev==="moderate"?"#e3a400":"#3fb950";
    defs.append("marker")
      .attr("id",`arrow-${sev}`)
      .attr("viewBox","0 -5 10 10").attr("refX",22).attr("refY",0)
      .attr("markerWidth",6).attr("markerHeight",6).attr("orient","auto")
      .append("path").attr("d","M0,-5L10,0L0,5").attr("fill",col).attr("opacity",.7);
  });

  const g = svg.append("g");
  svg.call(d3.zoom().scaleExtent([0.25,3]).on("zoom", e => g.attr("transform", e.transform)));

  nodes.forEach(n => {
    if (n.isRoot){ n.x=W/2; n.y=H/2; n.fx=W/2; n.fy=H/2; }
    else { n.x=W/2+(Math.random()-.5)*220; n.y=H/2+(Math.random()-.5)*220; }
  });

  if (simulation) simulation.stop();
  simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d=>d.id).distance(170).strength(0.55))
    .force("charge", d3.forceManyBody().strength(-460))
    .force("center", d3.forceCenter(W/2, H/2))
    .force("collision", d3.forceCollide(50));

  const edgeColor = s => s==="severe"?"#f85149": s==="moderate"?"#e3a400":"#3fb950";
  const edgeWidth = s => s==="severe"?2.8: s==="moderate"?2:1.6;
  const dashArray  = t => t==="Hematologic"?"none": t==="Metabolic"?"10,4": t==="Cardiovascular"?"5,3": t==="Neurological"?"2,5":"2,2";

  const linkSel = g.append("g").selectAll("line").data(links).join("line")
    .attr("stroke", d => edgeColor(d.severity))
    .attr("stroke-width", d => edgeWidth(d.severity))
    .attr("stroke-dasharray", d => dashArray(d.type))
    .attr("opacity",.78)
    .attr("marker-end", d => `url(#arrow-${d.severity})`)
    .on("mouseover", (event,d) => showTooltip(event,
      `<b>${d.source.id||d.source} ↔ ${d.target.id||d.target}</b><br/>
       <span style="color:#8b949e">${d.severity.toUpperCase()} · ${d.type}</span><br/>${d.desc}`))
    .on("mouseout", hideTooltip);

  const nodeG = g.append("g").selectAll("g").data(nodes).join("g")
    .attr("cursor","pointer")
    .call(d3.drag()
      .on("start",(event,d)=>{ if(!event.active) simulation.alphaTarget(.4).restart(); d.fx=d.x; d.fy=d.y; })
      .on("drag",(event,d)=>{ d.fx=event.x; d.fy=event.y; })
      .on("end",(event,d)=>{ if(!event.active) simulation.alphaTarget(0); if(!d.isRoot){d.fx=null;d.fy=null;} }))
    .on("click",(event,d)=>{ event.stopPropagation(); if(d.isRoot) showInfoCard(d); else buildGraph(d.id); })
    .on("mouseover",(event,d)=>showTooltip(event,`<b>${d.id}</b><br/><span style="color:#8b949e">${d.ingredient}</span><br/><span style="color:#58a6ff;font-size:.72rem">Click to ${d.isRoot?'see card':'explore'}</span>`))
    .on("mouseout",hideTooltip);

  nodeG.append("circle")
    .attr("r", d=>d.isRoot?30:21)
    .attr("fill", d=>d.isRoot?"#1f6feb":"#21262d")
    .attr("stroke", d=>d.isRoot?"#58a6ff":"#444d56")
    .attr("stroke-width", d=>d.isRoot?3:1.5);

  nodeG.append("text")
    .attr("text-anchor","middle").attr("dy","0.35em")
    .attr("font-size", d=>d.isRoot?"11px":"9.5px")
    .attr("fill","#e6edf3").attr("pointer-events","none")
    .text(d=>d.id.length>10?d.id.slice(0,9)+"…":d.id);

  simulation.on("tick",()=>{
    linkSel.attr("x1",d=>d.source.x).attr("y1",d=>d.source.y)
            .attr("x2",d=>d.target.x).attr("y2",d=>d.target.y);
    nodeG.attr("transform",d=>`translate(${d.x},${d.y})`);
  });

  setTimeout(()=>{ const r=nodes.find(n=>n.isRoot); r.fx=null; r.fy=null; }, 900);
}

// ─── INFO CARD (Baseball-card sidebar) ───────────────────────────────────────
function showInfoCard(drug) {
  const panel = document.getElementById("info-panel");
  panel.style.display = "flex";
  panel.style.flexDirection = "column";

  const rels = ALL_INTERACTIONS
    .filter(e => e.source===drug.id || e.target===drug.id)
    .sort((a,b)=>({severe:0,moderate:1,mild:2}[a.severity]-({severe:0,moderate:1,mild:2}[b.severity])));

  const similarHTML = (drug.similar||[]).sort()
    .map(s=>`<span class="similar-chip" title="Same ingredient: ${drug.ingredient}">${s}</span>`).join("");

  panel.innerHTML = `
    <div class="card-header">
      <div class="card-brand">
        ${drug.id}
        <button class="pronunc-btn" onclick="pronounce('${drug.pronounce||drug.id}')" title="Pronounce">
          🔊 ${drug.pronounce||drug.id}
        </button>
      </div>
      <div class="card-class">${drug.cls}</div>
    </div>
    <div class="card-body">
      <div class="card-section-title">Active Ingredient</div>
      <div class="card-val">${drug.ingredient}</div>

      <div class="card-section-title">Description</div>
      <div class="card-val">${drug.desc}</div>

      <div class="card-section-title">Same Medication — Other Brand Names</div>
      <div style="margin-top:4px">${similarHTML || '<span style="color:#8b949e;font-size:.8rem">None listed</span>'}</div>

      <div class="card-section-title" style="margin-top:16px">
        Negative Interactions
        <span style="background:#f851491a;color:#f85149;border:1px solid #f8514940;border-radius:8px;padding:1px 7px;font-size:.7rem;margin-left:6px">${rels.length}</span>
      </div>
      ${rels.map(r=>{
        const other = r.source===drug.id ? r.target : r.source;
        return `<div class="icard ${r.severity}">
          <div class="ic-title">
            <span style="cursor:pointer;color:#79c0ff" onclick="buildGraph('${other}')">${other}</span>
            <span class="ic-badge ${r.severity}">${r.severity}</span>
            <span style="color:#8b949e;font-size:.72rem;margin-left:auto">${r.type}</span>
          </div>
          <div class="ic-sub">${r.desc}</div>
        </div>`;
      }).join("")}
    </div>
    <button class="close-panel-btn" onclick="document.getElementById('info-panel').style.display='none'">✕ Close</button>`;
}

// ─── TOOLTIP ─────────────────────────────────────────────────────────────────
const tt = document.getElementById("tooltip");
function showTooltip(event, html){ tt.innerHTML=html; tt.style.display="block"; tt.style.left=(event.pageX+14)+"px"; tt.style.top=(event.pageY-10)+"px"; }
function hideTooltip(){ tt.style.display="none"; }

// ─── SEARCH ──────────────────────────────────────────────────────────────────
function searchInteraction(){
  const d1=document.getElementById("drug1").value.trim();
  const d2=document.getElementById("drug2").value.trim();
  const sr=document.getElementById("search-result");
  const srTitle=document.getElementById("sr-title");
  const srBody=document.getElementById("sr-body");

  if(!d1||!d2){ srTitle.textContent="Enter both drug names"; srBody.textContent=""; sr.style.display="block"; return; }

  const match=ALL_INTERACTIONS.find(e=>
    (e.source.toLowerCase()===d1.toLowerCase()&&e.target.toLowerCase()===d2.toLowerCase())||
    (e.source.toLowerCase()===d2.toLowerCase()&&e.target.toLowerCase()===d1.toLowerCase())
  );

  if(match){
    const col=match.severity==="severe"?"#f85149":match.severity==="moderate"?"#e3a400":"#3fb950";
    srTitle.innerHTML=`${match.source} ↔ ${match.target}`;
    srBody.innerHTML=`<span style="color:${col};font-weight:700">${match.severity.toUpperCase()}</span> · ${match.type}<br/><br/>${match.desc}`;
    history.push(`${d1}+${d2}`); renderHistory();
    buildGraph(match.source);
  } else {
    srTitle.textContent="No interaction found";
    srBody.innerHTML=`No recorded negative interaction between <b>${d1}</b> and <b>${d2}</b> in ODMAP database.`;
    const key=Object.keys(ALL_DRUGS).find(k=>k.toLowerCase()===d1.toLowerCase());
    if(key) buildGraph(key);
  }
  sr.style.display="block";
}

// ─── INIT ────────────────────────────────────────────────────────────────────
window.onload  = ()=>buildGraph("Warfarin");
window.onresize= ()=>buildGraph(currentRoot);
</script>
</body>
</html>"""

with open("./outputs/odmap_v2.html", "w") as f:
    f.write(html)

from IPython.display import display, HTML
display(HTML(open("./outputs/odmap_v2.html").read()), metadata={"alt": "ODMAP v2 drug network"})


# ## ODMAP v3 — Beige/Green Palette · Colloquial Names · Sticky Info Card · History Dropdown

# In[5]:


import os
os.makedirs("./outputs", exist_ok=True)

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>ODMAP — Drug Interaction Network</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#f5f0e8;color:#2d3a2e;font-family:'Segoe UI',sans-serif;display:flex;flex-direction:column;height:100vh;overflow:hidden}

  /* ── HEADER ── */
  #header{background:#2d3a2e;border-bottom:2px solid #4a6741;padding:10px 20px;display:flex;align-items:center;gap:16px;flex-shrink:0;flex-wrap:wrap}
  #header h1{font-size:1.2rem;color:#b8d4a8;letter-spacing:2px;font-weight:700}
  #header .subtitle{font-size:.78rem;color:#7a9e72}
  #search-area{display:flex;gap:8px;align-items:center;margin-left:auto;position:relative}
  #search-area input{background:#3d4f3e;border:1px solid #4a6741;border-radius:6px;color:#e8f0e4;padding:6px 12px;font-size:.85rem;width:150px}
  #search-area input:focus{outline:none;border-color:#8fbe7c}
  #search-area input::placeholder{color:#7a9e72}
  #go-btn{background:#4a6741;border:none;color:#e8f0e4;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:.85rem;font-weight:600}
  #go-btn:hover{background:#5a7d50}

  /* ── HISTORY DROPDOWN (only shown when search input is focused) ── */
  #history-dropdown{display:none;position:absolute;top:100%;right:0;margin-top:4px;background:#2d3a2e;border:1px solid #4a6741;border-radius:8px;padding:8px 10px;z-index:1100;min-width:260px;box-shadow:0 4px 16px #0003}
  #history-dropdown .hist-label{font-size:.72rem;color:#7a9e72;margin-bottom:6px;display:block;text-transform:uppercase;letter-spacing:.8px}
  #history-dropdown .hist-chips{display:flex;flex-wrap:wrap;gap:5px}
  .hist-chip{background:#3d4f3e;border:1px solid #4a6741;border-radius:12px;padding:3px 10px;font-size:.75rem;cursor:pointer;color:#b8d4a8;white-space:nowrap}
  .hist-chip:hover{background:#4a6741}

  /* ── SEARCH RESULT POPUP ── */
  #search-result{position:fixed;top:56px;right:20px;background:#f0ebe0;border:1px solid #c5b99a;border-radius:8px;padding:14px 18px;z-index:999;display:none;max-width:320px;font-size:.85rem;line-height:1.6;color:#2d3a2e;box-shadow:0 4px 16px #0002}
  #search-result h3{color:#4a6741;margin-bottom:6px}
  #search-result .close-btn{float:right;cursor:pointer;color:#8a7e6a;font-size:1rem}

  #main{display:flex;flex:1;overflow:hidden}
  #graph-area{flex:1;position:relative}
  svg{width:100%;height:100%}

  /* ── INFO PANEL ── */
  #info-panel{width:300px;background:#eee8d8;border-left:2px solid #c5b99a;overflow-y:auto;padding:0;flex-shrink:0;display:none;flex-direction:column}
  .card-header{background:#ddd5c2;padding:16px 18px 12px;border-bottom:1px solid #c5b99a}
  .card-brand{font-size:1.1rem;font-weight:700;color:#2d3a2e;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
  .card-class{font-size:.78rem;color:#7a6e5a;margin-top:3px}
  .pronunc-btn{background:#f5f0e8;border:1px solid #c5b99a;border-radius:6px;color:#4a6741;cursor:pointer;padding:3px 8px;font-size:.78rem;display:inline-flex;align-items:center;gap:4px;white-space:nowrap}
  .pronunc-btn:hover{background:#ddd5c2}
  .card-body{padding:14px 18px;flex:1}
  .card-section-title{font-size:.7rem;color:#7a6e5a;text-transform:uppercase;letter-spacing:1px;margin-top:14px;margin-bottom:4px;font-weight:600}
  .card-val{font-size:.85rem;color:#2d3a2e;line-height:1.5}
  .similar-chip{display:inline-block;background:#d8eecf;border:1px solid #a0c896;border-radius:10px;padding:2px 9px;font-size:.75rem;color:#3a5e34;margin:2px 2px 2px 0;cursor:pointer}
  .similar-chip:hover{background:#c5e0ba}
  .icard{background:#f0ebe0;border-radius:6px;padding:8px 10px;margin-top:8px;border-left:3px solid #4a6741}
  .icard .ic-title{font-size:.8rem;font-weight:600;color:#2d3a2e;display:flex;align-items:center;gap:6px}
  .ic-badge{font-size:.68rem;padding:1px 6px;border-radius:8px;font-weight:700;text-transform:uppercase}
  .ic-badge.severe{background:#c0392b22;color:#c0392b;border:1px solid #c0392b55}
  .ic-badge.moderate{background:#d4860022;color:#b8720a;border:1px solid #d4860055}
  .ic-badge.mild{background:#27ae6022;color:#27ae60;border:1px solid #27ae6055}
  .icard.severe{border-left-color:#c0392b}
  .icard.moderate{border-left-color:#d48600}
  .icard.mild{border-left-color:#27ae60}
  .icard .ic-sub{font-size:.75rem;color:#5a5040;margin-top:4px;line-height:1.4}
  .close-panel-btn{width:100%;background:#ddd5c2;border:none;border-top:1px solid #c5b99a;color:#5a5040;padding:8px;cursor:pointer;font-size:.8rem;margin-top:8px}
  .close-panel-btn:hover{background:#c5b99a;color:#2d3a2e}

  /* ── LEGEND ── */
  #legend{position:absolute;bottom:14px;left:14px;background:#f0ebe0cc;border:1px solid #c5b99a;border-radius:8px;padding:10px 14px;font-size:.73rem;line-height:1.9;backdrop-filter:blur(4px)}
  #legend .leg-title{color:#7a6e5a;margin-bottom:2px;font-weight:600;font-size:.72rem;text-transform:uppercase;letter-spacing:.8px}
  .leg-row{display:flex;align-items:center;gap:8px;color:#3d3028}

  #tooltip{position:fixed;background:#2d3a2e;border:1px solid #4a6741;border-radius:6px;padding:7px 11px;font-size:.78rem;pointer-events:none;display:none;z-index:800;max-width:240px;line-height:1.5;color:#e8f0e4}
</style>
</head>
<body>

<div id="header">
  <h1>⬡ ODMAP</h1>
  <div class="subtitle">Drug Interaction Network</div>
  <div id="search-area">
    <input id="drug1" placeholder="Drug 1" autocomplete="off"/>
    <input id="drug2" placeholder="Drug 2" autocomplete="off"/>
    <button id="go-btn" onclick="searchInteraction()">Go</button>
    <div id="history-dropdown">
      <span class="hist-label">Search History</span>
      <div class="hist-chips" id="hist-chips-container"></div>
    </div>
  </div>
</div>

<div id="search-result">
  <span class="close-btn" onclick="this.parentElement.style.display='none'">✕</span>
  <h3 id="sr-title"></h3>
  <div id="sr-body"></div>
</div>

<div id="main">
  <div id="graph-area">
    <svg id="svg"></svg>
    <div id="legend">
      <div class="leg-title">Severity</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#c0392b" stroke-width="2.5"/></svg> Severe</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#d48600" stroke-width="2" stroke-dasharray="6,3"/></svg> Moderate</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#27ae60" stroke-width="1.5" stroke-dasharray="2,3"/></svg> Mild</div>
      <div class="leg-title" style="margin-top:8px">Interaction Type</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#5a5040" stroke-width="2"/></svg> Hematologic</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#5a5040" stroke-width="2" stroke-dasharray="8,4"/></svg> Metabolic</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#5a5040" stroke-width="2" stroke-dasharray="4,2"/></svg> Cardiovascular</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#5a5040" stroke-width="2" stroke-dasharray="2,5"/></svg> Neurological</div>
    </div>
  </div>
  <div id="info-panel"></div>
</div>
<div id="tooltip"></div>

<script>
// ─── DATA ────────────────────────────────────────────────────────────────────
const ALL_DRUGS = {
  "Warfarin":    {ingredient:"Warfarin sodium",        pronounce:"WAR-fuh-rin",     cls:"Anticoagulant",        similar:["Coumadin","Jantoven"],                 desc:"Prevents blood clots by inhibiting Vitamin K-dependent clotting factors."},
  "Aspirin":     {ingredient:"Acetylsalicylic acid",   pronounce:"AS-pir-in",       cls:"NSAID / Antiplatelet", similar:["Bayer","Bufferin","Ecotrin"],          desc:"Reduces pain, fever, and platelet aggregation."},
  "Lipitor":     {ingredient:"Atorvastatin",           pronounce:"LIP-ih-tor",      cls:"Statin",               similar:["Torvast"],                            desc:"Lowers LDL cholesterol by inhibiting HMG-CoA reductase."},
  "Paxil":       {ingredient:"Paroxetine",             pronounce:"PAX-il",          cls:"SSRI",                 similar:["Pexeva","Brisdelle"],                 desc:"Selective serotonin reuptake inhibitor for depression and anxiety."},
  "Prozac":      {ingredient:"Fluoxetine",             pronounce:"PRO-zak",         cls:"SSRI",                 similar:["Sarafem","Rapiflux"],                 desc:"Increases serotonin levels; treats depression and OCD."},
  "Xanax":       {ingredient:"Alprazolam",             pronounce:"ZAN-ax",          cls:"Benzodiazepine",       similar:["Niravam","Alprazolam ER"],            desc:"Short-term management of anxiety disorders."},
  "Metformin":   {ingredient:"Metformin HCl",          pronounce:"met-FOR-min",     cls:"Biguanide",            similar:["Glucophage","Fortamet","Glumetza"],   desc:"First-line treatment for type 2 diabetes; reduces hepatic glucose output."},
  "Lisinopril":  {ingredient:"Lisinopril",             pronounce:"lye-SIN-oh-pril", cls:"ACE Inhibitor",        similar:["Zestril","Prinivil","Qbrelis"],       desc:"Treats high blood pressure and heart failure."},
  "Advil":       {ingredient:"Ibuprofen",              pronounce:"AD-vil",          cls:"NSAID",                similar:["Motrin","Nuprin","Ibuprofen"],        desc:"Reduces inflammation, pain, and fever."},
  "Amoxil":      {ingredient:"Amoxicillin trihydrate", pronounce:"a-MOX-il",        cls:"Antibiotic",           similar:["Trimox","Moxatag","Amoxicillin"],     desc:"Broad-spectrum penicillin antibiotic."},
  "Lanoxin":     {ingredient:"Digoxin",                pronounce:"la-NOX-in",       cls:"Cardiac Glycoside",    similar:["Digitek","Digoxin"],                  desc:"Strengthens heart contractions; treats heart failure and AFib."},
  "Zoloft":      {ingredient:"Sertraline",             pronounce:"ZO-loft",         cls:"SSRI",                 similar:["Lustral"],                            desc:"Treats depression, panic disorder, and PTSD."},
};

const ALL_INTERACTIONS = [
  {source:"Warfarin",  target:"Aspirin",    severity:"severe",   type:"Hematologic",    desc:"Concurrent use significantly increases bleeding risk due to additive antiplatelet and anticoagulant effects."},
  {source:"Warfarin",  target:"Advil",      severity:"severe",   type:"Hematologic",    desc:"NSAIDs inhibit platelet function and may displace Warfarin from protein binding, raising hemorrhage risk."},
  {source:"Warfarin",  target:"Amoxil",     severity:"moderate", type:"Metabolic",      desc:"Antibiotics alter gut flora that produce Vitamin K, potentially increasing INR unpredictably."},
  {source:"Warfarin",  target:"Lipitor",    severity:"moderate", type:"Metabolic",      desc:"Atorvastatin inhibits CYP2C9, raising Warfarin plasma levels and anticoagulation effect."},
  {source:"Paxil",     target:"Zoloft",     severity:"severe",   type:"Neurological",   desc:"Combining SSRIs increases serotonin syndrome risk: hyperthermia, seizures, cardiovascular collapse."},
  {source:"Paxil",     target:"Prozac",     severity:"severe",   type:"Neurological",   desc:"Two SSRIs together can precipitate life-threatening serotonin syndrome."},
  {source:"Prozac",    target:"Zoloft",     severity:"severe",   type:"Neurological",   desc:"Dual SSRI therapy dramatically increases serotonin toxicity risk."},
  {source:"Xanax",     target:"Prozac",     severity:"moderate", type:"Neurological",   desc:"Fluoxetine inhibits CYP3A4, slowing Alprazolam metabolism and potentiating CNS depression."},
  {source:"Xanax",     target:"Paxil",      severity:"moderate", type:"Neurological",   desc:"Paroxetine raises Alprazolam exposure through CYP3A4 inhibition, increasing sedation risk."},
  {source:"Lisinopril",target:"Advil",      severity:"moderate", type:"Cardiovascular", desc:"NSAIDs blunt the antihypertensive effect of ACE inhibitors and may worsen renal function."},
  {source:"Lisinopril",target:"Metformin",  severity:"mild",     type:"Metabolic",      desc:"ACE inhibitors may slightly enhance insulin sensitivity, risk of hypoglycemia with Metformin."},
  {source:"Lanoxin",   target:"Lisinopril", severity:"moderate", type:"Cardiovascular", desc:"ACE inhibitors can raise Digoxin levels through renal hemodynamic changes."},
  {source:"Lanoxin",   target:"Aspirin",    severity:"mild",     type:"Hematologic",    desc:"Low-dose aspirin has minimal effect on Digoxin but GI bleeding risk is additive."},
  {source:"Lipitor",   target:"Lanoxin",    severity:"moderate", type:"Metabolic",      desc:"Atorvastatin increases Digoxin AUC ~15% via P-glycoprotein inhibition — monitor levels."},
  {source:"Metformin", target:"Advil",      severity:"mild",     type:"Metabolic",      desc:"NSAIDs can impair renal function, reducing Metformin clearance and raising lactic acidosis risk."},
  {source:"Aspirin",   target:"Lisinopril", severity:"mild",     type:"Cardiovascular", desc:"High-dose aspirin may attenuate the hemodynamic benefits of ACE inhibitors in heart failure."},
];

// ─── STATE ───────────────────────────────────────────────────────────────────
let currentRoot = "Warfarin";
let history = [];
let simulation;
let cardPinned = false;   // true while info panel is open / sticky

// ─── HISTORY DROPDOWN — only on search-input focus ───────────────────────────
(function(){
  const d1 = document.getElementById("drug1");
  const d2 = document.getElementById("drug2");
  const drop = document.getElementById("history-dropdown");

  function showDrop(){ renderHistChips(); drop.style.display = history.length ? "block" : "none"; }
  function hideDrop(e){
    // delay so chip clicks register first
    setTimeout(()=>{ if(!drop.contains(document.activeElement)) drop.style.display="none"; }, 150);
  }
  d1.addEventListener("focus", showDrop);
  d2.addEventListener("focus", showDrop);
  d1.addEventListener("blur",  hideDrop);
  d2.addEventListener("blur",  hideDrop);
})();

function renderHistChips(){
  const container = document.getElementById("hist-chips-container");
  container.innerHTML = "";
  history.forEach((h, i) => {
    const chip = document.createElement("span");
    chip.className = "hist-chip";
    chip.textContent = h;
    chip.title = "Jump to " + h;
    chip.onmousedown = (e) => { e.preventDefault(); history = history.slice(0,i); buildGraph(h); };
    container.appendChild(chip);
  });
  document.getElementById("history-dropdown").style.display = history.length ? "block" : "none";
}

// ─── PRONUNCIATION ────────────────────────────────────────────────────────────
function pronounce(text) {
  if (!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.rate = 0.85; u.pitch = 1.0; u.lang = "en-US";
  window.speechSynthesis.speak(u);
}

// ─── GRAPH BUILDER ────────────────────────────────────────────────────────────
function buildGraph(rootName) {
  if (history[history.length-1] !== rootName) history.push(rootName);
  currentRoot = rootName;
  const relEdges = ALL_INTERACTIONS.filter(e => e.source===rootName || e.target===rootName);
  const neighborNames = new Set([rootName]);
  relEdges.forEach(e => { neighborNames.add(e.source); neighborNames.add(e.target); });
  const nodes = [...neighborNames].map(n => ({ id:n, isRoot:n===rootName, ...ALL_DRUGS[n] }));
  renderD3(nodes, relEdges.map(e=>({...e})), rootName);
}

// ─── D3 RENDER ────────────────────────────────────────────────────────────────
function renderD3(nodes, links, rootName) {
  const svg = d3.select("#svg");
  svg.selectAll("*").remove();

  const W = document.getElementById("graph-area").clientWidth;
  const H = document.getElementById("graph-area").clientHeight;

  const defs = svg.append("defs");
  ["severe","moderate","mild"].forEach(sev => {
    const col = sev==="severe"?"#c0392b": sev==="moderate"?"#d48600":"#27ae60";
    defs.append("marker")
      .attr("id",`arrow-${sev}`)
      .attr("viewBox","0 -5 10 10").attr("refX",22).attr("refY",0)
      .attr("markerWidth",6).attr("markerHeight",6).attr("orient","auto")
      .append("path").attr("d","M0,-5L10,0L0,5").attr("fill",col).attr("opacity",.8);
  });

  const g = svg.append("g");
  svg.call(d3.zoom().scaleExtent([0.25,3]).on("zoom", e => g.attr("transform", e.transform)));

  nodes.forEach(n => {
    if (n.isRoot){ n.x=W/2; n.y=H/2; n.fx=W/2; n.fy=H/2; }
    else { n.x=W/2+(Math.random()-.5)*220; n.y=H/2+(Math.random()-.5)*220; }
  });

  if (simulation) simulation.stop();
  simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d=>d.id).distance(170).strength(0.55))
    .force("charge", d3.forceManyBody().strength(-460))
    .force("center", d3.forceCenter(W/2, H/2))
    .force("collision", d3.forceCollide(50));

  const edgeColor = s => s==="severe"?"#c0392b": s==="moderate"?"#d48600":"#27ae60";
  const edgeWidth = s => s==="severe"?2.8: s==="moderate"?2:1.6;
  const dashArray  = t => t==="Hematologic"?"none": t==="Metabolic"?"10,4": t==="Cardiovascular"?"5,3":"2,5";

  const linkSel = g.append("g").selectAll("line").data(links).join("line")
    .attr("stroke", d => edgeColor(d.severity))
    .attr("stroke-width", d => edgeWidth(d.severity))
    .attr("stroke-dasharray", d => dashArray(d.type))
    .attr("opacity",.82)
    .attr("marker-end", d => `url(#arrow-${d.severity})`)
    .on("mouseover",(event,d)=>showTooltip(event,
      `<b>${d.source.id||d.source} ↔ ${d.target.id||d.target}</b><br/>
       <span style="color:#b8d4a8">${d.severity.toUpperCase()} · ${d.type}</span><br/>${d.desc}`))
    .on("mouseout", hideTooltip);

  const nodeG = g.append("g").selectAll("g").data(nodes).join("g")
    .attr("cursor","pointer")
    .call(d3.drag()
      .on("start",(event,d)=>{ if(!event.active) simulation.alphaTarget(.4).restart(); d.fx=d.x; d.fy=d.y; })
      .on("drag",(event,d)=>{ d.fx=event.x; d.fy=event.y; })
      .on("end",(event,d)=>{ if(!event.active) simulation.alphaTarget(0); if(!d.isRoot){d.fx=null;d.fy=null;} }))
    .on("click",(event,d)=>{
      event.stopPropagation();
      if(d.isRoot){ showInfoCard(d); cardPinned=true; }
      else { buildGraph(d.id); }
    })
    .on("mouseover",(event,d)=>showTooltip(event,
      `<b>${d.id}</b><br/><span style="color:#b8d4a8">${d.ingredient}</span><br/>
       <span style="color:#8fbe7c;font-size:.72rem">Click to ${d.isRoot?'see info card':'explore'}</span>`))
    .on("mouseout", hideTooltip);

  // Node circle — root gets green fill, others get beige
  nodeG.append("circle")
    .attr("r", d=>d.isRoot?30:21)
    .attr("fill", d=>d.isRoot?"#4a6741":"#ddd5c2")
    .attr("stroke", d=>d.isRoot?"#8fbe7c":"#a09080")
    .attr("stroke-width", d=>d.isRoot?3:1.5);

  nodeG.append("text")
    .attr("text-anchor","middle").attr("dy","0.35em")
    .attr("font-size", d=>d.isRoot?"11px":"9.5px")
    .attr("fill", d=>d.isRoot?"#e8f0e4":"#2d3a2e")
    .attr("font-weight", d=>d.isRoot?"700":"400")
    .attr("pointer-events","none")
    .text(d=>d.id.length>10?d.id.slice(0,9)+"…":d.id);

  simulation.on("tick",()=>{
    linkSel.attr("x1",d=>d.source.x).attr("y1",d=>d.source.y)
            .attr("x2",d=>d.target.x).attr("y2",d=>d.target.y);
    nodeG.attr("transform",d=>`translate(${d.x},${d.y})`);
  });

  setTimeout(()=>{ const r=nodes.find(n=>n.isRoot); r.fx=null; r.fy=null; }, 900);
}

// ─── INFO CARD (sticky — persists until user closes it) ───────────────────────
function showInfoCard(drug) {
  const panel = document.getElementById("info-panel");
  panel.style.display = "flex";
  panel.style.flexDirection = "column";

  const rels = ALL_INTERACTIONS
    .filter(e => e.source===drug.id || e.target===drug.id)
    .sort((a,b)=>({severe:0,moderate:1,mild:2}[a.severity]-({severe:0,moderate:1,mild:2}[b.severity])));

  const similarHTML = (drug.similar||[]).sort()
    .map(s=>`<span class="similar-chip" title="Same ingredient: ${drug.ingredient}">${s}</span>`).join("");

  panel.innerHTML = `
    <div class="card-header">
      <div class="card-brand">
        ${drug.id}
        <button class="pronunc-btn" onclick="pronounce('${drug.pronounce||drug.id}')" title="Pronounce">
          🔊 ${drug.pronounce||drug.id}
        </button>
      </div>
      <div class="card-class">${drug.cls}</div>
    </div>
    <div class="card-body">
      <div class="card-section-title">Active Ingredient</div>
      <div class="card-val">${drug.ingredient}</div>

      <div class="card-section-title">Description</div>
      <div class="card-val">${drug.desc}</div>

      <div class="card-section-title">Same Medication — Other Brand Names</div>
      <div style="margin-top:4px">${similarHTML||'<span style="color:#8a7e6a;font-size:.8rem">None listed</span>'}</div>

      <div class="card-section-title" style="margin-top:16px">
        Negative Interactions
        <span style="background:#c0392b22;color:#c0392b;border:1px solid #c0392b55;border-radius:8px;padding:1px 7px;font-size:.7rem;margin-left:6px">${rels.length}</span>
      </div>
      ${rels.map(r=>{
        const other = r.source===drug.id ? r.target : r.source;
        return `<div class="icard ${r.severity}">
          <div class="ic-title">
            <span style="cursor:pointer;color:#4a6741;font-weight:600" onclick="buildGraph('${other}');cardPinned=false;">${other}</span>
            <span class="ic-badge ${r.severity}">${r.severity}</span>
            <span style="color:#7a6e5a;font-size:.72rem;margin-left:auto">${r.type}</span>
          </div>
          <div class="ic-sub">${r.desc}</div>
        </div>`;
      }).join("")}
    </div>
    <button class="close-panel-btn" onclick="document.getElementById('info-panel').style.display='none';cardPinned=false;">✕ Close</button>`;
}

// ─── TOOLTIP ─────────────────────────────────────────────────────────────────
const tt = document.getElementById("tooltip");
function showTooltip(event, html){ tt.innerHTML=html; tt.style.display="block"; tt.style.left=(event.pageX+14)+"px"; tt.style.top=(event.pageY-10)+"px"; }
function hideTooltip(){ tt.style.display="none"; }

// ─── SEARCH ──────────────────────────────────────────────────────────────────
function searchInteraction(){
  const d1=document.getElementById("drug1").value.trim();
  const d2=document.getElementById("drug2").value.trim();
  const sr=document.getElementById("search-result");
  const srTitle=document.getElementById("sr-title");
  const srBody=document.getElementById("sr-body");

  if(!d1||!d2){ srTitle.textContent="Enter both drug names"; srBody.textContent=""; sr.style.display="block"; return; }

  const match=ALL_INTERACTIONS.find(e=>
    (e.source.toLowerCase()===d1.toLowerCase()&&e.target.toLowerCase()===d2.toLowerCase())||
    (e.source.toLowerCase()===d2.toLowerCase()&&e.target.toLowerCase()===d1.toLowerCase())
  );

  if(match){
    const col=match.severity==="severe"?"#c0392b":match.severity==="moderate"?"#d48600":"#27ae60";
    srTitle.innerHTML=`${match.source} ↔ ${match.target}`;
    srBody.innerHTML=`<span style="color:${col};font-weight:700">${match.severity.toUpperCase()}</span> · ${match.type}<br/><br/>${match.desc}`;
    if(history[history.length-1]!==`${d1}+${d2}`) history.push(`${d1}+${d2}`);
    buildGraph(match.source);
  } else {
    srTitle.textContent="No interaction found";
    srBody.innerHTML=`No recorded negative interaction between <b>${d1}</b> and <b>${d2}</b> in ODMAP database.`;
    const key=Object.keys(ALL_DRUGS).find(k=>k.toLowerCase()===d1.toLowerCase());
    if(key) buildGraph(key);
  }
  sr.style.display="block";
}

// Enter key triggers search
document.addEventListener("keydown", e=>{ if(e.key==="Enter"&&(document.activeElement.id==="drug1"||document.activeElement.id==="drug2")) searchInteraction(); });

// ─── INIT ────────────────────────────────────────────────────────────────────
window.onload  = ()=>buildGraph("Warfarin");
window.onresize= ()=>buildGraph(currentRoot);
</script>
</body>
</html>"""

with open("./outputs/odmap_v3.html", "w") as f:
    f.write(html)

from IPython.display import display, HTML
display(HTML(open("./outputs/odmap_v3.html").read()), metadata={"alt": "ODMAP v3 drug network"})


# ## ODMAP — Interactive Drug Interaction Network Prototype
# 
# **Stack:** D3.js v7 (`d3-force` simulation) · 12 drugs · 16 clinically accurate interactions
# 
# **Features implemented:**
# - Spring physics simulation — elastic drag, bounce-into-place animation (identical mechanism to Visual Thesaurus)
# - **Color-coded edges by severity:** Red = Severe, Orange = Moderate, Green = Mild
# - **Line styles by interaction type:** Solid = Hematologic · Long-dash = Metabolic · Short-dash = Cardiovascular · Dash-dot = Neurological · Dotted = Renal
# - **Re-rooting:** click any node → becomes the new center with its own subgraph (full Visual Thesaurus behavior)
# - **Info card sidebar** on node click: active ingredient, drug class, description, sorted interaction cards
# - **Tooltip** on hover for both nodes and edges
# - **Search:** two-drug interaction lookup with result popup
# - **History bar:** clickable breadcrumb chips for back-navigation
# 

# In[1]:


import os
os.makedirs("./outputs", exist_ok=True)

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>ODMAP — Drug Interaction Network</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#0d1117;color:#e6edf3;font-family:'Segoe UI',sans-serif;display:flex;flex-direction:column;height:100vh;overflow:hidden}
  #header{background:#161b22;border-bottom:1px solid #30363d;padding:10px 20px;display:flex;align-items:center;gap:16px;flex-shrink:0}
  #header h1{font-size:1.2rem;color:#58a6ff;letter-spacing:2px;font-weight:700}
  #search-area{display:flex;gap:8px;align-items:center;margin-left:auto}
  #search-area input{background:#21262d;border:1px solid #30363d;border-radius:6px;color:#e6edf3;padding:6px 12px;font-size:.85rem;width:160px}
  #search-area input:focus{outline:none;border-color:#58a6ff}
  #go-btn{background:#238636;border:none;color:#fff;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:.85rem;font-weight:600}
  #go-btn:hover{background:#2ea043}
  #search-result{position:fixed;top:56px;right:20px;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px 18px;z-index:999;display:none;max-width:320px;font-size:.85rem;line-height:1.6}
  #search-result h3{color:#58a6ff;margin-bottom:6px}
  #search-result .close-btn{float:right;cursor:pointer;color:#8b949e;font-size:1rem}
  #history-bar{background:#0d1117;border-bottom:1px solid #21262d;padding:6px 16px;display:flex;gap:8px;align-items:center;overflow-x:auto;flex-shrink:0;min-height:36px}
  #history-bar span{font-size:.75rem;color:#8b949e}
  .hist-chip{background:#21262d;border:1px solid #30363d;border-radius:12px;padding:3px 10px;font-size:.75rem;cursor:pointer;color:#58a6ff;white-space:nowrap}
  .hist-chip:hover{background:#30363d}
  #main{display:flex;flex:1;overflow:hidden}
  #graph-area{flex:1;position:relative}
  svg{width:100%;height:100%}
  #info-panel{width:280px;background:#161b22;border-left:1px solid #30363d;overflow-y:auto;padding:18px;flex-shrink:0;display:none}
  #info-panel h2{color:#58a6ff;font-size:1rem;margin-bottom:4px}
  #info-panel .sub{color:#8b949e;font-size:.78rem;margin-bottom:12px}
  #info-panel .label{font-size:.72rem;color:#8b949e;text-transform:uppercase;letter-spacing:1px;margin-top:10px}
  #info-panel .val{font-size:.85rem;color:#e6edf3;margin-top:2px}
  .icard{background:#21262d;border-radius:6px;padding:8px 10px;margin-top:8px;border-left:3px solid #58a6ff}
  .icard .ic-title{font-size:.8rem;font-weight:600;color:#e6edf3}
  .icard .ic-sub{font-size:.75rem;color:#8b949e;margin-top:2px}
  .icard.severe{border-left-color:#f85149}
  .icard.moderate{border-left-color:#e3a400}
  .icard.mild{border-left-color:#3fb950}
  #legend{position:absolute;bottom:14px;left:14px;background:#161b22cc;border:1px solid #30363d;border-radius:8px;padding:10px 14px;font-size:.75rem;line-height:1.9}
  #legend .leg-title{color:#8b949e;margin-bottom:4px;font-weight:600}
  .leg-row{display:flex;align-items:center;gap:8px}
  .leg-dot{width:12px;height:12px;border-radius:50%}
  svg line.severe{stroke:#f85149}
  svg line.moderate{stroke:#e3a400}
  svg line.mild{stroke:#3fb950}
  #tooltip{position:fixed;background:#21262d;border:1px solid #30363d;border-radius:6px;padding:7px 11px;font-size:.78rem;pointer-events:none;display:none;z-index:800;max-width:220px;line-height:1.5}
</style>
</head>
<body>

<div id="header">
  <h1>⬡ ODMAP</h1>
  <div style="font-size:.78rem;color:#8b949e">Drug Interaction Network</div>
  <div id="search-area">
    <input id="drug1" placeholder="Drug 1 (brand name)"/>
    <input id="drug2" placeholder="Drug 2 (brand name)"/>
    <button id="go-btn" onclick="searchInteraction()">Go</button>
  </div>
</div>

<div id="history-bar">
  <span>History:</span>
</div>

<div id="search-result">
  <span class="close-btn" onclick="this.parentElement.style.display='none'">✕</span>
  <h3 id="sr-title"></h3>
  <div id="sr-body"></div>
</div>

<div id="main">
  <div id="graph-area">
    <svg id="svg"></svg>
    <div id="legend">
      <div class="leg-title">Severity</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#f85149" stroke-width="2.5"/></svg> Severe</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#e3a400" stroke-width="2" stroke-dasharray="6,3"/></svg> Moderate</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#3fb950" stroke-width="1.5" stroke-dasharray="2,3"/></svg> Mild</div>
      <div class="leg-title" style="margin-top:8px">Interaction Type</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#8b949e" stroke-width="2"/></svg> Hematologic</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#8b949e" stroke-width="2" stroke-dasharray="8,4"/></svg> Metabolic</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#8b949e" stroke-width="2" stroke-dasharray="4,2"/></svg> Cardiovascular</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#8b949e" stroke-width="2" stroke-dasharray="1,4"/></svg> Neurological</div>
    </div>
  </div>
  <div id="info-panel"></div>
</div>
<div id="tooltip"></div>

<script>
// ─── DATA ────────────────────────────────────────────────────────────────────
const ALL_DRUGS = {
  "Warfarin":   {ingredient:"Warfarin sodium",   cls:"Anticoagulant",   desc:"Prevents blood clots by inhibiting Vitamin K-dependent clotting factors."},
  "Aspirin":    {ingredient:"Acetylsalicylic acid", cls:"NSAID/Antiplatelet", desc:"Reduces pain, fever, and platelet aggregation."},
  "Lipitor":    {ingredient:"Atorvastatin",      cls:"Statin",          desc:"Lowers LDL cholesterol by inhibiting HMG-CoA reductase."},
  "Paxil":      {ingredient:"Paroxetine",        cls:"SSRI",            desc:"Selective serotonin reuptake inhibitor for depression and anxiety."},
  "Prozac":     {ingredient:"Fluoxetine",        cls:"SSRI",            desc:"Increases serotonin levels; treats depression and OCD."},
  "Xanax":      {ingredient:"Alprazolam",        cls:"Benzodiazepine",  desc:"Short-term management of anxiety disorders."},
  "Metformin":  {ingredient:"Metformin HCl",     cls:"Biguanide",       desc:"First-line treatment for type 2 diabetes; reduces hepatic glucose output."},
  "Lisinopril": {ingredient:"Lisinopril",        cls:"ACE Inhibitor",   desc:"Treats high blood pressure and heart failure."},
  "Ibuprofen":  {ingredient:"Ibuprofen",         cls:"NSAID",           desc:"Reduces inflammation, pain, and fever."},
  "Amoxicillin":{ingredient:"Amoxicillin trihydrate", cls:"Antibiotic", desc:"Broad-spectrum penicillin antibiotic."},
  "Digoxin":    {ingredient:"Digoxin",           cls:"Cardiac Glycoside",desc:"Strengthens heart contractions; treats heart failure and AFib."},
  "Zoloft":     {ingredient:"Sertraline",        cls:"SSRI",            desc:"Treats depression, panic disorder, and PTSD."},
};

const ALL_INTERACTIONS = [
  {source:"Warfarin",   target:"Aspirin",    severity:"severe",   type:"Hematologic",    desc:"Concurrent use significantly increases bleeding risk due to additive antiplatelet and anticoagulant effects."},
  {source:"Warfarin",   target:"Ibuprofen",  severity:"severe",   type:"Hematologic",    desc:"NSAIDs inhibit platelet function and may displace Warfarin from protein binding, raising hemorrhage risk."},
  {source:"Warfarin",   target:"Amoxicillin",severity:"moderate", type:"Metabolic",      desc:"Antibiotics alter gut flora that produce Vitamin K, potentially increasing INR unpredictably."},
  {source:"Warfarin",   target:"Lipitor",    severity:"moderate", type:"Metabolic",      desc:"Atorvastatin inhibits CYP2C9, raising Warfarin plasma levels and anticoagulation effect."},
  {source:"Paxil",      target:"Zoloft",     severity:"severe",   type:"Neurological",   desc:"Combining SSRIs increases serotonin syndrome risk: hyperthermia, seizures, cardiovascular collapse."},
  {source:"Paxil",      target:"Prozac",     severity:"severe",   type:"Neurological",   desc:"Two SSRIs together can precipitate life-threatening serotonin syndrome."},
  {source:"Prozac",     target:"Zoloft",     severity:"severe",   type:"Neurological",   desc:"Dual SSRI therapy dramatically increases serotonin toxicity risk."},
  {source:"Xanax",      target:"Prozac",     severity:"moderate", type:"Neurological",   desc:"Fluoxetine inhibits CYP3A4, slowing Alprazolam metabolism and potentiating CNS depression."},
  {source:"Xanax",      target:"Paxil",      severity:"moderate", type:"Neurological",   desc:"Paroxetine raises Alprazolam exposure through CYP3A4 inhibition, increasing sedation risk."},
  {source:"Lisinopril", target:"Ibuprofen",  severity:"moderate", type:"Cardiovascular", desc:"NSAIDs blunt the antihypertensive effect of ACE inhibitors and may worsen renal function."},
  {source:"Lisinopril", target:"Metformin",  severity:"mild",     type:"Metabolic",      desc:"ACE inhibitors may slightly enhance insulin sensitivity, risk of hypoglycemia with Metformin."},
  {source:"Digoxin",    target:"Lisinopril", severity:"moderate", type:"Cardiovascular", desc:"ACE inhibitors can raise Digoxin levels through renal hemodynamic changes."},
  {source:"Digoxin",    target:"Aspirin",    severity:"mild",     type:"Hematologic",    desc:"Low-dose aspirin has minimal effect on Digoxin but GI bleeding risk is additive."},
  {source:"Lipitor",    target:"Digoxin",    severity:"moderate", type:"Metabolic",      desc:"Atorvastatin increases Digoxin AUC ~15% via P-glycoprotein inhibition — monitor Digoxin levels."},
  {source:"Metformin",  target:"Ibuprofen",  severity:"mild",     type:"Metabolic",      desc:"NSAIDs can impair renal function, reducing Metformin clearance and raising lactic acidosis risk."},
  {source:"Aspirin",    target:"Lisinopril", severity:"mild",     type:"Cardiovascular", desc:"High-dose aspirin may attenuate the hemodynamic benefits of ACE inhibitors in heart failure."},
];

// ─── STATE ───────────────────────────────────────────────────────────────────
let currentRoot = "Warfarin";
let history = [];
let simulation;

// ─── GRAPH BUILDER ───────────────────────────────────────────────────────────
function buildGraph(rootName) {
  if (history[history.length-1] !== rootName) {
    history.push(rootName);
    renderHistory();
  }
  currentRoot = rootName;

  const relEdges = ALL_INTERACTIONS.filter(
    e => e.source === rootName || e.target === rootName
  );
  const neighborNames = new Set([rootName]);
  relEdges.forEach(e => { neighborNames.add(e.source); neighborNames.add(e.target); });

  const nodes = [...neighborNames].map(n => ({
    id: n, isRoot: n === rootName, ...ALL_DRUGS[n]
  }));
  const links = relEdges.map(e => ({...e}));

  renderD3(nodes, links, rootName);
}

function renderHistory() {
  const bar = document.getElementById("history-bar");
  const chips = bar.querySelectorAll(".hist-chip");
  chips.forEach(c => c.remove());
  history.forEach((h, i) => {
    const chip = document.createElement("span");
    chip.className = "hist-chip";
    chip.textContent = h;
    chip.title = "Jump back to " + h;
    chip.onclick = () => {
      history = history.slice(0, i);
      buildGraph(h);
    };
    bar.appendChild(chip);
  });
}

// ─── D3 RENDER ───────────────────────────────────────────────────────────────
function renderD3(nodes, links, rootName) {
  const svg = d3.select("#svg");
  svg.selectAll("*").remove();

  const W = document.getElementById("graph-area").clientWidth;
  const H = document.getElementById("graph-area").clientHeight;

  const defs = svg.append("defs");
  ["severe","moderate","mild"].forEach(sev => {
    const col = sev==="severe"?"#f85149": sev==="moderate"?"#e3a400":"#3fb950";
    ["start","end"].forEach(pos => {
      defs.append("marker")
        .attr("id", `arrow-${sev}-${pos}`)
        .attr("viewBox","0 -5 10 10").attr("refX",22).attr("refY",0)
        .attr("markerWidth",6).attr("markerHeight",6)
        .attr("orient","auto")
        .append("path").attr("d","M0,-5L10,0L0,5").attr("fill",col).attr("opacity",0.7);
    });
  });

  const g = svg.append("g");

  // zoom + pan
  svg.call(d3.zoom().scaleExtent([0.3,3]).on("zoom", e => g.attr("transform", e.transform)));

  // init positions
  nodes.forEach(n => {
    if (n.isRoot) { n.x = W/2; n.y = H/2; n.fx = W/2; n.fy = H/2; }
    else { n.x = W/2 + (Math.random()-0.5)*200; n.y = H/2 + (Math.random()-0.5)*200; }
  });

  // force simulation
  if (simulation) simulation.stop();
  simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d=>d.id).distance(160).strength(0.6))
    .force("charge", d3.forceManyBody().strength(-420))
    .force("center", d3.forceCenter(W/2, H/2))
    .force("collision", d3.forceCollide(48));

  // edge dash patterns by type
  function dashArray(type, severity) {
    const base = type==="Hematologic"?"none": type==="Metabolic"?"10,4": type==="Cardiovascular"?"5,3": type==="Neurological"?"2,5":"2,2";
    return base;
  }
  function edgeColor(sev) {
    return sev==="severe"?"#f85149": sev==="moderate"?"#e3a400":"#3fb950";
  }
  function edgeWidth(sev) {
    return sev==="severe"?2.8: sev==="moderate"?2:1.6;
  }

  const linkSel = g.append("g").selectAll("line")
    .data(links).join("line")
    .attr("stroke", d => edgeColor(d.severity))
    .attr("stroke-width", d => edgeWidth(d.severity))
    .attr("stroke-dasharray", d => dashArray(d.type, d.severity))
    .attr("opacity", 0.75)
    .attr("marker-end", d => `url(#arrow-${d.severity}-end)`)
    .on("mouseover", function(event, d) {
      showTooltip(event, `<b>${d.source.id||d.source} ↔ ${d.target.id||d.target}</b><br/>
        <span style="color:#8b949e">${d.severity.toUpperCase()} · ${d.type}</span><br/>${d.desc}`);
    })
    .on("mouseout", hideTooltip);

  // node circles
  const nodeG = g.append("g").selectAll("g")
    .data(nodes).join("g")
    .attr("cursor","pointer")
    .call(d3.drag()
      .on("start", (event, d) => {
        if (!event.active) simulation.alphaTarget(0.4).restart();
        d.fx = d.x; d.fy = d.y;
      })
      .on("drag", (event, d) => { d.fx = event.x; d.fy = event.y; })
      .on("end", (event, d) => {
        if (!event.active) simulation.alphaTarget(0);
        if (!d.isRoot) { d.fx = null; d.fy = null; }
      })
    )
    .on("click", (event, d) => {
      event.stopPropagation();
      if (d.isRoot) showInfoCard(d);
      else buildGraph(d.id);
    })
    .on("mouseover", function(event, d) {
      showTooltip(event, `<b>${d.id}</b><br/><span style="color:#8b949e">${d.ingredient}</span>`);
    })
    .on("mouseout", hideTooltip);

  nodeG.append("circle")
    .attr("r", d => d.isRoot ? 28 : 20)
    .attr("fill", d => d.isRoot ? "#1f6feb" : "#21262d")
    .attr("stroke", d => d.isRoot ? "#58a6ff" : "#30363d")
    .attr("stroke-width", d => d.isRoot ? 3 : 1.5);

  nodeG.append("text")
    .attr("text-anchor","middle").attr("dy","0.35em")
    .attr("font-size", d => d.isRoot ? "11px" : "9.5px")
    .attr("fill","#e6edf3")
    .attr("pointer-events","none")
    .text(d => d.id.length > 10 ? d.id.slice(0,9)+"…" : d.id);

  simulation.on("tick", () => {
    linkSel
      .attr("x1", d => d.source.x).attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
    nodeG.attr("transform", d => `translate(${d.x},${d.y})`);
  });

  // unfix root after animation
  setTimeout(() => { nodes.find(n=>n.isRoot).fx = null; nodes.find(n=>n.isRoot).fy = null; }, 800);
}

// ─── INFO CARD ───────────────────────────────────────────────────────────────
function showInfoCard(drug) {
  const panel = document.getElementById("info-panel");
  panel.style.display = "block";
  const rels = ALL_INTERACTIONS.filter(e => e.source===drug.id || e.target===drug.id);
  const sevOrder = {severe:0, moderate:1, mild:2};
  rels.sort((a,b) => sevOrder[a.severity]-sevOrder[b.severity]);

  panel.innerHTML = `
    <h2>${drug.id}</h2>
    <div class="sub">${drug.cls}</div>
    <div class="label">Active Ingredient</div>
    <div class="val">${drug.ingredient}</div>
    <div class="label">Description</div>
    <div class="val">${drug.desc}</div>
    <div class="label" style="margin-top:14px">Negative Interactions (${rels.length})</div>
    ${rels.map(r => {
      const other = r.source===drug.id ? r.target : r.source;
      return `<div class="icard ${r.severity}">
        <div class="ic-title">${other} <span style="color:#8b949e;font-weight:400;font-size:.72rem">[${r.severity}]</span></div>
        <div class="ic-sub">${r.type} — ${r.desc}</div>
      </div>`;
    }).join("")}
    <button onclick="document.getElementById('info-panel').style.display='none'"
      style="margin-top:16px;background:#21262d;border:1px solid #30363d;color:#8b949e;
             padding:5px 12px;border-radius:6px;cursor:pointer;width:100%;font-size:.8rem">
      Close
    </button>`;
}

// ─── TOOLTIP ─────────────────────────────────────────────────────────────────
const tt = document.getElementById("tooltip");
function showTooltip(event, html) {
  tt.innerHTML = html; tt.style.display = "block";
  tt.style.left = (event.pageX+14)+"px"; tt.style.top = (event.pageY-10)+"px";
}
function hideTooltip() { tt.style.display = "none"; }

// ─── SEARCH ──────────────────────────────────────────────────────────────────
function searchInteraction() {
  const d1 = document.getElementById("drug1").value.trim();
  const d2 = document.getElementById("drug2").value.trim();
  const sr = document.getElementById("search-result");
  const srTitle = document.getElementById("sr-title");
  const srBody = document.getElementById("sr-body");

  if (!d1 || !d2) { srTitle.textContent="Enter both drug names"; srBody.textContent=""; sr.style.display="block"; return; }

  const match = ALL_INTERACTIONS.find(e =>
    (e.source.toLowerCase()===d1.toLowerCase() && e.target.toLowerCase()===d2.toLowerCase()) ||
    (e.source.toLowerCase()===d2.toLowerCase() && e.target.toLowerCase()===d1.toLowerCase())
  );

  if (match) {
    const col = match.severity==="severe"?"#f85149": match.severity==="moderate"?"#e3a400":"#3fb950";
    srTitle.innerHTML = `${match.source} ↔ ${match.target}`;
    srBody.innerHTML = `<span style="color:${col};font-weight:700">${match.severity.toUpperCase()}</span> · ${match.type}<br/><br/>${match.desc}`;
    history.push(`${d1}+${d2}`);
    renderHistory();
    buildGraph(match.source);
  } else {
    const known1 = ALL_DRUGS[Object.keys(ALL_DRUGS).find(k=>k.toLowerCase()===d1.toLowerCase())];
    const known2 = ALL_DRUGS[Object.keys(ALL_DRUGS).find(k=>k.toLowerCase()===d2.toLowerCase())];
    srTitle.textContent = "No interaction found";
    srBody.innerHTML = `No recorded negative interaction between <b>${d1}</b> and <b>${d2}</b> in ODMAP database.`;
    if (known1) buildGraph(Object.keys(ALL_DRUGS).find(k=>k.toLowerCase()===d1.toLowerCase()));
  }
  sr.style.display = "block";
}

// ─── INIT ────────────────────────────────────────────────────────────────────
window.onload = () => buildGraph("Warfarin");
window.onresize = () => buildGraph(currentRoot);
</script>
</body>
</html>"""

with open("./outputs/odmap.html", "w") as f:
    f.write(html)

from IPython.display import display, HTML
display(HTML(open("./outputs/odmap.html").read()), metadata={"alt": "ODMAP drug interaction network"})


# ## ODMAP v4 — Breadcrumb Trail · Saved List · Sources · Idle Rotation · Close Top-Left · History Autofill

# In[1]:


import os
os.makedirs("./outputs", exist_ok=True)

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>ODMAP — Drug Interaction Network</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#f5f0e8;color:#2d3a2e;font-family:'Segoe UI',sans-serif;display:flex;flex-direction:column;height:100vh;overflow:hidden}

  /* ── HEADER ── */
  #header{background:#2d3a2e;border-bottom:2px solid #4a6741;padding:8px 16px;display:flex;align-items:center;gap:12px;flex-shrink:0;flex-wrap:wrap}
  #header h1{font-size:1.15rem;color:#b8d4a8;letter-spacing:2px;font-weight:700;white-space:nowrap}
  #header .subtitle{font-size:.75rem;color:#7a9e72;white-space:nowrap}

  /* ── BREADCRUMB TRAIL ── */
  #breadcrumb-wrap{flex:1;display:flex;align-items:center;gap:0;overflow-x:auto;min-width:0;max-width:420px;scrollbar-width:thin;scrollbar-color:#4a6741 transparent}
  #breadcrumb-wrap::-webkit-scrollbar{height:3px}
  #breadcrumb-wrap::-webkit-scrollbar-thumb{background:#4a6741;border-radius:2px}
  #breadcrumb-inner{display:flex;align-items:center;gap:0;white-space:nowrap}
  .bc-step{font-size:.75rem;color:#b8d4a8;cursor:pointer;padding:3px 7px;border-radius:4px;transition:background .15s}
  .bc-step:hover{background:#3d4f3e}
  .bc-step.current{color:#e8f0e4;font-weight:600;background:#4a6741;cursor:default}
  .bc-arrow{color:#7a9e72;font-size:.75rem;padding:0 2px;user-select:none}

  /* ── SAVED LIST BUTTON ── */
  #saved-btn{background:#4a6741;border:1px solid #8fbe7c;color:#e8f0e4;padding:5px 11px;border-radius:6px;cursor:pointer;font-size:.78rem;font-weight:600;white-space:nowrap;flex-shrink:0}
  #saved-btn:hover{background:#5a7d50}

  /* ── SEARCH AREA ── */
  #search-area{display:flex;gap:8px;align-items:center;position:relative;flex-shrink:0}
  #search-area input{background:#3d4f3e;border:1px solid #4a6741;border-radius:6px;color:#e8f0e4;padding:5px 10px;font-size:.82rem;width:130px}
  #search-area input:focus{outline:none;border-color:#8fbe7c}
  #search-area input::placeholder{color:#7a9e72}
  #go-btn{background:#4a6741;border:none;color:#e8f0e4;padding:5px 12px;border-radius:6px;cursor:pointer;font-size:.82rem;font-weight:600}
  #go-btn:hover{background:#5a7d50}

  /* ── HISTORY DROPDOWN ── */
  #history-dropdown{display:none;position:absolute;top:100%;right:0;margin-top:4px;background:#2d3a2e;border:1px solid #4a6741;border-radius:8px;padding:8px 10px;z-index:1100;min-width:260px;box-shadow:0 4px 16px #0003}
  #history-dropdown .hist-label{font-size:.7rem;color:#7a9e72;margin-bottom:6px;display:block;text-transform:uppercase;letter-spacing:.8px}
  #history-dropdown .hist-chips{display:flex;flex-wrap:wrap;gap:5px}
  .hist-chip{background:#3d4f3e;border:1px solid #4a6741;border-radius:12px;padding:3px 10px;font-size:.75rem;cursor:pointer;color:#b8d4a8;white-space:nowrap}
  .hist-chip:hover{background:#4a6741}

  /* ── SEARCH RESULT POPUP ── */
  #search-result{position:fixed;top:56px;right:20px;background:#f0ebe0;border:1px solid #c5b99a;border-radius:8px;padding:14px 18px;z-index:999;display:none;max-width:320px;font-size:.85rem;line-height:1.6;color:#2d3a2e;box-shadow:0 4px 16px #0002}
  #search-result h3{color:#4a6741;margin-bottom:6px}
  #search-result .close-btn{float:right;cursor:pointer;color:#8a7e6a;font-size:1rem}

  /* ── SAVED LIST PANEL ── */
  #saved-panel{position:fixed;top:56px;left:50%;transform:translateX(-50%);background:#f0ebe0;border:1px solid #c5b99a;border-radius:10px;padding:16px 20px;z-index:1200;display:none;min-width:280px;max-width:360px;box-shadow:0 6px 24px #0003}
  #saved-panel h3{color:#4a6741;margin-bottom:10px;font-size:.95rem}
  #saved-panel .sp-close{float:right;cursor:pointer;color:#8a7e6a}
  #saved-input-row{display:flex;gap:8px;margin-bottom:8px}
  #saved-input{flex:1;background:#e8e0d0;border:1px solid #c5b99a;border-radius:6px;padding:5px 9px;font-size:.82rem;color:#2d3a2e}
  #saved-add-btn{background:#4a6741;border:none;color:#e8f0e4;padding:5px 12px;border-radius:6px;cursor:pointer;font-size:.82rem}
  #saved-add-btn:hover{background:#5a7d50}
  #saved-list-items{display:flex;flex-wrap:wrap;gap:6px;max-height:140px;overflow-y:auto}
  .saved-item{background:#d8eecf;border:1px solid #a0c896;border-radius:12px;padding:3px 10px;font-size:.78rem;color:#2d4a28;display:flex;align-items:center;gap:5px}
  .saved-item .si-remove{cursor:pointer;color:#c0392b;font-size:.85rem;line-height:1}
  .saved-item .si-remove:hover{color:#a93226}

  #main{display:flex;flex:1;overflow:hidden}
  #graph-area{flex:1;position:relative}
  svg{width:100%;height:100%}

  /* ── INFO PANEL ── */
  #info-panel{width:300px;background:#eee8d8;border-left:2px solid #c5b99a;overflow-y:auto;padding:0;flex-shrink:0;display:none;flex-direction:column}
  .card-top-bar{display:flex;align-items:center;justify-content:space-between;background:#ddd5c2;padding:8px 12px 0;border-bottom:none}
  .close-panel-btn-top{background:none;border:1px solid #c5b99a;border-radius:6px;color:#5a5040;padding:3px 9px;cursor:pointer;font-size:.78rem}
  .close-panel-btn-top:hover{background:#c5b99a;color:#2d3a2e}
  .card-header{background:#ddd5c2;padding:8px 18px 12px;border-bottom:1px solid #c5b99a}
  .card-brand{font-size:1.05rem;font-weight:700;color:#2d3a2e;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
  .card-class{font-size:.75rem;color:#7a6e5a;margin-top:2px}
  .pronunc-btn{background:#f5f0e8;border:1px solid #c5b99a;border-radius:6px;color:#4a6741;cursor:pointer;padding:3px 8px;font-size:.75rem;display:inline-flex;align-items:center;gap:4px;white-space:nowrap}
  .pronunc-btn:hover{background:#ddd5c2}
  .card-body{padding:12px 18px;flex:1}
  .card-section-title{font-size:.68rem;color:#7a6e5a;text-transform:uppercase;letter-spacing:1px;margin-top:12px;margin-bottom:3px;font-weight:600}
  .card-val{font-size:.83rem;color:#2d3a2e;line-height:1.5}
  .similar-chip{display:inline-block;background:#d8eecf;border:1px solid #a0c896;border-radius:10px;padding:2px 9px;font-size:.74rem;color:#3a5e34;margin:2px 2px 2px 0;cursor:pointer}
  .similar-chip:hover{background:#c5e0ba}
  .icard{background:#f0ebe0;border-radius:6px;padding:7px 9px;margin-top:7px;border-left:3px solid #4a6741}
  .icard .ic-title{font-size:.78rem;font-weight:600;color:#2d3a2e;display:flex;align-items:center;gap:5px}
  .ic-badge{font-size:.66rem;padding:1px 6px;border-radius:8px;font-weight:700;text-transform:uppercase}
  .ic-badge.severe{background:#c0392b22;color:#c0392b;border:1px solid #c0392b55}
  .ic-badge.moderate{background:#d4860022;color:#b8720a;border:1px solid #d4860055}
  .ic-badge.mild{background:#27ae6022;color:#27ae60;border:1px solid #27ae6055}
  .icard.severe{border-left-color:#c0392b}
  .icard.moderate{border-left-color:#d48600}
  .icard.mild{border-left-color:#27ae60}
  .icard .ic-sub{font-size:.73rem;color:#5a5040;margin-top:3px;line-height:1.4}
  .src-link{font-size:.7rem;color:#4a6741;text-decoration:none;display:inline-block;margin-top:4px}
  .src-link:hover{text-decoration:underline}

  /* ── LEGEND ── */
  #legend{position:absolute;bottom:14px;left:14px;background:#f0ebe0cc;border:1px solid #c5b99a;border-radius:8px;padding:10px 14px;font-size:.71rem;line-height:1.9;backdrop-filter:blur(4px)}
  #legend .leg-title{color:#7a6e5a;margin-bottom:2px;font-weight:600;font-size:.7rem;text-transform:uppercase;letter-spacing:.8px}
  .leg-row{display:flex;align-items:center;gap:7px;color:#3d3028}

  #tooltip{position:fixed;background:#2d3a2e;border:1px solid #4a6741;border-radius:6px;padding:6px 10px;font-size:.76rem;pointer-events:none;display:none;z-index:800;max-width:230px;line-height:1.5;color:#e8f0e4}
</style>
</head>
<body>

<div id="header">
  <h1>⬡ ODMAP</h1>
  <div class="subtitle">Drug Interaction Network</div>

  <!-- BREADCRUMB -->
  <div id="breadcrumb-wrap"><div id="breadcrumb-inner"></div></div>

  <!-- SAVED LIST -->
  <button id="saved-btn" onclick="toggleSavedPanel()">💊 Saved List</button>

  <!-- SEARCH -->
  <div id="search-area">
    <input id="drug1" placeholder="Drug 1" autocomplete="off"/>
    <input id="drug2" placeholder="Drug 2" autocomplete="off"/>
    <button id="go-btn" onclick="searchInteraction()">Go</button>
    <div id="history-dropdown">
      <span class="hist-label">Search History</span>
      <div class="hist-chips" id="hist-chips-container"></div>
    </div>
  </div>
</div>

<!-- SAVED LIST PANEL -->
<div id="saved-panel">
  <span class="sp-close" onclick="toggleSavedPanel()">✕</span>
  <h3>💊 My Saved Prescriptions</h3>
  <div id="saved-input-row">
    <input id="saved-input" placeholder="Add drug name…" autocomplete="off"/>
    <button id="saved-add-btn" onclick="addToSaved()">Add</button>
  </div>
  <div id="saved-list-items"></div>
</div>

<div id="search-result">
  <span class="close-btn" onclick="this.parentElement.style.display='none'">✕</span>
  <h3 id="sr-title"></h3>
  <div id="sr-body"></div>
</div>

<div id="main">
  <div id="graph-area">
    <svg id="svg"></svg>
    <div id="legend">
      <div class="leg-title">Severity</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#c0392b" stroke-width="2.5"/></svg> Severe</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#d48600" stroke-width="2" stroke-dasharray="6,3"/></svg> Moderate</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#27ae60" stroke-width="1.5" stroke-dasharray="2,3"/></svg> Mild</div>
      <div class="leg-title" style="margin-top:8px">Interaction Type</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#5a5040" stroke-width="2"/></svg> Hematologic</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#5a5040" stroke-width="2" stroke-dasharray="8,4"/></svg> Metabolic</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#5a5040" stroke-width="2" stroke-dasharray="4,2"/></svg> Cardiovascular</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#5a5040" stroke-width="2" stroke-dasharray="2,5"/></svg> Neurological</div>
      <div class="leg-title" style="margin-top:8px">Saved List</div>
      <div class="leg-row"><svg width="28" height="10"><circle cx="14" cy="5" r="4" fill="none" stroke="#a855f7" stroke-width="2.5"/></svg> Conflicts w/ saved</div>
    </div>
  </div>
  <div id="info-panel"></div>
</div>
<div id="tooltip"></div>

<script>
// ─── DATA ────────────────────────────────────────────────────────────────────
const ALL_DRUGS = {
  "Warfarin":   {ingredient:"Warfarin sodium",        pronounce:"WAR-fuh-rin",     cls:"Anticoagulant",        similar:["Coumadin","Jantoven"],               source:"https://www.fda.gov/drugs/drug-safety-and-availability/fda-drug-safety-communication-revised-recommendations-coadministration-blood-thinner-warfarin",  desc:"Prevents blood clots by inhibiting Vitamin K-dependent clotting factors."},
  "Aspirin":    {ingredient:"Acetylsalicylic acid",   pronounce:"AS-pir-in",       cls:"NSAID / Antiplatelet", similar:["Bayer","Bufferin","Ecotrin"],         source:"https://www.ncbi.nlm.nih.gov/books/NBK519032/",                                                                                               desc:"Reduces pain, fever, and platelet aggregation."},
  "Lipitor":    {ingredient:"Atorvastatin",           pronounce:"LIP-ih-tor",      cls:"Statin",               similar:["Torvast"],                           source:"https://www.ncbi.nlm.nih.gov/books/NBK430882/",                                                                                               desc:"Lowers LDL cholesterol by inhibiting HMG-CoA reductase."},
  "Paxil":      {ingredient:"Paroxetine",             pronounce:"PAX-il",          cls:"SSRI",                 similar:["Pexeva","Brisdelle"],                source:"https://www.ncbi.nlm.nih.gov/books/NBK546090/",                                                                                               desc:"Selective serotonin reuptake inhibitor for depression and anxiety."},
  "Prozac":     {ingredient:"Fluoxetine",             pronounce:"PRO-zak",         cls:"SSRI",                 similar:["Sarafem","Rapiflux"],                source:"https://www.ncbi.nlm.nih.gov/books/NBK459223/",                                                                                               desc:"Increases serotonin levels; treats depression and OCD."},
  "Xanax":      {ingredient:"Alprazolam",             pronounce:"ZAN-ax",          cls:"Benzodiazepine",       similar:["Niravam","Alprazolam ER"],           source:"https://www.ncbi.nlm.nih.gov/books/NBK538165/",                                                                                               desc:"Short-term management of anxiety disorders."},
  "Metformin":  {ingredient:"Metformin HCl",          pronounce:"met-FOR-min",     cls:"Biguanide",            similar:["Glucophage","Fortamet","Glumetza"],  source:"https://www.ncbi.nlm.nih.gov/books/NBK518983/",                                                                                               desc:"First-line treatment for type 2 diabetes; reduces hepatic glucose output."},
  "Lisinopril": {ingredient:"Lisinopril",             pronounce:"lye-SIN-oh-pril", cls:"ACE Inhibitor",        similar:["Zestril","Prinivil","Qbrelis"],      source:"https://www.ncbi.nlm.nih.gov/books/NBK482440/",                                                                                               desc:"Treats high blood pressure and heart failure."},
  "Advil":      {ingredient:"Ibuprofen",              pronounce:"AD-vil",          cls:"NSAID",                similar:["Motrin","Nuprin","Ibuprofen"],       source:"https://www.ncbi.nlm.nih.gov/books/NBK526103/",                                                                                               desc:"Reduces inflammation, pain, and fever."},
  "Amoxil":     {ingredient:"Amoxicillin trihydrate", pronounce:"a-MOX-il",        cls:"Antibiotic",           similar:["Trimox","Moxatag","Amoxicillin"],    source:"https://www.ncbi.nlm.nih.gov/books/NBK482250/",                                                                                               desc:"Broad-spectrum penicillin antibiotic."},
  "Lanoxin":    {ingredient:"Digoxin",                pronounce:"la-NOX-in",       cls:"Cardiac Glycoside",    similar:["Digitek","Digoxin"],                 source:"https://www.ncbi.nlm.nih.gov/books/NBK470554/",                                                                                               desc:"Strengthens heart contractions; treats heart failure and AFib."},
  "Zoloft":     {ingredient:"Sertraline",             pronounce:"ZO-loft",         cls:"SSRI",                 similar:["Lustral"],                           source:"https://www.ncbi.nlm.nih.gov/books/NBK547849/",                                                                                               desc:"Treats depression, panic disorder, and PTSD."},
};

const ALL_INTERACTIONS = [
  {source:"Warfarin",  target:"Aspirin",    severity:"severe",   type:"Hematologic",    desc:"Concurrent use significantly increases bleeding risk due to additive antiplatelet and anticoagulant effects.",source:"https://pubmed.ncbi.nlm.nih.gov/15692077/"},
  {source:"Warfarin",  target:"Advil",      severity:"severe",   type:"Hematologic",    desc:"NSAIDs inhibit platelet function and may displace Warfarin from protein binding, raising hemorrhage risk.",source:"https://pubmed.ncbi.nlm.nih.gov/17938526/"},
  {source:"Warfarin",  target:"Amoxil",     severity:"moderate", type:"Metabolic",      desc:"Antibiotics alter gut flora that produce Vitamin K, potentially increasing INR unpredictably.",source:"https://pubmed.ncbi.nlm.nih.gov/11902657/"},
  {source:"Warfarin",  target:"Lipitor",    severity:"moderate", type:"Metabolic",      desc:"Atorvastatin inhibits CYP2C9, raising Warfarin plasma levels and anticoagulation effect.",source:"https://pubmed.ncbi.nlm.nih.gov/12163597/"},
  {source:"Paxil",     target:"Zoloft",     severity:"severe",   type:"Neurological",   desc:"Combining SSRIs increases serotonin syndrome risk: hyperthermia, seizures, cardiovascular collapse.",source:"https://pubmed.ncbi.nlm.nih.gov/15820243/"},
  {source:"Paxil",     target:"Prozac",     severity:"severe",   type:"Neurological",   desc:"Two SSRIs together can precipitate life-threatening serotonin syndrome.",source:"https://pubmed.ncbi.nlm.nih.gov/15820243/"},
  {source:"Prozac",    target:"Zoloft",     severity:"severe",   type:"Neurological",   desc:"Dual SSRI therapy dramatically increases serotonin toxicity risk.",source:"https://pubmed.ncbi.nlm.nih.gov/15820243/"},
  {source:"Xanax",     target:"Prozac",     severity:"moderate", type:"Neurological",   desc:"Fluoxetine inhibits CYP3A4, slowing Alprazolam metabolism and potentiating CNS depression.",source:"https://pubmed.ncbi.nlm.nih.gov/9063941/"},
  {source:"Xanax",     target:"Paxil",      severity:"moderate", type:"Neurological",   desc:"Paroxetine raises Alprazolam exposure through CYP3A4 inhibition, increasing sedation risk.",source:"https://pubmed.ncbi.nlm.nih.gov/9063941/"},
  {source:"Lisinopril",target:"Advil",      severity:"moderate", type:"Cardiovascular", desc:"NSAIDs blunt the antihypertensive effect of ACE inhibitors and may worsen renal function.",source:"https://pubmed.ncbi.nlm.nih.gov/11756079/"},
  {source:"Lisinopril",target:"Metformin",  severity:"mild",     type:"Metabolic",      desc:"ACE inhibitors may slightly enhance insulin sensitivity, risk of hypoglycemia with Metformin.",source:"https://pubmed.ncbi.nlm.nih.gov/10480611/"},
  {source:"Lanoxin",   target:"Lisinopril", severity:"moderate", type:"Cardiovascular", desc:"ACE inhibitors can raise Digoxin levels through renal hemodynamic changes.",source:"https://pubmed.ncbi.nlm.nih.gov/1662795/"},
  {source:"Lanoxin",   target:"Aspirin",    severity:"mild",     type:"Hematologic",    desc:"Low-dose aspirin has minimal effect on Digoxin but GI bleeding risk is additive.",source:"https://pubmed.ncbi.nlm.nih.gov/1662795/"},
  {source:"Lipitor",   target:"Lanoxin",    severity:"moderate", type:"Metabolic",      desc:"Atorvastatin increases Digoxin AUC ~15% via P-glycoprotein inhibition — monitor levels.",source:"https://pubmed.ncbi.nlm.nih.gov/12163597/"},
  {source:"Metformin", target:"Advil",      severity:"mild",     type:"Metabolic",      desc:"NSAIDs can impair renal function, reducing Metformin clearance and raising lactic acidosis risk.",source:"https://pubmed.ncbi.nlm.nih.gov/12667685/"},
  {source:"Aspirin",   target:"Lisinopril", severity:"mild",     type:"Cardiovascular", desc:"High-dose aspirin may attenuate the hemodynamic benefits of ACE inhibitors in heart failure.",source:"https://pubmed.ncbi.nlm.nih.gov/11756079/"},
];

// ─── STATE ───────────────────────────────────────────────────────────────────
let currentRoot = "Warfarin";
let clickTrail  = [];   // breadcrumb trail
let history     = [];   // search history for dropdown
let savedList   = [];   // user's saved prescriptions
let simulation;
let rotationTimer = null;
let rotationAngle = 0;
let isInteracting = false;
let idleTimeout   = null;
let gTransform    = {x:0,y:0,k:1};
let currentNodes  = [];

// ─── HISTORY DROPDOWN ────────────────────────────────────────────────────────
(function(){
  const d1 = document.getElementById("drug1");
  const d2 = document.getElementById("drug2");
  const drop = document.getElementById("history-dropdown");
  let activeInput = null;

  function showDrop(input){ activeInput = input; renderHistChips(); drop.style.display = history.length ? "block" : "none"; }
  function hideDrop(){ setTimeout(()=>{ if(!drop.contains(document.activeElement)) drop.style.display="none"; }, 150); }
  d1.addEventListener("focus", ()=>showDrop(d1));
  d2.addEventListener("focus", ()=>showDrop(d2));
  d1.addEventListener("blur",  hideDrop);
  d2.addEventListener("blur",  hideDrop);

  window._activeSearchInput = ()=>activeInput;
})();

function renderHistChips(){
  const container = document.getElementById("hist-chips-container");
  container.innerHTML = "";
  history.forEach((h, i) => {
    const chip = document.createElement("span");
    chip.className = "hist-chip";
    chip.textContent = h;
    chip.onmousedown = (e) => {
      e.preventDefault();
      const inp = window._activeSearchInput();
      if(inp) inp.value = h;   // autofill the focused input
      document.getElementById("history-dropdown").style.display = "none";
      const key = Object.keys(ALL_DRUGS).find(k=>k.toLowerCase()===h.toLowerCase());
      if(key) buildGraph(key);
    };
    container.appendChild(chip);
  });
  document.getElementById("history-dropdown").style.display = history.length ? "block" : "none";
}

// ─── BREADCRUMB ──────────────────────────────────────────────────────────────
function updateBreadcrumb(){
  const inner = document.getElementById("breadcrumb-inner");
  inner.innerHTML = "";
  clickTrail.forEach((name, i) => {
    if(i > 0){
      const arr = document.createElement("span");
      arr.className = "bc-arrow"; arr.textContent = "›";
      inner.appendChild(arr);
    }
    const step = document.createElement("span");
    step.className = "bc-step" + (i===clickTrail.length-1 ? " current" : "");
    step.textContent = name;
    if(i < clickTrail.length-1){
      step.onclick = ()=>{ clickTrail = clickTrail.slice(0,i+1); buildGraph(name, true); };
    }
    inner.appendChild(step);
  });
  // auto-scroll to end
  const wrap = document.getElementById("breadcrumb-wrap");
  setTimeout(()=>{ wrap.scrollLeft = wrap.scrollWidth; }, 50);
}

// ─── SAVED LIST ──────────────────────────────────────────────────────────────
function toggleSavedPanel(){
  const p = document.getElementById("saved-panel");
  p.style.display = p.style.display==="block" ? "none" : "block";
}
function addToSaved(){
  const inp = document.getElementById("saved-input");
  const val = inp.value.trim();
  if(!val) return;
  if(!savedList.includes(val)){ savedList.push(val); renderSavedList(); refreshGraph(); }
  inp.value = "";
}
function removeFromSaved(name){
  savedList = savedList.filter(s=>s!==name);
  renderSavedList(); refreshGraph();
}
function renderSavedList(){
  const container = document.getElementById("saved-list-items");
  container.innerHTML = "";
  savedList.forEach(name => {
    const el = document.createElement("div");
    el.className = "saved-item";
    el.innerHTML = `${name}<span class="si-remove" onclick="removeFromSaved('${name}')">✕</span>`;
    container.appendChild(el);
  });
}
function conflictsWithSaved(drugName){
  return savedList.some(saved => {
    const n = saved.toLowerCase();
    return ALL_INTERACTIONS.some(e =>
      (e.source.toLowerCase()===drugName.toLowerCase() && e.target.toLowerCase()===n) ||
      (e.target.toLowerCase()===drugName.toLowerCase() && e.source.toLowerCase()===n)
    );
  });
}
function refreshGraph(){ buildGraph(currentRoot, true); }
document.getElementById("saved-input").addEventListener("keydown", e=>{ if(e.key==="Enter") addToSaved(); });

// ─── PRONUNCIATION ────────────────────────────────────────────────────────────
function pronounce(text) {
  if (!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.rate = 0.85; u.pitch = 1.0; u.lang = "en-US";
  window.speechSynthesis.speak(u);
}

// ─── IDLE ROTATION ───────────────────────────────────────────────────────────
function startRotation(){
  if(rotationTimer) return;
  const g = d3.select("#svg g");
  rotationTimer = setInterval(()=>{
    if(isInteracting || !currentNodes.length) return;
    rotationAngle += 0.003;   // radians per tick (~0.17 deg)
    const W = document.getElementById("graph-area").clientWidth;
    const H = document.getElementById("graph-area").clientHeight;
    const cx = W/2, cy = H/2;
    currentNodes.forEach(n => {
      if(n.fx_frozen != null) return;
      const dx = n.x - cx, dy = n.y - cy;
      const r = Math.sqrt(dx*dx+dy*dy);
      const a = Math.atan2(dy,dx) + 0.003;
      n.x = cx + r*Math.cos(a);
      n.y = cy + r*Math.sin(a);
    });
    if(simulation) simulation.alpha(0.05).restart();
  }, 40);
}
function resetIdle(){
  isInteracting = true;
  clearTimeout(idleTimeout);
  idleTimeout = setTimeout(()=>{ isInteracting=false; }, 3000);
}
document.addEventListener("mousemove", resetIdle);
document.addEventListener("mousedown", resetIdle);

// ─── GRAPH BUILDER ────────────────────────────────────────────────────────────
function buildGraph(rootName, silent=false) {
  if(!silent){ if(clickTrail[clickTrail.length-1] !== rootName) clickTrail.push(rootName); }
  if(history[history.length-1] !== rootName) history.push(rootName);
  currentRoot = rootName;
  updateBreadcrumb();

  const relEdges = ALL_INTERACTIONS.filter(e => e.source===rootName || e.target===rootName);
  const neighborNames = new Set([rootName]);
  relEdges.forEach(e => { neighborNames.add(e.source); neighborNames.add(e.target); });
  const nodes = [...neighborNames].map(n => ({ id:n, isRoot:n===rootName, ...ALL_DRUGS[n] }));
  currentNodes = nodes;
  renderD3(nodes, relEdges.map(e=>({...e})), rootName);
}

// ─── D3 RENDER ────────────────────────────────────────────────────────────────
function renderD3(nodes, links, rootName) {
  const svg = d3.select("#svg");
  svg.selectAll("*").remove();

  const W = document.getElementById("graph-area").clientWidth;
  const H = document.getElementById("graph-area").clientHeight;

  const defs = svg.append("defs");
  ["severe","moderate","mild"].forEach(sev => {
    const col = sev==="severe"?"#c0392b": sev==="moderate"?"#d48600":"#27ae60";
    defs.append("marker").attr("id",`arrow-${sev}`)
      .attr("viewBox","0 -5 10 10").attr("refX",22).attr("refY",0)
      .attr("markerWidth",6).attr("markerHeight",6).attr("orient","auto")
      .append("path").attr("d","M0,-5L10,0L0,5").attr("fill",col).attr("opacity",.8);
  });

  const g = svg.append("g");
  svg.call(d3.zoom().scaleExtent([0.25,3]).on("zoom", e => { gTransform=e.transform; g.attr("transform", e.transform); }));

  nodes.forEach(n => {
    if(n.isRoot){ n.x=W/2; n.y=H/2; n.fx=W/2; n.fy=H/2; }
    else { n.x=W/2+(Math.random()-.5)*220; n.y=H/2+(Math.random()-.5)*220; }
  });

  if(simulation) simulation.stop();
  simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d=>d.id).distance(175).strength(0.55))
    .force("charge", d3.forceManyBody().strength(-480))
    .force("center", d3.forceCenter(W/2, H/2))
    .force("collision", d3.forceCollide(52));

  const edgeColor = s => s==="severe"?"#c0392b": s==="moderate"?"#d48600":"#27ae60";
  const edgeWidth = s => s==="severe"?2.8: s==="moderate"?2:1.6;
  const dashArray  = t => t==="Hematologic"?"none": t==="Metabolic"?"10,4": t==="Cardiovascular"?"5,3":"2,5";

  const linkSel = g.append("g").selectAll("line").data(links).join("line")
    .attr("stroke", d => edgeColor(d.severity))
    .attr("stroke-width", d => edgeWidth(d.severity))
    .attr("stroke-dasharray", d => dashArray(d.type))
    .attr("opacity",.82)
    .attr("marker-end", d => `url(#arrow-${d.severity})`)
    .on("mouseover",(event,d)=>showTooltip(event,
      `<b>${d.source.id||d.source} ↔ ${d.target.id||d.target}</b><br/>
       <span style="color:#b8d4a8">${d.severity.toUpperCase()} · ${d.type}</span><br/>${d.desc}`))
    .on("mouseout", hideTooltip);

  const nodeG = g.append("g").selectAll("g").data(nodes).join("g")
    .attr("cursor","pointer")
    .call(d3.drag()
      .on("start",(event,d)=>{ resetIdle(); if(!event.active) simulation.alphaTarget(.4).restart(); d.fx=d.x; d.fy=d.y; })
      .on("drag",(event,d)=>{ d.fx=event.x; d.fy=event.y; })
      .on("end",(event,d)=>{ if(!event.active) simulation.alphaTarget(0); if(!d.isRoot){d.fx=null;d.fy=null;} }))
    .on("click",(event,d)=>{
      event.stopPropagation(); resetIdle();
      if(d.isRoot){ showInfoCard(d); }
      else { buildGraph(d.id); }
    })
    .on("mouseover",(event,d)=>showTooltip(event,
      `<b>${d.id}</b><br/><span style="color:#b8d4a8">${d.ingredient}</span><br/>
       <span style="color:#8fbe7c;font-size:.72rem">Click to ${d.isRoot?'see info card':'explore'}</span>`))
    .on("mouseout", hideTooltip);

  nodeG.append("circle")
    .attr("r", d=>d.isRoot?30:21)
    .attr("fill", d=>d.isRoot?"#4a6741":"#ddd5c2")
    .attr("stroke", d=>{
      if(conflictsWithSaved(d.id)) return "#a855f7";
      return d.isRoot?"#8fbe7c":"#a09080";
    })
    .attr("stroke-width", d=>conflictsWithSaved(d.id)?3.5:(d.isRoot?3:1.5))
    .attr("stroke-dasharray", d=>conflictsWithSaved(d.id)?"6,3":"none");

  nodeG.append("text")
    .attr("text-anchor","middle").attr("dy","0.35em")
    .attr("font-size", d=>d.isRoot?"11px":"9.5px")
    .attr("fill", d=>d.isRoot?"#e8f0e4":"#2d3a2e")
    .attr("font-weight", d=>d.isRoot?"700":"400")
    .attr("pointer-events","none")
    .text(d=>d.id.length>10?d.id.slice(0,9)+"…":d.id);

  simulation.on("tick",()=>{
    linkSel.attr("x1",d=>d.source.x).attr("y1",d=>d.source.y)
            .attr("x2",d=>d.target.x).attr("y2",d=>d.target.y);
    nodeG.attr("transform",d=>`translate(${d.x},${d.y})`);
  });

  setTimeout(()=>{ const r=nodes.find(n=>n.isRoot); r.fx=null; r.fy=null; }, 900);
  startRotation();
}

// ─── INFO CARD ────────────────────────────────────────────────────────────────
function showInfoCard(drug) {
  const panel = document.getElementById("info-panel");
  panel.style.display = "flex";
  panel.style.flexDirection = "column";

  const rels = ALL_INTERACTIONS
    .filter(e => e.source===drug.id || e.target===drug.id)
    .sort((a,b)=>({severe:0,moderate:1,mild:2}[a.severity]-({severe:0,moderate:1,mild:2}[b.severity])));

  const similarHTML = (drug.similar||[]).sort()
    .map(s=>`<span class="similar-chip" title="Same ingredient: ${drug.ingredient}">${s}</span>`).join("");

  panel.innerHTML = `
    <div class="card-top-bar">
      <button class="close-panel-btn-top" onclick="document.getElementById('info-panel').style.display='none'">✕ Close</button>
    </div>
    <div class="card-header">
      <div class="card-brand">
        ${drug.id}
        <button class="pronunc-btn" onclick="pronounce('${drug.pronounce||drug.id}')" title="Pronounce">
          🔊 ${drug.pronounce||drug.id}
        </button>
      </div>
      <div class="card-class">${drug.cls}</div>
    </div>
    <div class="card-body">
      <div class="card-section-title">Active Ingredient</div>
      <div class="card-val">${drug.ingredient}</div>

      <div class="card-section-title">Description</div>
      <div class="card-val">${drug.desc}
        <a class="src-link" href="${drug.source}" target="_blank" rel="noopener">📎 Source</a>
      </div>

      <div class="card-section-title">Same Medication — Other Brand Names</div>
      <div style="margin-top:4px">${similarHTML||'<span style="color:#8a7e6a;font-size:.8rem">None listed</span>'}</div>

      <div class="card-section-title" style="margin-top:14px">
        Negative Interactions
        <span style="background:#c0392b22;color:#c0392b;border:1px solid #c0392b55;border-radius:8px;padding:1px 7px;font-size:.68rem;margin-left:6px">${rels.length}</span>
      </div>
      ${rels.map(r=>{
        const other = r.source===drug.id ? r.target : r.source;
        return `<div class="icard ${r.severity}">
          <div class="ic-title">
            <span style="cursor:pointer;color:#4a6741;font-weight:600" onclick="buildGraph('${other}')">${other}</span>
            <span class="ic-badge ${r.severity}">${r.severity}</span>
            <span style="color:#7a6e5a;font-size:.7rem;margin-left:auto">${r.type}</span>
          </div>
          <div class="ic-sub">${r.desc}
            <a class="src-link" href="${r.source}" target="_blank" rel="noopener">📎 Source</a>
          </div>
        </div>`;
      }).join("")}
    </div>`;
}

// ─── TOOLTIP ─────────────────────────────────────────────────────────────────
const tt = document.getElementById("tooltip");
function showTooltip(event, html){ tt.innerHTML=html; tt.style.display="block"; tt.style.left=(event.pageX+14)+"px"; tt.style.top=(event.pageY-10)+"px"; }
function hideTooltip(){ tt.style.display="none"; }

// ─── SEARCH ──────────────────────────────────────────────────────────────────
function searchInteraction(){
  const d1=document.getElementById("drug1").value.trim();
  const d2=document.getElementById("drug2").value.trim();
  const sr=document.getElementById("search-result");
  const srTitle=document.getElementById("sr-title");
  const srBody=document.getElementById("sr-body");

  if(!d1||!d2){ srTitle.textContent="Enter both drug names"; srBody.textContent=""; sr.style.display="block"; return; }

  const match=ALL_INTERACTIONS.find(e=>
    (e.source.toLowerCase()===d1.toLowerCase()&&e.target.toLowerCase()===d2.toLowerCase())||
    (e.source.toLowerCase()===d2.toLowerCase()&&e.target.toLowerCase()===d1.toLowerCase())
  );

  if(match){
    const col=match.severity==="severe"?"#c0392b":match.severity==="moderate"?"#d48600":"#27ae60";
    srTitle.innerHTML=`${match.source} ↔ ${match.target}`;
    srBody.innerHTML=`<span style="color:${col};font-weight:700">${match.severity.toUpperCase()}</span> · ${match.type}<br/><br/>${match.desc}<br/><a class="src-link" href="${match.source}" target="_blank" rel="noopener">📎 Source</a>`;
    if(history[history.length-1]!==`${d1}+${d2}`) history.push(`${d1}+${d2}`);
    buildGraph(match.source);
  } else {
    srTitle.textContent="No interaction found";
    srBody.innerHTML=`No recorded negative interaction between <b>${d1}</b> and <b>${d2}</b> in ODMAP database.`;
    const key=Object.keys(ALL_DRUGS).find(k=>k.toLowerCase()===d1.toLowerCase());
    if(key) buildGraph(key);
  }
  sr.style.display="block";
}

document.addEventListener("keydown", e=>{ if(e.key==="Enter"&&(document.activeElement.id==="drug1"||document.activeElement.id==="drug2")) searchInteraction(); });

// ─── INIT ────────────────────────────────────────────────────────────────────
window.onload  = ()=>buildGraph("Warfarin");
window.onresize= ()=>buildGraph(currentRoot, true);
</script>
</body>
</html>"""

with open("./outputs/odmap_v4.html", "w") as f:
    f.write(html)

from IPython.display import display, HTML
display(HTML(open("./outputs/odmap_v4.html").read()), metadata={"alt": "ODMAP v4 drug network"})


# ## ODMAP v5 — Bug Fix: Duplicate `source` Key + Links Out of Node Titles

# In[2]:


import os
os.makedirs("./outputs", exist_ok=True)

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>ODMAP — Drug Interaction Network</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#f5f0e8;color:#2d3a2e;font-family:'Segoe UI',sans-serif;display:flex;flex-direction:column;height:100vh;overflow:hidden}

  #header{background:#2d3a2e;border-bottom:2px solid #4a6741;padding:8px 16px;display:flex;align-items:center;gap:12px;flex-shrink:0;flex-wrap:wrap}
  #header h1{font-size:1.15rem;color:#b8d4a8;letter-spacing:2px;font-weight:700;white-space:nowrap}
  #header .subtitle{font-size:.75rem;color:#7a9e72;white-space:nowrap}

  #breadcrumb-wrap{flex:1;display:flex;align-items:center;overflow-x:auto;min-width:0;max-width:420px;scrollbar-width:thin;scrollbar-color:#4a6741 transparent}
  #breadcrumb-wrap::-webkit-scrollbar{height:3px}
  #breadcrumb-wrap::-webkit-scrollbar-thumb{background:#4a6741;border-radius:2px}
  #breadcrumb-inner{display:flex;align-items:center;white-space:nowrap}
  .bc-step{font-size:.75rem;color:#b8d4a8;cursor:pointer;padding:3px 7px;border-radius:4px}
  .bc-step:hover{background:#3d4f3e}
  .bc-step.current{color:#e8f0e4;font-weight:600;background:#4a6741;cursor:default}
  .bc-arrow{color:#7a9e72;font-size:.75rem;padding:0 2px;user-select:none}

  #saved-btn{background:#4a6741;border:1px solid #8fbe7c;color:#e8f0e4;padding:5px 11px;border-radius:6px;cursor:pointer;font-size:.78rem;font-weight:600;white-space:nowrap;flex-shrink:0}
  #saved-btn:hover{background:#5a7d50}

  #search-area{display:flex;gap:8px;align-items:center;position:relative;flex-shrink:0}
  #search-area input{background:#3d4f3e;border:1px solid #4a6741;border-radius:6px;color:#e8f0e4;padding:5px 10px;font-size:.82rem;width:130px}
  #search-area input:focus{outline:none;border-color:#8fbe7c}
  #search-area input::placeholder{color:#7a9e72}
  #go-btn{background:#4a6741;border:none;color:#e8f0e4;padding:5px 12px;border-radius:6px;cursor:pointer;font-size:.82rem;font-weight:600}
  #go-btn:hover{background:#5a7d50}

  #history-dropdown{display:none;position:absolute;top:100%;right:0;margin-top:4px;background:#2d3a2e;border:1px solid #4a6741;border-radius:8px;padding:8px 10px;z-index:1100;min-width:260px;box-shadow:0 4px 16px #0003}
  #history-dropdown .hist-label{font-size:.7rem;color:#7a9e72;margin-bottom:6px;display:block;text-transform:uppercase;letter-spacing:.8px}
  .hist-chip{background:#3d4f3e;border:1px solid #4a6741;border-radius:12px;padding:3px 10px;font-size:.75rem;cursor:pointer;color:#b8d4a8;white-space:nowrap}
  .hist-chip:hover{background:#4a6741}

  #search-result{position:fixed;top:56px;right:20px;background:#f0ebe0;border:1px solid #c5b99a;border-radius:8px;padding:14px 18px;z-index:999;display:none;max-width:320px;font-size:.85rem;line-height:1.6;color:#2d3a2e;box-shadow:0 4px 16px #0002}
  #search-result h3{color:#4a6741;margin-bottom:6px}
  #search-result .close-btn{float:right;cursor:pointer;color:#8a7e6a}

  #saved-panel{position:fixed;top:56px;left:50%;transform:translateX(-50%);background:#f0ebe0;border:1px solid #c5b99a;border-radius:10px;padding:16px 20px;z-index:1200;display:none;min-width:280px;max-width:360px;box-shadow:0 6px 24px #0003}
  #saved-panel h3{color:#4a6741;margin-bottom:10px;font-size:.95rem}
  #saved-panel .sp-close{float:right;cursor:pointer;color:#8a7e6a}
  #saved-input-row{display:flex;gap:8px;margin-bottom:8px}
  #saved-input{flex:1;background:#e8e0d0;border:1px solid #c5b99a;border-radius:6px;padding:5px 9px;font-size:.82rem;color:#2d3a2e}
  #saved-add-btn{background:#4a6741;border:none;color:#e8f0e4;padding:5px 12px;border-radius:6px;cursor:pointer;font-size:.82rem}
  #saved-add-btn:hover{background:#5a7d50}
  #saved-list-items{display:flex;flex-wrap:wrap;gap:6px;max-height:140px;overflow-y:auto}
  .saved-item{background:#d8eecf;border:1px solid #a0c896;border-radius:12px;padding:3px 10px;font-size:.78rem;color:#2d4a28;display:flex;align-items:center;gap:5px}
  .saved-item .si-remove{cursor:pointer;color:#c0392b;font-size:.85rem}

  #main{display:flex;flex:1;overflow:hidden}
  #graph-area{flex:1;position:relative}
  svg{width:100%;height:100%}

  #info-panel{width:300px;background:#eee8d8;border-left:2px solid #c5b99a;overflow-y:auto;padding:0;flex-shrink:0;display:none;flex-direction:column}
  .card-top-bar{display:flex;align-items:center;justify-content:flex-start;background:#ddd5c2;padding:8px 12px 0}
  .close-panel-btn-top{background:none;border:1px solid #c5b99a;border-radius:6px;color:#5a5040;padding:3px 9px;cursor:pointer;font-size:.78rem}
  .close-panel-btn-top:hover{background:#c5b99a;color:#2d3a2e}
  .card-header{background:#ddd5c2;padding:8px 18px 12px;border-bottom:1px solid #c5b99a}
  .card-brand{font-size:1.05rem;font-weight:700;color:#2d3a2e;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
  .card-class{font-size:.75rem;color:#7a6e5a;margin-top:2px}
  .pronunc-btn{background:#f5f0e8;border:1px solid #c5b99a;border-radius:6px;color:#4a6741;cursor:pointer;padding:3px 8px;font-size:.75rem;display:inline-flex;align-items:center;gap:4px;white-space:nowrap}
  .pronunc-btn:hover{background:#ddd5c2}
  .card-body{padding:12px 18px;flex:1}
  .card-section-title{font-size:.68rem;color:#7a6e5a;text-transform:uppercase;letter-spacing:1px;margin-top:12px;margin-bottom:3px;font-weight:600}
  .card-val{font-size:.83rem;color:#2d3a2e;line-height:1.5}
  .similar-chip{display:inline-block;background:#d8eecf;border:1px solid #a0c896;border-radius:10px;padding:2px 9px;font-size:.74rem;color:#3a5e34;margin:2px 2px 2px 0;cursor:pointer}
  .similar-chip:hover{background:#c5e0ba}
  .icard{background:#f0ebe0;border-radius:6px;padding:7px 9px;margin-top:7px;border-left:3px solid #4a6741}
  .icard .ic-title{font-size:.78rem;font-weight:600;color:#2d3a2e;display:flex;align-items:center;gap:5px}
  .ic-badge{font-size:.66rem;padding:1px 6px;border-radius:8px;font-weight:700;text-transform:uppercase}
  .ic-badge.severe{background:#c0392b22;color:#c0392b;border:1px solid #c0392b55}
  .ic-badge.moderate{background:#d4860022;color:#b8720a;border:1px solid #d4860055}
  .ic-badge.mild{background:#27ae6022;color:#27ae60;border:1px solid #27ae6055}
  .icard.severe{border-left-color:#c0392b}
  .icard.moderate{border-left-color:#d48600}
  .icard.mild{border-left-color:#27ae60}
  .icard .ic-sub{font-size:.73rem;color:#5a5040;margin-top:3px;line-height:1.4}
  .src-link{font-size:.7rem;color:#4a6741;text-decoration:none;display:inline-block;margin-top:3px}
  .src-link:hover{text-decoration:underline}

  #legend{position:absolute;bottom:14px;left:14px;background:#f0ebe0cc;border:1px solid #c5b99a;border-radius:8px;padding:10px 14px;font-size:.71rem;line-height:1.9;backdrop-filter:blur(4px)}
  #legend .leg-title{color:#7a6e5a;margin-bottom:2px;font-weight:600;font-size:.7rem;text-transform:uppercase;letter-spacing:.8px}
  .leg-row{display:flex;align-items:center;gap:7px;color:#3d3028}

  #tooltip{position:fixed;background:#2d3a2e;border:1px solid #4a6741;border-radius:6px;padding:6px 10px;font-size:.76rem;pointer-events:none;display:none;z-index:800;max-width:230px;line-height:1.5;color:#e8f0e4}
</style>
</head>
<body>

<div id="header">
  <h1>⬡ ODMAP</h1>
  <div class="subtitle">Drug Interaction Network</div>
  <div id="breadcrumb-wrap"><div id="breadcrumb-inner"></div></div>
  <button id="saved-btn" onclick="toggleSavedPanel()">💊 Saved List</button>
  <div id="search-area">
    <input id="drug1" placeholder="Drug 1" autocomplete="off"/>
    <input id="drug2" placeholder="Drug 2" autocomplete="off"/>
    <button id="go-btn" onclick="searchInteraction()">Go</button>
    <div id="history-dropdown">
      <span class="hist-label">Search History</span>
      <div class="hist-chips" id="hist-chips-container"></div>
    </div>
  </div>
</div>

<div id="saved-panel">
  <span class="sp-close" onclick="toggleSavedPanel()">✕</span>
  <h3>💊 My Saved Prescriptions</h3>
  <div id="saved-input-row">
    <input id="saved-input" placeholder="Add drug name…" autocomplete="off"/>
    <button id="saved-add-btn" onclick="addToSaved()">Add</button>
  </div>
  <div id="saved-list-items"></div>
</div>

<div id="search-result">
  <span class="close-btn" onclick="this.parentElement.style.display='none'">✕</span>
  <h3 id="sr-title"></h3>
  <div id="sr-body"></div>
</div>

<div id="main">
  <div id="graph-area">
    <svg id="svg"></svg>
    <div id="legend">
      <div class="leg-title">Severity</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#c0392b" stroke-width="2.5"/></svg> Severe</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#d48600" stroke-width="2" stroke-dasharray="6,3"/></svg> Moderate</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#27ae60" stroke-width="1.5" stroke-dasharray="2,3"/></svg> Mild</div>
      <div class="leg-title" style="margin-top:8px">Interaction Type</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#5a5040" stroke-width="2"/></svg> Hematologic</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#5a5040" stroke-width="2" stroke-dasharray="8,4"/></svg> Metabolic</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#5a5040" stroke-width="2" stroke-dasharray="4,2"/></svg> Cardiovascular</div>
      <div class="leg-row"><svg width="28" height="10"><line x1="0" y1="5" x2="28" y2="5" stroke="#5a5040" stroke-width="2" stroke-dasharray="2,5"/></svg> Neurological</div>
      <div class="leg-title" style="margin-top:8px">Saved List</div>
      <div class="leg-row"><svg width="28" height="10"><circle cx="14" cy="5" r="4" fill="none" stroke="#a855f7" stroke-width="2.5" stroke-dasharray="3,2"/></svg> Conflicts w/ saved</div>
    </div>
  </div>
  <div id="info-panel"></div>
</div>
<div id="tooltip"></div>

<script>
// ─── DATA ─────────────────────────────────────────────────────────────────────
// NOTE: URL field is named "citation" (NOT "source") so it never collides with
// D3's forceLink reserved "source"/"target" node-resolution keys.
const ALL_DRUGS = {
  "Warfarin":   {ingredient:"Warfarin sodium",        pronounce:"WAR-fuh-rin",     cls:"Anticoagulant",        similar:["Coumadin","Jantoven"],               citation:"https://www.ncbi.nlm.nih.gov/books/NBK470395/",  desc:"Prevents blood clots by inhibiting Vitamin K-dependent clotting factors."},
  "Aspirin":    {ingredient:"Acetylsalicylic acid",   pronounce:"AS-pir-in",       cls:"NSAID / Antiplatelet", similar:["Bayer","Bufferin","Ecotrin"],         citation:"https://www.ncbi.nlm.nih.gov/books/NBK519032/",  desc:"Reduces pain, fever, and platelet aggregation."},
  "Lipitor":    {ingredient:"Atorvastatin",           pronounce:"LIP-ih-tor",      cls:"Statin",               similar:["Torvast"],                           citation:"https://www.ncbi.nlm.nih.gov/books/NBK430882/",  desc:"Lowers LDL cholesterol by inhibiting HMG-CoA reductase."},
  "Paxil":      {ingredient:"Paroxetine",             pronounce:"PAX-il",          cls:"SSRI",                 similar:["Pexeva","Brisdelle"],                citation:"https://www.ncbi.nlm.nih.gov/books/NBK546090/",  desc:"Selective serotonin reuptake inhibitor for depression and anxiety."},
  "Prozac":     {ingredient:"Fluoxetine",             pronounce:"PRO-zak",         cls:"SSRI",                 similar:["Sarafem","Rapiflux"],                citation:"https://www.ncbi.nlm.nih.gov/books/NBK459223/",  desc:"Increases serotonin levels; treats depression and OCD."},
  "Xanax":      {ingredient:"Alprazolam",             pronounce:"ZAN-ax",          cls:"Benzodiazepine",       similar:["Niravam","Alprazolam ER"],           citation:"https://www.ncbi.nlm.nih.gov/books/NBK538165/",  desc:"Short-term management of anxiety disorders."},
  "Metformin":  {ingredient:"Metformin HCl",          pronounce:"met-FOR-min",     cls:"Biguanide",            similar:["Glucophage","Fortamet","Glumetza"],  citation:"https://www.ncbi.nlm.nih.gov/books/NBK518983/",  desc:"First-line treatment for type 2 diabetes; reduces hepatic glucose output."},
  "Lisinopril": {ingredient:"Lisinopril",             pronounce:"lye-SIN-oh-pril", cls:"ACE Inhibitor",        similar:["Zestril","Prinivil","Qbrelis"],      citation:"https://www.ncbi.nlm.nih.gov/books/NBK482440/",  desc:"Treats high blood pressure and heart failure."},
  "Advil":      {ingredient:"Ibuprofen",              pronounce:"AD-vil",          cls:"NSAID",                similar:["Motrin","Nuprin","Ibuprofen"],       citation:"https://www.ncbi.nlm.nih.gov/books/NBK526103/",  desc:"Reduces inflammation, pain, and fever."},
  "Amoxil":     {ingredient:"Amoxicillin trihydrate", pronounce:"a-MOX-il",        cls:"Antibiotic",           similar:["Trimox","Moxatag","Amoxicillin"],    citation:"https://www.ncbi.nlm.nih.gov/books/NBK482250/",  desc:"Broad-spectrum penicillin antibiotic."},
  "Lanoxin":    {ingredient:"Digoxin",                pronounce:"la-NOX-in",       cls:"Cardiac Glycoside",    similar:["Digitek","Digoxin"],                 citation:"https://www.ncbi.nlm.nih.gov/books/NBK470554/",  desc:"Strengthens heart contractions; treats heart failure and AFib."},
  "Zoloft":     {ingredient:"Sertraline",             pronounce:"ZO-loft",         cls:"SSRI",                 similar:["Lustral"],                           citation:"https://www.ncbi.nlm.nih.gov/books/NBK547849/",  desc:"Treats depression, panic disorder, and PTSD."},
};

// "drug_a" / "drug_b" are used instead of "source" / "target" in the raw data
// to avoid stomping D3's reserved keys. They are mapped to source/target below.
const ALL_INTERACTIONS_RAW = [
  {drug_a:"Warfarin",  drug_b:"Aspirin",    severity:"severe",   type:"Hematologic",    citation:"https://pubmed.ncbi.nlm.nih.gov/15692077/", desc:"Concurrent use significantly increases bleeding risk due to additive antiplatelet and anticoagulant effects."},
  {drug_a:"Warfarin",  drug_b:"Advil",      severity:"severe",   type:"Hematologic",    citation:"https://pubmed.ncbi.nlm.nih.gov/17938526/", desc:"NSAIDs inhibit platelet function and may displace Warfarin from protein binding, raising hemorrhage risk."},
  {drug_a:"Warfarin",  drug_b:"Amoxil",     severity:"moderate", type:"Metabolic",      citation:"https://pubmed.ncbi.nlm.nih.gov/11902657/", desc:"Antibiotics alter gut flora that produce Vitamin K, potentially increasing INR unpredictably."},
  {drug_a:"Warfarin",  drug_b:"Lipitor",    severity:"moderate", type:"Metabolic",      citation:"https://pubmed.ncbi.nlm.nih.gov/12163597/", desc:"Atorvastatin inhibits CYP2C9, raising Warfarin plasma levels and anticoagulation effect."},
  {drug_a:"Paxil",     drug_b:"Zoloft",     severity:"severe",   type:"Neurological",   citation:"https://pubmed.ncbi.nlm.nih.gov/15820243/", desc:"Combining SSRIs increases serotonin syndrome risk: hyperthermia, seizures, cardiovascular collapse."},
  {drug_a:"Paxil",     drug_b:"Prozac",     severity:"severe",   type:"Neurological",   citation:"https://pubmed.ncbi.nlm.nih.gov/15820243/", desc:"Two SSRIs together can precipitate life-threatening serotonin syndrome."},
  {drug_a:"Prozac",    drug_b:"Zoloft",     severity:"severe",   type:"Neurological",   citation:"https://pubmed.ncbi.nlm.nih.gov/15820243/", desc:"Dual SSRI therapy dramatically increases serotonin toxicity risk."},
  {drug_a:"Xanax",     drug_b:"Prozac",     severity:"moderate", type:"Neurological",   citation:"https://pubmed.ncbi.nlm.nih.gov/9063941/",  desc:"Fluoxetine inhibits CYP3A4, slowing Alprazolam metabolism and potentiating CNS depression."},
  {drug_a:"Xanax",     drug_b:"Paxil",      severity:"moderate", type:"Neurological",   citation:"https://pubmed.ncbi.nlm.nih.gov/9063941/",  desc:"Paroxetine raises Alprazolam exposure through CYP3A4 inhibition, increasing sedation risk."},
  {drug_a:"Lisinopril",drug_b:"Advil",      severity:"moderate", type:"Cardiovascular", citation:"https://pubmed.ncbi.nlm.nih.gov/11756079/", desc:"NSAIDs blunt the antihypertensive effect of ACE inhibitors and may worsen renal function."},
  {drug_a:"Lisinopril",drug_b:"Metformin",  severity:"mild",     type:"Metabolic",      citation:"https://pubmed.ncbi.nlm.nih.gov/10480611/", desc:"ACE inhibitors may slightly enhance insulin sensitivity, risk of hypoglycemia with Metformin."},
  {drug_a:"Lanoxin",   drug_b:"Lisinopril", severity:"moderate", type:"Cardiovascular", citation:"https://pubmed.ncbi.nlm.nih.gov/1662795/",  desc:"ACE inhibitors can raise Digoxin levels through renal hemodynamic changes."},
  {drug_a:"Lanoxin",   drug_b:"Aspirin",    severity:"mild",     type:"Hematologic",    citation:"https://pubmed.ncbi.nlm.nih.gov/1662795/",  desc:"Low-dose aspirin has minimal effect on Digoxin but GI bleeding risk is additive."},
  {drug_a:"Lipitor",   drug_b:"Lanoxin",    severity:"moderate", type:"Metabolic",      citation:"https://pubmed.ncbi.nlm.nih.gov/12163597/", desc:"Atorvastatin increases Digoxin AUC ~15% via P-glycoprotein inhibition — monitor levels."},
  {drug_a:"Metformin", drug_b:"Advil",      severity:"mild",     type:"Metabolic",      citation:"https://pubmed.ncbi.nlm.nih.gov/12667685/", desc:"NSAIDs can impair renal function, reducing Metformin clearance and raising lactic acidosis risk."},
  {drug_a:"Aspirin",   drug_b:"Lisinopril", severity:"mild",     type:"Cardiovascular", citation:"https://pubmed.ncbi.nlm.nih.gov/11756079/", desc:"High-dose aspirin may attenuate the hemodynamic benefits of ACE inhibitors in heart failure."},
];

// Map drug_a/drug_b → source/target that D3 forceLink expects,
// keeping citation separate so D3 never mistakes it for a node reference.
const ALL_INTERACTIONS = ALL_INTERACTIONS_RAW.map(r => ({
  source: r.drug_a,
  target: r.drug_b,
  severity: r.severity,
  type: r.type,
  desc: r.desc,
  citation: r.citation
}));

// ─── STATE ────────────────────────────────────────────────────────────────────
let currentRoot = "Warfarin";
let clickTrail  = [];
let history     = [];
let savedList   = [];
let simulation;
let rotationTimer  = null;
let isInteracting  = false;
let idleTimeout    = null;
let currentNodes   = [];

// ─── HISTORY DROPDOWN ─────────────────────────────────────────────────────────
(function(){
  const d1   = document.getElementById("drug1");
  const d2   = document.getElementById("drug2");
  const drop = document.getElementById("history-dropdown");
  let activeInput = null;
  function showDrop(inp){ activeInput=inp; renderHistChips(); drop.style.display=history.length?"block":"none"; }
  function hideDrop(){ setTimeout(()=>{ if(!drop.contains(document.activeElement)) drop.style.display="none"; },150); }
  d1.addEventListener("focus",()=>showDrop(d1));
  d2.addEventListener("focus",()=>showDrop(d2));
  d1.addEventListener("blur", hideDrop);
  d2.addEventListener("blur", hideDrop);
  window._activeSearchInput = ()=>activeInput;
})();

function renderHistChips(){
  const container = document.getElementById("hist-chips-container");
  container.innerHTML="";
  history.forEach(h=>{
    const chip=document.createElement("span");
    chip.className="hist-chip"; chip.textContent=h;
    chip.onmousedown=e=>{
      e.preventDefault();
      const inp=window._activeSearchInput();
      if(inp) inp.value=h;
      document.getElementById("history-dropdown").style.display="none";
      const key=Object.keys(ALL_DRUGS).find(k=>k.toLowerCase()===h.toLowerCase());
      if(key) buildGraph(key);
    };
    container.appendChild(chip);
  });
  document.getElementById("history-dropdown").style.display=history.length?"block":"none";
}

// ─── BREADCRUMB ───────────────────────────────────────────────────────────────
function updateBreadcrumb(){
  const inner=document.getElementById("breadcrumb-inner");
  inner.innerHTML="";
  clickTrail.forEach((name,i)=>{
    if(i>0){ const a=document.createElement("span"); a.className="bc-arrow"; a.textContent="›"; inner.appendChild(a); }
    const step=document.createElement("span");
    step.className="bc-step"+(i===clickTrail.length-1?" current":"");
    step.textContent=name;
    if(i<clickTrail.length-1) step.onclick=()=>{ clickTrail=clickTrail.slice(0,i+1); buildGraph(name,true); };
    inner.appendChild(step);
  });
  const wrap=document.getElementById("breadcrumb-wrap");
  setTimeout(()=>{ wrap.scrollLeft=wrap.scrollWidth; },50);
}

// ─── SAVED LIST ───────────────────────────────────────────────────────────────
function toggleSavedPanel(){
  const p=document.getElementById("saved-panel");
  p.style.display=p.style.display==="block"?"none":"block";
}
function addToSaved(){
  const inp=document.getElementById("saved-input");
  const val=inp.value.trim();
  if(!val||savedList.includes(val)) return;
  savedList.push(val); renderSavedList(); refreshGraph();
  inp.value="";
}
function removeFromSaved(name){ savedList=savedList.filter(s=>s!==name); renderSavedList(); refreshGraph(); }
function renderSavedList(){
  const c=document.getElementById("saved-list-items"); c.innerHTML="";
  savedList.forEach(name=>{
    const el=document.createElement("div"); el.className="saved-item";
    el.innerHTML=`${name}<span class="si-remove" onclick="removeFromSaved('${name}')">✕</span>`;
    c.appendChild(el);
  });
}
function conflictsWithSaved(drugName){
  return savedList.some(saved=>{
    const n=saved.toLowerCase();
    return ALL_INTERACTIONS.some(e=>
      (e.source.toLowerCase()===drugName.toLowerCase()&&e.target.toLowerCase()===n)||
      (e.target.toLowerCase()===drugName.toLowerCase()&&e.source.toLowerCase()===n)
    );
  });
}
function refreshGraph(){ buildGraph(currentRoot,true); }
document.getElementById("saved-input").addEventListener("keydown",e=>{ if(e.key==="Enter") addToSaved(); });

// ─── PRONUNCIATION ─────────────────────────────────────────────────────────────
function pronounce(text){
  if(!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text);
  u.rate=0.85; u.pitch=1.0; u.lang="en-US";
  window.speechSynthesis.speak(u);
}

// ─── IDLE ROTATION ─────────────────────────────────────────────────────────────
function startRotation(){
  if(rotationTimer) return;
  rotationTimer=setInterval(()=>{
    if(isInteracting||!currentNodes.length) return;
    const W=document.getElementById("graph-area").clientWidth;
    const H=document.getElementById("graph-area").clientHeight;
    const cx=W/2, cy=H/2;
    currentNodes.forEach(n=>{
      const dx=n.x-cx, dy=n.y-cy;
      const r=Math.sqrt(dx*dx+dy*dy);
      const a=Math.atan2(dy,dx)+0.003;
      n.x=cx+r*Math.cos(a); n.y=cy+r*Math.sin(a);
    });
    if(simulation) simulation.alpha(0.05).restart();
  },40);
}
function resetIdle(){
  isInteracting=true;
  clearTimeout(idleTimeout);
  idleTimeout=setTimeout(()=>{ isInteracting=false; },3000);
}
document.addEventListener("mousemove",resetIdle);
document.addEventListener("mousedown",resetIdle);

// ─── GRAPH BUILDER ────────────────────────────────────────────────────────────
function buildGraph(rootName, silent=false){
  if(!silent){ if(clickTrail[clickTrail.length-1]!==rootName) clickTrail.push(rootName); }
  if(history[history.length-1]!==rootName) history.push(rootName);
  currentRoot=rootName;
  updateBreadcrumb();

  const relEdges=ALL_INTERACTIONS.filter(e=>e.source===rootName||e.target===rootName);
  const neighborNames=new Set([rootName]);
  relEdges.forEach(e=>{ neighborNames.add(e.source); neighborNames.add(e.target); });

  // Build node objects — spread only safe fields, never the full drug object
  // (avoids accidentally copying any "source" key into node data)
  const nodes=[...neighborNames].map(n=>{
    const d=ALL_DRUGS[n]||{ingredient:"Unknown",pronounce:n,cls:"Unknown",similar:[],citation:"",desc:""};
    return { id:n, isRoot:n===rootName, ingredient:d.ingredient, pronounce:d.pronounce,
             cls:d.cls, similar:d.similar, citation:d.citation, desc:d.desc };
  });
  currentNodes=nodes;

  // Deep-copy links so D3 can mutate source/target to node objects safely
  const links=relEdges.map(e=>({
    source:e.source, target:e.target,
    severity:e.severity, type:e.type, desc:e.desc, citation:e.citation
  }));

  renderD3(nodes, links, rootName);
}

// ─── D3 RENDER ────────────────────────────────────────────────────────────────
function renderD3(nodes, links, rootName){
  const svg=d3.select("#svg");
  svg.selectAll("*").remove();

  const W=document.getElementById("graph-area").clientWidth;
  const H=document.getElementById("graph-area").clientHeight;

  const defs=svg.append("defs");
  ["severe","moderate","mild"].forEach(sev=>{
    const col=sev==="severe"?"#c0392b":sev==="moderate"?"#d48600":"#27ae60";
    defs.append("marker").attr("id",`arrow-${sev}`)
      .attr("viewBox","0 -5 10 10").attr("refX",22).attr("refY",0)
      .attr("markerWidth",6).attr("markerHeight",6).attr("orient","auto")
      .append("path").attr("d","M0,-5L10,0L0,5").attr("fill",col).attr("opacity",.8);
  });

  const g=svg.append("g");
  svg.call(d3.zoom().scaleExtent([0.25,3]).on("zoom",e=>g.attr("transform",e.transform)));

  nodes.forEach(n=>{
    if(n.isRoot){ n.x=W/2; n.y=H/2; n.fx=W/2; n.fy=H/2; }
    else { n.x=W/2+(Math.random()-.5)*220; n.y=H/2+(Math.random()-.5)*220; }
  });

  if(simulation) simulation.stop();
  simulation=d3.forceSimulation(nodes)
    .force("link",d3.forceLink(links).id(d=>d.id).distance(175).strength(0.55))
    .force("charge",d3.forceManyBody().strength(-480))
    .force("center",d3.forceCenter(W/2,H/2))
    .force("collision",d3.forceCollide(52));

  const edgeColor=s=>s==="severe"?"#c0392b":s==="moderate"?"#d48600":"#27ae60";
  const edgeWidth=s=>s==="severe"?2.8:s==="moderate"?2:1.6;
  const dashArray =t=>t==="Hematologic"?"none":t==="Metabolic"?"10,4":t==="Cardiovascular"?"5,3":"2,5";

  const linkSel=g.append("g").selectAll("line").data(links).join("line")
    .attr("stroke",d=>edgeColor(d.severity))
    .attr("stroke-width",d=>edgeWidth(d.severity))
    .attr("stroke-dasharray",d=>dashArray(d.type))
    .attr("opacity",.82)
    .attr("marker-end",d=>`url(#arrow-${d.severity})`)
    .on("mouseover",(event,d)=>showTooltip(event,
      `<b>${d.source.id||d.source} ↔ ${d.target.id||d.target}</b><br/>
       <span style="color:#b8d4a8">${d.severity.toUpperCase()} · ${d.type}</span><br/>${d.desc}`))
    .on("mouseout",hideTooltip);

  const nodeG=g.append("g").selectAll("g").data(nodes).join("g")
    .attr("cursor","pointer")
    .call(d3.drag()
      .on("start",(event,d)=>{ resetIdle(); if(!event.active) simulation.alphaTarget(.4).restart(); d.fx=d.x; d.fy=d.y; })
      .on("drag",(event,d)=>{ d.fx=event.x; d.fy=event.y; })
      .on("end",(event,d)=>{ if(!event.active) simulation.alphaTarget(0); if(!d.isRoot){d.fx=null;d.fy=null;} }))
    .on("click",(event,d)=>{ event.stopPropagation(); resetIdle(); if(d.isRoot) showInfoCard(d); else buildGraph(d.id); })
    .on("mouseover",(event,d)=>showTooltip(event,
      `<b>${d.id}</b><br/><span style="color:#b8d4a8">${d.ingredient}</span><br/>
       <span style="color:#8fbe7c;font-size:.72rem">Click to ${d.isRoot?'see info card':'explore'}</span>`))
    .on("mouseout",hideTooltip);

  nodeG.append("circle")
    .attr("r",d=>d.isRoot?30:21)
    .attr("fill",d=>d.isRoot?"#4a6741":"#ddd5c2")
    .attr("stroke",d=>conflictsWithSaved(d.id)?"#a855f7":d.isRoot?"#8fbe7c":"#a09080")
    .attr("stroke-width",d=>conflictsWithSaved(d.id)?3.5:d.isRoot?3:1.5)
    .attr("stroke-dasharray",d=>conflictsWithSaved(d.id)?"6,3":"none");

  nodeG.append("text")
    .attr("text-anchor","middle").attr("dy","0.35em")
    .attr("font-size",d=>d.isRoot?"11px":"9.5px")
    .attr("fill",d=>d.isRoot?"#e8f0e4":"#2d3a2e")
    .attr("font-weight",d=>d.isRoot?"700":"400")
    .attr("pointer-events","none")
    .text(d=>d.id.length>10?d.id.slice(0,9)+"…":d.id);

  simulation.on("tick",()=>{
    linkSel.attr("x1",d=>d.source.x).attr("y1",d=>d.source.y)
            .attr("x2",d=>d.target.x).attr("y2",d=>d.target.y);
    nodeG.attr("transform",d=>`translate(${d.x},${d.y})`);
  });

  setTimeout(()=>{ const r=nodes.find(n=>n.isRoot); r.fx=null; r.fy=null; },900);
  startRotation();
}

// ─── INFO CARD ────────────────────────────────────────────────────────────────
function showInfoCard(drug){
  const panel=document.getElementById("info-panel");
  panel.style.display="flex"; panel.style.flexDirection="column";

  const rels=ALL_INTERACTIONS
    .filter(e=>e.source===drug.id||e.target===drug.id)
    .sort((a,b)=>({severe:0,moderate:1,mild:2}[a.severity]-({severe:0,moderate:1,mild:2}[b.severity])));

  const similarHTML=(drug.similar||[]).sort()
    .map(s=>`<span class="similar-chip" title="Same ingredient: ${drug.ingredient}">${s}</span>`).join("");

  panel.innerHTML=`
    <div class="card-top-bar">
      <button class="close-panel-btn-top" onclick="document.getElementById('info-panel').style.display='none'">✕ Close</button>
    </div>
    <div class="card-header">
      <div class="card-brand">
        ${drug.id}
        <button class="pronunc-btn" onclick="pronounce('${drug.pronounce||drug.id}')" title="Pronounce">
          🔊 ${drug.pronounce||drug.id}
        </button>
      </div>
      <div class="card-class">${drug.cls}</div>
    </div>
    <div class="card-body">
      <div class="card-section-title">Active Ingredient</div>
      <div class="card-val">${drug.ingredient}</div>

      <div class="card-section-title">Description</div>
      <div class="card-val">${drug.desc}<br/>
        <a class="src-link" href="${drug.citation}" target="_blank" rel="noopener">📎 NLM Source</a>
      </div>

      <div class="card-section-title">Same Medication — Other Brand Names</div>
      <div style="margin-top:4px">${similarHTML||'<span style="color:#8a7e6a;font-size:.8rem">None listed</span>'}</div>

      <div class="card-section-title" style="margin-top:14px">
        Negative Interactions
        <span style="background:#c0392b22;color:#c0392b;border:1px solid #c0392b55;border-radius:8px;padding:1px 7px;font-size:.68rem;margin-left:6px">${rels.length}</span>
      </div>
      ${rels.map(r=>{
        const other=r.source===drug.id?r.target:r.source;
        return `<div class="icard ${r.severity}">
          <div class="ic-title">
            <span style="cursor:pointer;color:#4a6741;font-weight:600" onclick="buildGraph('${other}')">${other}</span>
            <span class="ic-badge ${r.severity}">${r.severity}</span>
            <span style="color:#7a6e5a;font-size:.7rem;margin-left:auto">${r.type}</span>
          </div>
          <div class="ic-sub">${r.desc}<br/>
            <a class="src-link" href="${r.citation}" target="_blank" rel="noopener">📎 PubMed</a>
          </div>
        </div>`;
      }).join("")}
    </div>`;
}

// ─── TOOLTIP ──────────────────────────────────────────────────────────────────
const tt=document.getElementById("tooltip");
function showTooltip(event,html){ tt.innerHTML=html; tt.style.display="block"; tt.style.left=(event.pageX+14)+"px"; tt.style.top=(event.pageY-10)+"px"; }
function hideTooltip(){ tt.style.display="none"; }

// ─── SEARCH ───────────────────────────────────────────────────────────────────
function searchInteraction(){
  const d1=document.getElementById("drug1").value.trim();
  const d2=document.getElementById("drug2").value.trim();
  const sr=document.getElementById("search-result");
  const srTitle=document.getElementById("sr-title");
  const srBody=document.getElementById("sr-body");

  if(!d1||!d2){ srTitle.textContent="Enter both drug names"; srBody.textContent=""; sr.style.display="block"; return; }

  const match=ALL_INTERACTIONS.find(e=>
    (e.source.toLowerCase()===d1.toLowerCase()&&e.target.toLowerCase()===d2.toLowerCase())||
    (e.source.toLowerCase()===d2.toLowerCase()&&e.target.toLowerCase()===d1.toLowerCase())
  );

  if(match){
    const col=match.severity==="severe"?"#c0392b":match.severity==="moderate"?"#d48600":"#27ae60";
    srTitle.innerHTML=`${match.source} ↔ ${match.target}`;
    srBody.innerHTML=`<span style="color:${col};font-weight:700">${match.severity.toUpperCase()}</span> · ${match.type}<br/><br/>
      ${match.desc}<br/><a class="src-link" href="${match.citation}" target="_blank" rel="noopener">📎 PubMed</a>`;
    if(history[history.length-1]!==`${d1}+${d2}`) history.push(`${d1}+${d2}`);
    buildGraph(match.source);
  } else {
    srTitle.textContent="No interaction found";
    srBody.innerHTML=`No recorded interaction between <b>${d1}</b> and <b>${d2}</b> in ODMAP.`;
    const key=Object.keys(ALL_DRUGS).find(k=>k.toLowerCase()===d1.toLowerCase());
    if(key) buildGraph(key);
  }
  sr.style.display="block";
}

document.addEventListener("keydown",e=>{ if(e.key==="Enter"&&(document.activeElement.id==="drug1"||document.activeElement.id==="drug2")) searchInteraction(); });

// ─── INIT ─────────────────────────────────────────────────────────────────────
window.onload  = ()=>buildGraph("Warfarin");
window.onresize= ()=>buildGraph(currentRoot,true);
</script>
</body>
</html>"""

with open("./outputs/odmap_v5.html", "w") as f:
    f.write(html)

from IPython.display import display, HTML
display(HTML(open("./outputs/odmap_v5.html").read()), metadata={"alt": "ODMAP v5 drug network"})

