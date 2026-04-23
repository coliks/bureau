/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./website/templates/**/*html",
    "./website/static/javascript/**/*.js"
  ],
  theme: {
    extend: {
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif'],
        'manrope': ['Manrope', 'sans-serif'],
        'montserrat': ['Montserrat', 'sans-serif']
      }
    },
  },
  plugins: [],
}

