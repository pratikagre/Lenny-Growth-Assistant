/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        lenny: {
          50: '#fbf7f0',
          100: '#f5ecdc',
          200: '#edd8b8',
          300: '#e3be8e',
          400: '#d7a163',
          500: '#cb8643',
          600: '#bc6f37',
          700: '#9c552f',
          800: '#7e462c',
          900: '#673a27',
          950: '#381c13',
        }
      }
    },
  },
  plugins: [],
}
