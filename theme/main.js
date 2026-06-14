window.langCode = document.documentElement.lang || "en";

const SCISITEFORGE_LANGUAGE_STORAGE_KEY = "scisiteforgePreferredLanguage";
const SCISITEFORGE_DEFAULT_LANGUAGE = "en";
const SCISITEFORGE_CURRENT_LANGUAGE = window.langCode || SCISITEFORGE_DEFAULT_LANGUAGE;
const SCISITEFORGE_SUPPORTED_LANGUAGE_PATTERN = /^(en|es|fr|de|pt)$/;
const SCISITEFORGE_BUILTIN_SHELL_I18N = {
  en: {
    language_selector_label: "Language",
    translation_preview_title: "Translation unavailable:",
    translation_preview_body: "this page is not yet available in the selected language.",
    translation_preview_link: "Open translation queue",
    still_viewing_default: "You are viewing the English page.",
  },
  es: {
    language_selector_label: "Idioma",
    translation_preview_title: "Traducción no disponible:",
    translation_preview_body: "esta página aún no está disponible en el idioma seleccionado.",
    translation_preview_link: "Abrir cola de traducción",
    still_viewing_default: "Está viendo la página en inglés.",
  },
  fr: {
    language_selector_label: "Langue",
    translation_preview_title: "Traduction non disponible :",
    translation_preview_body: "cette page n'est pas encore disponible dans la langue sélectionnée.",
    translation_preview_link: "Ouvrir la file de traduction",
    still_viewing_default: "Vous consultez la page anglaise.",
  },
  de: {
    language_selector_label: "Sprache",
    translation_preview_title: "Übersetzung nicht verfügbar:",
    translation_preview_body: "diese Seite ist in der ausgewählten Sprache noch nicht verfügbar.",
    translation_preview_link: "Übersetzungswarteschlange öffnen",
    still_viewing_default: "Sie sehen die englische Seite.",
  },
  pt: {
    language_selector_label: "Idioma",
    translation_preview_title: "Tradução indisponível:",
    translation_preview_body: "esta página ainda não está disponível no idioma selecionado.",
    translation_preview_link: "Abrir fila de tradução",
    still_viewing_default: "Você está vendo a página em inglês.",
  },
};

function loadShellI18n() {
  const node = document.getElementById("scisiteforge-shell-i18n");
  if (!node?.textContent) {
    return {};
  }
  try {
    return JSON.parse(node.textContent);
  } catch (error) {
    return {};
  }
}

const SCISITEFORGE_SHELL_I18N = loadShellI18n();

function shellText(lang, key, fallback = "") {
  const bundle = SCISITEFORGE_SHELL_I18N[lang] || {};
  const builtin = SCISITEFORGE_BUILTIN_SHELL_I18N[lang] || {};
  const english = SCISITEFORGE_SHELL_I18N.en || {};
  const builtinEnglish = SCISITEFORGE_BUILTIN_SHELL_I18N.en || {};
  return bundle[key] || builtin[key] || english[key] || builtinEnglish[key] || fallback || key;
}

function applyShellTranslations(lang) {
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const key = node.getAttribute("data-i18n");
    if (!key) return;
    node.textContent = shellText(lang, key, node.textContent || "");
  });

  document.querySelectorAll("[data-i18n-nav]").forEach((node) => {
    const raw = node.getAttribute("data-i18n-nav");
    if (!raw) return;
    try {
      const payload = JSON.parse(raw);
      node.textContent = payload[lang] || payload.en || node.textContent || "";
    } catch (error) {
      // Ignore malformed navigation translation payloads.
    }
  });

  const select = document.getElementById("lang-switch");
  if (select) {
    select.setAttribute("aria-label", shellText(lang, "language_selector_label", select.getAttribute("aria-label") || "Language"));
  }
}

const yearNode = document.getElementById("year");
if (yearNode) {
  yearNode.textContent = new Date().getFullYear();
}

function pathLanguage() {
  const first = (window.location.pathname || "/").split("/").filter(Boolean)[0] || "";
  return SCISITEFORGE_SUPPORTED_LANGUAGE_PATTERN.test(first) ? first : "";
}

