import tailwindcss from "@tailwindcss/vite";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
//   modules: ['@nuxtjs/tailwindcss'],
  vite: {
    plugins: [tailwindcss()],
    server: {
        allowedHosts: ["being-inside.duckdns.org"]
    }
  },
  css: [
    '~/assets/css/main.css'
  ],
})