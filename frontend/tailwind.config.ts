import type { Config } from "tailwindcss";
export default {
  darkMode: "class",
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0a0a0f",
        panel: "#0f1117",
        border: "#1f2230",
        accent: "#7c5cff",
        accent2: "#22d3ee",
        good: "#22c55e",
        warn: "#f59e0b",
        bad: "#ef4444",
      },
      fontFamily: { sans: ["Inter","ui-sans-serif","system-ui"] },
      backgroundImage: {
        "grad-hero": "radial-gradient(80% 60% at 50% 0%, rgba(124,92,255,.35), transparent 60%)",
      },
    },
  },
  plugins: [],
} satisfies Config;
