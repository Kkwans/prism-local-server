import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { invoke } from '@tauri-apps/api/core';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Switch } from '@/components/ui/switch';
import { useConfigStore } from '@/stores/useConfigStore';
import { useToast } from '@/hooks/use-toast';
import type { AppConfig } from '@/types';

interface SettingsDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function SettingsDialog({ open, onOpenChange }: SettingsDialogProps) {
  const { config, saveConfig } = useConfigStore();
  const { toast } = useToast();
  
  const [formData, setFormData] = useState<AppConfig>({
    default_port: 8888,
    default_directory: '',
    default_entry_file: 'index.html',
    theme: 'system',
    auto_open_browser: true,
    minimize_to_tray: true,
  });

  // 加载配置
  useEffect(() => {
    if (open && config) {
      setFormData(config);
    }
  }, [open, config]);

  // 选择目录
  const handleSelectDirectory = async () => {
    try {
      const result = await invoke<string | null>('select_directory');
      if (result) {
        setFormData({ ...formData, default_directory: result });
      }
    } catch (error) {
      toast({
        title: "选择失败",
        description: String(error),
        variant: "destructive",
      });
    }
  };

  // 保存配置
  const handleSave = async () => {
    // 验证端口范围
    if (formData.default_port < 1024 || formData.default_port > 65535) {
      toast({
        title: "验证失败",
        description: "端口号必须在 1024-65535 范围内",
        variant: "destructive",
      });
      return;
    }

    try {
      await saveConfig(formData);
      toast({
        title: "保存成功",
        description: "配置已保存",
      });
      onOpenChange(false);
    } catch (error) {
      toast({
        title: "保存失败",
        description: String(error),
        variant: "destructive",
      });
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[550px] glass border-2">
        <DialogHeader>
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <div>
              <DialogTitle className="text-2xl">应用设置</DialogTitle>
              <DialogDescription className="text-sm mt-1">
                配置默认参数和应用行为
              </DialogDescription>
            </div>
          </div>
        </DialogHeader>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6 py-4"
        >
          {/* 默认端口号 */}
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <label className="text-sm font-semibold text-foreground">默认端口号</label>
            </div>
            <Input
              type="number"
              value={formData.default_port}
              onChange={(e) => setFormData({ ...formData, default_port: Number(e.target.value) })}
              min={1024}
              max={65535}
              placeholder="8888"
              className="bg-white border-2 focus:ring-2 focus:ring-blue-500 transition-all"
            />
            <p className="text-xs text-muted-foreground flex items-center gap-1">
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              范围: 1024-65535
            </p>
          </div>

          {/* 默认部署目录 */}
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
              </svg>
              <label className="text-sm font-semibold text-foreground">默认部署目录</label>
            </div>
            <div className="flex items-center gap-2">
              <Input
                value={formData.default_directory}
                onChange={(e) => setFormData({ ...formData, default_directory: e.target.value })}
                placeholder="留空则使用 EXE 所在目录"
                className="flex-1 bg-white border-2 focus:ring-2 focus:ring-green-500 transition-all h-10"
              />
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button 
                  variant="outline" 
                  onClick={handleSelectDirectory}
                  className="h-10 px-4 shadow-sm hover:shadow-md transition-all rounded-xl border-2 flex items-center justify-center"
                >
                  <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z" />
                  </svg>
                  浏览
                </Button>
              </motion.div>
            </div>
          </div>

          {/* 默认入口文件 */}
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <label className="text-sm font-semibold text-foreground">默认入口文件</label>
            </div>
            <Input
              value={formData.default_entry_file}
              onChange={(e) => setFormData({ ...formData, default_entry_file: e.target.value })}
              placeholder="index.html"
              className="bg-white border-2 focus:ring-2 focus:ring-orange-500 transition-all"
            />
          </div>

          <div className="border-t pt-4 space-y-4">
            {/* 自动打开浏览器 */}
            <div className="flex items-center justify-between p-3 rounded-xl bg-blue-50 hover:bg-blue-100 transition-colors">
              <div className="flex items-start gap-3">
                <svg className="w-5 h-5 text-blue-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                </svg>
                <div className="space-y-0.5">
                  <label className="text-sm font-semibold text-foreground cursor-pointer">自动打开浏览器</label>
                  <p className="text-xs text-muted-foreground">
                    启动服务后自动在浏览器中打开
                  </p>
                </div>
              </div>
              <Switch
                checked={formData.auto_open_browser}
                onCheckedChange={(checked) => setFormData({ ...formData, auto_open_browser: checked })}
              />
            </div>

            {/* 最小化到托盘 */}
            <div className="flex items-center justify-between p-3 rounded-xl bg-purple-50 hover:bg-purple-100 transition-colors">
              <div className="flex items-start gap-3">
                <svg className="w-5 h-5 text-purple-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <div className="space-y-0.5">
                  <label className="text-sm font-semibold text-foreground cursor-pointer">最小化到托盘</label>
                  <p className="text-xs text-muted-foreground">
                    关闭窗口时最小化到系统托盘
                  </p>
                </div>
              </div>
              <Switch
                checked={formData.minimize_to_tray}
                onCheckedChange={(checked) => setFormData({ ...formData, minimize_to_tray: checked })}
              />
            </div>
          </div>
        </motion.div>

        <DialogFooter className="gap-2">
          <Button 
            variant="outline" 
            onClick={() => onOpenChange(false)}
            className="shadow-sm hover:shadow-md transition-shadow"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
            取消
          </Button>
          <Button 
            onClick={handleSave}
            className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 shadow-md hover:shadow-lg transition-all"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            保存设置
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
