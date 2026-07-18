"use client";
import { useState } from "react";
import {
  Send,
  BookOpen,
  GitCompare,
  Search,
} from "lucide-react";

interface ChatInputProps {
  loading: boolean;
  onSend: (question: string) => void;
  onLiteratureReview: () => void;
  onCompare: () => void;
  onResearchGaps: () => void;
}

export default function ChatInput({
  loading,
  onSend,
  onLiteratureReview,
  onCompare,
  onResearchGaps,
}: ChatInputProps) {
  const [question, setQuestion] = useState("");

  const send = () => {
    if (!question.trim() || loading) return;

    onSend(question);
    setQuestion("");
  };

  return (
<div className="flex flex-col gap-2">
      <textarea
  value={question}
  disabled={loading}
  onChange={(e) => setQuestion(e.target.value)}
  onKeyDown={(e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }}
  placeholder="Ask anything about your selected papers..."
  rows={1}
  className="w-full resize-none border-0 bg-transparent text-base text-slate-800 placeholder:text-slate-400 focus:outline-none"
/>
      <div className="mt-1 flex items-center justify-between">

  <div className="flex gap-3">

    <button
      disabled={loading}
      onClick={onLiteratureReview}
      className="flex h-9 items-center gap-2 rounded-full bg-slate-100 px-5 text-sm font-medium text-slate-700 transition hover:bg-slate-200"
    >
      <BookOpen size={18} />
      Literature Review
    </button>

    <button
      disabled={loading}
      onClick={onCompare}
      className="flex h-9 items-center gap-2 rounded-full bg-slate-100 px-5 text-sm font-medium text-slate-700 transition hover:bg-slate-200"
    >
      <GitCompare size={18} />
      Compare Papers
    </button>

    <button
      disabled={loading}
      onClick={onResearchGaps}
      className="flex h-10 items-center gap-2 rounded-full bg-slate-100 px-5 text-sm font-medium text-slate-700 transition hover:bg-slate-200"
    >
      <Search size={18} />
      Research Gaps
    </button>
  </div>

  <button
    disabled={loading}
    onClick={send}
    className="flex h-10 w-28 items-center justify-center gap-2 rounded-full bg-blue-500 text-white transition hover:bg-blue-600"
  >
    <Send size={18} />
    {loading ? "Thinking..." : "Send"}
  </button>

</div>
    </div>
  );
}