// 服务器状态管理 - Zustand Store

import { create } from 'zustand';
import { invoke } from '@tauri-apps/api/core';
import type { ServerConfig, ServerInfo } from '../types';

interface ServerStore {
  servers: ServerInfo[];
  isLoading: boolean;
  error: string | null;
  
  // Actions
  startServer: (config: ServerConfig) => Promise<void>;
  stopServer: (serverId: string) => Promise<void>;
  restartServer: (serverId: string) => Promise<void>;
  refreshServerList: () => Promise<void>;
  setError: (error: string | null) => void;
}

export const useServerStore = create<ServerStore>((set) => ({
  servers: [],
  isLoading: false,
  error: null,

  startServer: async (config: ServerConfig) => {
    set({ isLoading: true, error: null });
    try {
      const serverInfo = await invoke<ServerInfo>('start_server', { config });
      set((state) => ({
        servers: [...state.servers, serverInfo],
        isLoading: false,
      }));
    } catch (error) {
      const errorMsg = error as string;
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
      const errorMsg = error as string;
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
      const errorMsg = error as string;
      set({ error: errorMsg, isLoading: false });
      throw error;
    }
  },

  refreshServerList: async () => {
    set({ isLoading: true, error: null });
    try {
      const servers = await invoke<ServerInfo[]>('list_servers');
      set({ servers, isLoading: false });
    } catch (error) {
      const errorMsg = error as string;
      set({ error: errorMsg, isLoading: false });
    }
  },

  setError: (error: string | null) => {
    set({ error });
  },
}));
