/* Runs in <head> before first paint so the saved theme never flashes. */
(function () {
  var root = document.documentElement;
  var theme = "system", motion = "";
  try {
    theme = localStorage.getItem("ab.theme") || "system";
    motion = localStorage.getItem("ab.motion") || "";
  } catch (e) { /* storage unavailable: fall back to system */ }
  if (theme === "system") {
    theme = window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  root.setAttribute("data-theme", theme);
  if (motion === "reduced") root.setAttribute("data-motion", "reduced");
})();
