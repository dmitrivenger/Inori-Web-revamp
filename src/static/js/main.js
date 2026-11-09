/* INORI — site behaviour (no dependencies) */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var SUPPORTED = ["he", "en", "ru"];
  var KEY = "inori-lang";
  var pageLang = doc.getAttribute("lang");

  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function read(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }

  /* Detect the visitor's language from the browser / OS settings */
  function detectLang() {
    var list = (navigator.languages && navigator.languages.length) ? navigator.languages : [navigator.language || ""];
    for (var i = 0; i < list.length; i++) {
      var code = String(list[i]).toLowerCase().split("-")[0];
      if (code === "iw") code = "he";
      if (SUPPORTED.indexOf(code) !== -1) return code;
    }
    return null;
  }

  /* Remember an explicit choice made in the language switcher */
  document.querySelectorAll("[data-set-lang]").forEach(function (a) {
    a.addEventListener("click", function () { store(KEY, a.getAttribute("data-set-lang")); });
  });

  /* Suggest the visitor's own language when they land on another one (no forced redirect) */
  var bar = document.querySelector(".langbar");
  if (bar && !read(KEY) && !sessionStorage.getItem("inori-langbar-closed")) {
    var want = detectLang();
    if (want && want !== pageLang) {
      var target = bar.querySelector('[data-langbar="' + want + '"]');
      if (target) {
        target.hidden = false;
        bar.classList.add("is-visible");
      }
    }
    bar.querySelectorAll(".langbar__x").forEach(function (x) {
      x.addEventListener("click", function () {
        bar.classList.remove("is-visible");
        try { sessionStorage.setItem("inori-langbar-closed", "1"); } catch (e) {}
      });
    });
  }

  /* Header: solid background after scrolling */
  var header = document.querySelector(".header");
  if (header && !header.classList.contains("header--solid")) {
    var onScroll = function () { header.classList.toggle("is-solid", window.scrollY > 30); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Mobile menu */
  var burger = document.querySelector(".burger");
  var nav = document.getElementById("nav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.style.overflow = open ? "hidden" : "";
      header.classList.add("is-solid");
    });
  }

  /* Dropdowns (click/keyboard support; hover handled in CSS) */
  document.querySelectorAll(".nav__drop").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.parentElement;
      var open = item.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  /* Language menu */
  var lang = document.querySelector(".lang");
  if (lang) {
    var lbtn = lang.querySelector(".lang__btn");
    lbtn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = lang.classList.toggle("is-open");
      lbtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("click", function () {
      lang.classList.remove("is-open");
      lbtn.setAttribute("aria-expanded", "false");
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (lang) lang.classList.remove("is-open");
    document.querySelectorAll(".nav__item.is-open").forEach(function (i) { i.classList.remove("is-open"); });
    closeModal();
  });

  /* Reveal on scroll */
  var els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* Video modal */
  var modal = document.querySelector(".modal");
  var lastFocus = null;
  function closeModal() {
    if (!modal || !modal.classList.contains("is-open")) return;
    var v = modal.querySelector("video");
    v.pause(); v.removeAttribute("src"); v.load();
    modal.classList.remove("is-open");
    if (lastFocus) lastFocus.focus();
  }
  document.querySelectorAll("[data-video]").forEach(function (b) {
    b.addEventListener("click", function () {
      if (!modal) return;
      lastFocus = b;
      var v = modal.querySelector("video");
      v.src = b.getAttribute("data-video");
      modal.classList.add("is-open");
      modal.querySelector(".modal__close").focus();
      v.play().catch(function () {});
    });
  });
  if (modal) {
    modal.querySelector(".modal__close").addEventListener("click", closeModal);
    modal.addEventListener("click", function (e) { if (e.target === modal) closeModal(); });
  }

  /* Contact form: opens the visitor's e-mail app with the message pre-filled */
  var form = document.querySelector("form[data-contact]");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector(".hp input").value) return; // bot
      if (!form.reportValidity()) return;
      var get = function (n) { var el = form.elements[n]; return el ? el.value.trim() : ""; };
      var roleSel = form.querySelector("select[name=role]");
      var role = roleSel.selectedIndex > 0 ? roleSel.options[roleSel.selectedIndex].text : "";
      var rows = [
        [form.querySelector("label[for=f-name]"), get("name")],
        [form.querySelector("label[for=f-company]"), get("company")],
        [form.querySelector("label[for=f-email]"), get("email")],
        [form.querySelector("label[for=f-phone]"), get("phone")],
        [form.querySelector("label[for=f-role]"), role]
      ].filter(function (r) { return r[1]; }).map(function (r) {
        return r[0].firstChild.textContent.trim() + ": " + r[1];
      });
      var body = rows.join("\n") + (get("message") ? "\n\n" + get("message") : "");
      window.location.href = "mailto:" + form.getAttribute("data-mail") +
        "?subject=" + encodeURIComponent("INORI website: " + get("name")) +
        "&body=" + encodeURIComponent(body);
    });
  }
})();
