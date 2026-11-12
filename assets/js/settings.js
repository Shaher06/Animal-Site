/* Settings page: theme, reduced motion, display name, personal animal list.
   Everything is stored in this browser (localStorage) and nowhere else. */
(function () {
  "use strict";
  var root = document.documentElement;
  var form = document.getElementById("settings");
  if (!form) return;

  function get(k, fallback) { try { var v = localStorage.getItem(k); return v === null ? fallback : v; } catch (e) { return fallback; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function del(k) { try { localStorage.removeItem(k); } catch (e) {} }

  /* Theme */
  function applyTheme(value) {
    var resolved = value;
    if (value === "system") {
      resolved = matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }
    root.setAttribute("data-theme", resolved);
  }
  var themeRadios = form.querySelectorAll("input[name=theme]");
  var savedTheme = get("ab.theme", "system");
  Array.prototype.forEach.call(themeRadios, function (r) {
    r.checked = r.value === savedTheme;
    r.addEventListener("change", function () { set("ab.theme", r.value); applyTheme(r.value); });
  });

  /* Reduced motion */
  var motion = document.getElementById("reduce-motion");
  motion.checked = get("ab.motion", "") === "reduced";
  motion.addEventListener("change", function () {
    if (motion.checked) { set("ab.motion", "reduced"); root.setAttribute("data-motion", "reduced"); }
    else { del("ab.motion"); root.removeAttribute("data-motion"); }
  });

  /* Display name */
  var nameInput = document.getElementById("display-name");
  var nameStatus = document.getElementById("name-status");
  nameInput.value = get("ab.name", "");
  document.getElementById("name-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var v = nameInput.value.trim();
    if (v.length > 30) { nameStatus.textContent = "Use 30 characters or fewer."; return; }
    if (v) { set("ab.name", v); nameStatus.textContent = "Saved in this browser: " + v + "."; }
    else { del("ab.name"); nameStatus.textContent = "Name cleared."; }
  });

  /* My animal list */
  var list = document.getElementById("my-list");
  var listForm = document.getElementById("list-form");
  var listInput = document.getElementById("list-input");
  var listError = document.getElementById("list-input-error");
  var listEmpty = document.getElementById("list-empty");
  var clearBtn = document.getElementById("list-clear");
  var animals = [];
  try { animals = JSON.parse(get("ab.list", "[]")); if (!Array.isArray(animals)) animals = []; } catch (e) { animals = []; }

  function save() { set("ab.list", JSON.stringify(animals)); }
  function render() {
    list.textContent = "";
    animals.forEach(function (name, i) {
      var li = document.createElement("li");
      var span = document.createElement("span");
      span.textContent = name;
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "btn btn--ghost btn--small";
      btn.textContent = "Remove";
      btn.setAttribute("aria-label", "Remove " + name + " from my list");
      btn.addEventListener("click", function () {
        animals.splice(i, 1); save(); render();
        listInput.focus();
      });
      li.appendChild(span); li.appendChild(btn);
      list.appendChild(li);
    });
    listEmpty.hidden = animals.length > 0;
    clearBtn.hidden = animals.length === 0;
  }
  listForm.addEventListener("submit", function (e) {
    e.preventDefault();
    var v = listInput.value.trim();
    var msg = "";
    if (!v) msg = "Type an animal name first.";
    else if (v.length > 40) msg = "Use 40 characters or fewer.";
    else if (animals.some(function (a) { return a.toLowerCase() === v.toLowerCase(); })) msg = v + " is already on your list.";
    else if (animals.length >= 30) msg = "Your list is full (30 animals). Remove one to add another.";
    listError.textContent = msg;
    if (msg) { listInput.setAttribute("aria-invalid", "true"); listInput.focus(); return; }
    listInput.removeAttribute("aria-invalid");
    animals.push(v); save(); render();
    listInput.value = ""; listInput.focus();
  });
  clearBtn.addEventListener("click", function () { animals = []; save(); render(); listInput.focus(); });
  render();

  /* Reset everything */
  document.getElementById("reset-all").addEventListener("click", function () {
    ["ab.theme", "ab.motion", "ab.name", "ab.list"].forEach(del);
    root.removeAttribute("data-motion");
    applyTheme("system");
    Array.prototype.forEach.call(themeRadios, function (r) { r.checked = r.value === "system"; });
    motion.checked = false; nameInput.value = ""; nameStatus.textContent = "";
    animals = []; render();
    document.getElementById("reset-status").textContent = "All settings were reset.";
  });
})();
