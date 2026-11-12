/* "Fish or not a fish?" quiz. Questions come from window.AB_QUIZ. */
(function () {
  "use strict";
  var root = document.getElementById("fish-quiz");
  var questions = window.AB_QUIZ;
  if (!root || !questions || !questions.length) return;

  var stage = root.querySelector("#quiz-stage");
  var bar = root.querySelector(".quiz__bar");
  var progress = root.querySelector(".quiz__progress");
  var counter = root.querySelector("#quiz-count");
  var feedback = root.querySelector("#quiz-feedback");
  var nextBtn = root.querySelector("#quiz-next");
  var index = 0, score = 0, answered = false;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  function setProgress(done) {
    var pct = Math.round((done / questions.length) * 100);
    bar.style.width = pct + "%";
    progress.setAttribute("aria-valuenow", String(done));
  }

  function showQuestion() {
    var q = questions[index];
    answered = false;
    stage.textContent = "";
    feedback.textContent = "";
    nextBtn.hidden = true;
    counter.textContent = "Question " + (index + 1) + " of " + questions.length;
    setProgress(index);

    var emoji = el("div", "quiz__emoji", q.emoji);
    emoji.setAttribute("aria-hidden", "true");
    stage.appendChild(emoji);
    stage.appendChild(el("h3", "quiz__q", "Is the " + q.name + " a fish?"));

    var opts = el("div", "quiz__options");
    opts.setAttribute("role", "group");
    opts.setAttribute("aria-label", "Answer");
    [["Yes, it's a fish", true], ["No, it isn't", false]].forEach(function (o) {
      var b = el("button", "btn btn--ghost", o[0]);
      b.type = "button";
      b.addEventListener("click", function () { answer(o[1], b, opts); });
      opts.appendChild(b);
    });
    stage.appendChild(opts);
    opts.firstChild.focus({ preventScroll: true });
  }

  function answer(choice, button, group) {
    if (answered) return;
    answered = true;
    var q = questions[index];
    var right = choice === q.fish;
    if (right) score++;
    button.setAttribute("data-state", right ? "correct" : "wrong");
    Array.prototype.forEach.call(group.children, function (b) { b.disabled = true; });
    feedback.textContent = "";
    feedback.appendChild(el("strong", "", right ? "Correct!" : "Not quite."));
    feedback.appendChild(document.createTextNode(q.why));
    nextBtn.textContent = index === questions.length - 1 ? "See my score" : "Next question";
    nextBtn.hidden = false;
    setProgress(index + 1);
    nextBtn.focus();
  }

  function showResult() {
    stage.textContent = "";
    feedback.textContent = "";
    nextBtn.hidden = true;
    counter.textContent = "Quiz complete";
    var box = el("div", "quiz__result");
    box.appendChild(el("div", "quiz__score", score + " / " + questions.length));
    var msg = score === questions.length ? "Perfect score. You really know your sea life!"
      : score >= questions.length * 0.6 ? "Great job. A few sea animals are trickier than they look."
      : "Good try. Many sea animals are not fish, so read the fish page and play again.";
    box.appendChild(el("p", "", msg));
    var again = el("button", "btn", "Play again");
    again.type = "button";
    again.addEventListener("click", function () { index = 0; score = 0; showQuestion(); });
    box.appendChild(again);
    stage.appendChild(box);
    again.focus();
  }

  nextBtn.addEventListener("click", function () {
    index++;
    if (index >= questions.length) showResult(); else showQuestion();
  });

  progress.setAttribute("aria-valuemax", String(questions.length));
  showQuestion();
})();
