export interface SourceCitation {
  id?: string;
  episode: string;
  guest: string;
  timestamp: string;
  publish_date?: string;
  youtube_url?: string;
  text: string;
  score: number;
  citation?: string;
}

export interface Artifact {
  id: string;
  message_id?: string;
  session_id: string;
  artifact_type: 'html' | 'markdown';
  title: string;
  content: string;
  created_at: string;
}

export interface Message {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  sources: SourceCitation[];
  provider?: string;
  mode?: 'default' | 'ship30';
  created_at: string;
  artifacts?: Artifact[];
}

export interface Session {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface HealthStatus {
  status: string;
  database: {
    status: string;
    latency_ms?: number;
    error?: string;
  };
  ollama: {
    status: string;
    available: boolean;
    base_url?: string;
    configured_model?: string;
    model_installed?: boolean;
    installed_models?: string[];
  };
  cloud_providers: {
    status: string;
    claude?: { configured: boolean; model: string };
    openai?: { configured: boolean; model: string };
  };
  vector_index: {
    status: string;
    chunks_indexed: number;
  };
  version: string;
}
