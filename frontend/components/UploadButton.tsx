"use client";
import { useRef } from "react";
import { Upload } from "lucide-react";

interface UploadButtonProps {
  open: boolean;
  onUpload: (file: File) => void;
  uploading: boolean;
}

export default function UploadButton({
  open,
  onUpload,
  uploading,
}: UploadButtonProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  return (
    <>
      {open ? (
        <button
          onClick={() => inputRef.current?.click()}
          className="flex w-[92%] mx-auto items-center justify-center gap-2 rounded-full bg-blue-400 py-2.5 text-sm font-medium text-white transition hover:bg-blue-500"
        >
          <Upload size={17} />

          {uploading ? "Uploading..." : "Upload Paper"}
        </button>
      ) : (
        <button
          onClick={() => inputRef.current?.click()}
          className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-blue-400 hover:bg-blue-500 text-white transition hover:bg-blue-500"
          title="Upload Paper"
        >
          <Upload size={15} />
        </button>
      )}

      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        hidden
        onChange={(e) => {
          const file = e.target.files?.[0];

          if (file) {
            onUpload(file);
          }
        }}
      />
    </>
  );
}