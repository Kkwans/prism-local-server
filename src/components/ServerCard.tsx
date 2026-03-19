import { useState, useEffect, memo } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { useToast } from '@/hooks/use-toast';
import type { ServerInfo } from '@/types';

interface ServerCardProps {
  server: ServerInfo;
  onStop: (serverId: string) => Promise<void>;
  onRestart: (serverId: string) => Promise<void>;
}

export const ServerCard = memo(function ServerCard({ server, onStop, onRestart }: ServerCardProps) {
  const [uptime, setUptime] = useState('00:00:00');
  const [showStopDialog, setShowStopDialog] = useState(false);
  const { toast } = useToast();

  // 实时更新运行时长
  useEffect(() => {
    const updateUptime = () => {
      const now = Date.now();
      const diff = Math.floor((now - server.start_time) / 1000);
      const hours = Math.floor(diff / 3600);
      const minutes = Math.floor((diff % 3600) / 60);
      const seconds = diff % 60;
      setUptime(
        `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
      );
    };

    updateUptime();
    const interval = setInterval(updateUptime, 1000);
    return () => clearInterval(interval);
  }, [server.start_time]);

  // 复制链接到剪贴板
  const handleCopyUrl = async (url: string) => {
    try {
      await navigator.clipboard.writeText(url);
      toast({
        title: "复制成功",
        description: `已复制: ${url}`,
      });
    } catch (error) {
      toast({
        title: "复制失败",
        description: String(error),
        variant: "destructive",
      });
    }
  };

  // 在浏览器中打开
  const handleOpenInBrowser = async (url: string) => {
    try {
      const opener = await import('@tauri-apps/plugin-opener');
      await opener.openUrl(url);
    } catch (error) {
      toast({
        title: "打开失败",
        description: String(error),
        variant: "destructive",
      });
    }
  };

  // 停止服务
  const handleStop = async () => {
    setShowStopDialog(false);
    try {
      await onStop(server.id);
      toast({
        title: "服务已停止",
        description: `服务 "${server.name}" 已成功停止`,
      });
    } catch (error) {
      toast({
        title: "停止失败",
        description: String(error),
        variant: "destructive",
      });
    }
  };

  // 重启服务
  const handleRestart = async () => {
    try {
      await onRestart(server.id);
      toast({
        title: "服务已重启",
        description: `服务 "${server.name}" 已成功重启`,
      });
    } catch (error) {
      toast({
        title: "重启失败",
        description: String(error),
        variant: "destructive",
      });
    }
  };

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.3 }}
      >
        <Card className="glass card-shadow hover:shadow-xl transition-all duration-300 border-2">
          <CardContent className="p-6">
            {/* 头部：服务名称和状态 */}
            <div className="flex justify-between items-start mb-6">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-lg">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-foreground" title={server.name}>
                    {server.name}
                  </h3>
                  <p className="text-sm text-muted-foreground">端口: {server.port}</p>
                </div>
              </div>
              <span className="status-badge px-4 py-2 text-white rounded-full text-sm font-medium flex items-center gap-2">
                <span className="w-2 h-2 bg-white rounded-full animate-pulse"></span>
                运行中
              </span>
            </div>

            {/* 服务信息 */}
            <div className="space-y-3 mb-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4">
              <div className="flex items-start gap-2">
                <svg className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
                <div className="flex-1 min-w-0">
                  <span className="text-xs text-muted-foreground">目录</span>
                  <p className="text-sm font-mono text-foreground truncate" title={server.directory}>
                    {server.directory.length > 60
                      ? `...${server.directory.slice(-57)}`
                      : server.directory}
                  </p>
                </div>
              </div>
              
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-green-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                </svg>
                <div className="flex-1">
                  <span className="text-xs text-muted-foreground">本地访问</span>
                  <a
                    href={server.local_url}
                    onClick={(e) => {
                      e.preventDefault();
                      handleOpenInBrowser(server.local_url);
                    }}
                    className="text-sm text-blue-600 hover:text-blue-700 font-medium cursor-pointer hover:underline block"
                  >
                    {server.local_url}
                  </a>
                </div>
              </div>

              {server.lan_urls.map((url, idx) => (
                <div key={idx} className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-purple-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0" />
                  </svg>
                  <div className="flex-1">
                    <span className="text-xs text-muted-foreground">局域网访问</span>
                    <a
                      href={url}
                      onClick={(e) => {
                        e.preventDefault();
                        handleOpenInBrowser(url);
                      }}
                      className="text-sm text-purple-600 hover:text-purple-700 font-medium cursor-pointer hover:underline block"
                    >
                      {url}
                    </a>
                  </div>
                </div>
              ))}

              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-orange-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                  <span className="text-xs text-muted-foreground">运行时长</span>
                  <p className="text-sm font-mono font-semibold text-foreground">{uptime}</p>
                </div>
              </div>
            </div>

            {/* 操作按钮 */}
            <div className="grid grid-cols-2 gap-3">
              <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleOpenInBrowser(server.local_url)}
                  className="w-full shadow-sm hover:shadow-md transition-all border-2 hover:border-blue-300 hover:bg-blue-50"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  打开浏览器
                </Button>
              </motion.div>

              <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleCopyUrl(server.local_url)}
                  className="w-full shadow-sm hover:shadow-md transition-all border-2 hover:border-green-300 hover:bg-green-50"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  复制链接
                </Button>
              </motion.div>

              <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={handleRestart}
                  className="w-full shadow-sm hover:shadow-md transition-all"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  重启
                </Button>
              </motion.div>

              <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}>
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={() => setShowStopDialog(true)}
                  className="w-full shadow-sm hover:shadow-md transition-all"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
                  </svg>
                  停止
                </Button>
              </motion.div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* 停止确认对话框 */}
      <Dialog open={showStopDialog} onOpenChange={setShowStopDialog}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <svg className="w-6 h-6 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              确认停止服务
            </DialogTitle>
            <DialogDescription className="text-base">
              确定要停止服务 <span className="font-semibold text-foreground">"{server.name}"</span> 吗？
              <br />
              此操作将关闭端口 <span className="font-semibold text-foreground">{server.port}</span>。
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="gap-2 sm:gap-0">
            <Button variant="outline" onClick={() => setShowStopDialog(false)}>
              取消
            </Button>
            <Button variant="destructive" onClick={handleStop}>
              确认停止
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
});
