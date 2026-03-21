// 服务器状态管理 - Zustand Store

import { create } from 'zustand';
import { invoke } from '@tauri-apps/api/core';
import type { ServerConfig, ServerInfo } from '../types';

interface ServerStore {
  servers: ServerInfo[];
  isLoading: boolean;
  error: string | null;
  
  // Actions
  fetchServers: () => Promise<void>;
  startServer: (config: ServerConfig) => Promise<ServerInfo>;
  stopServer: (serverId: string) => Promise<void>;
  restartServer: (serverId: string) => Promise<void>;
  refreshServerList: () => Promise<void>;
  setError: (error: string | null) => void;
}

export const useServerStore = create<ServerStore>((set, get) => ({
  servers: [],
  isLoading: false,
  error: null,

  fetchServers: async () => {
    set({ isLoading: true, error: null });
    try {
      const servers = await invoke<ServerInfo[]>('list_servers');
      set({ servers, isLoading: false });
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : '获取服务列表失败';
      set({ error: errorMsg, isLoading: false });
    }
  },

  startServer: async (config: ServerConfig) => {
    set({ isLoading: true, error: null });
    try {
      const serverInfo = await invoke<ServerInfo>('start_server', { config });
      set((state) => ({
        servers: [...state.servers, serverInfo],
        isLoading: false,
      }));
      return serverInfo; // 返回服务信息，供调用者检测端口变更
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      set({ error: errorMsg, isLoading: false });
      throw error;
    }
  },

  stopServer: async (serverId: string) => {
    set({ isLoading: true, error: null });
    try {
      await invoke('stop_server', { serverId });
      set((state) => ({
        servers: state.servers.filter((s) => s.id !== serverId),
        isLoading: false,
      }));
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      set({ error: errorMsg, isLoading: false });
      throw error;
    }
  },

  restartServer: async (serverId: string) => {
    set({ isLoading: true, error: null });
    try {
      const serverInfo = await invoke<ServerInfo>('restart_server', { serverId });
      set((state) => ({
        servers: state.servers.map((s) => (s.id === serverId ? serverInfo : s)),
        isLoading: false,
      }));
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      set({ error: errorMsg, isLoading: false });
      throw error;
    }
  },

  refreshServerList: async () => {
    // 别名,调用 fetchServers
    await get().fetchServers();
  },

  setError: (error: string | null) => {
    set({ error });
  },
}));