function fallbackLanguage() {
  const params = new URLSearchParams(window.location.search || "");
  const lang = params.get("lang") || "";
  if (params.get("translation_fallback") === "1" && SCISITEFORGE_SUPPORTED_LANGUAGE_PATTERN.test(lang)) {
    return lang;
  }
  return "";
}

function localizedPathFor(lang) {
  const currentPath = window.location.pathname || "/";
  const parts = currentPath.split("/").filter(Boolean);
  if (parts.length > 0 && SCISITEFORGE_SUPPORTED_LANGUAGE_PATTERN.test(parts[0])) {
    if (lang === SCISITEFORGE_DEFAULT_LANGUAGE) {
      parts.shift();
    } else {
      parts[0] = lang;
    }
  } else if (lang !== SCISITEFORGE_DEFAULT_LANGUAGE) {
    parts.unshift(lang);
  }
  const nextPath = "/" + parts.join("/");
  return nextPath.endsWith("/") ? nextPath : nextPath + (currentPath.endsWith("/") ? "/" : "");
}

function setPreferredLanguage(lang) {
  try {
    window.localStorage.setItem(SCISITEFORGE_LANGUAGE_STORAGE_KEY, lang);
  } catch (error) {
    // Ignore storage failures.
  }
}

function getPreferredLanguage() {
  try {
    return window.localStorage.getItem(SCISITEFORGE_LANGUAGE_STORAGE_KEY) || SCISITEFORGE_DEFAULT_LANGUAGE;
  } catch (error) {
    return SCISITEFORGE_DEFAULT_LANGUAGE;
  }
}

function ensureTranslationBanner() {
  let banner = document.querySelector(".translation-fallback-banner");
  if (banner) {
    return banner;
  }
  const shell = document.querySelector(".site-shell");
  const anchor = shell?.querySelector(".site-topbar, .site-header");
  if (!shell || !anchor) {
    return null;
  }
  banner = document.createElement("div");
  banner.className = "translation-fallback-banner";
  banner.hidden = true;
  anchor.insertAdjacentElement("afterend", banner);
  return banner;
}

function updateTranslationBanner(lang, covered) {
  const banner = ensureTranslationBanner();
  if (!banner) {
    return;
  }
  if (!lang || lang === SCISITEFORGE_DEFAULT_LANGUAGE || covered) {
    banner.hidden = true;
    banner.textContent = "";
    return;
  }
  banner.hidden = false;
  banner.innerHTML =
    `<strong>${shellText(lang, "translation_preview_title", "Translation preview:")}</strong> ` +
    `${shellText(lang, "translation_preview_body", "this language is in the translation queue for the current page set.")} ` +
    `${shellText(lang, "still_viewing_default", "You are still viewing the default language.")} ` +
    `<a href="/translation-status/">${shellText(lang, "translation_preview_link", "Open translation queue")}</a>.`;
}

function switchLanguage(lang) {
  if (!lang) return;
  setPreferredLanguage(lang);
  window.location.href = localizedPathFor(lang);
}

document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("lang-switch");
  if (select) {
    const fallback = fallbackLanguage();
    const requested = fallback || pathLanguage();
    const preferred = requested || getPreferredLanguage() || SCISITEFORGE_CURRENT_LANGUAGE;
    if ([...select.options].some((option) => option.value === preferred)) {
      select.value = preferred;
    }
    if (requested || preferred !== SCISITEFORGE_DEFAULT_LANGUAGE) {
      setPreferredLanguage(select.value);
    }
    if (!fallback && !pathLanguage() && select.value !== SCISITEFORGE_DEFAULT_LANGUAGE) {
      window.location.replace(localizedPathFor(select.value));
      return;
    }
    const option = select.selectedOptions?.[0];
    applyShellTranslations(select.value);
    updateTranslationBanner(select.value, !fallback && option?.getAttribute("data-coverage") === "true");
    select.addEventListener("change", (event) => {
      switchLanguage(event.target.value);
    });
  } else {
    applyShellTranslations(getPreferredLanguage());
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
});
