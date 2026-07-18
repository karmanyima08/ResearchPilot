import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Image from "next/image";
interface Source {
  paper_name: string;
  heading: string;
  part: number;
}

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  suggestions?: string[];
  onSend: (question: string) => void;
}

export default function ChatMessage({
    role,
    content,
    sources,
    suggestions,
    onSend,
}: ChatMessageProps) {
  const isUser = role === "user";
  const [showSources, setShowSources] = useState(false);

  return (
    <div
      className={`flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
  className={`w-full rounded-[28px] px-6 py-5 transition-all ${
  isUser
    ? "ml-auto max-w-fit bg-gradient-to-r from-blue-500 to-sky-500 text-white shadow-[0_10px_30px_rgba(37,99,235,.25)]"
    : "max-w-4xl border border-white/60 bg-white/65 text-slate-800 backdrop-blur-2xl shadow-[0_20px_60px_rgba(37,99,235,.12)]"
}`}
>
        <div>
  <ReactMarkdown
    remarkPlugins={[remarkGfm]}
  components={{
    h1: ({ children }) => (
  <h1
    className={`mb-5 text-3xl font-bold ${
      isUser ? "text-white" : "text-slate-900"
    }`}
  >
    {children}
  </h1>
),

h2: ({ children }) => (
  <h2
    className={`mb-3 mt-6 text-2xl font-semibold ${
      isUser ? "text-white" : "text-slate-900"
    }`}
  >
    {children}
  </h2>
),
    p: ({ children }) => (
  <p
    className={`mb-4 leading-8 text-[15px] ${
      isUser ? "text-white" : "text-slate-700"
    }`}
  >
    {children}
  </p>
),
    ul: ({ children }) => (
      <ul className="mb-5 list-disc space-y-2 pl-6">
        {children}
      </ul>
    ),
    ol: ({ children }) => (
      <ol className="mb-3 list-decimal pl-5">
        {children}
      </ol>
    ),
    li: ({ children }) => (
      <li className="mb-1">
        {children}
      </li>
    ),
    code: ({ children }) => (
  <code className="rounded bg-gray-200 px-1 py-0.5 font-mono text-red-600">
    {children}
  </code>
),

pre: ({ children }) => (
  <pre className="my-4 overflow-x-auto rounded-xl bg-gray-900 p-4 text-sm text-white">
    {children}
  </pre>
),
    table: ({ children }) => (
  <table className="my-4 w-full border-collapse border border-gray-300">
    {children}
  </table>
),

thead: ({ children }) => (
  <thead className="bg-gray-100">
    {children}
  </thead>
),

tbody: ({ children }) => (
  <tbody>{children}</tbody>
),

tr: ({ children }) => (
  <tr className="border-b">
    {children}
  </tr>
),

th: ({ children }) => (
  <th className="border border-slate-2000 px-4 py-2 text-left font-semibold">
    {children}
  </th>
),

td: ({ children }) => (
  <td className="border border-slate-200 px-4 py-2">
    {children}
  </td>
),
  }}
>
  {content}
</ReactMarkdown>

  {sources && sources.length > 0 && (
  <div className="mt-6 border-t border-slate-200 pt-4">

    <button
      onClick={() => setShowSources(!showSources)}
      className="flex items-center gap-2 text-sm font-semibold text-slate-700 transition hover:text-blue-600"
    >
      <Image
        src="/researchpilot-logo.png"
        alt="ResearchPilot"
        width={24}
        height={24}
      />

      {showSources ? "▼" : "▶"} Sources ({sources.length})
    </button>

    {showSources && (
      <div className="mt-4 space-y-3">
        {sources.map((source, index) => (
          <div
            key={index}
            className="
              rounded-2xl
              border
              border-white/60
              bg-white/70
              backdrop-blur-xl
              p-4
              shadow-[0_10px_30px_rgba(37,99,235,.08)]
            "
          >
            <p className="font-semibold text-slate-800">
              📄 {source.paper_name}
            </p>

            {source.heading && (
              <p className="text-sm text-slate-500">
                Section: {source.heading}
              </p>
            )}

            {source.part !== undefined && (
              <p className="text-sm text-slate-500">
                Part {source.part}
              </p>
            )}
          </div>
        ))}
      </div>
    )}

    {!isUser && suggestions && suggestions.length > 0 && (
      <div className="mt-4 flex flex-wrap gap-2">
        {suggestions.map((suggestion, index) => (
          <button
            key={index}
            onClick={() => onSend(suggestion)}
            className="rounded-full bg-gray-100 px-3 py-2 text-sm transition hover:bg-gray-200"
          >
            {suggestion}
          </button>
        ))}
      </div>
    )}

    {!isUser && (
      <div className="mt-6 flex justify-end border-t border-slate-200/60 pt-4">
        <button
          onClick={async () => {
            const response = await fetch(
              "http://127.0.0.1:8000/export/docx",
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  title: "ResearchPilot Export",
                  content,
                }),
              }
            );

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = "ResearchPilot.docx";
            a.click();

            window.URL.revokeObjectURL(url);
          }}
          className=" rounded-full    border  border-blue-200   bg-white/80   px-4   py-2   text-sm   font-medium  text-blue-600  backdrop-blur-md
            transition  hover:bg-blue-500   hover:text-white
          "
        >
          📄 Export to Word
        </button>
      </div>
    )}

  </div>
)}
        </div>
      </div>
    </div>
  );
}

