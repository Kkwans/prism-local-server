// 配置状态管理 - Zustand Store

import { create } from 'zustand';
import { invoke } from '@tauri-apps/api/core';
import type { AppConfig } from '../types';

interface ConfigStore {
  config: AppConfig | null;
  isLoading: boolean;
  
  // Actions
  loadConfig: () => Promise<void>;
  saveConfig: (config: AppConfig) => Promise<void>;
  updateConfig: (partial: Partial<AppConfig>) => void;
}

export const useConfigStore = create<ConfigStore>((set) => ({
  config: null,
  isLoading: false,

  loadConfig: async () => {
    set({ isLoading: true });
    try {
      const config = await invoke<AppConfig>('load_app_config');
      set({ config, isLoading: false });
    } catch (error) {
      console.error('加载配置失败:', error);
      set({ isLoading: false });
    }
  },

  saveConfig: async (config: AppConfig) => {
    set({ isLoading: true });
    try {
      await invoke('save_app_config', { config });
      set({ config, isLoading: false });
    } catch (error) {
      console.error('保存配置失败:', error);
      set({ isLoading: false });
      throw error;
    }
  },

  updateConfig: (partial: Partial<AppConfig>) => {
    set((state) => ({
      config: state.config ? { ...state.config, ...partial } : null,
    }));
  },
}));
