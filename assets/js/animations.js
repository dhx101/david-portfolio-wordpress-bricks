(function () {
  if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined" || typeof SplitText === "undefined") {
    return;
  }

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) return;

  gsap.registerPlugin(ScrollTrigger, SplitText);

  // Wraps each split unit (word or line) in its own overflow-hidden box, so
  // animating the unit's yPercent makes it rise up from behind a mask
  // instead of just fading in on top of whatever's below it.
  function maskReveal(elements, display) {
    elements.forEach(function (el) {
      var mask = document.createElement("span");
      mask.className = "reveal-mask";
      mask.style.display = display;
      mask.style.overflow = "hidden";
      mask.style.verticalAlign = "top";
      el.parentNode.insertBefore(mask, el);
      mask.appendChild(el);
    });
  }

  // Card contents (headings, labels, paragraphs inside a project/study/job
  // "terminal" card) shouldn't get their own word-by-word reveal — they just
  // ride along with the card's single fade-up (see grid reveal below) instead
  // of animating separately on top of it.
  function isInsideCard(el) {
    return !!el.closest(".terminal");
  }

  document.fonts.ready.then(function () {
    // 1. Split-text word reveal for every heading (outside cards)
    document.querySelectorAll("h1.brxe-heading, h2.brxe-heading, h3.brxe-heading").forEach(function (heading) {
      if (isInsideCard(heading)) return;
      var split = new SplitText(heading, { type: "words", wordsClass: "word" });
      maskReveal(split.words, "inline-block");
      gsap.set(split.words, { yPercent: 110 });
      gsap.to(split.words, {
        yPercent: 0,
        duration: 0.7,
        ease: "power3.out",
        stagger: 0.045,
        scrollTrigger: {
          trigger: heading,
          start: "top 92%",
          toggleActions: "play none none none",
          fastScrollEnd: true
        }
      });
    });

    // 2. Split-text line reveal for the intro/label paragraphs (rise from behind a mask, line by line)
    // "top 97%" (rather than a lower %) is intentional: an element sitting very
    // close to the bottom of the page (e.g. the footer copyright line) may run out
    // of scroll room before its top ever reaches a stricter percentage down the
    // viewport, and its reveal would then never fire no matter how far the user
    // scrolls. A start point this close to "as soon as it's barely visible" is
    // always reachable.
    document.querySelectorAll(".label-holo.brxe-text-basic, p.brxe-text-basic.label").forEach(function (p) {
      if (isInsideCard(p)) return;
      var split = new SplitText(p, { type: "lines", linesClass: "line" });
      maskReveal(split.lines, "block");
      gsap.set(split.lines, { yPercent: 100 });
      gsap.to(split.lines, {
        yPercent: 0,
        duration: 0.6,
        ease: "power2.out",
        stagger: 0.08,
        scrollTrigger: {
          trigger: p,
          start: "top 97%",
          toggleActions: "play none none none",
          fastScrollEnd: true
        }
      });
    });

    // 3. Staggered fade-up reveal for card/badge grids
    var gridSelectors = [
      ".brx-grid",
      ".proyectos-grid",
      ".estudios-list",
      ".experiencia-list",
      ".home-preview-list",
      ".infraestructure-content",
      "#brxe-vzdezc",
      "#brxe-qyctxd"
    ];
    document.querySelectorAll(gridSelectors.join(",")).forEach(function (grid) {
      var items = grid.children;
      if (!items.length) return;
      gsap.set(items, { opacity: 0, y: 48 });
      gsap.to(items, {
        opacity: 1,
        y: 0,
        duration: 0.65,
        ease: "power2.out",
        stagger: 0.09,
        scrollTrigger: {
          trigger: grid,
          start: "top 92%",
          toggleActions: "play none none none",
          fastScrollEnd: true
        }
      });
    });

    // 4. Image reveal: soft scale-in + fade as images enter the viewport
    document.querySelectorAll(".background-glow img, .project-card-image img, .study-card-image img, .brxe-image img").forEach(function (img) {
      gsap.fromTo(
        img,
        { scale: 1.12, opacity: 0 },
        {
          scale: 1,
          opacity: 1,
          duration: 1.1,
          ease: "power2.out",
          scrollTrigger: {
            trigger: img,
            start: "top 92%",
            toggleActions: "play none none none",
            fastScrollEnd: true
          }
        }
      );
    });

    // 5. Terminal boot log: typewriter-style staggered line reveal (hero terminal)
    var terminalLines = document.querySelectorAll(".terminal-line, .terminal-output");
    if (terminalLines.length) {
      gsap.set(terminalLines, { opacity: 0, x: -12 });
      gsap.to(terminalLines, {
        opacity: 1,
        x: 0,
        duration: 0.4,
        stagger: 0.16,
        delay: 0.4,
        ease: "power1.out"
      });
    }

    // 6. Header + hero entrance on load
    gsap.from("#brx-header", { opacity: 0, y: -24, duration: 0.7, ease: "power2.out", clearProps: "transform" });

    // 7. Section labels ("00 // USER_PROFILE" etc.) - word-by-word reveal from behind a mask
    document.querySelectorAll(".label.text-blue.brxe-text-basic:not(.label-holo)").forEach(function (label) {
      if (isInsideCard(label)) return;
      var split = new SplitText(label, { type: "words", wordsClass: "word" });
      maskReveal(split.words, "inline-block");
      gsap.set(split.words, { yPercent: 100 });
      gsap.to(split.words, {
        yPercent: 0,
        duration: 0.4,
        stagger: 0.05,
        ease: "power2.out",
        scrollTrigger: {
          trigger: label,
          start: "top 96%",
          toggleActions: "play none none none",
          fastScrollEnd: true
        }
      });
    });

    ScrollTrigger.refresh();

    // Safety net: under real-world load (slow web-font swap, an impatient
    // scroller racing the setup script), a reveal's target can end up out of
    // sync with what GSAP's own tween thinks it already animated — the tween
    // reports itself complete while the element on screen still shows its
    // pre-reveal offset, and re-driving that same tween (progress(), gsap.set
    // with the same cached value, etc.) is a no-op because GSAP skips writes
    // it believes are redundant. So instead of trusting GSAP's bookkeeping,
    // directly clear the raw CSS on any split word/line that's already been
    // scrolled well into view but still visually hasn't revealed itself.
    function sweepStuckReveals() {
      document.querySelectorAll(".word, .line").forEach(function (el) {
        var rect = el.getBoundingClientRect();
        if (rect.top > window.innerHeight) return; // still below the fold — correctly not revealed yet
        var transform = getComputedStyle(el).transform;
        if (transform && transform !== "none" && transform !== "matrix(1, 0, 0, 1, 0, 0)") {
          el.style.transform = "none";
          el.style.translate = "none";
          el.style.opacity = "1";
        }
      });
    }
    sweepStuckReveals();
    var sweepTimer;
    window.addEventListener("scroll", function () {
      clearTimeout(sweepTimer);
      sweepTimer = setTimeout(sweepStuckReveals, 150);
    }, { passive: true });
  });
})();
