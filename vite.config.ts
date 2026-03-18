import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },

  // Vite 选项针对 Tauri 开发和打包优化
  clearScreen: false,
  
  // 构建优化
  build: {
    target: 'esnext',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,  // 移除 console.log
        drop_debugger: true,
      },
    },
  },
  
  // Tauri 期望固定端口，如果端口不可用则失败
  server: {
    port: 1420,
    strictPort: true,
    watch: {
      // 3. 告诉 vite 忽略监视 `src-tauri`
      ignored: ["**/src-tauri/**"],
    },
  },
});
