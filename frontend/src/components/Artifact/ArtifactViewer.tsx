import React, { useState } from 'react';
import { X, Copy, Check, Download, Maximize2, Minimize2, Code, Eye, Sparkles } from 'lucide-react';
import { Artifact } from '../../types';
import { SandboxedIframe } from './SandboxedIframe';
import { MarkdownRenderer } from './MarkdownRenderer';

interface ArtifactViewerProps {
  artifact: Artifact | null;
  onClose: () => void;
}

export const ArtifactViewer: React.FC<ArtifactViewerProps> = ({ artifact, onClose }) => {
  const [viewTab, setViewTab] = useState<'preview' | 'code'>('preview');
  const [copied, setCopied] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  if (!artifact) return null;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(artifact.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (e) {
      console.error('Failed to copy artifact content', e);
    }
  };

  const handleDownload = () => {
    const ext = artifact.artifact_type === 'html' ? 'html' : 'md';
    const blob = new Blob([artifact.content], {
      type: artifact.artifact_type === 'html' ? 'text/html' : 'text/markdown',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${artifact.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.${ext}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div
      className={`border-l border-stone-200 bg-white flex flex-col z-20 transition-all duration-200 shadow-xl ${
        isFullscreen
          ? 'fixed inset-0 z-50'
          : 'w-full lg:w-[48%] h-[calc(100vh-3.5rem)] shrink-0'
      }`}
    >
      {/* Header */}
      <div className="h-12 border-b border-stone-200 px-4 flex items-center justify-between bg-stone-50/80 shrink-0">
        <div className="flex items-center gap-2 min-w-0 pr-2">
          <Sparkles className="w-4 h-4 text-amber-600 shrink-0" />
          <h2 className="text-xs font-bold text-stone-900 truncate" title={artifact.title}>
            {artifact.title}
          </h2>
          <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-stone-200/80 text-stone-700 shrink-0">
            {artifact.artifact_type.toUpperCase()}
          </span>
        </div>

        <div className="flex items-center gap-1.5">
          {/* Tab Switcher (Preview / Code) */}
          <div className="flex items-center bg-stone-200/70 p-0.5 rounded-lg text-xs font-medium mr-2">
            <button
              onClick={() => setViewTab('preview')}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-md transition-all ${
                viewTab === 'preview'
                  ? 'bg-white text-stone-900 shadow-xs'
                  : 'text-stone-600 hover:text-stone-900'
              }`}
            >
              <Eye className="w-3.5 h-3.5" />
              <span>Preview</span>
            </button>
            <button
              onClick={() => setViewTab('code')}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-md transition-all ${
                viewTab === 'code'
                  ? 'bg-white text-stone-900 shadow-xs'
                  : 'text-stone-600 hover:text-stone-900'
              }`}
            >
              <Code className="w-3.5 h-3.5" />
              <span>Source</span>
            </button>
          </div>

          {/* Copy Button */}
          <button
            onClick={handleCopy}
            className="p-1.5 text-stone-500 hover:text-stone-800 hover:bg-stone-200/60 rounded-lg transition-colors"
            title="Copy Source to Clipboard"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
          </button>

          {/* Download Button */}
          <button
            onClick={handleDownload}
            className="p-1.5 text-stone-500 hover:text-stone-800 hover:bg-stone-200/60 rounded-lg transition-colors"
            title="Download Artifact File"
          >
            <Download className="w-4 h-4" />
          </button>

          {/* Fullscreen Toggle */}
          <button
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="p-1.5 text-stone-500 hover:text-stone-800 hover:bg-stone-200/60 rounded-lg transition-colors"
            title={isFullscreen ? 'Exit Fullscreen' : 'Expand to Fullscreen'}
          >
            {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>

          {/* Close */}
          <button
            onClick={onClose}
            className="p-1.5 text-stone-400 hover:text-stone-700 hover:bg-stone-200/60 rounded-lg transition-colors ml-1"
            title="Close Artifact Viewer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-hidden relative">
        {viewTab === 'preview' ? (
          artifact.artifact_type === 'html' ? (
            <SandboxedIframe content={artifact.content} title={artifact.title} />
          ) : (
            <div className="h-full overflow-y-auto p-6 font-editorial">
              <MarkdownRenderer content={artifact.content} />
            </div>
          )
        ) : (
          <div className="h-full overflow-y-auto bg-stone-900 p-4 text-stone-100 font-mono text-xs">
            <pre className="whitespace-pre-wrap leading-relaxed">
              <code>{artifact.content}</code>
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};
