/* Home page extras: animal of the day and rotating fact. */
(function () {
  "use strict";
  var data = window.AB_DATA;
  if (!data) return;

  // Animal of the day: same animal all day, changes at midnight (local time)
  var slot = document.getElementById("featured-animal");
  if (slot) {
    var d = new Date();
    var dayNumber = Math.floor(new Date(d.getFullYear(), d.getMonth(), d.getDate()) / 86400000);
    var withPhoto = data.animals.filter(function (a) { return a.img; });
    var a = withPhoto[dayNumber % withPhoto.length];
    var cat = data.categories.filter(function (c) { return c.id === a.cat; })[0];
    slot.style.setProperty("--c", cat.color);
    slot.style.setProperty("--c-ink", cat.ink);
    slot.style.setProperty("--c-tint", cat.tint);
    slot.style.setProperty("--focus", a.focus || "50% 50%");
    var img = slot.querySelector("img");
    img.src = "assets/img/animals/" + a.img + ".webp";
    img.alt = a.alt;
    slot.querySelector("[data-f-cat]").textContent = cat.name;
    slot.querySelector("[data-f-name]").textContent = a.name;
    slot.querySelector("[data-f-sci]").textContent = a.sci;
    slot.querySelector("[data-f-summary]").textContent = a.summary;
    slot.querySelector("[data-animal]").setAttribute("data-animal", a.id);
    slot.hidden = false;
  }

  // Rotating "did you know" facts: every animal's fun fact plus each category's
  var factText = document.getElementById("fact-text");
  var factSource = document.getElementById("fact-source");
  var factBtn = document.getElementById("fact-next");
  if (factText && factBtn) {
    var facts = data.animals.map(function (a) { return { t: a.fun, s: a.name }; })
      .concat(data.categories.map(function (c) { return { t: c.didyouknow, s: c.name }; }));
    var index = Math.floor(Math.random() * facts.length);
    var show = function () {
      factText.textContent = facts[index].t;
      factSource.textContent = facts[index].s;
    };
    factBtn.addEventListener("click", function () {
      index = (index + 1) % facts.length;
      show();
    });
    show();
  }
})();
