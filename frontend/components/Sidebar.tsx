import Image from "next/image";
import { useState } from "react";
import { PanelLeftClose, PanelLeftOpen } from "lucide-react";
import PaperList from "./PaperList";
import UploadButton from "./UploadButton";
interface Paper {
  paper_id: string;
  paper_name: string;
}

interface SidebarProps {
  open: boolean;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
  papers: Paper[];
  uploading: boolean;
  selectedPapers: Paper[];
  onToggle: (paper: Paper) => void;
  onDelete: (paperId: string) => void;
  onUpload: (file: File) => void;
}

export default function Sidebar({
  open,
  setOpen,
  papers,
  uploading,
  selectedPapers,
  onToggle,
  onDelete,
  onUpload,
}: SidebarProps) {
  const [search, setSearch] = useState("");
  const filteredPapers = papers.filter((paper) =>
  paper.paper_name.toLowerCase().includes(search.toLowerCase())
);
  return (
    <aside
      className={`h-screen bg-white border-r border-slate-200 transition-all duration-300 flex flex-col ${
        open ? "w-46" : "w-15"
      }`}
    >

      {/* Header */}

      {open ? (

        <div className="flex items-center justify-between px-1 py-4 border-b">

          <div className="flex items-center gap-1">

            <Image
              src="/researchpilot-logo.png"
              alt="logo"
              width={42}
              height={42}
              className="rounded-lg"
            />

            <div>

              <h1 className="font-bold text-[12px] text-slate-800">
                ResearchPilot
              </h1>

              <p className="text-[9px] text-slate-500">
                AI Research Assistant
              </p>

            </div>


          </div>

          <button
            onClick={() => setOpen(false)}
            className="flex h-10 w-5items-center justify-center rounded-lg border border-slate-200 bg-white shadow-sm transition hover:bg-slate-100"
          >
            <PanelLeftClose
              size={17}
              className="text-slate-700"
            />
          </button>


        </div>



      )
          : (

        <div className="flex flex-col items-center gap-5 py-5 border-b">

          <button
            onClick={() => setOpen(true)}
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 bg-white shadow-sm transition hover:bg-slate-100"
          >
            <PanelLeftOpen
              size={17}
              className="text-slate-700"
            />
          </button>

          <Image
            src="/researchpilot-logo.png"
            alt="logo"
            width={36}
            height={36}
            className="rounded-lg"
          />

        </div>

      )}


      {/* Upload */}

<div
  className={`${
    open ? "px-3 pt-4 pb-2" : "flex justify-center py-4  "
  }`}
>
  <UploadButton

    open={open}
    uploading={uploading}
    onUpload={onUpload}
  />
</div>

{/* Search */}

{open && (
  <div className="px-4 pb-4 text-xs text-slate-800 ">
    <input
      type="text"
      placeholder="Search papers..."
      value={search}
      onChange={(e) => setSearch(e.target.value)}
      className="w-full rounded-full border border-slate-400 bg-white px-4 py-2 text-sm outline-none focus:border-blue-800"
    />
  </div>
)}

      {/* Papers */}

      <div className="flex-1 overflow-y-auto">

        {open && (
          <div className="px-4">

            <h2 className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-500">
              Uploaded Papers
            </h2>

          </div>
        )}

        <div className={open ? "px-3" : "px-1"}>

          <PaperList
            open={open}
            papers={filteredPapers}
            selectedPapers={selectedPapers}
            onToggle={onToggle}
            onDelete={onDelete}
          />

        </div>

      </div>

      {/* Footer */}

      <div
        className={`border-t border-slate-200 ${
          open
            ? "px-4 py-4"
            : "flex justify-center py-4"
        }`}
      >
        {open ? (
          <div>

            <p className="text-sm font-semibold text-slate-700">
              ResearchPilot
            </p>

            <p className="text-xs text-slate-400">
              Version 1.0
            </p>

          </div>
        ) : (
          <div className="text-xs font-bold text-slate-400">
            RP
          </div>
        )}
      </div>

    </aside>
  );
}