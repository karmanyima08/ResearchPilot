import { FileText } from "lucide-react";
interface Paper {
  paper_id: string;
  paper_name: string;
}
interface PaperListProps {
  open: boolean;
  papers: Paper[];
  selectedPapers: Paper[];
  onToggle: (paper: Paper) => void;
  onDelete: (paperId: string) => void;
}

export default function PaperList({
  open,
  papers,
  selectedPapers,
  onToggle,
  onDelete,
}: PaperListProps) {
  return (
    <div className="space-y-2">

      {papers.map((paper) => {

        const selected = selectedPapers.some(
          (p) => p.paper_id === paper.paper_id
        );

        if (!open) {
          return (
            <button
              key={paper.paper_id}
              title={paper.paper_name}
              onClick={() => onToggle(paper)}
              className={`mx-auto flex h-13 w-13 items-center justify-center rounded-lg transition ${
                selected
                  ? "bg-blue-100 text-blue-600"
                  : "text-slate-500 hover:bg-slate-100"
              }`}
            >
              <FileText size={18} />
            </button>
          );
        }

        return (
          <div
            key={paper.paper_id}
            className={`rounded-xl border px-3 py-2.5 transition ${
              selected
                ? "border-blue-400 bg-blue-50"
                : "border-slate-200 bg-white hover:border-blue-300"
            }`}
          >
            <label className="flex items-start gap-3 cursor-pointer">

              <input
                type="checkbox"
                checked={selected}
                onChange={() => onToggle(paper)}
                className="mt-0.5 h-4 w-4"
              />

              <div className="flex-1">

                <p className="truncate text-[14px] font-medium text-slate-800">
                  {paper.paper_name}
                </p>

                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDelete(paper.paper_id);
                  }}
                  className="mt-0.5 text-[11px] text-red-500 hover:text-red-700"
                >
                  Delete
                </button>

              </div>

            </label>

          </div>
        );
      })}
    </div>
  );
}