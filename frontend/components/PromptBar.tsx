"use client";
import ChatInput from "./ChatInput";
interface Paper {
  paper_id: string;
  paper_name: string;
}

interface PromptBarProps {
  loading: boolean;
  selectedPapers: Paper[];

  onSend: (question: string) => void;
  onLiteratureReview: () => void;
  onCompare: () => void;
  onResearchGaps: () => void;
}

export default function PromptBar({
  loading,
  selectedPapers,
  onSend,
  onLiteratureReview,
  onCompare,
  onResearchGaps,
}: PromptBarProps) {
  return (
    <div
      className="
        border-t
        border-white/40
        bg-white/20
        backdrop-blur-xl
      "
    >
      <div className="mx-auto max-w-4xl px-8 py-4">

        {selectedPapers.length > 0 && (
          <>
            <p className="mb-3 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
              Selected Papers
            </p>

            <div className="mb-4 flex flex-wrap gap-2">
              {selectedPapers.map((paper) => (
                <div
                  key={paper.paper_id}
                  className="
                    flex
                    items-center
                    rounded-full
                    border
                    border-blue-200/70
                    bg-white/60
                    backdrop-blur-md
                    px-4
                    py-1
                    text-sm
                    font-medium
                    text-slate-700
                    shadow-[0_8px_20px_rgba(59,130,246,0.10)]
                    transition
                    hover:bg-white/80
                    hover:shadow-[0_12px_30px_rgba(59,130,246,0.18)]
                  "
                >
                  📄

                  <span className="ml-2 max-w-[220px] truncate">
                    {paper.paper_name}
                  </span>
                </div>
              ))}
            </div>
          </>
        )}

        <div
          className="
            rounded-[28px]
            border
            border-white/60
            bg-white/70
            backdrop-blur-2xl
            p-3
            shadow-[0_20px_60px_rgba(37,99,235,0.15)]
          "
        >
          <ChatInput
            loading={loading}
            onSend={onSend}
            onLiteratureReview={onLiteratureReview}
            onCompare={onCompare}
            onResearchGaps={onResearchGaps}
          />
        </div>

      </div>
    </div>
  );
}