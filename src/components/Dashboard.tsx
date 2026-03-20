import { useState, useCallback, memo, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ServerCard } from './ServerCard';
import { SettingsDialog } from './SettingsDialog';
import { Button } from '@/components/ui/button';
import { useServerStore } from '@/stores/useServerStore';
import { useConfigStore } from '@/stores/useConfigStore';
import { useToast } from '@/hooks/use-toast';
import type { ServerConfig } from '@/types';

export const Dashboard = memo(function Dashboard() {
  const { servers, startServer, stopServer, restartServer, refreshServerList, isLoading } = useServerStore();
  const { config } = useConfigStore();
  const { toast } = useToast();
  
  const [showSettings, setShowSettings] = useState(false);
  const [directory, setDirectory] = useState('');
  const [port, setPort] = useState(8888);
  const [lastRefreshTime, setLastRefreshTime] = useState(0);

  // 防抖刷新：限制刷新频率为 500ms
  const handleRefresh = useCallback(() => {
    const now = Date.now();
    if (now - lastRefreshTime < 500) {
      return; // 忽略过于频繁的刷新请求
    }
    setLastRefreshTime(now);
    refreshServerList();
  }, [lastRefreshTime, refreshServerList]);

  // 应用启动时刷新服务列表
  useEffect(() => {
    handleRefresh();
  }, [handleRefresh]);

  // 配置加载后自动填充到主界面(仅在输入框为空时)
  useEffect(() => {
    if (config && !directory) {
      setDirectory(config.default_directory || '');
    }
  }, [config, directory]);

  useEffect(() => {
    if (config && port === 8888 && config.default_port !== 8888) {
      setPort(config.default_port);
    }
  }, [config, port]);

  // 使用 useCallback 优化回调函数
  const handleStartServer = useCallback(async () => {
    if (!directory) {
      toast({
        title: "错误",
        description: "请先选择部署目录",
        variant: "destructive",
      });
      return;
    }

    const serverConfig: ServerConfig = {
      port,
      directory,
      entry_file: config?.default_entry_file || 'index.html',
    };

    try {
      const serverInfo = await startServer(serverConfig);
      
      // 检测端口是否发生变更
      if (serverInfo.port !== port) {
        toast({
          title: "端口已自动调整",
          description: `原端口 ${port} 被占用，已自动切换到端口 ${serverInfo.port}`,
        });
      } else {
        toast({
          title: "启动成功",
          description: `服务已在端口 ${serverInfo.port} 上启动`,
        });
      }
      
      // 清空输入
      setDirectory('');
      setPort(8888);
    } catch (error) {
      toast({
        title: "启动失败",
        description: String(error),
        variant: "destructive",
      });
    }
  }, [directory, port, config, startServer, toast]);

  // 使用 useMemo 缓存空状态组件，避免不必要的重渲染
  const emptyState = useMemo(() => (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.25 }}
      className="glass rounded-xl p-12 text-center"
    >
      <div className="text-6xl mb-4">🚀</div>
      <h3 className="text-xl font-semibold mb-2">暂无运行中的服务</h3>
      <p className="text-muted-foreground">
        点击上方"启动服务"按钮来部署你的第一个本地服务器
      </p>
    </motion.div>
  ), []);

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* 顶部标题栏 */}
        <div className="flex justify-between items-center mb-8">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
            className="flex items-center gap-4"
          >
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-lg">
              <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </div>
            <div>
              <h1 className="text-4xl font-bold title-gradient">
                棱镜本地服务器
              </h1>
              <p className="text-sm text-muted-foreground mt-1">高性能 HTML 静态文件部署工具</p>
            </div>
          </motion.div>
          
          <div className="flex gap-3">
            <motion.div 
              whileHover={{ scale: 1.03 }} 
              whileTap={{ scale: 0.97 }}
              transition={{ duration: 0.15 }}
            >
              <Button
                variant="outline"
                onClick={handleRefresh}
                disabled={isLoading}
                className="shadow-sm hover:shadow-md transition-shadow"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                刷新列表
              </Button>
            </motion.div>
            
            <motion.div 
              whileHover={{ scale: 1.03 }} 
              whileTap={{ scale: 0.97 }}
              transition={{ duration: 0.15 }}
            >
              <Button
                variant="secondary"
                onClick={() => setShowSettings(true)}
                className="shadow-sm hover:shadow-md transition-shadow"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                设置
              </Button>
            </motion.div>
          </div>
        </div>

        {/* 启动服务区域 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.3 }}
          className="glass rounded-2xl p-8 mb-8 card-shadow"
          style={{ willChange: 'transform' }}
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
            </div>
            <h2 className="text-2xl font-semibold text-foreground">启动新服务</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="flex-shrink-0">
              <label className="block text-sm font-medium text-foreground mb-2">部署目录</label>
              <div className="flex items-center gap-3">
                <input
                  type="text"
                  value={directory}
                  onChange={(e) => setDirectory(e.target.value)}
                  placeholder="选择要部署的目录"
                  className="flex-1 px-4 py-3 bg-white rounded-xl border-2 border-border focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all shadow-sm h-12 min-w-0"
                />
                <motion.div 
                  whileHover={{ scale: 1.03 }} 
                  whileTap={{ scale: 0.97 }}
                  transition={{ duration: 0.15 }}
                  className="flex-shrink-0"
                >
                  <Button
                    variant="outline"
                    onClick={async () => {
                      try {
                        const { invoke } = await import('@tauri-apps/api/core');
                        const result = await invoke<string | null>('select_directory');
                        if (result) {
                          setDirectory(result);
                        }
                      } catch (error) {
                        toast({
                          title: "选择失败",
                          description: String(error),
                          variant: "destructive",
                        });
                      }
                    }}
                    className="h-12 px-6 shadow-sm hover:shadow-md transition-all rounded-xl border-2 flex items-center justify-center w-[100px]"
                  >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                    </svg>
                    浏览
                  </Button>
                </motion.div>
              </div>
            </div>

            <div className="flex-shrink-0">
              <label className="block text-sm font-medium text-foreground mb-2">端口号</label>
              <input
                type="number"
                value={port}
                onChange={(e) => setPort(Number(e.target.value))}
                min={1024}
                max={65535}
                className="w-full px-4 py-3 bg-white rounded-xl border-2 border-border focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all shadow-sm h-12"
              />
            </div>
          </div>

          <motion.div 
            whileHover={{ scale: 1.02 }} 
            whileTap={{ scale: 0.98 }}
            transition={{ duration: 0.15 }}
            className="flex-shrink-0"
            style={{ willChange: 'transform' }}
          >
            <Button
              onClick={handleStartServer}
              disabled={isLoading}
              size="lg"
              className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white shadow-lg hover:shadow-xl transition-all"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {isLoading ? '启动中...' : '启动服务'}
            </Button>
          </motion.div>
        </motion.div>

        {/* 服务列表区域 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.3 }}
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
              </svg>
            </div>
            <h2 className="text-2xl font-semibold text-foreground">运行中的服务</h2>
            {servers.length > 0 && (
              <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                {servers.length} 个服务
              </span>
            )}
          </div>
          
          {isLoading && servers.length === 0 ? (
            // 加载状态
            <div className="grid gap-4">
              {[1, 2].map((i) => (
                <div key={i} className="glass rounded-xl p-6 animate-pulse">
                  <div className="h-6 bg-secondary rounded w-1/3 mb-4"></div>
                  <div className="space-y-2">
                    <div className="h-4 bg-secondary rounded w-full"></div>
                    <div className="h-4 bg-secondary rounded w-2/3"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : servers.length === 0 ? (
            // 空状态 - 使用缓存的组件
            emptyState
          ) : (
            // 服务列表
            <div className="grid grid-cols-1 2xl:grid-cols-2 gap-3">
              <AnimatePresence mode="popLayout">
                {servers.map((server, index) => (
                  <motion.div
                    key={server.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    transition={{ delay: index * 0.05, duration: 0.25 }}
                  >
                    <ServerCard
                      server={server}
                      onStop={stopServer}
                      onRestart={restartServer}
                    />
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          )}
        </motion.div>
      </div>

      {/* 设置对话框 */}
      <SettingsDialog open={showSettings} onOpenChange={setShowSettings} />
    </div>
  );
});
