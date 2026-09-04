import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, Feather, Compass, Loader2, ArrowUpCircle } from 'lucide-react';
import { Message, SourceCitation, Artifact } from '../../types';
import { MessageItem } from './MessageItem';

interface ChatPaneProps {
  messages: Message[];
  isStreaming: boolean;
  streamingStatus: string | null;
  onSendMessage: (text: string, mode: 'default' | 'ship30') => void;
  onSelectSource: (source: SourceCitation) => void;
  onSelectArtifact: (artifact: Artifact) => void;
  onSelectTemplate: (prompt: string, mode?: 'default' | 'ship30') => void;
}

export const ChatPane: React.FC<ChatPaneProps> = ({
  messages,
  isStreaming,
  streamingStatus,
  onSendMessage,
  onSelectSource,
  onSelectArtifact,
  onSelectTemplate,
}) => {
  const [inputText, setInputText] = useState('');
  const [mode, setMode] = useState<'default' | 'ship30'>('default');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isStreaming, streamingStatus]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() || isStreaming) return;
    onSendMessage(inputText.trim(), mode);
    setInputText('');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const starters = [
    {
      title: "Brian Chesky on Roadmaps",
      subtitle: "Why Airbnb abandoned traditional PM for one company-wide roadmap",
      prompt: "What was Brian Chesky's rationale for getting rid of traditional product managers at Airbnb and moving to a single roadmap?",
      mode: 'default' as const,
    },
    {
      title: "Elena Verna on B2B Loops",
      subtitle: "Turn answers into a 1,250-word Ship 30 essay on product-led sales",
      prompt: "Explain Elena Verna's frameworks on B2B growth loops and product-led sales versus traditional top-down enterprise sales.",
      mode: 'ship30' as const,
    },
    {
      title: "Interactive PLG Calculator",
      subtitle: "Generate an executable HTML artifact with live sliders",
      prompt: "Generate an interactive HTML/CSS ROI and Viral Coefficient calculator based on Lenny's guests' metrics.",
      mode: 'default' as const,
    },
    {
      title: "Shreyas Doshi on PM Thinking",
      subtitle: "Tactical advice on PM career ladders and strategic leverage",
      prompt: "What are Shreyas Doshi's key principles for distinguishing high-leverage product leaders from average execution PMs?",
      mode: 'ship30' as const,
    }
  ];

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-3.5rem)] bg-transparent overflow-hidden relative">
      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="max-w-2xl mx-auto px-4 py-12 flex flex-col items-center justify-center min-h-[70vh] text-center">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-amber-500 to-amber-700 text-white flex items-center justify-center shadow-md mb-4">
              <Compass className="w-6 h-6" />
            </div>
            <h1 className="text-2xl font-extrabold text-stone-900 tracking-tight mb-2">
              The Lenny Growth Assistant
            </h1>
            <p className="text-sm text-stone-600 max-w-md leading-relaxed mb-8">
              Ask deep tactical questions strictly grounded in 300+ transcripts from premier founders and product leaders.
            </p>

            {/* Starter Prompts Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full text-left">
              {starters.map((s, idx) => (
                <button
                  key={idx}
                  onClick={() => onSelectTemplate(s.prompt, s.mode)}
                  className="p-3.5 rounded-xl bg-white/75 backdrop-blur-md border border-stone-200/70 hover:border-amber-400 hover:shadow-md hover:bg-white/90 text-left transition-all group"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-bold text-stone-900 group-hover:text-amber-800">
                      {s.title}
                    </span>
                    {s.mode === 'ship30' && (
                      <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-amber-100 text-amber-900">
                        Ship 30
                      </span>
                    )}
                  </div>
                  <p className="text-[11px] text-stone-500 line-clamp-2 leading-relaxed">
                    {s.subtitle}
                  </p>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="divide-y divide-stone-100">
            {messages.map((m) => (
              <MessageItem
                key={m.id}
                message={m}
                onSelectSource={onSelectSource}
                onSelectArtifact={onSelectArtifact}
              />
            ))}

            {/* Streaming Status Indicator */}
            {isStreaming && (
              <div className="p-4 bg-white/60 border-y border-stone-200/50 flex items-center gap-3">
                <Loader2 className="w-4 h-4 text-amber-600 animate-spin" />
                <span className="text-xs text-stone-600 font-medium">
                  {streamingStatus || 'Lenny Assistant is synthesizing grounded answer...'}
                </span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Composer */}
      <div className="p-4 border-t border-stone-200/70 bg-white/60 backdrop-blur-xl">
        <div className="max-w-3xl mx-auto">
          {/* Mode Selector Pill Bar */}
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-1 bg-white/70 backdrop-blur-md p-0.5 rounded-lg text-xs font-medium border border-stone-200/70 shadow-2xs">
              <button
                type="button"
                onClick={() => setMode('default')}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-md transition-all ${
                  mode === 'default'
                    ? 'bg-amber-600 text-white shadow-xs font-semibold'
                    : 'text-stone-600 hover:text-stone-900'
                }`}
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>Standard RAG Q&A</span>
              </button>
              <button
                type="button"
                onClick={() => setMode('ship30')}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-md transition-all ${
                  mode === 'ship30'
                    ? 'bg-amber-600 text-white shadow-xs font-semibold'
                    : 'text-stone-600 hover:text-stone-900'
                }`}
              >
                <Feather className="w-3.5 h-3.5" />
                <span>Ship 30 for 30 Essay</span>
              </button>
            </div>

            <span className="text-[11px] text-stone-500 font-medium hidden sm:inline">
              Enter to send, Shift+Enter for new line
            </span>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="relative flex items-end">
            <textarea
              ref={textareaRef}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={
                mode === 'ship30'
                  ? "Describe the topic or operator mental model you'd like transformed into a ~1,250-word Ship 30 essay..."
                  : "Ask anything about product strategy, growth loops, roadmaps, or Lenny's guests..."
              }
              rows={2}
              className="w-full resize-none p-3 pr-12 rounded-xl border border-stone-300/80 focus:border-amber-500 focus:ring-2 focus:ring-amber-500/20 text-xs sm:text-sm text-stone-900 placeholder:text-stone-400 bg-white/80 backdrop-blur-md focus:bg-white transition-all outline-none shadow-xs"
            />
            <button
              type="submit"
              disabled={!inputText.trim() || isStreaming}
              className="absolute right-2.5 bottom-2.5 p-2 bg-stone-900 hover:bg-stone-800 disabled:bg-stone-200 text-white disabled:text-stone-400 rounded-lg transition-all shadow-xs"
              title="Send Prompt"
            >
              {isStreaming ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
