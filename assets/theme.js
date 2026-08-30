// Two-state toggle: an explicit choice is stored and wins over the OS
// setting; with nothing stored we follow prefers-color-scheme (and live
// OS changes, which pure CSS handles).
(() => {
  'use strict';
  const KEY = 'infocompendium-theme';
  const darkQuery = window.matchMedia('(prefers-color-scheme: dark)');

  function effectiveTheme() {
    const attr = document.documentElement.getAttribute('data-theme');
    if (attr === 'light' || attr === 'dark') return attr;
    return darkQuery.matches ? 'dark' : 'light';
  }

  function applyTheme(mode) {
    document.documentElement.setAttribute('data-theme', mode);
    try {
      localStorage.setItem(KEY, mode);
    } catch {
      /* private mode, etc. */
    }
  }

  document.getElementById('theme-toggle')?.addEventListener('click', () => {
    applyTheme(effectiveTheme() === 'dark' ? 'light' : 'dark');
  });
})();
