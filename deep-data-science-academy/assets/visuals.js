/* Visual learning layer.
   Every diagram here TEACHES something: each one encodes a relationship, a flow,
   or a transformation. No decoration-only graphics. SVGs are generated in the
   browser (no image downloads, works offline, scales on mobile).            */
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

  function svg(w, h, body) {
    return `<svg viewBox="0 0 ${w} ${h}" xmlns="${NS}" role="img" aria-label="diagram">${body}</svg>`;
  }
  function box(x, y, w, h, text, opts = {}) {
    const fill = opts.fill || 'rgba(78,161,255,.14)';
    const stroke = opts.stroke || 'rgba(78,161,255,.75)';
    const tcol = opts.color || 'currentColor';
    const lines = String(text).split('\n');
    const fs = opts.fs || 12;
    const tspans = lines.map((l, i) =>
      `<tspan x="${x + w / 2}" y="${y + h / 2 + (i - (lines.length - 1) / 2) * (fs + 2) + fs / 3}">${esc(l)}</tspan>`).join('');
    return `<g><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="9" fill="${fill}" stroke="${stroke}" stroke-width="1.4"/>
      <text text-anchor="middle" font-size="${fs}" fill="${tcol}">${tspans}</text></g>`;
  }
  function arrow(x1, y1, x2, y2, label) {
    const mid = label ? `<text x="${(x1 + x2) / 2}" y="${(y1 + y2) / 2 - 5}" font-size="10.5" text-anchor="middle" fill="currentColor" opacity=".72">${esc(label)}</text>` : '';
    return `<g opacity=".85"><line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="currentColor" stroke-width="1.3" marker-end="url(#ah)"/>${mid}</g>`;
  }
  function circle(cx, cy, r, text, opts = {}) {
    return `<g><circle cx="${cx}" cy="${cy}" r="${r}" fill="${opts.fill || 'rgba(126,231,135,.16)'}" stroke="${opts.stroke || 'rgba(126,231,135,.8)'}" stroke-width="1.3"/>
      <text x="${cx}" y="${cy + 4}" text-anchor="middle" font-size="${opts.fs || 11.5}" fill="currentColor">${esc(text)}</text></g>`;
  }
  const defs = `<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="currentColor" opacity=".8"/></marker></defs>`;

  const generics = {
    pipeline() {
      const labels = ['INPUT\nraw data / question', 'PROCESSING\ntransform + model', 'OUTPUT\nvalidated result'];
      let s = defs;
      labels.forEach((l, i) => { s += box(20 + i * 200, 40, 160, 62, l, { fs: 11.5 }); });
      s += arrow(180, 71, 218, 71); s += arrow(380, 71, 418, 71);
      s += box(20, 118, 540, 34, 'feedback: validate -> revise -> re-run  (never one-way)', { fill: 'rgba(255,180,84,.12)', stroke: 'rgba(255,180,84,.6)', fs: 11 });
      return svg(580, 168, s);
    },
    'ds-three-pillars'() {
      let s = defs;
      s += circle(150, 80, 60, 'Statistics', { fill: 'rgba(78,161,255,.16)' });
      s += circle(300, 80, 60, 'Computing', { fill: 'rgba(126,231,135,.16)', stroke: 'rgba(126,231,135,.8)' });
      s += circle(225, 175, 60, 'Domain', { fill: 'rgba(194,151,255,.16)', stroke: 'rgba(194,151,255,.8)' });
      s += `<text x="225" y="245" text-anchor="middle" font-size="11.5" fill="currentColor" opacity=".8">overlap = the actual job</text>`;
      return svg(450, 262, s);
    },
    'role-matrix'() {
      const cols = ['Report /\nexperiment', 'Question +\nmodel', 'Pipeline +\nservice', 'LLM product\n+ evals'];
      const rows = ['Data Analyst', 'Data Scientist', 'ML Engineer', 'AI Engineer'];
      let s = defs;
      rows.forEach((r, i) => {
        s += box(10, 16 + i * 44, 130, 34, r, { fs: 11.5, fill: 'rgba(19,26,36,.6)' });
        s += box(150, 16 + i * 44, 150, 34, cols[i], { fs: 11, fill: 'rgba(78,161,255,.14)' });
      });
      s += `<text x="10" y="205" font-size="11" fill="currentColor" opacity=".75">Owned artefact decides the interview format and the on-call duty.</text>`;
      return svg(320, 218, s);
    },
    'crisp-dm'() {
      const names = ['Business\nunderstanding', 'Data\nunderstanding', 'Data\npreparation', 'Modelling', 'Evaluation', 'Deployment'];
      let s = defs;
      names.forEach((n, i) => {
        const x = 15 + i * 96;
        s += box(x, 30, 84, 52, n, { fs: 9.6, fill: i < 3 ? 'rgba(78,161,255,.14)' : 'rgba(194,151,255,.14)' });
        if (i < names.length - 1) s += arrow(x + 84, 56, x + 95, 56);
      });
      s += `<path d="M560 92 q 20 46 -120 46 q -300 0 -340 -20" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 4" opacity=".6" marker-end="url(#ah)"/>`;
      s += `<text x="230" y="126" font-size="10.5" fill="currentColor" opacity=".75">iteration stays cheap only if each stage artefact is versioned</text>`;
      return svg(600, 140, s);
    },
    environments() {
      let s = defs;
      s += box(10, 20, 180, 40, 'GLOBAL site-packages', { fill: 'rgba(255,123,114,.12)', stroke: 'rgba(255,123,114,.7)', fs: 11 });
      s += box(10, 70, 84, 34, 'project A\npandas 1.5', { fs: 10 });
      s += box(104, 70, 86, 34, 'project B\npandas 2.2', { fs: 10 });
      s += `<text x="10" y="122" font-size="10.5" fill="currentColor" opacity=".8">conflict: one shared set</text>`;
      s += box(250, 20, 160, 40, 'ENV A (pinned)', { fill: 'rgba(126,231,135,.14)', stroke: 'rgba(126,231,135,.75)', fs: 11 });
      s += box(430, 20, 160, 40, 'ENV B (pinned)', { fill: 'rgba(126,231,135,.14)', stroke: 'rgba(126,231,135,.75)', fs: 11 });
      s += `<text x="250" y="122" font-size="10.5" fill="currentColor" opacity=".8">isolated: reproducible per project</text>`;
      return svg(610, 134, s);
    },
    'notebook-kernel'() {
      let s = defs;
      s += box(20, 20, 150, 70, 'notebook file\n(.ipynb JSON)\ncells + saved outputs', { fs: 10.6 });
      s += box(210, 20, 150, 70, 'kernel process\n(variables in RAM)\nexecution_count', { fs: 10.6, fill: 'rgba(194,151,255,.14)', stroke: 'rgba(194,151,255,.75)' });
      s += arrow(170, 55, 208, 55, 'runs');
      s += `<text x="20" y="118" font-size="11" fill="currentColor" opacity=".82">Out-of-order execution = gap between what the file claims and what the kernel holds.</text>`;
      s += `<text x="20" y="136" font-size="11" fill="currentColor" opacity=".82">Fix: Restart &amp; Run All, or move logic into src/ modules.</text>`;
      return svg(400, 146, s);
    },
    'name-object'() {
      let s = defs;
      s += box(10, 24, 80, 30, 'name a', { fs: 11 });
      s += box(10, 64, 80, 30, 'name b', { fs: 11 });
      s += box(190, 44, 150, 30, 'object [1,2,3] mutable', { fs: 10.4, fill: 'rgba(255,180,84,.14)', stroke: 'rgba(255,180,84,.7)' });
      s += arrow(90, 39, 188, 55); s += arrow(90, 79, 188, 66);
      s += `<text x="10" y="120" font-size="10.8" fill="currentColor" opacity=".8">b = a binds a second name to the SAME object (no copy)</text>`;
      return svg(360, 132, s);
    },
    'string-slice'() {
      const chars = 't i p s _ c s v'.split(' ');
      let s = defs;
      chars.forEach((c, i) => { s += box(20 + i * 34, 30, 30, 30, c, { fs: 12.5 }); });
      chars.forEach((c, i) => {
        s += `<text x="${35 + i * 34}" y="76" font-size="10.5" text-anchor="middle" fill="currentColor" opacity=".8">${i}</text>`;
        s += `<text x="${35 + i * 34}" y="94" font-size="10.5" text-anchor="middle" fill="currentColor" opacity=".55">${i - 8}</text>`;
      });
      s += `<text x="20" y="120" font-size="11" fill="currentColor" opacity=".85">s[2:5] = c s v | s[-3:] = c s v | s[::2] = t p _ s</text>`;
      return svg(320, 132, s);
    },
    'gradient-descent'() {
      let s = defs;
      s += `<path d="M30 130 Q 150 10 300 118" fill="none" stroke="rgba(78,161,255,.85)" stroke-width="2"/>`;
      [[60, 106], [105, 65], [150, 42], [196, 45], [240, 76], [275, 100]].forEach(([x, y], i) => {
        s += `<circle cx="${x}" cy="${y}" r="${5 - i * 0.35}" fill="rgba(126,231,135,.85)"/>`;
      });
      s += `<text x="30" y="152" font-size="10.8" fill="currentColor" opacity=".8">each step = parameter - learning_rate * gradient ; too large a step overshoots, too small crawls</text>`;
      return svg(320, 162, s);
    },
    attention() {
      let s = defs;
      s += box(20, 30, 70, 26, 'query', { fs: 11 }); s += box(20, 70, 70, 26, 'key', { fs: 11 }); s += box(20, 110, 70, 26, 'value', { fs: 11 });
      s += box(150, 55, 110, 52, 'scaled dot\nproduct', { fs: 11, fill: 'rgba(194,151,255,.14)', stroke: 'rgba(194,151,255,.75)' });
      s += box(300, 55, 110, 52, 'weighted sum\nof values', { fs: 11, fill: 'rgba(126,231,135,.14)', stroke: 'rgba(126,231,135,.75)' });
      s += arrow(90, 43, 148, 70); s += arrow(90, 83, 148, 83); s += arrow(90, 123, 148, 96);
      s += arrow(260, 81, 298, 81);
      s += `<text x="20" y="160" font-size="10.8" fill="currentColor" opacity=".8">softmax(QK^T / sqrt(d_k)) V : weights say how much each token contributes</text>`;
      return svg(430, 172, s);
    },
    'vector-search'() {
      let s = defs;
      s += box(20, 30, 120, 44, 'query\ntext -> vector', { fs: 10.6 });
      s += box(190, 30, 130, 44, 'ANN index\nHNSW / IVF', { fs: 10.6, fill: 'rgba(194,151,255,.14)' });
      s += box(370, 30, 150, 44, 'top-k chunks\n(+ metadata filter)', { fs: 10.6, fill: 'rgba(126,231,135,.14)' });
      s += arrow(140, 52, 188, 52); s += arrow(320, 52, 368, 52);
      s += `<text x="20" y="100" font-size="10.8" fill="currentColor" opacity=".8">cosine similarity ranks documents; rerankers then reorder the top-k for precision</text>`;
      return svg(540, 112, s);
    },
    'rag-architecture'() {
      let s = defs;
      s += box(10, 20, 120, 40, 'documents\n(PDF, docs)', { fs: 10.4 });
      s += box(150, 20, 110, 40, 'chunk +\nembed', { fs: 10.4 });
      s += box(280, 20, 110, 40, 'vector\nstore', { fs: 10.4, fill: 'rgba(194,151,255,.14)' });
      s += arrow(130, 40, 148, 40); s += arrow(260, 40, 278, 40);
      s += box(10, 90, 120, 40, 'user\nquestion', { fs: 10.4 });
      s += box(150, 90, 110, 40, 'retrieve\ntop-k', { fs: 10.4 });
      s += box(280, 90, 110, 40, 'LLM +\ncontext', { fs: 10.4, fill: 'rgba(126,231,135,.14)' });
      s += box(410, 90, 120, 40, 'answer +\ncitations', { fs: 10.4 });
      s += arrow(130, 110, 148, 110); s += arrow(260, 110, 278, 110); s += arrow(390, 110, 408, 110);
      s += arrow(335, 60, 335, 88, 'grounding');
      s += `<text x="10" y="152" font-size="10.6" fill="currentColor" opacity=".8">evaluate: faithfulness, context precision/recall, answer relevance (Day 255)</text>`;
      return svg(545, 164, s);
    },
    'ml-pipeline'() {
      const steps = ['raw', 'clean', 'features', 'split', 'train', 'evaluate', 'register', 'serve'];
      let s = defs;
      steps.forEach((t, i) => { s += box(10 + i * 76, 30, 68, 34, t, { fs: 10.6, fill: i > 4 ? 'rgba(126,231,135,.13)' : 'rgba(78,161,255,.13)' }); });
      steps.forEach((t, i) => { if (i < steps.length - 1) s += arrow(78 + i * 76, 47, 84 + i * 76, 47); });
      s += `<text x="10" y="90" font-size="10.6" fill="currentColor" opacity=".82">every arrow is a place leakage can enter - fit only on train, transform test</text>`;
      return svg(620, 102, s);
    },
    'mlops-loop'() {
      let s = defs;
      s += circle(90, 70, 46, 'train', { fill: 'rgba(78,161,255,.16)' });
      s += circle(230, 70, 46, 'deploy', { fill: 'rgba(126,231,135,.16)' });
      s += circle(370, 70, 46, 'monitor', { fill: 'rgba(255,180,84,.16)' });
      s += arrow(136, 70, 184, 70); s += arrow(276, 70, 324, 70);
      s += `<path d="M370 116 q -140 70 -280 0" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="4 4" marker-end="url(#ah)" opacity=".75"/>`;
      s += `<text x="230" y="146" font-size="10.6" text-anchor="middle" fill="currentColor" opacity=".82">drift detected -> retrain (automated only with a gate + evaluation)</text>`;
      return svg(470, 160, s);
    },
    'confusion-matrix'() {
      const cells = [['TP', 'FN'], ['FP', 'TN']];
      let s = defs;
      cells.forEach((row, i) => row.forEach((c, j) => {
        const good = (i === 0 && j === 0) || (i === 1 && j === 1);
        s += box(90 + j * 90, 40 + i * 50, 84, 44, c + '\n' + (c === 'TP' ? 'caught' : c === 'FN' ? 'missed' : c === 'FP' ? 'false alarm' : 'correct reject'),
          { fs: 10, fill: good ? 'rgba(126,231,135,.15)' : 'rgba(255,123,114,.14)' });
      }));
      s += `<text x="18" y="66" font-size="10.5" fill="currentColor" opacity=".8">actual +</text>`;
      s += `<text x="18" y="118" font-size="10.5" fill="currentColor" opacity=".8">actual -</text>`;
      s += `<text x="110" y="30" font-size="10.5" fill="currentColor" opacity=".8">pred +</text>`;
      s += `<text x="200" y="30" font-size="10.5" fill="currentColor" opacity=".8">pred -</text>`;
      return svg(290, 160, s);
    },
    'normal-distribution'() {
      let path = 'M20 130 ';
      for (let i = 0; i <= 60; i++) {
        const x = 20 + i * 4.6;
        const z = (i - 30) / 9;
        const y = 130 - 100 * Math.exp(-0.5 * z * z);
        path += `L${x.toFixed(1)} ${y.toFixed(1)} `;
      }
      let s = defs + `<path d="${path}" fill="rgba(78,161,255,.16)" stroke="rgba(78,161,255,.85)" stroke-width="1.6"/>`;
      s += `<line x1="158" y1="130" x2="158" y2="30" stroke="currentColor" stroke-dasharray="3 3" opacity=".6"/>`;
      s += `<text x="158" y="150" font-size="10.5" text-anchor="middle" fill="currentColor" opacity=".8">mean</text>`;
      s += `<text x="20" y="166" font-size="10.6" fill="currentColor" opacity=".82">68% within 1 SD, 95% within 2 SD, 99.7% within 3 SD - the empirical rule</text>`;
      return svg(310, 176, s);
    },
    boxplot() {
      let s = defs;
      s += `<line x1="30" y1="70" x2="290" y2="70" stroke="currentColor" stroke-width="1.2" opacity=".7"/>`;
      s += `<rect x="110" y="46" width="100" height="48" fill="rgba(78,161,255,.14)" stroke="rgba(78,161,255,.85)"/>`;
      s += `<line x1="160" y1="46" x2="160" y2="94" stroke="currentColor" stroke-width="2"/>`;
      s += `<line x1="60" y1="70" x2="110" y2="70" stroke="currentColor"/><line x1="60" y1="56" x2="60" y2="84" stroke="currentColor"/>`;
      s += `<line x1="210" y1="70" x2="270" y2="70" stroke="currentColor"/><line x1="270" y1="56" x2="270" y2="84" stroke="currentColor"/>`;
      s += `<circle cx="288" cy="70" r="4" fill="rgba(255,123,114,.9)"/>`;
      s += `<text x="30" y="118" font-size="10.6" fill="currentColor" opacity=".82">min | Q1 - median - Q3 | max, dots beyond 1.5*IQR are flagged outliers</text>`;
      return svg(310, 128, s);
    },
    'decision-tree'() {
      let s = defs;
      s += box(120, 14, 120, 30, 'age > 30 ?', { fs: 11 });
      s += box(30, 76, 110, 30, 'income > 50k ?', { fs: 10.4 });
      s += box(220, 76, 110, 30, 'tenure > 2y ?', { fs: 10.4 });
      s += box(10, 138, 66, 26, 'class 0', { fs: 10 }); s += box(86, 138, 66, 26, 'class 1', { fs: 10 });
      s += box(200, 138, 66, 26, 'class 1', { fs: 10 }); s += box(276, 138, 66, 26, 'class 0', { fs: 10 });
      s += arrow(170, 44, 100, 74); s += arrow(190, 44, 262, 74);
      s += arrow(70, 106, 48, 136); s += arrow(110, 106, 128, 136);
      s += arrow(250, 106, 236, 136); s += arrow(292, 106, 306, 136);
      s += `<text x="10" y="182" font-size="10.6" fill="currentColor" opacity=".82">each split maximises purity (Gini/entropy); depth controls overfitting</text>`;
      return svg(360, 194, s);
    },
    kmeans() {
      let s = defs;
      const pts = [[50, 40], [70, 55], [60, 70], [200, 45], [220, 60], [205, 75], [130, 130], [150, 145], [120, 150]];
      pts.forEach(([x, y], i) => {
        const c = i < 3 ? 'rgba(78,161,255,.9)' : i < 6 ? 'rgba(126,231,135,.9)' : 'rgba(194,151,255,.9)';
        s += `<circle cx="${x}" cy="${y}" r="5" fill="${c}"/>`;
      });
      s += circle(60, 55, 34, '', { fill: 'none', stroke: 'rgba(78,161,255,.6)' });
      s += circle(208, 60, 34, '', { fill: 'none', stroke: 'rgba(126,231,135,.6)' });
      s += circle(133, 142, 34, '', { fill: 'none', stroke: 'rgba(194,151,255,.6)' });
      s += `<text x="10" y="192" font-size="10.6" fill="currentColor" opacity=".82">assign points to nearest centroid, then move centroid to the mean of its points - repeat</text>`;
      return svg(290, 204, s);
    },
    pca() {
      let s = defs;
      for (let i = 0; i < 40; i++) {
        const t = i / 40; const x = 30 + t * 220 + (Math.random() * 26 - 13);
        const y = 150 - t * 100 + (Math.random() * 26 - 13);
        s += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="3" fill="rgba(78,161,255,.55)"/>`;
      }
      s += `<line x1="40" y1="160" x2="270" y2="40" stroke="rgba(255,180,84,.95)" stroke-width="2"/>`;
      s += `<line x1="120" y1="60" x2="200" y2="140" stroke="rgba(126,231,135,.8)" stroke-width="1.6" stroke-dasharray="4 3"/>`;
      s += `<text x="196" y="34" font-size="10.5" fill="currentColor" opacity=".85">PC1 (most variance)</text>`;
      s += `<text x="200" y="158" font-size="10.5" fill="currentColor" opacity=".8">PC2</text>`;
      s += `<text x="14" y="190" font-size="10.6" fill="currentColor" opacity=".82">project data onto the direction of maximum variance, then the next orthogonal one</text>`;
      return svg(300, 200, s);
    },
    convolution() {
      let s = defs;
      for (let r = 0; r < 6; r++) for (let c = 0; c < 6; c++) {
        const v = (r * 6 + c) % 7; const shade = 40 + v * 22;
        s += `<rect x="${20 + c * 20}" y="${20 + r * 20}" width="19" height="19" fill="rgb(${shade},${shade + 20},${shade + 45})" stroke="rgba(255,255,255,.08)"/>`;
      }
      s += `<rect x="${20 + 1 * 20}" y="${20 + 1 * 20}" width="59" height="59" fill="none" stroke="rgba(255,180,84,.95)" stroke-width="2.2"/>`;
      s += box(160, 40, 60, 60, 'kernel\n3x3', { fs: 10.6, fill: 'rgba(255,180,84,.14)', stroke: 'rgba(255,180,84,.8)' });
      s += arrow(140, 70, 158, 70);
      s += box(240, 46, 80, 48, 'feature\nmap', { fs: 11, fill: 'rgba(126,231,135,.14)', stroke: 'rgba(126,231,135,.8)' });
      s += arrow(222, 70, 238, 70);
      s += `<text x="14" y="164" font-size="10.6" fill="currentColor" opacity=".82">sliding window dot-product: the kernel learns which local pattern to fire on</text>`;
      return svg(340, 176, s);
    },
    'sql-joins'() {
      let s = defs;
      const t = (x, colour, label) => `<g><rect x="${x}" y="30" width="120" height="60" rx="8" fill="${colour}" stroke="rgba(255,255,255,.25)"/><text x="${x + 60}" y="64" text-anchor="middle" font-size="11" fill="currentColor">${label}</text></g>`;
      s += t(20, 'rgba(78,161,255,.16)', 'customers');
      s += t(200, 'rgba(126,231,135,.16)', 'orders');
      s += arrow(140, 60, 198, 60, 'ON id = customer_id');
      s += box(20, 106, 300, 30, 'LEFT JOIN keeps every customer, NULLs where no order matched', { fs: 10.6, fill: 'rgba(255,180,84,.12)', stroke: 'rgba(255,180,84,.6)' });
      s += `<text x="20" y="156" font-size="10.6" fill="currentColor" opacity=".82">check cardinality first: a one-to-many join multiplies rows and inflates SUM()</text>`;
      return svg(350, 168, s);
    },
    dataframe() {
      let s = defs;
      const cols = ['id', 'city', 'sales'];
      cols.forEach((c, j) => { s += box(60 + j * 78, 20, 74, 26, c, { fs: 11, fill: 'rgba(78,161,255,.18)' }); });
      const rows = [['1', 'Lahore', '1200'], ['2', 'Karachi', '980'], ['3', 'Islamabad', '1540']];
      rows.forEach((r, i) => r.forEach((v, j) => { s += box(60 + j * 78, 50 + i * 28, 74, 24, v, { fs: 10.6, fill: 'rgba(19,26,36,.55)' }); }));
      s += `<text x="6" y="70" font-size="10.5" fill="currentColor" opacity=".75">index 0</text>`;
      s += `<text x="6" y="98" font-size="10.5" fill="currentColor" opacity=".75">1</text>`;
      s += `<text x="6" y="126" font-size="10.5" fill="currentColor" opacity=".75">2</text>`;
      s += `<text x="60" y="152" font-size="10.6" fill="currentColor" opacity=".82">axis=0 aggregates down columns; axis=1 aggregates across a row</text>`;
      return svg(320, 164, s);
    },
    broadcast() {
      let s = defs;
      s += box(20, 22, 120, 40, 'A: (3, 4)', { fs: 11 });
      s += box(170, 22, 90, 40, 'B: (4,)', { fs: 11, fill: 'rgba(194,151,255,.16)' });
      s += box(290, 22, 130, 40, 'A - mean(A, axis=1, keepdims=True)', { fs: 9.6, fill: 'rgba(126,231,135,.14)' });
      s += arrow(140, 42, 168, 42); s += arrow(260, 42, 288, 42);
      s += `<text x="20" y="86" font-size="10.8" fill="currentColor" opacity=".85">compare shapes right-to-left: 1 stretches, equal passes, anything else raises ValueError</text>`;
      s += `<text x="20" y="106" font-size="10.8" fill="currentColor" opacity=".85">(3,1) - (3,4) works; (3,) - (4,) fails - reshape to (3,1) or use keepdims</text>`;
      return svg(440, 120, s);
    },
    'api-flow'() {
      let s = defs;
      s += box(10, 30, 90, 40, 'client\nGET /predict?x=5', { fs: 9.6 });
      s += box(130, 30, 100, 40, 'server\nvalidate (Pydantic)', { fs: 9.6, fill: 'rgba(194,151,255,.14)' });
      s += box(260, 30, 100, 40, 'model\npredict()', { fs: 9.6, fill: 'rgba(126,231,135,.14)' });
      s += box(390, 30, 110, 40, 'response\n200 {y: 12.4}', { fs: 9.6 });
      s += arrow(100, 50, 128, 50); s += arrow(230, 50, 258, 50); s += arrow(360, 50, 388, 50);
      s += `<text x="10" y="100" font-size="10.6" fill="currentColor" opacity=".82">status codes: 200 ok, 400 bad input, 422 validation, 500 server bug, 503 overloaded</text>`;
      return svg(510, 112, s);
    },
    'docker-layers'() {
      let s = defs;
      const layers = ['base image: python:3.11-slim', 'dependencies (requirements.txt)', 'source code', 'command / entrypoint'];
      layers.forEach((l, i) => { s += box(20, 130 - i * 34, 300, 30, l, { fs: 10.6, fill: i === 1 ? 'rgba(78,161,255,.15)' : 'rgba(19,26,36,.6)' }); });
      s += `<text x="20" y="164" font-size="10.6" fill="currentColor" opacity=".82">layers cache: copy requirements before source so code edits do not reinstall packages</text>`;
      return svg(340, 176, s);
    },
  };

  function render(visual) {
    if (!visual) return '';
    const key = visual.svg_key;
    let body;
    if (generics[key]) body = generics[key]();
    else {
      const nodes = visual.nodes || [];
      let s = defs;
      const w = 560, perRow = Math.min(nodes.length, 3);
      nodes.forEach((n, i) => {
        const row = Math.floor(i / perRow), col = i % perRow;
        s += box(20 + col * 180, 24 + row * 62, 160, 46, n, { fs: 10.8 });
        if (col > 0) s += arrow(20 + col * 180 - 20, 47 + row * 62, 20 + col * 180 - 2, 47 + row * 62);
      });
      body = svg(w, 40 + Math.ceil(nodes.length / perRow) * 62, s);
    }
    return `<div class="visual-box">${body}<p class="visual-cap">${esc(visual.caption || '')}</p></div>`;
  }

  window.AcademyVisuals = { render };
})();
