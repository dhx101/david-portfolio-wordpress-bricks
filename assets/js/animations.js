(function () {
  if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined" || typeof SplitText === "undefined") {
    return;
  }

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) return;

  gsap.registerPlugin(ScrollTrigger, SplitText);

  document.fonts.ready.then(function () {
    // 1. Split-text char reveal for every heading
    document.querySelectorAll("h1.brxe-heading, h2.brxe-heading, h3.brxe-heading").forEach(function (heading) {
      var split = new SplitText(heading, { type: "chars,words", charsClass: "char" });
      gsap.set(split.chars, { opacity: 0, yPercent: 110, rotateZ: 4 });
      gsap.to(split.chars, {
        opacity: 1,
        yPercent: 0,
        rotateZ: 0,
        duration: 0.7,
        ease: "power3.out",
        stagger: 0.018,
        scrollTrigger: {
          trigger: heading,
          start: "top 88%",
          toggleActions: "play none none none"
        }
      });
    });

    // 2. Split-text line reveal for the intro/label paragraphs (fade + slide, line by line)
    document.querySelectorAll(".label-holo.brxe-text-basic, p.brxe-text-basic.label").forEach(function (p) {
      var split = new SplitText(p, { type: "lines", linesClass: "line" });
      gsap.set(split.lines, { opacity: 0, y: 16 });
      gsap.to(split.lines, {
        opacity: 1,
        y: 0,
        duration: 0.6,
        ease: "power2.out",
        stagger: 0.08,
        scrollTrigger: {
          trigger: p,
          start: "top 90%",
          toggleActions: "play none none none"
        }
      });
    });

    // 3. Staggered fade-up reveal for card/badge grids
    var gridSelectors = [
      ".brx-grid",
      ".proyectos-grid",
      ".estudios-list",
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
          start: "top 85%",
          toggleActions: "play none none none"
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
            start: "top 88%",
            toggleActions: "play none none none"
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
    gsap.from("#brx-header", { opacity: 0, y: -24, duration: 0.7, ease: "power2.out" });

    // 7. Section labels ("00 // USER_PROFILE" etc.) - letter-by-letter typing feel
    document.querySelectorAll(".label.text-blue.brxe-text-basic:not(.label-holo)").forEach(function (label) {
      var split = new SplitText(label, { type: "chars", charsClass: "char" });
      gsap.set(split.chars, { opacity: 0 });
      gsap.to(split.chars, {
        opacity: 1,
        duration: 0.02,
        stagger: 0.02,
        ease: "none",
        scrollTrigger: {
          trigger: label,
          start: "top 92%",
          toggleActions: "play none none none"
        }
      });
    });

    ScrollTrigger.refresh();
  });
})();
