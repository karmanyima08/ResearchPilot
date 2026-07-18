"use client";
import Header from "./Header";
import ChatBox from "./ChatBox";
import PromptBar from "./PromptBar";

interface Paper {
  paper_id: string;
  paper_name: string;
}

interface Source {
  paper_name: string;
  heading: string;
  part: number;
}

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  suggestions?: string[];
}

interface ChatSectionProps {
  loading: boolean;
  messages: Message[];
  selectedPapers: Paper[];

  onSend: (question: string) => void;
  onLiteratureReview: () => void;
  onCompare: () => void;
  onResearchGaps: () => void;
}

export default function ChatSection({
  loading,
  messages,
  selectedPapers,
  onSend,
  onLiteratureReview,
  onCompare,
  onResearchGaps,
}: ChatSectionProps) {
  return (
    <section className="flex flex-1 flex-col overflow-hidden">

      <Header
        title="ResearchPilot"
        subtitle="AI-powered Research Assistant for Literature Reviews, Paper Comparison, Research Gap Discovery, and Academic Q&A."
      />

      <div className="flex-1 overflow-y-auto px-6 py-6">

        <div
          className="  mx-auto    flex   h-full   w-full   max-w-6xl  flex-col   overflow-hidden   rounded-[32px]  border
            border-white/60  bg-white/55    backdrop-blur-2xl   shadow-[0_25px_70px_rgba(37,99,235,0.12)]  "
        >
          <div className="flex-1 overflow-y-auto px-10 py-8">

            <ChatBox
              messages={messages}
              onSend={onSend}
            />

          </div>

          <PromptBar
            loading={loading}
            selectedPapers={selectedPapers}
            onSend={onSend}
            onLiteratureReview={onLiteratureReview}
            onCompare={onCompare}
            onResearchGaps={onResearchGaps}
          />

        </div>

      </div>

    </section>
  );
}