import React from 'react';
import { HealthStatus } from '../../types';
import { Activity, Database, Cpu } from 'lucide-react';

interface StatusBadgeProps {
  health: HealthStatus | null;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ health }) => {
  if (!health) {
    return (
      <div className="flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-full bg-stone-100 text-stone-500 border border-stone-200">
        <span className="w-1.5 h-1.5 rounded-full bg-stone-400 animate-pulse" />
        Connecting...
      </div>
    );
  }

  const isHealthy = health.status === 'healthy';
  const ollamaOnline = health.ollama?.available;
  const chunkCount = health.vector_index?.chunks_indexed || 0;

  return (
    <div className="flex items-center gap-2">
      {/* DB & Chunks indicator */}
      <div 
        title={`Database: ${health.database.status} (${health.database.latency_ms || 0}ms) | Indexed Chunks: ${chunkCount}`}
        className="hidden md:flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-full bg-stone-100 text-stone-600 border border-stone-200"
      >
        <Database className="w-3 h-3 text-stone-500" />
        <span>{chunkCount} Chunks</span>
      </div>

      {/* Ollama local status */}
      <div 
        title={ollamaOnline ? `Ollama active at ${health.ollama.base_url}` : 'Ollama offline. Toggle to Cloud or Demo.'}
        className={`flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-full border ${
          ollamaOnline 
            ? 'bg-emerald-50 text-emerald-700 border-emerald-200' 
            : 'bg-amber-50 text-amber-700 border-amber-200'
        }`}
      >
        <Cpu className="w-3 h-3" />
        <span>{ollamaOnline ? 'Ollama Online' : 'Ollama Offline'}</span>
        <span className={`w-1.5 h-1.5 rounded-full ${ollamaOnline ? 'bg-emerald-500' : 'bg-amber-500'}`} />
      </div>
    </div>
  );
};
