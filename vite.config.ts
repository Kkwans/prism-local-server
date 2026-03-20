import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./frontend"),
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
    // 代码分割优化 - Vite 8.0 使用函数形式
    rollupOptions: {
      output: {
        manualChunks: (id) => {
          // 将 React 相关库分离到单独的 chunk
          if (id.includes('node_modules/react') || id.includes('node_modules/react-dom')) {
            return 'react-vendor';
          }
          // 将 UI 组件库分离
          if (id.includes('node_modules/framer-motion') || id.includes('node_modules/zustand')) {
            return 'ui-vendor';
          }
          // 将 Tauri API 分离
          if (id.includes('node_modules/@tauri-apps')) {
            return 'tauri-vendor';
          }
        },
      },
    },
    // 设置 chunk 大小警告阈值
    chunkSizeWarningLimit: 500,
  },
  
  // Tauri 期望固定端口，如果端口不可用则失败
  server: {
    port: 1420,
    strictPort: true,
    watch: {
      // 3. 告诉 vite 忽略监视 backend
      ignored: ["**/backend/**"],
    },
  },
});
