// Auto-update year
document.getElementById('year')?.textContent = new Date().getFullYear();

// Language switcher
function switchLanguage(lang) {
  const currentPath = window.location.pathname;
  let newPath = currentPath.replace(new RegExp(`^/${window.langCode}/|^/`), `/${lang}/`);
  if (!currentPath.startsWith(`/${lang}/`)) {
    newPath = `/${lang}${currentPath}`;
  }
  window.location.href = newPath;
}

// Optional: expose langCode for JS logic
window.langCode = document.documentElement.lang || 'en';
