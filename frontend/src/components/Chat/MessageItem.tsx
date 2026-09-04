import React from 'react';
import { Message, SourceCitation, Artifact } from '../../types';
import { MarkdownRenderer } from '../Artifact/MarkdownRenderer';
import { Compass, User, Sparkles, ExternalLink, FileCode, Layers, Mic } from 'lucide-react';

interface MessageItemProps {
  message: Message;
  onSelectSource: (source: SourceCitation) => void;
  onSelectArtifact: (artifact: Artifact) => void;
}

export const MessageItem: React.FC<MessageItemProps> = ({
  message,
  onSelectSource,
  onSelectArtifact,
}) => {
  const isUser = message.role === 'user';

  return (
    <div className={`py-4 px-4 sm:px-6 flex gap-3 sm:gap-4 ${isUser ? 'bg-transparent' : 'bg-white/60 border-y border-stone-200/50'}`}>
      {/* Avatar */}
      <div className="shrink-0 mt-0.5">
        {isUser ? (
          <div className="w-7 h-7 rounded-full bg-stone-900 text-white flex items-center justify-center text-xs shadow-xs">
            <User className="w-3.5 h-3.5" />
          </div>
        ) : (
          <div className="w-7 h-7 rounded-full bg-gradient-to-br from-amber-500 to-amber-700 text-white flex items-center justify-center text-xs shadow-xs">
            <Compass className="w-4 h-4" />
          </div>
        )}
      </div>

      {/* Message Body */}
      <div className="flex-1 min-w-0 space-y-3">
        {/* Header line with role & provider metadata */}
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold text-stone-900">
            {isUser ? 'You' : 'Lenny Growth Assistant'}
          </span>
          {!isUser && message.provider && (
            <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-stone-100 text-stone-600 border border-stone-200/60">
              {message.provider.toUpperCase()}
            </span>
          )}
          {!isUser && message.mode === 'ship30' && (
            <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-amber-100 text-amber-900 border border-amber-200">
              Ship 30 Essay
            </span>
          )}
        </div>

        {/* Markdown Content */}
        <MarkdownRenderer content={message.content} />

        {/* Source Citations Pills */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="pt-2 border-t border-stone-100">
            <p className="text-[11px] font-bold uppercase tracking-wider text-stone-500 mb-1.5 flex items-center gap-1">
              <Mic className="w-3 h-3 text-amber-600" />
              Verified Podcast Sources ({message.sources.length})
            </p>
            <div className="flex flex-wrap gap-1.5">
              {message.sources.map((s, idx) => (
                <button
                  key={idx}
                  onClick={() => onSelectSource(s)}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs bg-stone-100/80 hover:bg-amber-100 text-stone-700 hover:text-amber-950 border border-stone-200 hover:border-amber-300 transition-colors shadow-2xs"
                  title={`View excerpt from ${s.guest} (${s.timestamp})`}
                >
                  <span className="font-semibold">{s.guest}</span>
                  <span className="text-stone-400">({s.timestamp || '00:00:00'})</span>
                  <span className="text-[10px] text-emerald-700 font-mono">
                    {Math.round(s.score * 100)}%
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Generated Artifacts Cards */}
        {!isUser && message.artifacts && message.artifacts.length > 0 && (
          <div className="pt-2 space-y-2">
            {message.artifacts.map((art) => (
              <div
                key={art.id}
                onClick={() => onSelectArtifact(art)}
                className="flex items-center justify-between p-3 rounded-xl bg-gradient-to-r from-amber-50 to-stone-50 border border-amber-200/80 hover:border-amber-400 cursor-pointer shadow-xs hover:shadow-sm transition-all group"
              >
                <div className="flex items-center gap-2.5 min-w-0 pr-2">
                  <div className="p-2 rounded-lg bg-white border border-amber-200 text-amber-700 shadow-2xs">
                    <FileCode className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-amber-700">
                      Interactive {art.artifact_type.toUpperCase()} Artifact
                    </span>
                    <h4 className="text-xs font-bold text-stone-900 group-hover:text-amber-900 truncate">
                      {art.title}
                    </h4>
                  </div>
                </div>
                <button className="px-3 py-1.5 bg-white text-stone-800 text-xs font-semibold rounded-lg border border-stone-200 group-hover:bg-amber-600 group-hover:text-white group-hover:border-amber-600 transition-all flex items-center gap-1 shrink-0">
                  <span>Open Artifact</span>
                  <ExternalLink className="w-3 h-3" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
