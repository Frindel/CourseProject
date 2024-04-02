import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

//https://vitejs.dev/config/
export default defineConfig({
  optimizeDeps: {
    exclude: ['js-big-decimal']
  },

  plugins: [vue()],
  server: {
    watch: {
      usePolling: true
    }
  }
})