import React, { useMemo } from 'react';
import DOMPurify from 'dompurify';
import { ShieldCheck, Lock } from 'lucide-react';

interface SandboxedIframeProps {
  content: string;
  title: string;
}

export const SandboxedIframe: React.FC<SandboxedIframeProps> = ({ content, title }) => {
  // Sanitize markup prior to injecting into iframe srcdoc
  const cleanHtml = useMemo(() => {
    return DOMPurify.sanitize(content, {
      WHOLE_DOCUMENT: true,
      ADD_TAGS: ['style', 'link', 'script', 'input', 'button', 'canvas'],
      ADD_ATTR: ['target', 'id', 'class', 'style', 'type', 'value', 'min', 'max', 'step', 'oninput', 'onclick', 'placeholder'],
    });
  }, [content]);

  return (
    <div className="flex flex-col h-full bg-white relative">
      {/* Security Banner */}
      <div className="bg-stone-50 border-b border-stone-200 px-3 py-1.5 flex items-center justify-between text-[11px] text-stone-500 shrink-0">
        <div className="flex items-center gap-1.5 text-emerald-700 font-medium">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          <span>DOMPurify Sanitized & Isolated</span>
        </div>
        <div className="flex items-center gap-1 text-stone-600 font-mono text-[10px]">
          <Lock className="w-3 h-3 text-stone-500" />
          <span>sandbox="allow-scripts" (no same-origin)</span>
        </div>
      </div>

      {/* Sandboxed iframe */}
      <iframe
        title={title}
        srcDoc={cleanHtml}
        // Strict security isolation:
        // - allow-scripts enables interactive UI controls, calculators, and canvas widgets
        // - omission of allow-same-origin prevents access to host cookies, localStorage, and parent window
        sandbox="allow-scripts"
        referrerPolicy="no-referrer"
        className="w-full flex-1 border-none bg-white"
      />
    </div>
  );
};
