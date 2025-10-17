import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    host: true, // o "0.0.0.0" para escuchar externamente
    allowedHosts: ["goshawk-mutual-phoenix.ngrok-free.app"], // permite el host de ngrok
    hmr: {
      host: "goshawk-mutual-phoenix.ngrok-free.app",
      protocol: "wss",
      clientPort: 443,
    },
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  esbuild: {
    target: "esnext",
  },
})
