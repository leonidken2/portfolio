(function () {
  "use strict";

  // Hero bars grow once, when they come into view
  var roas = document.querySelector(".roas");
  if (roas) {
    var reveal = function () { roas.classList.add("is-in"); };
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) { reveal(); io.disconnect(); } });
      }, { threshold: 0.35 });
      io.observe(roas);
    } else { reveal(); }
  }

  // Channel filter: scopes KPI strip and highlights matching panels
  document.querySelectorAll(".seg").forEach(function (seg) {
    var dash = seg.closest(".dash");
    seg.addEventListener("click", function (ev) {
      var btn = ev.target.closest("button[data-view]");
      if (!btn) return;
      var view = btn.getAttribute("data-view");
      dash.setAttribute("data-view", view);
      seg.querySelectorAll("button").forEach(function (b) {
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      dash.querySelectorAll(".kpis[data-view]").forEach(function (k) {
        k.hidden = k.getAttribute("data-view") !== view;
      });
      dash.querySelectorAll(".panel[data-ch]").forEach(function (p) {
        var chs = p.getAttribute("data-ch").split(" ");
        p.classList.toggle("is-match", chs.indexOf(view) !== -1);
      });
    });
  });

  // Table view toggle (every dashboard has a table twin)
  document.querySelectorAll(".tbl-toggle").forEach(function (btn) {
    var target = document.getElementById(btn.getAttribute("aria-controls"));
    var label = btn.querySelector("span");
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", open ? "false" : "true");
      target.hidden = open;
      label.textContent = btn.getAttribute(open ? "data-show" : "data-hide");
    });
  });

  // Tooltip for chart marks: value first, label second
  var tip = document.createElement("div");
  tip.className = "tip";
  tip.setAttribute("role", "status");
  var tipVal = document.createElement("b");
  var tipLab = document.createElement("span");
  tip.appendChild(tipVal);
  tip.appendChild(tipLab);
  document.body.appendChild(tip);

  function place(x, y) {
    var w = tip.offsetWidth, h = tip.offsetHeight;
    var left = Math.min(window.innerWidth - w - 8, Math.max(8, x + 14));
    var top = y - h - 12;
    if (top < 8) top = y + 18;
    tip.style.left = left + "px";
    tip.style.top = top + "px";
  }
  function show(el) {
    tipVal.textContent = el.getAttribute("data-tip") || "";
    tipLab.textContent = el.getAttribute("data-tip-label") || "";
    tip.classList.add("on");
  }
  function hide() { tip.classList.remove("on"); }

  document.querySelectorAll("[data-tip]").forEach(function (el) {
    el.addEventListener("pointerenter", function (e) { show(el); place(e.clientX, e.clientY); });
    el.addEventListener("pointermove", function (e) { place(e.clientX, e.clientY); });
    el.addEventListener("pointerleave", hide);
    el.addEventListener("focus", function () {
      show(el);
      var r = el.getBoundingClientRect();
      place(r.left + r.width / 2, r.top);
    });
    el.addEventListener("blur", hide);
  });
  window.addEventListener("scroll", hide, { passive: true });
})();
