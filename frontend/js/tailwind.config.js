tailwind.config = {
  theme: {
    extend: {
      colors: {
        "bg-deep": "#080C14",
        "bg-dark": "#0D1220",
        "bg-card": "#131929",
        "bg-surface": "#1A2236",
        border: "#1E2D45",
        accent: "#A78BFA",
        accent2: "#6366F1",
        warn: "#F59E0B",
        danger: "#EF4444",
        "text-1": "#F0F4FF",
        "text-2": "#8A9BBB",
        "text-3": "#4A5878",
      },
      fontFamily: {
        mono: ["Space Mono", "monospace"],
        sans: ["DM Sans", "sans-serif"],
      },
      boxShadow: {
        card: "0 1px 0 0 rgba(255,255,255,0.03) inset, 0 12px 32px -16px rgba(0,0,0,0.7)",
        "glow-accent": "0 0 0 1px rgba(167,139,250,0.35), 0 14px 40px -18px rgba(167,139,250,0.45)",
        "glow-warn": "0 8px 26px -10px rgba(245,158,11,0.55)",
        "glow-green": "0 0 18px -2px rgba(74,222,128,0.55)",
      },
      backgroundImage: {
        "accent-grad": "linear-gradient(135deg, #A78BFA 0%, #6366F1 100%)",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        "fade-up": "fade-up 0.4s ease both",
      },
    },
  },
};
