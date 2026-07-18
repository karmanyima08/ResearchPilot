export default function TypingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="rounded-xl border border-gray-200 bg-white px-5 py-4 shadow-sm">
        <div className="flex gap-2">
          <span className="h-2 w-2 animate-bounce rounded-full bg-gray-500"></span>
          <span
            className="h-2 w-2 animate-bounce rounded-full bg-gray-500"
            style={{ animationDelay: "0.2s" }}
          ></span>
          <span
            className="h-2 w-2 animate-bounce rounded-full bg-gray-500"
            style={{ animationDelay: "0.4s" }}
          ></span>
        </div>
      </div>
    </div>
  );
}