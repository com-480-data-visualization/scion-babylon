function css(name) {
  return "rgb(" + getComputedStyle(document.documentElement).getPropertyValue(name) + ")";
}

// copied colors from chart.js to fit congo theme
window.congoColors = {
  primary300: css("--color-primary-300"),
  primary400: css("--color-primary-400"),
  primary500: css("--color-primary-500"),
  primary200: css("--color-primary-200"),
  neutral100: css("--color-neutral-100"),
  neutral700: css("--color-neutral-700"),
};
