/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      spacing: {
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh",
      },
      minHeight: {
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh",
      },
    },
  },
  plugins: [],
};
