// 配置状态管理 - Zustand Store

import { create } from 'zustand';
import { invoke } from '@tauri-apps/api/core';
import type { AppConfig } from '../types';

interface ConfigStore {
  config: AppConfig | null;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  loadConfig: () => Promise<void>;
  saveConfig: (config: AppConfig) => Promise<void>;
  updateConfig: (partial: Partial<AppConfig>) => void;
  updateDefaultDirectory: () => Promise<void>;
}

export const useConfigStore = create<ConfigStore>((set) => ({
  config: null,
  isLoading: false,
  error: null,

  loadConfig: async () => {
    set({ isLoading: true, error: null });
    try {
      const config = await invoke<AppConfig>('load_app_config');
      set({ config, isLoading: false });
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : '加载配置失败';
      console.error('加载配置失败:', error);
      set({ isLoading: false, error: errorMsg });
    }
  },

  saveConfig: async (config: AppConfig) => {
    set({ isLoading: true, error: null });
    try {
      await invoke('save_app_config', { config });
      set({ config, isLoading: false });
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : '保存配置失败';
      console.error('保存配置失败:', error);
      set({ isLoading: false, error: errorMsg });
      throw error;
    }
  },

  updateConfig: (partial: Partial<AppConfig>) => {
    set((state) => ({
      config: state.config ? { ...state.config, ...partial } : null,
    }));
  },

  updateDefaultDirectory: async () => {
    set({ isLoading: true, error: null });
    try {
      // 调用 Rust 后端获取 EXE 所在目录
      const exeDir = await invoke<string>('get_executable_directory');
      set((state) => ({
        config: state.config ? { ...state.config, default_directory: exeDir } : null,
        isLoading: false,
      }));
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : '获取 EXE 目录失败';
      console.error('获取 EXE 目录失败:', error);
      set({ isLoading: false, error: errorMsg });
    }
  },
}));
