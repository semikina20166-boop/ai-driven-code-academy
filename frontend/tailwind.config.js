/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        academy: {
          bg: "#080c14",
          panel: "#121826",
          border: "#1f293d",
          accent: "#8b5cf6", // premium purple
          accentGold: "#fbbf24", // premium gold
          success: "#10b981", // emerald
          warn: "#f59e0b",
          muted: "#64748b",
        },
      },
      fontFamily: {
        sans: ["Outfit", "Segoe UI", "system-ui", "sans-serif"],
        mono: ["Consolas", "Monaco", "monospace"],
      },
    },
  },
  plugins: [],
};
