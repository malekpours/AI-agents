// موتور ساده اسلاید — ایجنت‌های هوش مصنوعی برای کنشگران
// کنترل: فلش راست/چپ یا Space، F تمام‌صفحه، Esc فهرست، P حالت مدرس

(function () {
  "use strict";

  var slides = Array.prototype.slice.call(document.querySelectorAll(".slide"));
  var current = 0;
  var presenter = false;
  var notesBox = null;

  if (slides.length === 0) return;

  // شماره اولیه از هش (#3)
  var h = parseInt((location.hash || "").replace("#", ""), 10);
  if (!isNaN(h) && h >= 1 && h <= slides.length) current = h - 1;

  // ناوبری پایین صفحه
  var nav = document.createElement("div");
  nav.className = "nav";
  nav.innerHTML =
    '<button type="button" data-act="next" title="بعدی (فلش چپ)">بعدی ←</button>' +
    '<button type="button" data-act="prev" title="قبلی (فلش راست)">→ قبلی</button>';
  document.body.appendChild(nav);

  var counter = document.createElement("div");
  counter.className = "counter";
  document.body.appendChild(counter);

  function pad(n) { return (n < 10 ? "0" : "") + n; }

  function show(i) {
    current = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach(function (s, idx) {
      s.classList.toggle("active", idx === current);
    });
    counter.textContent = pad(current + 1) + " / " + pad(slides.length);
    document.getElementById("progress").style.width =
      ((current + 1) / slides.length) * 100 + "%";
    location.hash = "#" + (current + 1);
    if (presenter && notesBox) {
      var n = slides[current].getAttribute("data-notes") || "—";
      notesBox.textContent = n;
    }
  }

  // جعبه یادداشت مدرس
  function togglePresenter() {
    presenter = !presenter;
    document.body.classList.toggle("presenter", presenter);
    if (presenter) {
      notesBox = document.createElement("div");
      notesBox.className = "notes";
      notesBox.title = "یادداشت‌های مدرس — با P ببندید";
      document.body.appendChild(notesBox);
    } else if (notesBox) {
      notesBox.remove();
      notesBox = null;
    }
    show(current);
  }

  // نمای فهرست
  function toggleOverview() {
    var any = document.body.classList.toggle("overview");
    if (any) {
      slides.forEach(function (s, idx) {
        s.classList.add("active");
        s.style.display = "block";
        s.style.position = "relative";
        s.style.minHeight = "140px";
        s.style.padding = "1rem 2rem";
        s.style.borderBottom = "1px solid #2a3854";
        s.style.cursor = "pointer";
        s.onclick = function () {
          clearOverview();
          show(idx);
        };
      });
      counter.textContent = "فهرست — برای انتخاب کلیک کنید";
    } else {
      clearOverview();
      show(current);
    }
  }

  function clearOverview() {
    document.body.classList.remove("overview");
    slides.forEach(function (s) {
      s.style.display = "";
      s.style.position = "";
      s.style.minHeight = "";
      s.style.padding = "";
      s.style.borderBottom = "";
      s.style.cursor = "";
      s.onclick = null;
    });
  }

  function next() { show(current + 1); }
  function prev() { show(current - 1); }

  document.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft" || e.key === " " || e.key === "PageDown") {
      e.preventDefault(); next();
    } else if (e.key === "ArrowRight" || e.key === "PageUp") {
      e.preventDefault(); prev();
    } else if (e.key === "ArrowDown") { e.preventDefault(); next(); }
    else if (e.key === "ArrowUp") { e.preventDefault(); prev(); }
    else if (e.key === "Home") { e.preventDefault(); show(0); }
    else if (e.key === "End") { e.preventDefault(); show(slides.length - 1); }
    else if (e.key === "f" || e.key === "F") {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
    } else if (e.key === "p" || e.key === "P") {
      togglePresenter();
    } else if (e.key === "Escape") {
      toggleOverview();
    }
  });

  // کلیک روی دکمه‌های ناوبری
  nav.addEventListener("click", function (e) {
    var act = e.target && e.target.getAttribute("data-act");
    if (act === "next") next();
    if (act === "prev") prev();
  });

  // لمس (اسوایپ) برای تبلت
  var touchX = null;
  document.addEventListener("touchstart", function (e) {
    touchX = e.touches[0].clientX;
  }, { passive: true });
  document.addEventListener("touchend", function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) { dx > 0 ? prev() : next(); }
    touchX = null;
  }, { passive: true });

  window.addEventListener("hashchange", function () {
    var h = parseInt((location.hash || "").replace("#", ""), 10);
    if (!isNaN(h) && h >= 1 && h <= slides.length && h - 1 !== current) show(h - 1);
  });

  show(current);
})();
