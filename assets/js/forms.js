/* Front-end validation for the login, register and contact forms.
   Nothing is sent to a server: login/register are demos, and the contact
   form opens the visitor's own email app (mailto:). */
(function () {
  "use strict";
  var CONTACT_EMAIL = "animalbase111@gmail.com";
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function field(form, name) { return form.elements[name]; }

  function setError(input, message) {
    var err = document.getElementById(input.id + "-error");
    if (err) err.textContent = message || "";
    if (message) input.setAttribute("aria-invalid", "true");
    else input.removeAttribute("aria-invalid");
    return !message;
  }

  function validate(form, rules) {
    var firstBad = null;
    Object.keys(rules).forEach(function (name) {
      var input = field(form, name);
      var msg = rules[name](input.value.trim());
      setError(input, msg);
      if (msg && !firstBad) firstBad = input;
    });
    if (firstBad) firstBad.focus();
    return !firstBad;
  }

  var rules = {
    username: function (v) {
      if (!v) return "Enter a username.";
      if (v.length < 3 || v.length > 30) return "Use 3 to 30 characters.";
      if (!/^[A-Za-z0-9_.-]+$/.test(v)) return "Use letters, numbers, dots, dashes or underscores only.";
      return "";
    },
    loginPassword: function (v) { return v ? "" : "Enter your password."; },
    email: function (v) {
      if (!v) return "Enter your email address.";
      return EMAIL_RE.test(v) ? "" : "Enter a valid email, like name@example.com.";
    },
    newPassword: function (v) {
      if (v.length < 8) return "Use at least 8 characters.";
      if (!/[A-Za-z]/.test(v) || !/[0-9]/.test(v)) return "Include at least one letter and one number.";
      return "";
    },
    age: function (v) {
      var n = Number(v);
      if (!v) return "Enter your age.";
      if (!Number.isInteger(n) || n < 7 || n > 120) return "Enter an age from 7 to 120.";
      return "";
    },
    name: function (v) { return v.length >= 2 ? "" : "Enter your name (at least 2 characters)."; },
    message: function (v) {
      if (v.length < 10) return "Write at least 10 characters.";
      if (v.length > 1000) return "Keep your message under 1000 characters.";
      return "";
    }
  };

  function status(node, state, text) {
    node.hidden = false;
    node.setAttribute("data-state", state);
    node.textContent = text;
  }

  function remember(name) { try { localStorage.setItem("ab.name", name); } catch (e) {} }

  /* ----- Login / register page ----- */
  var tabs = document.querySelectorAll("[role=tab]");
  if (tabs.length) {
    var tabList = Array.prototype.slice.call(tabs);
    var select = function (tab, focus) {
      tabList.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
      if (focus) tab.focus();
    };
    tabList.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        var next = e.key === "ArrowRight" ? (i + 1) % tabList.length
          : e.key === "ArrowLeft" ? (i - 1 + tabList.length) % tabList.length : -1;
        if (next > -1) { e.preventDefault(); select(tabList[next], true); }
      });
    });
    if (location.hash === "#register") select(tabList[1]);

    document.querySelectorAll("[data-switch]").forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        select(tabList[a.getAttribute("data-switch") === "register" ? 1 : 0], true);
      });
    });

    document.querySelectorAll(".password-wrap button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var input = document.getElementById(btn.getAttribute("aria-controls"));
        var show = input.type === "password";
        input.type = show ? "text" : "password";
        btn.textContent = show ? "Hide" : "Show";
        btn.setAttribute("aria-pressed", String(show));
      });
    });
  }

  var login = document.getElementById("login-form");
  if (login) {
    login.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = validate(login, { username: rules.username, loginPassword: rules.loginPassword });
      var out = document.getElementById("login-status");
      if (!ok) { out.hidden = true; return; }
      var name = field(login, "username").value.trim();
      remember(name);
      status(out, "success", "Demo mode: there are no real accounts here, so nothing was checked or sent. We saved the name “" + name + "” in this browser only. You can head to the home page now.");
      document.getElementById("login-continue").hidden = false;
      login.reset();
    });
  }

  var register = document.getElementById("register-form");
  if (register) {
    register.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = validate(register, { username: rules.username, email: rules.email, newPassword: rules.newPassword, age: rules.age });
      var out = document.getElementById("register-status");
      if (!ok) { out.hidden = true; return; }
      var name = field(register, "username").value.trim();
      remember(name);
      status(out, "success", "Demo mode: no account was created and nothing was sent anywhere. We saved the name “" + name + "” in this browser only.");
      document.getElementById("register-continue").hidden = false;
      register.reset();
    });
  }

  /* ----- Contact page ----- */
  var contact = document.getElementById("contact-form");
  if (contact) {
    contact.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = validate(contact, { name: rules.name, email: rules.email, message: rules.message });
      var out = document.getElementById("contact-status");
      if (!ok) { out.hidden = true; return; }
      var body = "From: " + field(contact, "name").value.trim() + " <" + field(contact, "email").value.trim() + ">\n\n" + field(contact, "message").value.trim();
      var url = "mailto:" + CONTACT_EMAIL + "?subject=" + encodeURIComponent("Animal Base contact message") + "&body=" + encodeURIComponent(body);
      status(out, "success", "Your email app should open with the message ready to send. Nothing is sent from this page. If nothing opens, write to " + CONTACT_EMAIL + " directly.");
      window.location.href = url;
    });
    var msg = field(contact, "message");
    var counter = document.getElementById("message-count");
    msg.addEventListener("input", function () { counter.textContent = msg.value.length + " / 1000"; });
  }
})();
