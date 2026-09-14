/* AI Tutor
   Two modes:
   1) OFFLINE (default, zero cost, always works): answers are composed from the
      current lesson's own materials - concept, code, mistakes, quiz, interview
      bank. It knows the current lesson and topic because it is given the lesson
      JSON on every navigation.
   2) LIVE (optional): add an OpenAI-compatible endpoint + key in settings. The
      browser calls the endpoint directly with the lesson as context, so no key
      ever touches this app's server.
*/
(function () {
  'use strict';
  const LS_SETTINGS = 'ddsa.tutor.settings.v1';
  let lesson = null;
  let history = [];
  let settings = loadSettings();
  let quizPointer = 0;

  function loadSettings() {
    try { return JSON.parse(localStorage.getItem(LS_SETTINGS)) || {}; } catch (e) { return {}; }
  }
  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

  function setLesson(l) {
    lesson = l;
    if (l) {
      $('#tutorContext').textContent = `Day ${l.day} \u00b7 ${l.title}`;
      history = [];
      quizPointer = 0;
      $('#tutorLog').innerHTML = '';
      say(`I am your tutor for **Day ${l.day}: ${l.title}**.\n\n` +
        `Topics today: ${l.topics.slice(0, 4).join('; ')}.\n\n` +
        `Ask me anything, or use a quick button: explain simply, quiz me, interview me, give me a coding problem, or ask why your code is wrong.`);
    }
  }

  function say(text, who) {
    const log = $('#tutorLog');
    const node = document.createElement('div');
    node.className = `msg ${who || 'bot'}`;
    node.innerHTML = esc(text)
      .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
      .replace(/`([^`]+)`/g, '<code>$1</code>');
    log.appendChild(node);
    log.scrollTop = log.scrollHeight;
  }

  /* ------------------------- offline answer engine ------------------------ */
  function offlineAnswer(intent, userText) {
    if (!lesson) return 'Open a lesson first - I answer inside the current day.';
    const t = (userText || '').toLowerCase();
    const pick = (arr, n) => (arr || []).slice(0, n || 3);
    const bullet = (arr) => arr.map((x) => `- ${x}`).join('\n');

    if (intent === 'simple' || intent === 'beginner') {
      return `**Simply put.**\n${lesson.concept.intuition}\n\n**Analogy.**\n${lesson.concept.analogy}\n\n` +
        `**In one line for revision:** ${lesson.recap[0] || lesson.title}`;
    }
    if (intent === 'technical') {
      return `**Technical explanation.**\n${lesson.concept.internals}\n\n**Deeper.**\n${lesson.concept.deep}\n\n` +
        (lesson.concept.math ? `**Mathematics.**\n${lesson.concept.math}\n\n` : '') +
        `**Where it fails.**\n${bullet(pick(lesson.common_mistakes.map((m) => m.mistake + ' -> ' + m.fix), 3))}`;
    }
    if (intent === 'example' || intent === 'realworld') {
      const code = lesson.code_examples[0];
      return `**Real-world use.**\n${lesson.real_world}\n\n` +
        (code ? `**Worked example: ${code.title}**\n\`\`\`\n${code.code.split('\n').slice(0, 18).join('\n')}\n\`\`\`\n` +
          (code.output ? `Expected output:\n${code.output}\n` : '') : '') +
        `\n**Production notes.**\n${bullet(pick(lesson.production, 3))}`;
    }
    if (intent === 'coding') {
      const ex = lesson.practice.filter((p) => /medium|hard/.test(p.level))[0] || lesson.practice[0];
      return `**Coding problem (Day ${lesson.day}).**\n${ex ? ex.task : lesson.mini_challenge.brief}\n\n` +
        `**Hint.** ${ex ? ex.hint : lesson.mini_challenge.stretch}\n\n` +
        `**Deliverable.** ${lesson.mini_challenge.deliverable}\n\n` +
        `Paste your code and I will help you debug it: describe the exact error message and the line it points to.`;
    }
    if (intent === 'quiz') {
      const q = lesson.quiz[quizPointer % lesson.quiz.length];
      quizPointer += 1;
      return `**Quiz question.**\n${q.q}\n\n${q.options.map((o, i) => `${String.fromCharCode(65 + i)}. ${o}`).join('\n')}\n\n` +
        `Reply with the letter. (Correct answer + explanation: ${String.fromCharCode(65 + q.answer)} - ${q.explain})`;
    }
    if (intent === 'interview') {
      const q = lesson.interview_questions[0];
      return `**Interview drill.**\nQ: ${q.q}\n\nModel answer:\n${q.a}\n\n` +
        `Now answer out loud in 60 seconds, then check: did you include a limitation? Did you give a concrete example?`;
    }
    if (intent === 'whywrong') {
      return `**Debugging checklist for Day ${lesson.day}.**\n` +
        bullet(pick(lesson.debugging.map((d) => `${d.symptom} | cause: ${d.cause} | fix: ${d.fix}`), 3)) +
        `\n\n**Tell me three things and I can narrow it down:**\n1. the exact error text (last line of the traceback),\n` +
        `2. the shape/dtype of your input data,\n3. the smallest input that still fails.\n\n` +
        `General rule: print the value and its type BEFORE the failing line, not after.`;
    }
    if (intent === 'production') {
      return `**Production considerations (Day ${lesson.day}).**\n${bullet(pick(lesson.production, 4))}\n\n` +
        `**Deployment context.** ${lesson.project_link}`;
    }

    // free text: keyword match against the lesson's own sections
    const corpus = [
      ['concept (what)', lesson.concept.what], ['why it matters', lesson.why_this_matters],
      ['how it works', lesson.concept.how], ['internals', lesson.concept.internals],
      ['intuition', lesson.concept.intuition], ['analogy', lesson.concept.analogy],
      ['deep dive', lesson.concept.deep], ['maths', lesson.concept.math || ''],
      ['real world', lesson.real_world], ['recap', lesson.recap.join(' ')],
      ['objectives', lesson.learning_objectives.join(' ')],
      ['code', lesson.code_examples.map((c) => c.title + ' ' + c.code).join('\n').slice(0, 1200)],
      ['mistakes', lesson.common_mistakes.map((m) => `${m.mistake} ${m.why} ${m.fix}`).join(' ')],
      ['debugging', lesson.debugging.map((d) => `${d.symptom} ${d.cause} ${d.fix}`).join(' ')],
      ['interview', lesson.interview_questions.map((q) => `${q.q} ${q.a}`).join(' ')],
    ];
    const words = t.split(/\s+/).filter((w) => w.length > 3);
    let best = null, bestScore = 0;
    corpus.forEach(([name, text]) => {
      if (!text) return;
      const low = text.toLowerCase();
      const score = words.reduce((acc, w) => acc + (low.split(w).length - 1), 0);
      if (score > bestScore) { bestScore = score; best = { name, text }; }
    });
    if (best && bestScore > 0) {
      return `**Closest match from today's lesson (${best.name}).**\n${best.text.slice(0, 900)}\n\n` +
        `If that is not what you meant, rephrase with a keyword, or press "Explain this technically" / "Give me an example".`;
    }
    return `I answer from **Day ${lesson.day}: ${lesson.title}**.\n\n` +
      `Today's topics: ${lesson.topics.join('; ')}.\n\nTry:\n` +
      `- "explain ${lesson.topics[0]} simply"\n- "give me a coding problem on ${lesson.topics[0]}"\n` +
      `- "quiz me"\n- "how is ${lesson.topics[0]} used in production?"\n\n` +
      `For a live model that can go beyond this lesson, add an API key in settings.`;
  }

  /* ------------------------------- live mode ------------------------------ */
  async function liveAnswer(userText) {
    const ctx = lesson ? {
      day: lesson.day, title: lesson.title, phase: lesson.phase.name, topics: lesson.topics,
      objectives: lesson.learning_objectives, concept: lesson.concept,
      code: lesson.code_examples.map((c) => ({ title: c.title, code: c.code })),
      mistakes: lesson.common_mistakes, production: lesson.production,
      interview: lesson.interview_questions,
    } : {};
    const system = 'You are a patient, precise data science tutor inside a 275-day academy. ' +
      'Answer using the lesson context when relevant. Prefer short structured answers with a concrete example. ' +
      'Never invent facts about the original course; label added knowledge as EXTENSION.\n\n' +
      'LESSON CONTEXT:\n' + JSON.stringify(ctx).slice(0, 12000);
    const messages = [{ role: 'system', content: system }]
      .concat(history.slice(-6))
      .concat([{ role: 'user', content: userText }]);
    const res = await fetch(settings.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${settings.key}` },
      body: JSON.stringify({ model: settings.model || 'gpt-4o-mini', messages, temperature: 0.3 }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    return data.choices?.[0]?.message?.content || JSON.stringify(data).slice(0, 800);
  }

  /* --------------------------------- wiring ------------------------------- */
  function submit(text, intent) {
    if (!text && !intent) return;
    if (text) { say(text, 'user'); history.push({ role: 'user', content: text }); }
    const local = offlineAnswer(intent, text);
    say(local);
    history.push({ role: 'assistant', content: local });

    if (settings.endpoint && settings.key && text) {
      say('(consulting the connected model...)');
      liveAnswer(text)
        .then((reply) => { say(reply); history.push({ role: 'assistant', content: reply }); })
        .catch((err) => say(`Live model unavailable (${err.message}). Offline answer above still applies.`));
    }
  }

  function init() {
    $('#tutorQuick')?.addEventListener('click', (e) => {
      const btn = e.target.closest('button[data-intent]');
      if (!btn) return;
      const intent = btn.dataset.intent;
      say(btn.textContent, 'user');
      submit(null, intent);
    });
    $('#tutorForm')?.addEventListener('submit', (e) => {
      e.preventDefault();
      const v = $('#tutorInput').value.trim();
      if (!v) return;
      $('#tutorInput').value = '';
      submit(v, null);
    });
  }

  window.AcademyTutor = {
    setLesson,
    reloadSettings: () => { settings = loadSettings(); },
    ask: (text, intent) => submit(text, intent),
  };
  document.addEventListener('DOMContentLoaded', init);
})();
