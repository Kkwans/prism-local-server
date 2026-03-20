import { useEffect } from 'react';
import { Dashboard } from './components/Dashboard';
import { Toaster } from '@/components/ui/toaster';
import { useServerStore } from './stores/useServerStore';
import { useConfigStore } from './stores/useConfigStore';

function App() {
  const { refreshServerList } = useServerStore();
  const { loadConfig } = useConfigStore();

  useEffect(() => {
    loadConfig();
    refreshServerList();
  }, []);

  return (
    <>
      <Dashboard />
      <Toaster />
    </>
  );
}

export default App;
