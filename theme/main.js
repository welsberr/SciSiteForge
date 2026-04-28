window.langCode = document.documentElement.lang || "en";

document.getElementById("year")?.textContent = new Date().getFullYear();

function switchLanguage(lang) {
  if (!lang) return;
  const currentPath = window.location.pathname || "/";
  const parts = currentPath.split("/").filter(Boolean);
  if (parts.length > 0 && parts[0].length === 2) {
    parts[0] = lang;
  } else {
    parts.unshift(lang);
  }
  const nextPath = "/" + parts.join("/");
  window.location.href = nextPath.endsWith("/") ? nextPath : nextPath + (currentPath.endsWith("/") ? "/" : "");
}

document.querySelectorAll("[data-src]").forEach((button) => {
  button.addEventListener("click", () => {
    const target = button.getAttribute("data-src");
    if (!target) return;
    const content = button.parentElement?.querySelector(".content");
    if (!content) return;
    fetch(target)
      .then((resp) => resp.text())
      .then((html) => {
        content.innerHTML = html;
      });
  });
});
