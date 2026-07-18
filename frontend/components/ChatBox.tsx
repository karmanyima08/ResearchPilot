"use client";
import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import TypingIndicator from "./TypingIndicator";
import Image from "next/image";
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
interface ChatBoxProps {
  messages: Message[];
  onSend: (question: string) => void;
}

export default function ChatBox({ messages, onSend }: ChatBoxProps) {

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto px-8 py-6">

<div className="mx-auto max-w-5xl space-y-8">
  {messages.length === 0 && (
  <div className="flex h-full flex-col items-center justify-center text-center text-gray-500">

    <div className="text-7xl">
      <Image
  src="/researchpilot-logo.png"
  alt="ResearchPilot Logo"
  width={100}
  height={100}
  className="rounded-lg"
/>
    </div>

    <h2 className="mt-6 text-2xl font-bold">
      Welcome to ResearchPilot
    </h2>

    <p className="mt-3 max-w-lg">
      Upload research papers, select them from the sidebar,
      and ask questions, generate literature reviews,
      compare papers, or discover research gaps.
    </p>

  </div>
)}
      {messages.map((message, index) => {
        if (
          message.role === "assistant" &&
          message.content === "Thinking..."
        ) {
          return <TypingIndicator key={index} />;
        }

        return (
          <ChatMessage
    key={index}
    role={message.role}
    content={message.content}
    sources={message.sources}
    suggestions={message.suggestions}
    onSend={onSend}
/>
        );
      })}

      <div ref={bottomRef} />
    </div>
      </div>
  );
}