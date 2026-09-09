(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ── 1. Inject SVG circle around .circled elements ────────────────────────
  const CIRCLE_PATH = 'M50 6 C 18 4, 6 22, 8 32 C 11 50, 50 58, 80 52 C 95 49, 96 28, 88 16 C 78 4, 60 4, 50 6 Z';
  document.querySelectorAll('.circled').forEach((el) => {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 100 60');
    svg.setAttribute('preserveAspectRatio', 'none');
    svg.setAttribute('aria-hidden', 'true');
    svg.classList.add('circled-trace', 'draw-stroke');
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', CIRCLE_PATH);
    path.setAttribute('fill', 'none');
    path.setAttribute('stroke', 'currentColor');
    path.setAttribute('stroke-width', '2.5');
    path.setAttribute('stroke-linecap', 'round');
    svg.appendChild(path);
    el.appendChild(svg);
  });

  // ── 2. Prepare every .draw-stroke (compute path lengths) ─────────────────
  document.querySelectorAll('.draw-stroke').forEach((svg) => {
    svg.querySelectorAll('path, line, polyline').forEach((p) => {
      let len = 0;
      try { len = p.getTotalLength(); } catch (_) { len = 300; }
      p.style.strokeDasharray = len;
      p.style.strokeDashoffset = reduced ? 0 : len;
    });
  });

  if (reduced) {
    document.querySelectorAll('[data-reveal]').forEach((el) => el.classList.add('is-revealed'));
    document.querySelectorAll('.polaroid-drop').forEach((el) => el.classList.add('is-landed'));
    document.querySelectorAll('.tl-item').forEach((el) => el.classList.add('is-active'));
    document.querySelectorAll('.draw-stroke, .highlight, .underline-hand').forEach((el) => el.classList.add('is-drawn'));
    return;
  }

  // ── 3. Assign stagger delay on timeline items based on index ──────────────
  document.querySelectorAll('.timeline .tl-item').forEach((el, i) => {
    if (!el.hasAttribute('data-reveal-delay')) el.setAttribute('data-reveal-delay', String(Math.min(i, 4)));
  });

  // Pre-compute cascade delays for grouped polaroids (e.g. .hobbies)
  const polaroidDelay = new WeakMap();
  document.querySelectorAll('.hobbies .polaroid-drop').forEach((el, i) => {
    polaroidDelay.set(el, i * 180);
  });

  // ── 4. Single IntersectionObserver dispatching to the right behavior ─────
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      if (el.matches('[data-reveal]')) el.classList.add('is-revealed');
      if (el.classList.contains('polaroid-drop')) {
        const delay = polaroidDelay.get(el) || 0;
        if (delay) setTimeout(() => el.classList.add('is-landed'), delay);
        else el.classList.add('is-landed');
      }
      if (el.classList.contains('draw-stroke') || el.classList.contains('highlight') || el.classList.contains('underline-hand')) {
        el.classList.add('is-drawn');
      }
      io.unobserve(el);
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });

  document.querySelectorAll('[data-reveal], .polaroid-drop, .draw-stroke, .highlight, .underline-hand').forEach((el) => {
    // Hero polaroid is handled by the load-time setTimeout below for nicer pacing
    if (el.matches('.hero-pose .polaroid-drop')) return;
    io.observe(el);
  });

  // ── 5/6. Timeline — line progress + dot activation, both tied to scroll ──
  // Dots flip to orange exactly when the vertical orange line reaches them.
  const timeline = document.querySelector('.timeline');
  if (timeline) {
    const items = Array.from(timeline.querySelectorAll('.tl-item'));
    let ticking = false;
    const update = () => {
      const r = timeline.getBoundingClientRect();
      const tlH = r.height;
      const mid = window.innerHeight * 0.5;
      const p = Math.max(0, Math.min(1, (mid - r.top) / tlH));
      timeline.style.setProperty('--tl-progress', p.toFixed(3));
      // The orange line in timeline-local Y: top:8px, height = p*(H-16).
      // So its bottom edge is at 8 + p*(H-16).
      const lineBottom = 8 + p * Math.max(0, tlH - 16);
      // Each .tl-item::before is at top:6px, 18px tall → center at offsetTop + 15.
      items.forEach((el) => {
        const dotCenter = el.offsetTop + 15;
        el.classList.toggle('is-active', lineBottom >= dotCenter);
      });
      ticking = false;
    };
    const onScroll = () => {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    update();
  }

  // ── 6b. Site frames — the captured screenshot scrolls while it's on screen ─
  // Only the frames actually in view animate, so a page holding six of them
  // never pays for more than the one or two the visitor is looking at.
  const frames = document.querySelectorAll('.site-frame');
  if (frames.length) {
    const frameIO = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        entry.target.classList.toggle('is-playing', entry.isIntersecting);
      });
    }, { threshold: 0.4 });
    frames.forEach((el) => frameIO.observe(el));
  }

  // ── 7. Hero polaroid drops on load (above the fold) ──────────────────────
  window.addEventListener('load', () => {
    document.querySelectorAll('.hero-pose .polaroid-drop').forEach((el) => {
      setTimeout(() => el.classList.add('is-landed'), 350);
    });
  });
})();
