/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: "#0B2A5B",
          light: "#123B7A",
          dark: "#081D40",
        },
        brand: {
          red: "#E2231A",
          redDark: "#B81B14",
        },
        surface: {
          DEFAULT: "#F4F5F7",
          card: "#FFFFFF",
          border: "#D5D9E0",
        },
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "sans-serif",
        ],
      },
      boxShadow: {
        card: "0 1px 3px rgba(11, 42, 91, 0.08), 0 1px 2px rgba(11, 42, 91, 0.06)",
        panel: "0 4px 16px rgba(11, 42, 91, 0.10)",
      },
      borderRadius: {
        xl2: "0.875rem",
      },
    },
  },
  plugins: [],
};
