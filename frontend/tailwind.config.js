/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,ts,js}"],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          "Plus Jakarta Sans",
          "Noto Sans SC",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "sans-serif",
        ],
      },
      colors: {
        brand: {
          50: "#F5F3FF",
          100: "#EDE9FE",
          200: "#DDD6FE",
          300: "#C4B5FD",
          400: "#A78BFA",
          500: "#8B5CF6",
          600: "#7C3AED",
          700: "#6D28D9",
          800: "#5B21B6",
          900: "#4C1D95",
        },
        accent: {
          DEFAULT: "#EC4899",
        },
        cta: {
          DEFAULT: "#F97316",
          dark: "#EA580C",
        },
      },
      boxShadow: {
        card: "0 4px 24px -12px rgba(15,23,42,0.10)",
        cardHover: "0 16px 48px -16px rgba(124,58,237,0.28)",
        cta: "0 10px 36px -10px rgba(249,115,22,0.55)",
      },
      backgroundImage: {
        "brand-gradient": "linear-gradient(135deg, #7C3AED 0%, #EC4899 100%)",
        "cta-gradient": "linear-gradient(135deg, #FB923C 0%, #F97316 60%, #DB2777 100%)",
      },
      keyframes: {
        glow: {
          "0%, 100%": { opacity: "0.7" },
          "50%": { opacity: "1" },
        },
        floaty: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-6px)" },
        },
      },
      animation: {
        glow: "glow 6s ease-in-out infinite",
        floaty: "floaty 8s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
