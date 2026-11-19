/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        workstation: {
          950: "#080b0f",
          900: "#0d1117",
          850: "#131821",
          800: "#18202c",
          700: "#222d3d",
          600: "#2d3a4d",
          border: "#253041",
          accent: "#00d2ff",
          green: "#00ff88",
          orange: "#ff9900",
          red: "#ff3366",
        },
      },
      fontFamily: {
        mono: ["JetBrains Mono", "Menlo", "Monaco", "Consolas", "Courier New", "monospace"],
      },
    },
  },
  plugins: [],
};
