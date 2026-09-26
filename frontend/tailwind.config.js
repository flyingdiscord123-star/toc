/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#17252a",
        paper: "#f5f7f4",
        teal: "#087f8c",
        coral: "#e9795f",
        fog: "#e4ebe7"
      },
      fontFamily: {
        display: ["DM Sans", "sans-serif"],
        body: ["Source Sans 3", "sans-serif"]
      }
    }
  },
  plugins: []
};
