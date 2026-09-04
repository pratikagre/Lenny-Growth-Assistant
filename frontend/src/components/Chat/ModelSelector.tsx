import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Cpu, Sparkles, Terminal, Check } from 'lucide-react';
import { HealthStatus } from '../../types';

interface ModelSelectorProps {
  selectedProvider: string;
  onSelectProvider: (provider: string) => void;
  health: HealthStatus | null;
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({
  selectedProvider,
  onSelectProvider,
  health,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const ollamaOnline = health?.ollama?.available;

  const providers = [
    {
      id: 'ollama',
      name: 'Local Ollama',
      model: health?.ollama?.configured_model || 'llama3.2:3b',
      badge: ollamaOnline ? 'Ready' : 'Offline',
      badgeColor: ollamaOnline ? 'text-emerald-700 bg-emerald-100' : 'text-amber-700 bg-amber-100',
      icon: Cpu,
      description: 'Privacy-first offline local LLM for evaluation demo',
    },
    {
      id: 'claude',
      name: 'Anthropic Claude',
      model: 'claude-3-5-sonnet',
      badge: health?.cloud_providers?.claude?.configured ? 'Configured' : 'Needs Key',
      badgeColor: health?.cloud_providers?.claude?.configured ? 'text-blue-700 bg-blue-100' : 'text-stone-600 bg-stone-100',
      icon: Sparkles,
      description: 'Enterprise intelligence and long-form analytical nuance',
    },
    {
      id: 'openai',
      name: 'OpenAI GPT-4o',
      model: 'gpt-4o',
      badge: health?.cloud_providers?.openai?.configured ? 'Configured' : 'Needs Key',
      badgeColor: health?.cloud_providers?.openai?.configured ? 'text-blue-700 bg-blue-100' : 'text-stone-600 bg-stone-100',
      icon: Sparkles,
      description: 'High-speed multi-modal reasoning engine',
    },
    {
      id: 'mock',
      name: 'Evaluation Demo Provider',
      model: 'High-Fidelity Deterministic',
      badge: 'Zero-Dep',
      badgeColor: 'text-purple-700 bg-purple-100',
      icon: Terminal,
      description: 'Instant verification mode with guaranteed citations and artifacts',
    },
  ];

  const current = providers.find((p) => p.id === selectedProvider) || providers[0];
  const Icon = current.icon;

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-1.5 bg-white hover:bg-stone-50 border border-stone-200 rounded-lg shadow-sm text-xs font-medium text-stone-800 transition-colors"
      >
        <Icon className="w-3.5 h-3.5 text-stone-600" />
        <span className="font-semibold">{current.name}</span>
        <span className="text-stone-400 hidden sm:inline">({current.model})</span>
        <ChevronDown className={`w-3.5 h-3.5 text-stone-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-white border border-stone-200 rounded-xl shadow-xl z-50 p-1.5 animate-in fade-in slide-in-from-top-2 duration-150">
          <div className="px-3 py-2 border-b border-stone-100 mb-1">
            <p className="text-xs font-semibold text-stone-900">Select LLM Runtime Provider</p>
            <p className="text-[11px] text-stone-500">Switch inference engine dynamically without altering code</p>
          </div>
          <div className="space-y-1">
            {providers.map((p) => {
              const PIcon = p.icon;
              const isSelected = p.id === selectedProvider;
              return (
                <button
                  key={p.id}
                  onClick={() => {
                    onSelectProvider(p.id);
                    setIsOpen(false);
                  }}
                  className={`w-full text-left p-2.5 rounded-lg flex items-start gap-2.5 transition-colors ${
                    isSelected ? 'bg-amber-50/80 border border-amber-200/70' : 'hover:bg-stone-50'
                  }`}
                >
                  <PIcon className={`w-4 h-4 mt-0.5 ${isSelected ? 'text-amber-700' : 'text-stone-500'}`} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-1 mb-0.5">
                      <span className="text-xs font-semibold text-stone-900">{p.name}</span>
                      <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded-full ${p.badgeColor}`}>
                        {p.badge}
                      </span>
                    </div>
                    <p className="text-[11px] text-stone-500 leading-snug">{p.description}</p>
                  </div>
                  {isSelected && <Check className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
