/* Shared behaviour: mobile menu, Animals menu, quick theme toggle. */
(function () {
  "use strict";
  var KEY = "ab.theme";

  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  // Mobile navigation
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  function setNav(open) {
    if (!toggle || !nav) return;
    nav.setAttribute("data-open", String(open));
    toggle.setAttribute("aria-expanded", String(open));
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNav(nav.getAttribute("data-open") !== "true");
    });
  }

  // "Animals" menu
  var menuBtn = document.querySelector("[data-menu-button]");
  var menu = document.getElementById("animals-menu");
  function setMenu(open, returnFocus) {
    if (!menuBtn || !menu) return;
    menu.hidden = !open;
    menuBtn.setAttribute("aria-expanded", String(open));
    if (!open && returnFocus) menuBtn.focus();
  }
  if (menuBtn && menu) {
    menuBtn.addEventListener("click", function () { setMenu(menu.hidden, false); });
    document.addEventListener("click", function (e) {
      if (!menu.hidden && !menu.contains(e.target) && !menuBtn.contains(e.target)) setMenu(false);
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (menu && !menu.hidden) setMenu(false, true);
    else if (nav && nav.getAttribute("data-open") === "true") { setNav(false); toggle.focus(); }
  });

  // Quick light/dark toggle (Settings has all three themes)
  var themeBtn = document.querySelector(".theme-toggle");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var root = document.documentElement;
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      store(KEY, next);
    });
  }

  // Greeting for a name saved on the Login or Settings page
  var greet = document.querySelector("[data-greeting]");
  if (greet) {
    var saved = "";
    try { saved = localStorage.getItem("ab.name") || ""; } catch (e) {}
    if (saved) greet.textContent = "Welcome back, " + saved + ".";
  }
})();
