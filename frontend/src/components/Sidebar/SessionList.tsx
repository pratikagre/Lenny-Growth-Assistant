import React from 'react';
import { Plus, MessageSquare, Trash2, Mic2, FileText, ChevronRight, Compass } from 'lucide-react';
import { Session } from '../../types';

interface SessionListProps {
  sessions: Session[];
  activeSessionId: string | null;
  onSelectSession: (id: string) => void;
  onNewSession: () => void;
  onDeleteSession: (id: string, e: React.MouseEvent) => void;
  onSelectTemplate: (prompt: string, mode?: 'default' | 'ship30') => void;
  isOpen: boolean;
}

export const SessionList: React.FC<SessionListProps> = ({
  sessions,
  activeSessionId,
  onSelectSession,
  onNewSession,
  onDeleteSession,
  onSelectTemplate,
  isOpen,
}) => {
  if (!isOpen) return null;

  const templates = [
    {
      title: "Brian Chesky's Single Roadmap",
      guest: "Brian Chesky",
      prompt: "What was Brian Chesky's rationale for redesigning product management and moving Airbnb to one single company-wide roadmap?",
      mode: 'default' as const,
    },
    {
      title: "Elena Verna's B2B Growth Loops",
      guest: "Elena Verna",
      prompt: "Explain Elena Verna's frameworks on B2B product-led growth loops and product-led sales versus traditional top-down sales.",
      mode: 'ship30' as const,
    },
    {
      title: "Interactive PLG Calculator",
      guest: "Elena & Casey",
      prompt: "Generate an interactive HTML/CSS ROI and Viral Coefficient calculator based on Lenny's guests' metrics.",
      mode: 'default' as const,
    },
    {
      title: "Shreyas Doshi on PM Thinking",
      guest: "Shreyas Doshi",
      prompt: "What are Shreyas Doshi's key principles for distinguishing great product managers from average PMs?",
      mode: 'ship30' as const,
    }
  ];

  return (
    <aside className="w-72 border-r border-stone-200 bg-stone-50/70 backdrop-blur-md flex flex-col h-[calc(100vh-3.5rem)] shrink-0 select-none">
      {/* New Session Button */}
      <div className="p-3 border-b border-stone-200/60">
        <button
          onClick={onNewSession}
          className="w-full flex items-center justify-between px-3.5 py-2.5 bg-stone-900 hover:bg-stone-800 text-white rounded-xl shadow-sm text-xs font-semibold transition-all hover:scale-[1.01] active:scale-[0.99]"
        >
          <div className="flex items-center gap-2">
            <Plus className="w-4 h-4" />
            <span>New Strategy Chat</span>
          </div>
          <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] bg-stone-800 border border-stone-700 text-stone-300 rounded font-mono">
            ⌘N
          </kbd>
        </button>
      </div>

      {/* Suggested Starter Templates */}
      <div className="p-3 border-b border-stone-200/60">
        <p className="text-[11px] font-bold uppercase tracking-wider text-stone-600 mb-2 px-1">
          Landmark Playbooks
        </p>
        <div className="space-y-1">
          {templates.map((t, idx) => (
            <button
              key={idx}
              onClick={() => onSelectTemplate(t.prompt, t.mode)}
              className="w-full text-left p-2 rounded-lg hover:bg-stone-200/60 text-xs text-stone-700 flex items-center justify-between group transition-colors"
            >
              <div className="min-w-0 pr-1">
                <p className="font-medium truncate text-stone-800 group-hover:text-amber-900">{t.title}</p>
                <span className="text-[10px] text-stone-600 flex items-center gap-1">
                  <Mic2 className="w-2.5 h-2.5" />
                  {t.guest} {t.mode === 'ship30' && '• Ship 30 Essay'}
                </span>
              </div>
              <ChevronRight className="w-3.5 h-3.5 text-stone-600 group-hover:text-stone-700 shrink-0" />
            </button>
          ))}
        </div>
      </div>

      {/* Chat Sessions History */}
      <div className="flex-1 overflow-y-auto p-3 space-y-1">
        <p className="text-[11px] font-bold uppercase tracking-wider text-stone-600 mb-2 px-1">
          Recent Sessions
        </p>
        {sessions.length === 0 ? (
          <div className="text-center py-8 text-stone-600 text-xs">
            <MessageSquare className="w-6 h-6 mx-auto mb-2 opacity-30" />
            No chat sessions yet.
          </div>
        ) : (
          sessions.map((s) => {
            const isActive = s.id === activeSessionId;
            return (
              <div
                key={s.id}
                onClick={() => onSelectSession(s.id)}
                className={`group flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer text-xs transition-colors ${
                  isActive
                    ? 'bg-amber-100/70 text-amber-950 font-semibold shadow-xs'
                    : 'text-stone-700 hover:bg-stone-200/50'
                }`}
              >
                <div className="flex items-center gap-2.5 min-w-0 pr-2">
                  <MessageSquare className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-amber-700' : 'text-stone-400'}`} />
                  <span className="truncate">{s.title || 'Untitled Session'}</span>
                </div>
                <button
                  onClick={(e) => onDeleteSession(s.id, e)}
                  title="Delete Session"
                  className="opacity-0 group-hover:opacity-100 text-stone-400 hover:text-rose-600 p-1 rounded transition-opacity"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            );
          })
        )}
      </div>

      {/* Footer Info */}
      <div className="p-3 border-t border-stone-200/60 bg-white/40 text-[11px] text-stone-500">
        <div className="flex items-center justify-between">
          <span className="flex items-center gap-1">
            <Compass className="w-3 h-3 text-amber-600" />
            Lenny Growth v1.0
          </span>
          <span className="text-[10px] text-stone-400">Forward Deployed</span>
        </div>
      </div>
    </aside>
  );
};
