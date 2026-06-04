/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "../src/templates/**/*.html",
      "../src/static/assets/public/js/*.js",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#00095C',
      },
      backgroundImage: {
        'gradient-blue-gray': 'linear-gradient(to right, #4A90E2, #E2E8F0)',
      },
    },
  },
  plugins: [],
};


