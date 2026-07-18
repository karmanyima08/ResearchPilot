"use client";
import { useEffect, useState } from "react";
import api from "@/services/api";
import Sidebar from "@/components/Sidebar";
import ChatSection from "@/components/ChatSection";
interface Paper {
  paper_id: string;
  paper_name: string;
  uploaded_at?: string;
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

export default function Home() {
  const [papers, setPapers] = useState<Paper[]>([]);
  const [uploading, setUploading] = useState(false);
  const [selectedPapers, setSelectedPapers] = useState<Paper[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);
const [loading, setLoading] = useState(false);
  const loadPapers = async () => {

      try {
      const res = await api.get("/papers");
      setPapers(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadPapers();
  }, []);

  //  ONE function used everywhere
  const sendQuestion = async (question: string) => {


    if (selectedPapers.length === 0) {
      alert("Please select at least one paper.");
      return;
    }

    setLoading(true);

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: question,
      },
      {
        role: "assistant",
        content: "Thinking...",
      },
    ]);

    try {

      const response = await api.post("/chat", {
    question,
    paper_ids: selectedPapers.map((p) => p.paper_id),

    history: messages.map((m) => ({
        role: m.role,
        content: m.content,
    })),
});

      setMessages((prev) => {

        const updated = [...prev];

        updated[updated.length - 1] = {
  role: "assistant",
  content: response.data.answer,
  sources: response.data.sources,
  suggestions: response.data.suggestions,
};

        return updated;
      });

    } catch (err)

    {

      console.error(err);

      setMessages((prev) => {

        const updated = [...prev];

        updated[updated.length - 1] = {
          role: "assistant",
          content: "Sorry, something went wrong.",
        };

        return updated;

      });

    }
    finally {
  setLoading(false);
}
  };

  const handleLiteratureReview = async () => {
  if (selectedPapers.length === 0) {
    alert("Select at least one paper.");
    return;
  }
  setLoading(true);

  try {
    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: "Generating literature review...",
      },
    ]);

    const response = await api.post("/chat/literature-review", {
      paper_ids: selectedPapers.map((p) => p.paper_id),
    });

    setMessages((prev) => {
      const updated = [...prev];

      updated[updated.length - 1] = {
        role: "assistant",
        content: response.data.answer,
        sources: response.data.sources,
        suggestions: response.data.suggestions,
      };

      return updated;
    });
  } catch (err) {
    console.error(err);
  } finally {
    setLoading(false);
  }
};

  const handleCompare = async () => {
  if (selectedPapers.length < 2) {
    alert("Select at least two papers.");
    return;
  }

  setLoading(true);

  try {
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: `Compare ${selectedPapers.length} selected papers`,
      },
      {
        role: "assistant",
        content: "Comparing papers...",
      },
    ]);

    const response = await api.post("/chat/compare", {
      paper_ids: selectedPapers.map((p) => p.paper_id),
    });

    setMessages((prev) => {
      const updated = [...prev];

      updated[updated.length - 1] = {
        role: "assistant",
        content: response.data.answer,
        sources: response.data.sources,
        suggestions: [
          "Explain the comparison",    "Which paper should I read first?",  "Summarize the differences",   "Identify research gaps",
        ],
      };

      return updated;
    });
  } catch (err) {
    console.error(err);
  } finally {
    setLoading(false);
  }
};

  const handleResearchGaps = async () => {
  if (selectedPapers.length === 0) {
    alert("Select at least one paper.");
    return;
  }

  setLoading(true);

  try {
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: "Find research gaps in the selected papers",
      },
      {
        role: "assistant",
        content: "Finding research gaps...",
      },
    ]);

    const response = await api.post("/chat/research-gaps", {
      paper_ids: selectedPapers.map((p) => p.paper_id),
    });

    setMessages((prev) => {
      const updated = [...prev];

      updated[updated.length - 1] = {
        role: "assistant",
        content: response.data.answer,
        sources: response.data.sources,
        suggestions: [   "Suggest thesis topics",    "Explain the biggest gap",  "Which gap is easiest to solve?",  "Generate future work",
        ],
      };

      return updated;
    });
  } catch (err) {
    console.error(err);
  } finally {
    setLoading(false);
  }
};

  return (
<main
  className=" flex  h-screen  overflow-hidden  bg-[radial-gradient(circle_at_top,#93c5fd_0%,#bfdbfe_18%,#dbeafe_35%,#eff6ff_60%,#f8fbff_80%,#ffffff_100%)]
  "
>    <Sidebar
  open={sidebarOpen}
  setOpen={setSidebarOpen}
  papers={papers}
  uploading={uploading}
  selectedPapers={selectedPapers}

        onToggle={(paper) => {
          setSelectedPapers((prev) => {

            const exists = prev.some(
              (p) => p.paper_id === paper.paper_id
            );

            if (exists) {
              return prev.filter(
                (p) => p.paper_id !== paper.paper_id
              );
            }

            return [...prev, paper];
          });
        }}

        onDelete={async (paperId) => {
          try {

            await api.delete(`/papers/${paperId}`);

            await loadPapers();

            setSelectedPapers((prev) =>
              prev.filter(
                (p) => p.paper_id !== paperId
              )
            );

            setMessages([]);

          } catch (err) {
            console.error(err);
            alert("Failed to delete paper.");
          }
          finally {
  setLoading(false);
}

        }}

        onUpload={async (file) => {

          const formData = new FormData();
          formData.append("file", file);

          try {

            setUploading(true);

            const response = await api.post(
              "/api/v1/papers/upload",
              formData,
              {
                headers: {
                  "Content-Type": "multipart/form-data",
                },
              }
            );

            console.log(response.data);

            await loadPapers();

          } catch (err: any) {

            if (err.response?.status === 409) {
              alert("This paper has already been uploaded.");
            } else {
              console.error(err);
            }

          } finally {
            setUploading(false);
          }

        }}
      />

      <ChatSection
  loading={loading}
  messages={messages}
  selectedPapers={selectedPapers}
  onSend={sendQuestion}
  onLiteratureReview={handleLiteratureReview}
  onCompare={handleCompare}
  onResearchGaps={handleResearchGaps}
/>
    </main>
  );

}