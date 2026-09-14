/* Deep Data Science & AI Academy - UI logic (kept separate from content and styling) */
(function () {
  'use strict';

  const LS = {
    progress: 'ddsa.progress.v1',
    bookmarks: 'ddsa.bookmarks.v1',
    notes: 'ddsa.notes.v1',
    quiz: 'ddsa.quiz.v1',
    mode: 'ddsa.mode.v1',
    theme: 'ddsa.theme.v1',
    settings: 'ddsa.tutor.settings.v1',
  };
  const state = {
    day: 1,
    lesson: null,
    curriculum: null,
    searchIndex: [],
    mode: localStorage.getItem(LS.mode) || 'deep',
    progress: readJSON(LS.progress, {}),
    bookmarks: readJSON(LS.bookmarks, {}),
    notes: readJSON(LS.notes, {}),
    quizState: readJSON(LS.quiz, {}),
  };

  function readJSON(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key)) || fallback; } catch (e) { return fallback; }
  }
  function writeJSON(key, value) { localStorage.setItem(key, JSON.stringify(value)); }
  const $ = (sel) => document.querySelector(sel);
  const el = (tag, cls, html) => { const n = document.createElement(tag); if (cls) n.className = cls; if (html != null) n.innerHTML = html; return n; };
  const escapeHtml = (s) => String(s == null ? '' : s).replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

  /* ------------------------------------------------------------------ */
  /* data access: API first, static-file fallback (works on any host)     */
  /* ------------------------------------------------------------------ */
  async function getJSON(path, fallbackPath) {
    const candidates = [path];
    if (fallbackPath) candidates.push(fallbackPath);
    for (const url of candidates) {
      try {
        const res = await fetch(url, { cache: 'no-cache' });
        if (res.ok) return await res.json();
      } catch (e) { /* try next */ }
    }
    return null;
  }
  const api = {
    curriculum: () => getJSON('api/curriculum', './curriculum.json'),
    day: (d) => getJSON(`api/day/${d}`, `./content/day_${String(d).padStart(3, '0')}.json`),
    searchIndex: () => getJSON('./assets/search_index.json'),
    quizBank: () => getJSON('./quizzes/quiz_bank.json'),
    flashBank: () => getJSON('./flashcards/flashcard_bank.json'),
    interviewBank: () => getJSON('./interview/interview_bank.json'),
  };

  /* ------------------------------------------------------------------ */
  /* boot                                                                */
  /* ------------------------------------------------------------------ */
  async function boot() {
    document.body.dataset.mode = state.mode;
    document.documentElement.dataset.theme = localStorage.getItem(LS.theme) || 'dark';
    document.querySelectorAll('.mode-btn').forEach((b) => b.classList.toggle('active', b.dataset.mode === state.mode));
    state.searchIndex = (await api.searchIndex()) || [];
    state.curriculum = await api.curriculum();
    renderPhaseNav();
    updateProgressUI();
    const initial = Number((location.hash.match(/#\/day\/(\d+)/) || [])[1] || 1);
    await goToDay(initial);
    wireEvents();
  }

  /* ------------------------------------------------------------------ */
  /* navigation                                                          */
  /* ------------------------------------------------------------------ */
  function renderPhaseNav() {
    const nav = $('#phaseNav');
    nav.innerHTML = '';
    if (!state.curriculum) { nav.innerHTML = '<p class="muted">curriculum.json not found - run tools/build_content.py</p>'; return; }
    state.curriculum.phases.forEach((p) => {
      const d = el('details', 'phase');
      const done = p.days.filter((x) => state.progress[x.day]).length;
      d.innerHTML = `<summary><span class="pnum">P${p.n}</span><span>${escapeHtml(p.name)}</span>
        <span class="pdays">${p.start}-${p.end} &middot; ${done}/${p.count}</span></summary>`;
      const wrap = el('div', 'phase-days');
      p.days.forEach((day) => {
        const a = el('a', 'day-link' + (state.progress[day.day] ? ' done' : ''));
        a.href = `#/day/${day.day}`;
        a.dataset.day = day.day;
        const tag = day.tag && day.tag !== 'src' ? `<span class="tag ${day.tag}">${day.tag === 'ext' ? 'EXT' : 'MIX'}</span>` : '';
        a.innerHTML = `<span class="dnum">${day.day}${state.progress[day.day] ? ' &#10003;' : ''}</span><span>${escapeHtml(day.title)}</span>${tag}`;
        a.addEventListener('click', (e) => { e.preventDefault(); goToDay(day.day); closeSidebar(); });
        wrap.appendChild(a);
      });
      d.appendChild(wrap);
      nav.appendChild(d);
    });
    highlightActiveDay();
  }

  function highlightActiveDay() {
    document.querySelectorAll('.day-link').forEach((a) => a.classList.toggle('active', Number(a.dataset.day) === state.day));
    const active = document.querySelector('.day-link.active');
    if (active && active.closest('details') && window.innerWidth > 1020) active.closest('details').open = true;
  }

  async function goToDay(day) {
    day = Math.max(1, Math.min(275, Number(day) || 1));
    state.day = day;
    location.hash = `#/day/${day}`;
    $('#lesson').innerHTML = `<div class="loading"><div class="spinner"></div><p>Loading Day ${day}...</p></div>`;
    const lesson = await api.day(day);
    if (!lesson) {
      $('#lesson').innerHTML = `<div class="section"><h2>Day ${day} has not been built yet</h2>
        <p>Run <code>python3 tools/build_content.py</code> at the project root to generate the lesson files.</p></div>`;
      return;
    }
    state.lesson = lesson;
    renderLesson(lesson);
    updateNav();
    highlightActiveDay();
    window.scrollTo({ top: 0, behavior: 'instant' in window ? 'instant' : 'auto' });
    if (window.AcademyTutor) window.AcademyTutor.setLesson(lesson);
  }

  function updateNav() {
    $('#dayCounter').textContent = `Day ${state.day} / 275`;
    $('#btnPrev').disabled = state.day <= 1;
    $('#btnNext').disabled = state.day >= 275;
    $('#btnDone').textContent = state.progress[state.day] ? 'Completed \u2713 (undo)' : 'Mark day complete';
    $('#btnBookmark').textContent = state.bookmarks[state.day] ? 'Bookmarked \u2605' : 'Bookmark';
    const first = state.lesson ? state.lesson.nav.phase_first : 1;
    const phaseName = state.lesson ? state.lesson.phase.name : '';
    $('#brandSub').textContent = phaseName ? `Phase ${state.lesson.phase.n} \u00b7 ${phaseName}` : '275 days \u00b7 16 phases';
  }

  /* ------------------------------------------------------------------ */
  /* lesson rendering                                                    */
  /* ------------------------------------------------------------------ */
  function labelChip(name) { return `<span class="label-chip label-${name}">${name}</span>`; }

  function section(id, num, title, body, extraClass) {
    return `<section id="${id}" class="section ${extraClass || ''}">
      <h2><span class="num">${num}</span>${title}</h2>${body}</section>`;
  }

  function codeBlock(c, idx) {
    const label = c.label ? labelChip(c.label) : '';
    const out = c.output ? `<div class="out-label">Expected output</div><pre class="output">${escapeHtml(c.output)}</pre>` : '';
    const lineby = (c.line_by_line && c.line_by_line.length)
      ? `<details class="lineby"><summary>Line-by-line explanation (${c.line_by_line.length} points)</summary>
          <ol>${c.line_by_line.map((l) => `<li>${escapeHtml(l)}</li>`).join('')}</ol></details>` : '';
    return `<div class="code-block">
      <div class="code-head"><span class="title">${idx + 1}. ${escapeHtml(c.title)}</span>${label}
        <span class="badge">${escapeHtml(c.language || 'python')}</span>
        <button class="ghost-btn copy-btn" data-copy="${idx}">Copy code</button></div>
      <pre class="code" data-code="${idx}">${escapeHtml(c.code)}</pre>${out}${lineby}
      ${c.notes ? `<p class="muted" style="font-size:12.5px;margin-top:6px">${escapeHtml(c.notes)}</p>` : ''}
    </div>`;
  }

  function renderLesson(L) {
    const parts = [];
    const tagBadge = L.tag === 'ext' ? '<span class="badge ext">ACADEMY EXTENSION</span>'
      : L.tag === 'mix' ? '<span class="badge mix">SOURCE + EXTENSION</span>' : '<span class="badge">SOURCE-BACKED</span>';

    /* head */
    parts.push(`<header class="lesson-head">
      <div class="eyebrow">
        <span class="badge phase">Phase ${L.phase.n}</span>
        <span class="badge">${escapeHtml(L.difficulty)}</span>
        <span class="badge">${L.est_minutes} min</span>
        <span class="badge ${L.depth}">${L.depth === 'full' ? 'FULL LESSON' : 'GUIDED LESSON'}</span>
        ${tagBadge}
      </div>
      <h1 class="lesson-title">Day ${L.day}: ${escapeHtml(L.title)}</h1>
      <p class="lesson-sub">${escapeHtml(L.subtitle)}</p>
      ${L.tagline ? `<p class="tagline">${escapeHtml(L.tagline)}</p>` : ''}
    </header>`);

    /* 1 objectives */
    parts.push(section('objectives', 1, 'Learning objectives',
      `<ul>${L.learning_objectives.map((o) => `<li>${escapeHtml(o)}</li>`).join('')}</ul>`, 'sec-objectives'));

    /* 2 prerequisites */
    parts.push(section('prereq', 2, 'Prerequisites',
      `<ul>${L.prerequisites.map((p) => `<li>${escapeHtml(p)}</li>`).join('')}</ul>`));

    /* 3 why */
    parts.push(section('why', 3, 'Why this matters', `<p>${escapeHtml(L.why_this_matters)}</p>`));

    /* 4 concept: what/why/how */
    const C = L.concept;
    parts.push(section('concept', 4, `Concept ${labelChip('EXPLANATION')}`, `
      <div class="cards">
        <div class="card"><h4>What</h4><p>${escapeHtml(C.what)}</p></div>
        <div class="card"><h4>Why</h4><p>${escapeHtml(C.why)}</p></div>
        <div class="card"><h4>How - step by step</h4><p>${escapeHtml(C.how)}</p></div>
        ${C.topic_cards ? `<div class="card"><h4>Topic cards - work through each in order</h4>
          ${C.topic_cards.map((t) => `<div style="margin-bottom:10px"><b>${escapeHtml(t.topic)}</b>
            <ul>${t.prompts.map((p) => `<li>${escapeHtml(p)}</li>`).join('')}</ul></div>`).join('')}</div>` : ''}
      </div>`));

    /* 5 simple explanation (beginner) + intuition + analogy */
    parts.push(section('simple', 5, 'Simple explanation', `
      <div class="beginner-only"><p>${escapeHtml(C.intuition)}</p></div>
      <div class="advanced-only"><p>${escapeHtml(C.intuition)}</p></div>`, 'sec-simple'));

    /* 6 intuition */
    parts.push(section('intuition', 6, 'Intuition', `<p>${escapeHtml(C.intuition)}</p>`));

    /* 7 analogy */
    parts.push(section('analogy', 7, 'Real-world analogy', `<p>${escapeHtml(C.analogy)}</p>`));

    /* 8 visual */
    parts.push(section('visual', 8, 'Visual explanation',
      (window.AcademyVisuals ? window.AcademyVisuals.render(L.visual) : '')
      + `<p class="muted">${escapeHtml(L.visual.title)}</p>`, 'sec-visual'));

    /* 9 deep */
    parts.push(section('internals', 9, 'Internals - how it works underneath', `<p>${escapeHtml(C.internals)}</p>`));
    parts.push(section('deep', 10, 'Deep technical explanation', `
      <p>${escapeHtml(C.deep)}</p>
      ${C.math ? `<div class="card"><h4>Mathematics</h4><p>${escapeHtml(C.math)}</p></div>` : ''}`));

    /* 11 code */
    parts.push(section('code', 11, `Code examples ${labelChip('PRACTICE')}`,
      L.code_examples.length
        ? L.code_examples.map(codeBlock).join('')
        : '<p class="muted">No code attached to this lesson yet - the repository notebooks linked in the source section contain the original implementations.</p>',
      'sec-code'));

    /* 12 source trace */
    const T = L.source_trace;
    parts.push(section('source', 12, 'Source traceability', `
      <div class="card"><h4>Phase note</h4><p>${escapeHtml(T.phase_note)}</p></div>
      <div class="card" style="margin-top:10px"><h4>Original lecture moments (Urdu/Hindi)</h4>
        ${T.moments && T.moments.length ? T.moments.map((m) => `
          <div class="trace-item">
            <div class="trace-meta">${escapeHtml(m.timestamp)}<br>${escapeHtml(m.date || '')}</div>
            <div><p class="quote">${escapeHtml(m.quote)}</p>
              <a href="${m.deep_link}" target="_blank" rel="noopener">Watch at ${escapeHtml(m.timestamp)} - ${escapeHtml(m.video_title)}</a>
              ${m.fallback ? '<p class="muted" style="font-size:11.5px">Lecture opening (no topic-specific keyword match found - watch from here for context)</p>'
                           : `<p class="muted" style="font-size:11.5px">matched on: ${escapeHtml((m.matched_terms || []).join(', '))}</p>`}</div>
          </div>`).join('')
        : `<p class="muted">No keyword-matched transcript moment for this lesson. Full lecture links are listed below.</p>`}
      </div>
      ${T.videos && T.videos.length ? `<div class="card" style="margin-top:10px"><h4>Original recordings for this day</h4>
        <ul>${T.videos.map((v) => `<li><a href="${v.url}" target="_blank" rel="noopener">${escapeHtml(v.title)}</a>
          <span class="muted">(${escapeHtml(v.date || '')})</span></li>`).join('')}</ul></div>` : ''}
      ${T.code && T.code.length ? `<div class="card" style="margin-top:10px"><h4>Repository code used in this lesson</h4>
        <ul>${T.code.map((c) => `<li><code>${escapeHtml(c.path)}</code>${c.heading ? ` - ${escapeHtml(c.heading)}` : ''}</li>`).join('')}</ul></div>` : ''}
      <div class="card" style="margin-top:10px"><h4>Content labels used in this academy</h4>
        <ul>${Object.entries(L.labels).map(([k, v]) => `<li>${labelChip(k)} ${escapeHtml(Array.isArray(v) ? v[0] : v)}</li>`).join('')}</ul>
        <p class="muted" style="font-size:12.5px">${escapeHtml(T.traceability)}</p></div>`));

    /* 13 mistakes */
    parts.push(section('mistakes', 13, 'Common mistakes',
      L.common_mistakes.length ? L.common_mistakes.map((m) => `
        <div class="issue"><div class="head">${escapeHtml(m.mistake)}</div>
          <p><b>Why it hurts:</b> ${escapeHtml(m.why)}</p>
          <p><b>Fix:</b> ${escapeHtml(m.fix)}</p></div>`).join('')
        : '<p class="muted">Add your own mistakes list as you work: every error you hit once should be written here.</p>'));

    /* 14 debugging */
    parts.push(section('debugging', 14, 'Debugging examples',
      L.debugging.length ? L.debugging.map((d) => `
        <div class="issue debug"><div class="head">Symptom: ${escapeHtml(d.symptom)}</div>
          <p><b>Cause:</b> ${escapeHtml(d.cause)}</p><p><b>Fix:</b> ${escapeHtml(d.fix)}</p></div>`).join('')
        : '<p class="muted">No debugging scenarios recorded for this lesson.</p>'));

    /* 15 practice */
    parts.push(section('practice', 15, `Practice exercises ${labelChip('PRACTICE')}`,
      L.practice.length ? L.practice.map((p, i) => `
        <div class="exercise">
          <div class="code-head"><span class="lvl ${escapeHtml(p.level)}">${escapeHtml(p.level)}</span>
            <b>Exercise ${i + 1}</b></div>
          <p>${escapeHtml(p.task)}</p>
          <details><summary>Hint</summary><p>${escapeHtml(p.hint)}</p></details>
          <details><summary>Solution sketch</summary><p>${escapeHtml(p.solution)}</p></details>
        </div>`).join('')
        : '<p class="muted">Practice for this lesson: reimplement the linked repository notebook from the source section without looking.</p>',
      'sec-practice'));

    /* 16 challenge */
    parts.push(section('challenge', 16, `Mini challenge ${labelChip('PROJECT')}`, `
      <div class="card"><h3>${escapeHtml(L.mini_challenge.title)}</h3>
        <p>${escapeHtml(L.mini_challenge.brief)}</p>
        <p><b>Deliverable:</b> ${escapeHtml(L.mini_challenge.deliverable)}</p>
        <p><b>Stretch:</b> ${escapeHtml(L.mini_challenge.stretch)}</p></div>`, 'sec-challenge'));

    /* 17 interview */
    parts.push(section('interview', 17, `Interview questions ${labelChip('INTERVIEW')}`,
      `<div class="table-wrap"><table><thead><tr><th>Question</th><th>Model answer</th><th>Level</th></tr></thead><tbody>
        ${L.interview_questions.map((q) => `<tr><td>${escapeHtml(q.q)}</td><td>${escapeHtml(q.a)}</td>
          <td><span class="badge">${escapeHtml(q.level)}</span></td></tr>`).join('')}
      </tbody></table></div>`, 'sec-interview'));

    /* 18 real world */
    parts.push(section('realworld', 18, 'Real-world application', `<p>${escapeHtml(L.real_world)}</p>`));

    /* 19 production */
    parts.push(section('production', 19, `Production considerations ${labelChip('PRODUCTION')}`,
      `<ul>${L.production.map((p) => `<li>${escapeHtml(p)}</li>`).join('')}</ul>`));

    /* 20 recap */
    parts.push(section('recap', 20, 'Recap', `<ul>${L.recap.map((r) => `<li>${escapeHtml(r)}</li>`).join('')}</ul>`, 'sec-recap'));

    /* 21 revision */
    parts.push(section('revision', 21, 'Revision mode', `
      <div class="card"><p><b>One-liner:</b> ${escapeHtml(L.revision.one_liner)}</p>
        <p><b>Must remember:</b> ${L.revision.must_remember.map(escapeHtml).join(' &middot; ')}</p>
        <p><b>Code recall:</b> ${escapeHtml(L.revision.code_recall)}</p>
        <p><b>Teach-back:</b> ${escapeHtml(L.revision.teach_back)}</p></div>`, 'sec-revision'));

    /* 22 flashcards */
    parts.push(section('flashcards', 22, 'Flashcards', `
      <p class="muted">Click a card to flip it. Say the answer out loud before flipping.</p>
      <div class="fc-grid">${L.flashcards.map((c) => `
        <div class="fc"><div class="fc-inner">
          <div class="fc-face front">${escapeHtml(c.front)}</div>
          <div class="fc-face back">${escapeHtml(c.back)}</div>
        </div></div>`).join('')}</div>`));

    /* 23 quiz */
    parts.push(section('quiz', 23, 'Checkpoint quiz', renderQuiz(L), 'sec-quiz'));

    /* 24 project link */
    parts.push(section('project', 24, `Project connection ${labelChip('PROJECT')}`,
      `<p>${escapeHtml(L.project_link)}</p>`, 'sec-project'));

    $('#lesson').innerHTML = parts.join('');
    wireQuiz(L);
    wireCopyButtons(L);
  }

  function renderQuiz(L) {
    const saved = state.quizState[L.day] || {};
    return `<div id="quizBox">${L.quiz.map((q, qi) => {
      const chosen = saved[qi];
      return `<div class="quiz-q" data-q="${qi}">
        <div class="qtext">Q${qi + 1}. ${escapeHtml(q.q)}</div>
        ${q.options.map((o, oi) => {
        const cls = chosen == null ? '' : (oi === q.answer ? 'correct' : (oi === chosen ? 'wrong' : ''));
        return `<div class="opt ${cls}" data-q="${qi}" data-o="${oi}">
            <span class="key">${String.fromCharCode(65 + oi)}</span><span>${escapeHtml(o)}</span></div>`;
      }).join('')}
        <div class="quiz-explain" ${chosen == null ? 'hidden' : ''}>${escapeHtml(q.explain || '')}</div>
      </div>`;
    }).join('')}
      <div class="quiz-score" id="quizScore"></div>
      ${L.quiz[0] && L.quiz[0].type === 'self-check'
        ? '<p class="muted">This day uses guided self-checks until its full authored lesson is generated. Be honest - the checklist is the assessment.</p>'
        : ''}</div>`;
  }

  function wireQuiz(L) {
    const box = $('#quizBox');
    if (!box) return;
    box.querySelectorAll('.opt').forEach((opt) => {
      opt.addEventListener('click', () => {
        const qi = Number(opt.dataset.q);
        const oi = Number(opt.dataset.o);
        const cur = state.quizState[L.day] || {};
        if (cur[qi] != null) return;                       // one attempt per question
        cur[qi] = oi;
        state.quizState[L.day] = cur;
        writeJSON(LS.quiz, state.quizState);
        // repaint this question
        const qEl = box.querySelector(`.quiz-q[data-q="${qi}"]`);
        qEl.querySelectorAll('.opt').forEach((o, idx) => {
          o.classList.remove('correct', 'wrong');
          if (idx === L.quiz[qi].answer) o.classList.add('correct');
          else if (idx === oi) o.classList.add('wrong');
        });
        const ex = qEl.querySelector('.quiz-explain');
        if (ex) ex.hidden = false;
        updateQuizScore(L);
      });
    });
    updateQuizScore(L);
  }

  function updateQuizScore(L) {
    const cur = state.quizState[L.day] || {};
    const answered = Object.keys(cur).length;
    const correct = Object.entries(cur).filter(([i, a]) => L.quiz[i] && a === L.quiz[i].answer).length;
    const box = $('#quizScore');
    if (box) box.textContent = answered ? `Score: ${correct}/${answered} answered correctly (${L.quiz.length} questions)` : '';
  }

  function wireCopyButtons() {
    document.querySelectorAll('[data-copy]').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const i = btn.dataset.copy;
        const code = document.querySelector(`pre.code[data-code="${i}"]`);
        if (!code) return;
        try {
          await navigator.clipboard.writeText(code.textContent);
          toast('Code copied');
        } catch (e) {
          const r = document.createRange(); r.selectNode(code);
          window.getSelection().removeAllRanges(); window.getSelection().addRange(r);
          toast('Selected - press Ctrl/Cmd+C');
        }
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* search                                                              */
  /* ------------------------------------------------------------------ */
  function localSearch(q) {
    const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    const out = [];
    state.searchIndex.forEach((item) => {
      const title = (item.title || '').toLowerCase();
      const hay = [title, item.phase_name || '', (item.topics || []).join(' '), (item.keywords || []).join(' '),
        (item.objectives || []).join(' ')].join(' ').toLowerCase();
      let score = 0;
      terms.forEach((t) => { if (title.includes(t)) score += 6; score += 2 * (hay.split(t).length - 1); });
      if (score) out.push({ ...item, score });
    });
    return out.sort((a, b) => b.score - a.score).slice(0, 30);
  }

  async function runSearch(q) {
    const box = $('#searchResults');
    if (!q || q.length < 2) { box.hidden = true; return; }
    let results = null;
    try {
      const res = await fetch(`api/search?q=${encodeURIComponent(q)}`);
      if (res.ok) results = await res.json();
    } catch (e) { /* offline */ }
    if (!results || !results.length) results = localSearch(q);
    if (!results.length) { box.innerHTML = '<div class="sr-item">No matches. Try: joins, attention, drift, docker, PCA.</div>'; box.hidden = false; return; }
    box.innerHTML = results.map((r) => `<a class="sr-item" href="#/day/${r.day}" data-day="${r.day}">
      <b>Day ${r.day}</b> ${escapeHtml(r.title)}
      <small>Phase ${r.phase} &middot; ${escapeHtml(r.phase_name || '')} &middot; ${escapeHtml(r.difficulty || '')}${r.tag === 'ext' ? ' &middot; extension' : ''}</small></a>`).join('');
    box.hidden = false;
    box.querySelectorAll('.sr-item').forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault(); box.hidden = true; $('#search').value = ''; goToDay(Number(a.dataset.day));
    }));
  }

  /* ------------------------------------------------------------------ */
  /* events & utilities                                                  */
  /* ------------------------------------------------------------------ */
  function wireEvents() {
    $('#btnPrev').addEventListener('click', () => goToDay(state.day - 1));
    $('#btnNext').addEventListener('click', () => goToDay(state.day + 1));
    $('#dayGo').addEventListener('click', () => { goToDay($('#dayJump').value); $('#dayJump').value = ''; });
    $('#dayJump').addEventListener('keydown', (e) => { if (e.key === 'Enter') $('#dayGo').click(); });

    $('#btnDone').addEventListener('click', () => {
      if (state.progress[state.day]) delete state.progress[state.day]; else state.progress[state.day] = Date.now();
      writeJSON(LS.progress, state.progress); updateProgressUI(); renderPhaseNav(); updateNav();
      toast(state.progress[state.day] ? 'Day marked complete' : 'Marked incomplete');
    });
    $('#btnBookmark').addEventListener('click', () => {
      if (state.bookmarks[state.day]) delete state.bookmarks[state.day]; else state.bookmarks[state.day] = Date.now();
      writeJSON(LS.bookmarks, state.bookmarks); updateNav(); toast('Bookmarks updated');
    });
    $('#btnPrint').addEventListener('click', () => window.print());

    $('#btnNotes').addEventListener('click', openNotes);
    $('#saveNotes').addEventListener('click', saveNotes);
    $('#btnTutor').addEventListener('click', () => toggleTutor(true));
    $('#openTutorSide').addEventListener('click', () => toggleTutor(true));
    $('#closeTutor').addEventListener('click', () => toggleTutor(false));
    $('#openHelp').addEventListener('click', () => { $('#helpModal').hidden = false; });
    $('#openSettings').addEventListener('click', openSettingsModal);
    $('#saveSettings').addEventListener('click', saveSettings);
    $('#clearSettings').addEventListener('click', clearSettings);
    $('#toggleTheme').addEventListener('click', () => {
      const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = next; localStorage.setItem(LS.theme, next);
    });
    document.querySelectorAll('[data-close-modal]').forEach((b) => b.addEventListener('click', () => {
      b.closest('.modal').hidden = true;
    }));
    document.querySelectorAll('.modal').forEach((m) => m.addEventListener('click', (e) => { if (e.target === m) m.hidden = true; }));

    document.querySelectorAll('.mode-btn').forEach((b) => b.addEventListener('click', () => {
      state.mode = b.dataset.mode; localStorage.setItem(LS.mode, state.mode);
      document.body.dataset.mode = state.mode;
      document.querySelectorAll('.mode-btn').forEach((x) => x.classList.toggle('active', x.dataset.mode === state.mode));
      toast(`Mode: ${state.mode}`);
    }));

    $('#search').addEventListener('input', (e) => runSearch(e.target.value.trim()));
    $('#search').addEventListener('blur', () => setTimeout(() => { $('#searchResults').hidden = true; }, 180));
    $('#openSidebar').addEventListener('click', () => $('#sidebar').classList.add('open'));
    $('#closeSidebar').addEventListener('click', closeSidebar);

    // flashcards flip (event delegation - cards are re-rendered per lesson)
    $('#lesson').addEventListener('click', (e) => {
      const card = e.target.closest('.fc');
      if (card) card.classList.toggle('flipped');
    });

    window.addEventListener('hashchange', () => {
      const m = location.hash.match(/#\/day\/(\d+)/);
      if (m && Number(m[1]) !== state.day) goToDay(Number(m[1]));
    });

    document.addEventListener('keydown', (e) => {
      if (/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) return;
      const k = e.key.toLowerCase();
      if (k === 'j') goToDay(state.day + 1);
      else if (k === 'k') goToDay(state.day - 1);
      else if (k === '/') { e.preventDefault(); $('#search').focus(); }
      else if (k === 't') toggleTutor($('#tutor').hidden);
      else if (k === 'n') openNotes();
      else if (k === 'm') $('#btnDone').click();
      else if (k === 'escape') { $('#tutor').hidden = true; closeSidebar(); document.querySelectorAll('.modal').forEach((m) => m.hidden = true); }
      else if ('123456'.includes(k)) {
        const modes = ['beginner', 'deep', 'code', 'interview', 'project', 'revision'];
        const btn = document.querySelector(`.mode-btn[data-mode="${modes[Number(k) - 1]}"]`);
        if (btn) btn.click();
      }
    });
  }

  function closeSidebar() { $('#sidebar').classList.remove('open'); }

  function toggleTutor(show) {
    $('#tutor').hidden = !show;
    if (show && window.AcademyTutor) window.AcademyTutor.setLesson(state.lesson);
  }

  function openNotes() {
    $('#notesArea').value = state.notes[state.day] || '';
    $('#notesMeta').textContent = `Day ${state.day} notes are saved in this browser.`;
    $('#notesModal').hidden = false;
    $('#notesArea').focus();
  }
  function saveNotes() {
    state.notes[state.day] = $('#notesArea').value;
    writeJSON(LS.notes, state.notes);
    $('#notesModal').hidden = true;
    toast('Notes saved');
  }

  function openSettingsModal() {
    const s = readJSON(LS.settings, {});
    $('#setEndpoint').value = s.endpoint || '';
    $('#setModel').value = s.model || '';
    $('#setKey').value = s.key || '';
    $('#settingsModal').hidden = false;
  }
  function saveSettings() {
    writeJSON(LS.settings, { endpoint: $('#setEndpoint').value.trim(), model: $('#setModel').value.trim(), key: $('#setKey').value });
    $('#settingsModal').hidden = true;
    toast('Tutor settings saved in this browser');
    if (window.AcademyTutor) window.AcademyTutor.reloadSettings();
  }
  function clearSettings() {
    localStorage.removeItem(LS.settings);
    $('#setEndpoint').value = ''; $('#setModel').value = ''; $('#setKey').value = '';
    if (window.AcademyTutor) window.AcademyTutor.reloadSettings();
    toast('Tutor settings cleared');
  }

  function updateProgressUI() {
    const done = Object.keys(state.progress).length;
    $('#progressFill').style.width = `${(done / 275) * 100}%`;
    $('#progressLabel').textContent = `${done} / 275 days complete`;
  }

  let toastTimer;
  function toast(msg) {
    const t = $('#toast');
    t.textContent = msg; t.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { t.hidden = true; }, 2200);
  }

  window.Academy = { goToDay, getState: () => state, toast, api };
  document.addEventListener('DOMContentLoaded', boot);
})();
