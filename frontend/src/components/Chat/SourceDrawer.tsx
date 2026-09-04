import React from 'react';
import { X, ExternalLink, Clock, Mic, Award } from 'lucide-react';
import { SourceCitation } from '../../types';

interface SourceDrawerProps {
  source: SourceCitation | null;
  onClose: () => void;
}

export const SourceDrawer: React.FC<SourceDrawerProps> = ({ source, onClose }) => {
  if (!source) return null;

  return (
    <div className="fixed inset-0 bg-black/40 backdrop-blur-xs z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-xl w-full max-h-[85vh] shadow-2xl border border-stone-200 flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="p-4 border-b border-stone-100 flex items-center justify-between bg-stone-50">
          <div className="flex items-center gap-2">
            <span className="p-1.5 bg-amber-100 text-amber-800 rounded-lg">
              <Mic className="w-4 h-4" />
            </span>
            <div>
              <h3 className="text-sm font-bold text-stone-900">{source.guest}</h3>
              <p className="text-xs text-stone-500 line-clamp-1">{source.episode}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-stone-400 hover:text-stone-700 hover:bg-stone-200 rounded-lg transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Metadata Badges */}
        <div className="px-4 py-2 bg-stone-100/60 border-b border-stone-100 flex items-center gap-3 text-xs text-stone-600 flex-wrap">
          <div className="flex items-center gap-1 font-mono">
            <Clock className="w-3.5 h-3.5 text-stone-400" />
            <span>Timestamp: {source.timestamp || '00:00:00'}</span>
          </div>
          <div className="flex items-center gap-1 font-medium text-emerald-700">
            <Award className="w-3.5 h-3.5" />
            <span>Relevance Score: {Math.round(source.score * 100)}%</span>
          </div>
          {source.youtube_url && (
            <a
              href={source.youtube_url}
              target="_blank"
              rel="noreferrer"
              className="ml-auto text-amber-700 hover:text-amber-900 flex items-center gap-1 font-medium hover:underline"
            >
              <span>Watch on YouTube</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          )}
        </div>

        {/* Full Transcript Excerpt */}
        <div className="p-5 overflow-y-auto flex-1 text-sm text-stone-800 leading-relaxed font-editorial bg-stone-50/30">
          <div className="p-4 rounded-xl bg-white border border-stone-200/80 shadow-xs">
            <p className="whitespace-pre-wrap">{source.text}</p>
          </div>
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-stone-100 bg-white flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-1.5 text-xs font-semibold bg-stone-900 text-white rounded-lg hover:bg-stone-800 transition-colors"
          >
            Close Excerpt
          </button>
        </div>
      </div>
    </div>
  );
};
