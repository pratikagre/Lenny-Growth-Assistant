import React, { useState, useEffect } from 'react';
import { Header } from './components/Common/Header';
import { SessionList } from './components/Sidebar/SessionList';
import { ChatPane } from './components/Chat/ChatPane';
import { ArtifactViewer } from './components/Artifact/ArtifactViewer';
import { SourceDrawer } from './components/Chat/SourceDrawer';
import { Session, Message, Artifact, SourceCitation, HealthStatus } from './types';
import { fetchHealth, fetchSessions, createSession, fetchSessionDetail, deleteSession, streamChat } from './lib/api';

export const App: React.FC = () => {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [activeArtifact, setActiveArtifact] = useState<Artifact | null>(null);
  const [activeSource, setActiveSource] = useState<SourceCitation | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [selectedProvider, setSelectedProvider] = useState<string>('ollama');
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingStatus, setStreamingStatus] = useState<string | null>(null);

  // 1. Initial Load: Probe health and load sessions
  useEffect(() => {
    const init = async () => {
      try {
        const h = await fetchHealth();
        setHealth(h);
        // If Ollama is offline and no cloud keys, default to mock provider for immediate evaluation
        if (!h.ollama?.available && !h.cloud_providers?.claude?.configured && !h.cloud_providers?.openai?.configured) {
          setSelectedProvider('mock');
        } else if (h.ollama?.available) {
          setSelectedProvider('ollama');
        }
      } catch (e) {
        console.warn('Initial health check notice', e);
        setSelectedProvider('mock');
      }

      try {
        const sessList = await fetchSessions();
        setSessions(sessList);
        if (sessList.length > 0) {
          selectSession(sessList[0].id);
        } else {
          handleNewSession();
        }
      } catch (e) {
        console.error('Failed to load initial sessions', e);
      }
    };
    init();
  }, []);

  // Poll health every 30 seconds
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const h = await fetchHealth();
        setHealth(h);
      } catch {}
    }, 30000);
    return () => clearInterval(interval);
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'b') {
        e.preventDefault();
        setIsSidebarOpen((prev) => !prev);
      }
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'n') {
        e.preventDefault();
        handleNewSession();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const selectSession = async (sessionId: string) => {
    setActiveSessionId(sessionId);
    try {
      const detail = await fetchSessionDetail(sessionId);
      setMessages(detail.messages);
      if (detail.artifacts && detail.artifacts.length > 0) {
        setActiveArtifact(detail.artifacts[detail.artifacts.length - 1]);
      } else {
        setActiveArtifact(null);
      }
    } catch (e) {
      console.error('Failed to fetch session detail', e);
    }
  };

  const handleNewSession = async () => {
    try {
      const newSess = await createSession('New Strategy Session');
      setSessions((prev) => [newSess, ...prev]);
      setActiveSessionId(newSess.id);
      setMessages([]);
      setActiveArtifact(null);
    } catch (e) {
      console.error('Failed to create new session', e);
    }
  };

  const handleDeleteSession = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await deleteSession(sessionId);
      const remaining = sessions.filter((s) => s.id !== sessionId);
      setSessions(remaining);
      if (activeSessionId === sessionId) {
        if (remaining.length > 0) {
          selectSession(remaining[0].id);
        } else {
          handleNewSession();
        }
      }
    } catch (e) {
      console.error('Failed to delete session', e);
    }
  };

  const handleSendMessage = async (text: string, mode: 'default' | 'ship30' = 'default') => {
    let currentSessionId = activeSessionId;
    if (!currentSessionId) {
      const newS = await createSession(text.slice(0, 40));
      currentSessionId = newS.id;
      setActiveSessionId(newS.id);
      setSessions((prev) => [newS, ...prev]);
    }

    // Append user message immediately
    const userMsg: Message = {
      id: `user-${Date.now()}`,
      session_id: currentSessionId,
      role: 'user',
      content: text,
      sources: [],
      mode,
      created_at: new Date().toISOString(),
    };

    const asstTempId = `asst-${Date.now()}`;
    const asstMsg: Message = {
      id: asstTempId,
      session_id: currentSessionId,
      role: 'assistant',
      content: '',
      sources: [],
      provider: selectedProvider,
      mode,
      created_at: new Date().toISOString(),
      artifacts: [],
    };

    setMessages((prev) => [...prev, userMsg, asstMsg]);
    setIsStreaming(true);
    setStreamingStatus('Searching 300+ transcripts...');

    await streamChat(
      {
        session_id: currentSessionId,
        message: text,
        provider: selectedProvider,
        mode,
      },
      // onToken
      (token: string) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === asstTempId ? { ...m, content: m.content + token } : m
          )
        );
      },
      // onSources
      (sources: SourceCitation[]) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === asstTempId ? { ...m, sources } : m
          )
        );
        setStreamingStatus(null);
      },
      // onArtifacts
      (artifacts: Artifact[]) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === asstTempId ? { ...m, artifacts } : m
          )
        );
        if (artifacts && artifacts.length > 0) {
          setActiveArtifact(artifacts[artifacts.length - 1]);
        }
      },
      // onStatus
      (status: string) => {
        setStreamingStatus(status);
      },
      // onError
      (error: Error) => {
        console.error('Streaming error', error);
        setMessages((prev) =>
          prev.map((m) =>
            m.id === asstTempId
              ? { ...m, content: m.content + `\n\n**Error:** ${error.message}` }
              : m
          )
        );
        setIsStreaming(false);
        setStreamingStatus(null);
      },
      // onDone
      async () => {
        setIsStreaming(false);
        setStreamingStatus(null);
        // Refresh session list to pick up updated title
        try {
          const updatedSessions = await fetchSessions();
          setSessions(updatedSessions);
        } catch {}
      }
    );
  };

  const handleSelectTemplate = (prompt: string, mode?: 'default' | 'ship30') => {
    handleSendMessage(prompt, mode || 'default');
  };

  return (
    <div className="h-screen w-screen flex flex-col overflow-hidden bg-gradient-radiant font-sans text-stone-900">
      {/* Top Header */}
      <Header
        onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
        selectedProvider={selectedProvider}
        onSelectProvider={setSelectedProvider}
        health={health}
      />

      {/* Main App Workspace */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sessions Sidebar */}
        <SessionList
          sessions={sessions}
          activeSessionId={activeSessionId}
          onSelectSession={selectSession}
          onNewSession={handleNewSession}
          onDeleteSession={handleDeleteSession}
          onSelectTemplate={handleSelectTemplate}
          isOpen={isSidebarOpen}
        />

        {/* Center Chat Workspace */}
        <ChatPane
          messages={messages}
          isStreaming={isStreaming}
          streamingStatus={streamingStatus}
          onSendMessage={handleSendMessage}
          onSelectSource={(source) => setActiveSource(source)}
          onSelectArtifact={(artifact) => setActiveArtifact(artifact)}
          onSelectTemplate={handleSelectTemplate}
        />

        {/* Right Artifact Viewer (Claude Artifacts Style) */}
        {activeArtifact && (
          <ArtifactViewer
            artifact={activeArtifact}
            onClose={() => setActiveArtifact(null)}
          />
        )}
      </div>

      {/* Grounded Citation Excerpt Modal */}
      {activeSource && (
        <SourceDrawer
          source={activeSource}
          onClose={() => setActiveSource(null)}
        />
      )}
    </div>
  );
};

export default App;
