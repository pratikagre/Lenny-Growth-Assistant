import React from 'react';
import { PanelLeft, Sparkles, Compass } from 'lucide-react';
import { ModelSelector } from '../Chat/ModelSelector';
import { StatusBadge } from './StatusBadge';
import { HealthStatus } from '../../types';

interface HeaderProps {
  onToggleSidebar: () => void;
  selectedProvider: string;
  onSelectProvider: (provider: string) => void;
  health: HealthStatus | null;
}

export const Header: React.FC<HeaderProps> = ({
  onToggleSidebar,
  selectedProvider,
  onSelectProvider,
  health,
}) => {
  return (
    <header className="h-14 border-b border-stone-200 bg-white/80 backdrop-blur-md px-4 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="p-1.5 text-stone-500 hover:text-stone-800 hover:bg-stone-100 rounded-lg transition-colors"
          title="Toggle Sidebar (Cmd+B)"
        >
          <PanelLeft className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-amber-500 to-amber-700 flex items-center justify-center text-white shadow-sm">
            <Compass className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-sm text-stone-900 tracking-tight">The Lenny Growth Assistant</span>
              <span className="hidden sm:inline-flex items-center px-2 py-0.5 text-[10px] font-semibold bg-amber-100 text-amber-800 rounded-full">
                300+ Episodes
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <StatusBadge health={health} />
        <ModelSelector
          selectedProvider={selectedProvider}
          onSelectProvider={onSelectProvider}
          health={health}
        />
      </div>
    </header>
  );
};
